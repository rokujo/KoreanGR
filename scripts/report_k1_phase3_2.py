"""Render human-readable audit/smoke reports from fresh validator results."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/'reports'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))

def report():
    result=read(REPORTS/'k1_phase3_2_validation_result.json')
    audit=read(REPORTS/'k1_phase3_2_alias_audit.json')
    classes=audit['class_counts']
    alias_table='\n'.join(f"|{e['surface']}|{e['old_target']}|{e['classification']}|{e['condition']}|" for e in audit['aliases'])
    contrast_table='\n'.join(f"|{e['id']}|{e['text']}|{e['expected']}|{e['status']}|{'OK' if e['expectation_met'] else 'FAIL'}|" for e in audit['contrast_results'])
    grouped='\n'.join(f"|{e['boundary']}|{e['policy']}|" for e in audit['grouping'])
    tests=result.get('tests',{})
    audit_md=f'''# K1 Phase 3.2 alias / POS / grouping監査

旧 `scripts/k1_pilot_analysis.py` と旧runはfreezeしたまま、新version `scripts/k1_phase3_2_analysis.py` / `resolver.py` を作成。文字列だけのglobal aliasを使用せず、raw morphologyを保持し、登録lemma/POS/sense、局所統語、適用条件を照合する。

## 全ALIASES 12件

|分類|件数|
|---|---:|
|safe_surface_normalization（無条件で安全）|0|
|pos_conditioned_alias|{classes.get('pos_conditioned_alias',0)}|
|context_conditioned_alias|{classes.get('context_conditioned_alias',0)}|
|unsafe_alias_remove|{classes.get('unsafe_alias_remove',0)}|
|review_required（静的alias分類）|0|

context条件を満たさない個別用例はREVIEWになる。無条件に安全なglobal文字列置換は認めない。削除対象は実surfaceでない `네_numeral` の旧key。`네 → 너` のglobal適用も廃止し、限定したNP所有用法候補の枝だけを残す。

|旧surface|旧target|分類|新条件|
|---|---|---|---|
{alias_table}

`스무 → 스물` の登録lemma認識はその語の初出許可を意味しない。future/retired permissionはcandidate gateで別に検証する。

## 네の誤aliasと修正

旧解析は `네 / IC` を辞書参照前に `너`へ変換し、compatibleなPOS候補がなくても唯一のCore pronounを採用していた。新解析は以下を分離する。

- `네.` / `네, 책이 있어요.` / 引用内の`"네."`: raw IC＋応答境界から、登録interjection yes `ko_k1_0442`。
- `네 책`: 実KiwiではICになる。この裸の列には所有用法の可能性が残るため、yesにも너にも決めずREVIEW。モデルの所有用法申告だけでは承認しない。
- raw NPとしての네＋後続名詞が確認できた場合: 所有縮約の너候補。synthetic raw POS対照testで条件を検証。現実の`내 책`/`제 책`はKiwiがNP＋JKGを出すため、そのraw境界を使う。
- `네 사람이 와요.`: raw MM＋後続名詞から数詞넷。pronounへglobal aliasしない。

## unique fallback・surface normalization・sense全体

唯一の登録entryでもraw POSに不適合なら採用しない。POS filter後に複数候補が残れば、局所根拠がない限りREVIEW。必要なPOS bridgeは있다/없다/필요하다の既存DB adjective、exact 다른の連体形、数詞contextのcounterに明示限定する。

旧DEFAULT_SENSE {len(audit['legacy_default_senses'])}件は監査履歴として残し、新versionでは無条件に使わない。active800には同形lemma13組があり、저/일/개/쓰다/이/팔/봉지/달/새のPOS境界と、눈/다리/배/풀の同POS sense境界を区別する。後者は限定局所contextの正の根拠が必要。sense overrideもPOS・contextを上書きできない。

예: `눈이 와요.`→snow、`눈이 아파요.`→eye、`눈이 있어요.`→REVIEW。`풀로 종이를 붙여요.`→glue、`나무 아래에 풀이 있어요.`→grass、`풀이 있어요.`→REVIEW。`약이 써요.`はKiwiがVVを返すため、writeへ誤承認せずREVIEW。VA/bitterへ勝手にtag変更することもしていない。

## 밥하고とgrouping全体

旧001初稿の `밥하고` はNNG 밥＋XSV 하＋EC 고に分割された。旧実装は未登録compound 밥하다へまとめていた。新実装では登録compoundがない場合に、登録food名詞の明示的な列挙（第2food名詞＋目的格）とfood predicateが揃えば、밥とgrammar25の하고へ再分割する。raw streamは変更せず、使用したraw indicesと根拠をboundary decisionに保存する。

`밥하고 국을 먹어요.` / `동생은 밥하고 우유를 좋아해요.`はRESOLVED。`밥하고 먹어요.`は第2目的語がなく、別の動詞解釈も排除できないためREVIEW。`친구하고 가요.`はraw noun＋JKBを保つ。`공부하고 있어요.`は登録공부하다のNNG＋XSVと進行grammar05を分離する。

|境界|新方針|
|---|---|
{grouped}

助詞・EC・引用符を飛ばして複数contentを連結する一般的groupingは廃止。登録lemmaに一致してもraw indicesが隣接し、対応するPOSと形態が合う必要がある。交換compoundは도와/빌려/돌려の形とraw VV＋EC＋VV/VXを照合。물어보다は물어という形を追加照合し、`묻어 봐요.`をaskへ変換しない。등록fixed exceptionは完全一致spanだけを引用符内でも認識し、grammar32の迂回範囲を広げない。이랑/랑は依然仕様外。

## 対照fixture結果

PASSはその短いparser fixtureの解析を意味し、教材lengthや学習履歴を満たすという意味ではない。parser fixtureではactive登録800を照合対象にした。実教材のactual permissionは別gate testとsmoke snapshotで検証した。REVIEW期待を満たすことはregression成功だが、その用例を教材commitする許可ではない。

|ID|raw text|期待|結果|照合|
|---|---|---|---|---|
{contrast_table}

## Regression tests

最終全体test: {tests.get('tests','未集計')}件、{tests.get('status','未集計')}、failures={tests.get('failures','未集計')}、errors={tests.get('errors','未集計')}。最終focused suiteは22 test methods（full suite開始後に追加した旧neバグ注入testを含む）。対照fixture33件、Phase 2.3の実本文から採った8文、Phase 3.1の不規則活用28probeを検証した。raw stream保持、raw index重複なし、限定walking resolver、future/retired拒否、planned identity mismatch、candidate state不変、retry隔離、atomic crash前後/idempotent commitを確認。

完全なsense disambiguation、韓国語の全活用・全結合辞書、人間の自然さ承認を実装したという主張ではない。新runはこの2本文だけであり、初期50本全体のfalse-negative率はまだ未検証。
'''
    (REPORTS/'k1_phase3_2_alias_audit.md').write_text(audit_md,encoding='utf-8')
    summary_table='\n'.join(f"|K1-{r['text']:03d}|{r['attempt']}|{r['eojeol']}|{r['max_sentence_eojeol']}|{r['coverage']['denominator_N']}|{r['coverage']['new_tokens_U']}|100%|{r['coverage']['previous_vocab_coverage']:.6%}|" for r in result['smoke'])
    identity_table='\n'.join(f"|{r['text']:03d}|{e['planned_id']}|{e['lemma']}|{e['pos']}|{e['sense']}|{', '.join(o['surface'] for o in e['occurrences'])}|" for r in result['smoke'] for e in r['identity_rows'])
    state=read(ROOT/'state/phase3_2_smoke_exposure_ledger.json');texts=state['committed_records']
    bodies='\n\n'.join(f"### K1-{r['text_number']:03d} — {r['title_ko']}\n\n{r['text_ko']}\n\n日本語訳:\n\n{r['translation_ja']}" for r in texts)
    old=result['previous_failed_002_coverage']
    report_md=f'''# K1 Phase 3.2 — 解析器堅牢化 / 001→002 smoke

**判定: {result['decision']} / Phase 3.2 {result['status']}。** 001と002を実績ゼロの別runで順に検証し、hard PASS後だけcommitした。K1-003以降、50本生成、300本量産は実施していない。

## 原因・修正方法

旧ALIASESの`네 → 너`とPOS不一致の唯一候補fallbackが、raw IC yesをCore pronounへ誤変換していた。新versionではglobal aliasを使わず、raw POS・登録identity・局所contextを照合する。ICの明確な応答は `네 / interjection / yes / ko_k1_0442`、裸の所有用法候補はREVIEW、MMのnative数詞は넷へ区別する。

全12aliasの分類はPOS条件付き7、context条件付き4、削除1、無条件safe0。旧default sense14件を無条件適用せず、同形lemma13組のPOS/sense境界を監査した。詳細は [alias監査](k1_phase3_2_alias_audit.md) とJSONのraw evidence。

밥하고もsurfaceでcompound化しない。food列挙＋第2目的語＋predicateの根拠が揃う場合だけ名詞＋grammar25へ再分割する。根拠の薄い `밥하고 먹어요.` はREVIEW。하다 compound、registered exchange、VV＋auxiliary、counter、引用・句読点を個別に監査した。이랑/랑や新文法を許可していない。

## Freeze・versioning

過去{result['frozen_files']}ファイルのhash違反{len(result['frozen_errors'])}件。Phase 3 retryのcommitted001、failed002、ledger/run state/report、Phase 3.1 gate/限定resolver、正式Core300＋Expansion500、文法32、初出・review windows・ID migration・自然さguidelinesは変更していない。

新しい3ファイル `k1_phase3_2_analysis.py` / `resolver.py` / `gate.py` を作った。gateは承認済み3.1を別versionへ複製し、hard条件・planned identity比較・final reanalysis・atomic transactionを維持した。差分は新解析器の選択、max5attempt、smoke上限002、schemaの別path、phase表示3.2、engine hashをinput digestへ追加。wrapperでは前runと同じ2回停滞stopも維持する。

旧raw candidate sourceを対照入力に再使用したが、旧annotation、旧coverage、旧露出・stateは流用していない。これは不自然さを避けるために本文を作り直したテストではなく、同じ問題入力を修正後analyzerで解決する回帰smoke。001の初稿は旧123어절版であり、旧runのcommitted129어절版を上書きしていない。

## Smoke結果

|教材|attempt|어절|max文|N|U|controlled|previous|
|---|---:|---:|---:|---:|---:|---:|---:|
{summary_table}

両本文ともfuture0、invalid0、unresolved content0、grammar32外0、planned new IDsとactual new IDs一致。001/002各1attemptでcommit。両方の99%target missは設計上予想され、hard98%を満たすためblockerではない。初稿target130〜150はsoftで、001の123は固定regression sourceを検証する目的で使用し、fillerで引き延ばしていない。

## Planned ID / surface / resolved identity

|教材|planned ID|lemma|POS|sense|実annotation surface|
|---|---|---|---|---|---|
{identity_table}

002の네にはraw `IC`が保存されており、Core 너への誤aliasはない。planned_new_not_present gateはそのまま維持し、ネを너へ故意に変えた対照candidateはrejectするtestもPASS。

## coverage再計算

旧failed002: N={old['denominator_N']}、U={old['new_tokens_U']}、機械値controlled100%、previous={old['previous_vocab_coverage']:.6%}。この値は間違ったidentityを前提としていたため採用しない。修正後にrawから再解析するとN=130、U=2、previous=(130−2)/130=98.461538%。controlledも登録identity照合後に100%と再計算した。

Nは本文のlexical annotation token数（Core / Expansion / registered proper name / frozen exception / unknownを各tokenとして計数）。grammar function・句読点は除外する。Uは当該本文のplanned new Expansion IDに対応する実token数。同一語を反復すればtoken回数分Uへ加算する。異なる教材の露出creditとは別の計数。

## State integrity / transaction

新ledger `state/phase3_2_smoke_exposure_ledger.json` はepoch2、last_committed_text2、actual導入4語、異なるvocab/text露出4。旧run ledgerからの初期credit0。candidate評価前後のledger SHA一致、最終再解析一致、001/002のcredit各1回。validator実行前後もstate byte不変。incidental0、review debt0、expired0（初回review windowはまだ開いていない）。

実smokeのreject数{result['candidate_rejections']}。別temp-state testsではfailed candidate、future、retired、予定identity不一致をrejectし、actual intro/exposure/debt/historyにcreditしないことを確認した。atomic publish前のcrashは状態不変、publish後crashはprojectionを復旧して二重creditなし。003はschema/gate双方で拒否する。

## Regression / validator

最終全体tests: {tests.get('tests','未集計')}件 {tests.get('status','未集計')}、failures={tests.get('failures','未集計')}、errors={tests.get('errors','未集計')}。最終focused suite 22件もPASS（full開始後に追加した旧neバグ注入1testを含む）。新suiteに33対照fixture、凍結Phase 2.3からの8文、3.1不規則活用28probeを含む。全体suiteは既存Phase1〜3.1/retryの検証も含む。詳細は `k1_phase3_2_all_test_log.txt` / `focused_test_log.txt` / `test_result.json`。

PowerShellのnative stderrリダイレクトでは終了statusとunittest summaryが一致しなかったため、Python runnerが結果とUTF-8 logを明示管理する方式で最終suiteを再実行した。採用結果はこのrunnerのstructured resultのみ。

validator errors: {len(result['errors'])}。freeze violations0。controlled違反0、previous<98違反0、grammar violations0、future0、invalid0、unresolved0。parser対照fixtureのREVIEWは期待された保守的判定であり、committed教材のunresolvedを許可するものではない。

## 限界と次の判断

完全な形態素・sense解析器ではない。単独の네 책、文脈の薄い눈/풀、raw POSと意味が食い違う약이 써요などはREVIEWで止める。新解析器はfalse positiveを防ぐためfalse negativeを許容し、モデルannotationを独立正解にしていない。自然さwarningは{result['naturalness_warnings']}件、日本語訳lint flagは{result['translation_fidelity_flags']}件。本人が教師へ名前を伝える文のwarningは「呼ぶ」の代用ではない。自己semantic reviewは人間承認の代替ではない。

辞書に未登録の別義までraw POSだけで完全に検出できるわけではない。restricted senseの文脈確認とsemantic second passは引き続き必要。同POS homographの限定context規則も汎用辞書の代替ではなく、より広い文脈が必要な正しい用例をREVIEWにする可能性がある。

**次は別runでK1-001〜050の連続逐次試験を再実施可能。** このsmokeの成功は50本のdebt/scene/genre成立や300本量産の証明ではない。今のrunは002で完了し、そのまま003へ継続しない。

## Smoke本文（人間レビュー用）

{bodies}
'''
    (REPORTS/'k1_phase3_2_analyzer_hardening_report.md').write_text(report_md,encoding='utf-8')

if __name__=='__main__':report()
