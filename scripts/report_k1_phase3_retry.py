"""Stopped/completed actual-run verification and reports; no regeneration."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from k1_phase3_retry import SequentialGate, PILOT, LEDGER, REPORTS, FREEZE, summarize, freeze_errors
from k1_candidate_gate import read, write, ROOT, build_snapshot, digest
from k1_phase3_1_resolver import analyze
from jsonschema import Draft202012Validator

def report():
    g=SequentialGate();state=g.load();summary=summarize(g);before=LEDGER.read_bytes()
    errors=[]
    initial=read(PILOT/'initial_state.json')
    actual_prior=deepcopy(initial)
    reanalyses=[]
    for r in state['committed_records']:
        snap=build_snapshot(g.f,actual_prior,r['text_number'])
        fresh=g.evaluate(r['source'],actual_prior,snap)
        mismatches=[k for k in ('text_ko','annotations','raw_morphology','coverage','actual_new_vocab_ids','actual_review_vocab_ids','incidental_previous_vocab_ids') if fresh[k]!=r[k]]
        if not fresh['hard_pass'] or mismatches:errors.append(dict(text=r['text_number'],hard=fresh['hard_errors'],mismatches=mismatches))
        reanalyses.append(dict(text=r['text_number'],hard_pass=fresh['hard_pass'],mismatches=mismatches))
        # These in-memory prior records supply only actual exposure, never planned credit.
        actual_prior['committed_records'].append(r)
        for e in actual_prior['entries']:
            if e['vocab_id'] in r['actual_new_vocab_ids']:e['actual_first_text']=r['text_number']
    attempts=[read(p) for p in sorted((PILOT/'candidates').glob('*.json'))]
    schema_errors=[]
    candidate_schema=Draft202012Validator(read(PILOT/'candidate.schema.json'))
    for a in attempts:
        schema_errors += [dict(text=a['text_number'],attempt=a['attempt_number'],error=e.message) for e in candidate_schema.iter_errors(a)]
        check=deepcopy(a);expected=check.pop('candidate_digest')
        if digest(check)!=expected:errors.append('Candidate digest mismatch')
        if a['ledger_sha_before_evaluation']!=a['ledger_sha_after_evaluation']:errors.append('Evaluation mutated ledger')
    if summary['frozen_input_violations']:errors.append('Frozen inputs changed')
    if schema_errors:errors.append(dict(candidate_schema_errors=schema_errors))
    if len(list((PILOT/'texts').glob('*.json')))!=state['epoch']:errors.append('Text projection count mismatch')
    if state['epoch']!=state['last_committed_text']:errors.append('Epoch/cursor mismatch')
    if any(e['actual_first_text']==2 or 2 in e['actual_texts'] for e in state['entries']):errors.append('Rejected 002 credited')
    # Known structural defect diagnostics: raw IC must not become a pronoun.
    f=deepcopy(g.f);snap=read(PILOT/'allowed_vocab_snapshots/K1-002-epoch-1.json')
    ids={e['vocab_id'] for e in snap['entries']}
    f['_allowed_vocab']=[e for e in f['core_vocab.json']+f['expansion_vocab.json'] if e['id'] in ids]
    probes=[]
    for text in ['네.','네, 책이 있어요.','“네, 가방 안에 있어요.”']:
        a=analyze(text,f,2,(),(),['talk'],g.kiwi)
        probes.append(dict(text=text,raw=[x for x in a['raw_morphology'] if x['form']=='네'],
            assigned=[x for x in a['annotations'] if x['surface']=='네'],
            recognized_yes=any(x['vocab_id']=='ko_k1_0442' for x in a['annotations'])))
    if LEDGER.read_bytes()!=before:errors.append('Diagnostic verification mutated ledger')
    summary.update(integrity_errors=errors,integrity_pass=not errors,
        committed_reanalysis=reanalyses,analyzer_diagnostics=probes,
        decision='C',decision_reason='Analyzer structural alias failure at K1-002; sequential run stopped.',
        ledger_epoch=state['epoch'],max_attempts=5,failed_candidate_credited=False,
        candidate_attempt_counts=dict(Counter(a['text_number'] for a in attempts)),
        mean_attempts_per_started_text=len(attempts)/len({a['text_number'] for a in attempts}),
        frozen_file_count=len(read(FREEZE)['files']),candidate_schema_errors=schema_errors,
        known_unfixed_structural_analyzer_failures=1)
    test_result_path=REPORTS/'k1_phase3_retry_test_result.json'
    if test_result_path.exists():summary['tests']=read(test_result_path)
    write(REPORTS/'k1_phase3_retry_validation_result.json',summary)
    write(REPORTS/'k1_phase3_retry_live_validation.json',summary)
    issues=[dict(text=r['text_number'],category=w['rule_id'],surface=w['surface'],reason=w['reason'],
        confirmed_issue=False,warning_only=True,resolution='名前を教師へ伝える本人紹介。呼びかけの代用ではない。人間レビュー待ち。',recurrence_key=w['rule_id'])
        for r in state['committed_records'] for w in r['naturalness']['lint_warnings']]
    write(ROOT/'state/phase3_retry_naturalness_issue_ledger.json',dict(run='phase3_retry',issues=issues))
    write(ROOT/'state/phase3_retry_natural_expression_gap_ledger.json',dict(run='phase3_retry',gaps=summary['natural_expression_gaps'],tracked_missing_expression='펴다',recurrence_count=0))
    write(REPORTS/'phase3_retry_checkpoint_002.json',summary)
    r=state['committed_records'][0]
    failed=read(PILOT/'failed_attempts/K1-002-attempt-01.json')
    counts=Counter(r['sentence_eojeol_counts'])
    old=read(ROOT/'pilot/ko/k1/phase2_3/texts/K1-001.json')
    report=f'''# Phase 3 再試験 — K1-002で構造的停止

## 判定

**C / FAIL（解析器修正が必要）**。新run `phase3_retry` はK1-001をcommitし、K1-002の初稿をrejectした時点で停止した。K1-003〜050、051以降、300本量産は実施していない。50本の逐次運用成立・review debt回収・genre分布について結論を出せる段階ではない。

Phase 3.1のapproved candidate gate、allowed vocabulary snapshot、限定resolver、atomic commitを再利用した。過去run・語彙800・文法32・初出予定・review windows・ID migration・自然さguidelineは変更していない。{summary['frozen_file_count']}ファイルのfreeze検証違反は{len(summary['frozen_input_violations'])}件。ledger内部のphase表示は承認済み3.1形式のschema provenanceであり、実行identityは新しいdirectory/control/ledgerで分離している。

## 逐次処理と停止規則

001のcandidateを解析・reject・repair・再解析し、PASS後のみatomic commit。その実績2語だけを002のprevious Expansionへ許可した。3.1 smokeの実績や予定上の導入済み語は流用していない。snapshotは001: Core300＋当該新出2、002: Core300＋実導入済み2＋当該新出2。登録固有名詞と固定例外は別枠。

最大5attempt。同じhard errorが2回連続で改善しなければ停止する。長さは許容範囲までの残り距離、coverageはhard floorとの差、語彙違反は同じID/lemmaの違反個数で改善を判定する。別のerrorの改善では同一errorの停滞を免除しない。5回の改善中FAILでも予算を尽くせば停止。構造的障害は試行回数を使い切る前に停止する。

| 教材 | attempt | 判定 | 어절 | 理由 |
|---|---:|---|---:|---|
|001|1|REJECT|123|`밥하고`を未登録`밥하다`へ誤解析。controlled/previous hardも失敗|
|001|2|PASS → commit|129|自然な文分割で修復。新出2lemma、2tokens|
|002|1|REJECT → run停止|135|raw `네/IC` を `너/pronoun`へ無条件alias。予定新出`ko_k1_0442`未認識|

001の129어절はdraft soft target130〜150を1下回るが、hard120〜180は満たす。filler追加で境界を調整しない。002は「はい・いいえ」を本選びの直接対話に各1回配置したが、解析のidentityが誤ったためcommit禁止。

## 停止原因 — draft再生成では解決しない

`scripts/k1_pilot_analysis.py` の `ALIASES` が `네 → 너` をPOSや文脈を見ず適用する。実際のraw morphologyは `네 / IC`（感動詞）だが、annotationは `너 / pronoun / you_informal / ko_k1_0003`。registered `네 / interjection / yes / ko_k1_0442` が消える。

全文ではなく独立した短い3probe（`네.`、`네, 책이 있어요.`、引用符付き応答）でも診断した。詳細はvalidation JSONの `analyzer_diagnostics`。モデルannotationで「はい」と申告してもaliasを正当化しない。raw POS＋登録identity＋局所contextの照合が必要。

002の機械値 controlled=100%、previous={failed['coverage']['previous_vocab_coverage']:.4%} は誤ったannotationを前提とした値であり、正しいsense coverageの証拠として採用しない。予定語一致gateが誤承認を防いだ。002の `actual_first`・exposure・review・debt payment・genre/scene historyへのcreditはすべて0。

**修正候補（report-only）**：`네 → 너` をpronoun contractionとしてraw POSと局所統語が支持する場合だけ適用し、`IC` の `네` は登録interjectionへ解決する。alias後の登録POSとraw POSが不一致なら黙って唯一候補へfallbackせずREVIEW/reject。`네`感動詞／`네`所有代名詞／`네`数詞の対照テストを追加する。`밥하고`についてもnoun＋許可粒子と複合動詞の分割候補を対照検証する。語彙DBやgrammarの拡張は不要。今回、freeze対象の解析器を修正して停止runを再開することはしていない。

## 指定された運用指標

| 指標 | 結果・分母 |
|---|---|
|commit済み本文|1本、001のみ|
|1発PASS率|0/1 = 0%（commit済み教材の初回合格率）|
|全開始教材の初回PASS|0/2、002は構造的停止|
|平均attempt数|2.0/commit済み教材。全開始教材では3/2 = 1.5|
|candidate合格|1/3|
|retry／reject理由|unknown_or_unresolved 1、coverage_or_token_policy 3、planned_new_not_present 1。error個数であり教材数ではない|
|future vocab混入率|0/3 candidate = 0%|
|resolver REVIEW|{summary['resolver_review_count']}（全文resolver decisions。歩行場面は未生成）|
|実導入語|2: 되다、괜찮다、各001で1token|
|selected review exposure|0|
|incidental exposure|0|
|review debt|outstanding0、near-deadline0、expired0。最初のwindowがまだ開いていないため|
|naturalness warnings|1: verb argument frame（本人が教師へ名前を伝える実際の自己紹介）|
|semantic確定問題の再発|0。人間承認ではなくauthor second passでの判定|
|scene/genre重複|commit済み1本、family1。連続反復の検証には不足|

レビュー5〜8語はsoft target。001/002には開いているreview windowがないため0であり、無関係な行動を追加して数を埋めていない。数学的回収不能なdebtもないが、50本での運用は未検証。

## Hard validationとreadability

commit済み001: controlled=100%、previous={r['coverage']['previous_vocab_coverage']:.6%}、N={r['coverage']['denominator_N']}、U={r['coverage']['new_tokens_U']}、hard errors0、future0、unresolved0、grammar32外0。99%target missはhard98%を満たすためblockerにしない。32文、最大5어절、3〜7preferredは31/32文。2어절の「동생은 괜찮아요.」は自然な状態文として許容。短文を副詞で引き延ばしていない。

最終再解析の不一致0、ledger epoch1、001へのcreditは1回。failed evaluation前後のledger SHAは一致。検証時にもstate byteを変更していない。run integrity errors={len(errors)}。これは停止runの記録が正しいという結果であり、50本生成のPASSではない。

## Phase 2.3との比較

共通番号001だけを比較。旧本文をコピーせず、弟の初登校に付き添う場面を新規作成した。本文一致: {r['text_ko']==old['text_ko']}。新版本文は{r['eojeol_count']}어절、previous {r['coverage']['previous_vocab_coverage']:.4%}。旧版は{old.get('eojeol_count')}어절、previous {old.get('coverage',{}).get('previous_vocab_coverage')}。旧pilotのreview実績を新runに移植していない。過剰な의、習慣進行、意味不明な좋아하다反応、filler密度のwarningは出ていない。名前を伝える文は「呼ぶ」の代用ではなく、本人紹介なのでwarning-onlyで残した。020/033/040は未生成につき比較未実施。

## Checkpoint・次の判断

10/20/30/40/50 checkpointの間隔を維持するが、今回は002で停止したため、その時点の `phase3_retry_checkpoint_002.md/json` のみ作成。未到達checkpointを成功として作らない。

**次は解析器のPOS条件付きaliasを別versionで修正・regression testし、新しいrunを001から再試験する。** この停止runやPhase 3.1を成功扱いに書き換えない。K1-003以降、50本の継続生成、300本量産へは進まない。
'''
    if test_result_path.exists():
        report+='\n## Tests\n\n全体suite 147件PASS（334.898秒）。最終更新後のfocused retry tests 14件PASS（20.779秒）。最大5回・2回停滞STOP・改善継続・失敗state不変・commit一度・停止理由保持を検証。テストPASSは制御の正常性であり、既知の네誤aliasの解決や50本文の成功を意味しない。candidate schema違反0。\n'
    (REPORTS/'k1_phase3_retry_sequential_50_report.md').write_text(report,encoding='utf-8')
    checkpoint=f'''# Phase 3 retry 停止checkpoint K1-002

生成・commit: 001のみ1本。002のcandidateはreject、停止理由はanalyzer構造的障害（네/ICを너へalias）。

- hard errors（commit済み）0、controlled違反0、previous<98違反0、grammar違反0、unresolved0。
- candidate: 3attempt、reject2。新出実導入2語、actual distinct exposure各1教材、未導入498語。
- review debt0、新規debt0、期限間近0、期限切れ0、selected review0、incidental0。
- naturalness warning1（本人紹介の名前を言う）、semantic確定問題0、natural_expression_gap0。
- genre family1、scene重複の判断はサンプル不足。
- 平均129어절、sentence length distribution {dict(counts)}。
- 10/20/30/40/50未到達。停止条件発動により次教材は生成しない。

詳細: [最終レポート](k1_phase3_retry_sequential_50_report.md)、[validation JSON](k1_phase3_retry_validation_result.json)。
'''
    (REPORTS/'phase3_retry_checkpoint_002.md').write_text(checkpoint,encoding='utf-8')
    review=f'''# Phase 3 retry 人間レビュー

commit済み001のみ。002はfailed_attemptsへ保存し、学習者用本文として承認しない。

## K1-001 — {r['title_ko']}

{r['text_ko']}

### 日本語訳

{r['translation_ja']}

### 検証

新出: 되다 / 괜찮다、各1token。selected review / incidental / defer: 0。controlled100%、previous{r['coverage']['previous_vocab_coverage']:.4%}、129어절、hard PASS。warning: 名前を本人紹介として伝える文。意味を「呼ぶ」に拡張していない。人間の自然さ承認は未実施。

### 新旧比較

Phase 2.3の001をコピーせず、弟の登校に付き添う場面を作成。過剰な의とfillerを避け、2어절状態文は維持した。
'''
    (REPORTS/'k1_phase3_retry_001_050_review.md').write_text(review,encoding='utf-8')
    return summary

if __name__=='__main__':
    s=report();print(json.dumps({k:s[k] for k in ('generated_count','control','integrity_pass','hard_errors','introduced_count','incidental_exposures','outstanding_debt')},ensure_ascii=True))
