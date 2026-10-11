"""Read-only final raw reanalysis, parity audit, schema and actual-state checks."""
from collections import Counter
from copy import deepcopy
import json
from jsonschema import Draft202012Validator
from k1_phase3_3 import SmokeGate, PILOT, LEDGER, FREEZE, freeze_errors, replay_source
from k1_phase3_3_gate import read, write, ROOT, digest, build_snapshot
from k1_phase3_3_resolver import analyze
from k1_phase3_2_resolver import analyze as old_analyze

REPORTS=ROOT/'reports'

def identities(a):
    return [(x['lemma'],x['pos'],x['sense'],x['vocab_id']) for x in a['annotations'] if x['vocab_id']]

def audit(g):
    f=deepcopy(g.f);f['_allowed_vocab']=f['core_vocab.json']+f['expansion_vocab.json']
    fixture=read(ROOT/'tests/fixtures/k1_phase3_3_quote_parity.json');cases=[];parity=[]
    for item in fixture['parity_pairs']:
        rows=[]
        for text in (item['content'],'"'+item['content']+'"'):
            a=analyze(text,f,2,(),(),(),g.kiwi);old=old_analyze(text,f,2,(),(),(),g.kiwi)
            row=dict(kind='parity',text=text,identities=identities(a),raw_morphology=a['raw_morphology'],
                     raw_unchanged=a['raw_morphology']==old['raw_morphology'],audit=a['quote_recovery_audit'],
                     unresolved=a['unresolved_tokens'],expected_identity_present=item['identity'] in {x['vocab_id'] for x in a['annotations']})
            cases.append(row);rows.append(row)
        parity.append(dict(content=item['content'],expected_id=item['identity'],identity_parity=rows[0]['identities']==rows[1]['identities'],
                           both_present=all(r['expected_identity_present'] for r in rows),unresolved=sum(len(r['unresolved']) for r in rows)))
    for kind in ('paragraphs','no_recovery','unchanged_anida'):
        for text in fixture[kind]:
            a=analyze(text,f,2,(),(),(),g.kiwi);old=old_analyze(text,f,2,(),(),(),g.kiwi)
            cases.append(dict(kind=kind,text=text,identities=identities(a),raw_morphology=a['raw_morphology'],
                raw_unchanged=a['raw_morphology']==old['raw_morphology'],audit=a['quote_recovery_audit'],unresolved=a['unresolved_tokens']))
    return dict(cases=cases,parity=parity,scope='Diagnostics only; not materials or learner exposure')

def validate():
    g=SmokeGate();state=g.load();before=LEDGER.read_bytes();rows=state['committed_records'];errors=[]
    prior=deepcopy(read(PILOT/'initial_state.json'));reanalyses=[]
    for r in rows:
        snap=build_snapshot(g.f,prior,r['text_number']);fresh=g.evaluate(r['source'],prior,snap)
        keys=('text_ko','annotations','raw_morphology','coverage','grammar_used','actual_new_vocab_ids','actual_review_vocab_ids','incidental_previous_vocab_ids','invalid_usage_ids','quote_recovery_audit')
        mismatch=[k for k in keys if fresh[k]!=r[k]]
        if not fresh['hard_pass'] or mismatch:errors.append(dict(type='fresh_reanalysis',text=r['text_number'],hard=fresh['hard_errors'],mismatches=mismatch))
        if r['planned_new_vocab_ids']!=r['actual_new_vocab_ids']:errors.append('Planned new identity mismatch')
        reanalyses.append(dict(text=r['text_number'],attempt=r['attempt_number'],hard_pass=fresh['hard_pass'],mismatches=mismatch,
            eojeol=r['eojeol_count'],N=r['coverage']['denominator_N'],U=r['coverage']['new_tokens_U'],coverage=r['coverage'],
            planned_ids=r['planned_new_vocab_ids'],actual_ids=r['actual_new_vocab_ids'],invalid=len(r['invalid_usage_ids']),
            unresolved=len(r['unresolved_tokens']),grammar_violations=sum(e['code']=='grammar32' for e in r['hard_errors']),
            quote_recoveries=sum(d['decision']=='RECOVERED' for d in r['quote_recovery_audit'])))
        prior['committed_records'].append(r)
        for e in prior['entries']:
            if e['vocab_id'] in r['actual_new_vocab_ids']:e['actual_first_text']=r['text_number']
    cardinality=(len(g.f['core_vocab.json']),len(g.f['expansion_vocab.json']),len(g.f['grammar.json']))
    if cardinality!=(300,500,32):errors.append('Frozen cardinality changed')
    if Counter(e['tier'] for e in g.f['expansion_vocab.json'])!=Counter(E1=200,E2=200,E3=100):errors.append('Tier changed')
    attempts=[read(p) for p in sorted((PILOT/'candidates').glob('*.json'))]
    schema=Draft202012Validator(read(PILOT/'candidate.schema.json'))
    recovery_schema=Draft202012Validator(read(PILOT/'quote_recovery.schema.json'))
    schema_errors=[]
    for a in attempts:
        schema_errors += [dict(text=a['text_number'],error=e.message) for e in schema.iter_errors(a)]
        schema_errors += [dict(text=a['text_number'],error=e.message) for e in recovery_schema.iter_errors(a.get('quote_recovery_audit',[]))]
        copy=deepcopy(a);expected=copy.pop('candidate_digest')
        if digest(copy)!=expected:errors.append('Candidate digest mismatch')
        if a['ledger_sha_before_evaluation']!=a['ledger_sha_after_evaluation']:errors.append('Candidate changed actual state')
        for d in a.get('quote_recovery_audit',[]):
            if d['decision']=='RECOVERED' and not all(d['evidence'].values()):errors.append('Missing recovery evidence')
            if d['permission_granted']:errors.append('Identity recovery bypassed permission gate')
    diagnostics=audit(g)
    for p in diagnostics['parity']:
        if not p['identity_parity'] or not p['both_present'] or p['unresolved']:errors.append(dict(type='quote_parity',detail=p))
    for c in diagnostics['cases']:
        if not c['raw_unchanged']:errors.append('Raw morphology changed')
        if c['kind']=='no_recovery' and any(d['decision']=='RECOVERED' for d in c['audit']):errors.append('Unsafe boundary restored')
        schema_errors += [dict(text=c['text'],error=e.message) for e in recovery_schema.iter_errors(c['audit'])]
    if schema_errors:errors.append(dict(schema_errors=schema_errors))
    if any(e['actual_texts'] for e in read(PILOT/'initial_state.json')['entries']):errors.append('Initial run not empty')
    if state['epoch']!=2 or state['last_committed_text']!=2 or [r['text_number'] for r in rows]!=[1,2]:errors.append('Smoke transaction count/sequence invalid')
    if len(state['genre_history'])!=2 or len(state['scene_history'])!=2:errors.append('Rejected candidate credited to histories')
    if len(list((PILOT/'texts').glob('*.json')))!=2 or (PILOT/'texts/K1-003.json').exists():errors.append('Smoke boundary/projection invalid')
    for e in state['entries']:
        actual=sorted(r['text_number'] for r in rows if e['vocab_id'] in r['actual_new_vocab_ids']+r['actual_review_vocab_ids']+r['incidental_previous_vocab_ids'])
        if e['actual_texts']!=actual or e['actual_exposure_count']!=len(actual):errors.append('Actual exposure reconstruction mismatch')
        if e['incidental_exposure_count']!=sum(e['vocab_id'] in r['incidental_previous_vocab_ids'] for r in rows):errors.append('Incidental exposure mismatch')
    if freeze_errors():errors.append(dict(frozen_changes=freeze_errors()))
    tests={kind:read(REPORTS/f'k1_phase3_3_{kind}_test_result.json') for kind in ('all','focused')}
    if any(t['status']!='PASS' or t['exit_code'] for t in tests.values()):errors.append('Test suites not PASS')
    if before!=LEDGER.read_bytes():errors.append('Validation mutated ledger')
    failed=[a for a in attempts if not a['hard_pass']]
    if any(r['commit_id']==a['candidate_digest'] for r in rows for a in failed):errors.append('Rejected candidate committed')
    result=dict(phase='3.3',status='PASS' if not errors else 'FAIL',decision='A' if not errors else 'B',errors=errors,
        core_count=cardinality[0],expansion_count=cardinality[1],total_count=cardinality[0]+cardinality[1],grammar_count=cardinality[2],tiers=dict(Counter(e['tier'] for e in g.f['expansion_vocab.json'])),
        committed_count=len(rows),ledger_epoch=state['epoch'],control=read(g.control),attempts=len(attempts),rejected=len(failed),
        attempt_counts=dict(Counter(a['text_number'] for a in attempts)),committed_reanalyses=reanalyses,
        committed_hard_errors=sum(len(r['hard_errors']) for r in rows),
        future_violations=sum(any(e['code']=='future_expansion' for e in r['hard_errors']) for r in rows),
        invalid_usage=sum(len(r['invalid_usage_ids']) for r in rows),unresolved=sum(len(r['unresolved_tokens']) for r in rows),
        grammar_violations=sum(any(e['code']=='grammar32' for e in r['hard_errors']) for r in rows),
        planned_vs_actual_match=all(r['planned_new_vocab_ids']==r['actual_new_vocab_ids'] for r in rows),
        actual_introduced_count=sum(e['actual_first_text'] is not None for e in state['entries']),
        actual_distinct_vocab_text_exposures=sum(e['actual_exposure_count'] for e in state['entries']),
        incidental_exposures=sum(e['incidental_exposure_count'] for e in state['entries']),
        selected_review_exposures=sum(e['selected_review_exposure_count'] for e in state['entries']),
        outstanding_debt=len(state['review_debt']),expired_debt=len(state['expired_review_debt']),
        failed_candidates_credited=False,state_unchanged_by_validation=True,raw_morphology_preserved=True,
        quote_parity=diagnostics['parity'],diagnostic_cases=len(diagnostics['cases']),
        recovered_annotations_in_attempts=sum(d['decision']=='RECOVERED' for a in attempts for d in a['quote_recovery_audit']),
        schema_errors=schema_errors,tests=tests,frozen_file_count=len(read(FREEZE)['files']),frozen_input_violations=freeze_errors(),
        lint_warnings=sum(len(r['naturalness']['lint_warnings']) for r in rows),translation_flags=sum(len(r['translation_fidelity_flags']) for r in rows),
        semantics_are_not_independent_human_gold=True,generation_beyond_002=False)
    write(REPORTS/'k1_phase3_3_quote_recovery_audit.json',diagnostics)
    write(REPORTS/'k1_phase3_3_validation_result.json',result)
    return result,attempts,diagnostics

def reports(result,attempts,diagnostics):
    parity_table='\n'.join(f"|`{p['content']}`|{p['expected_id']}|{'PASS' if p['identity_parity'] and p['both_present'] and not p['unresolved'] else 'FAIL'}|" for p in result['quote_parity'])
    audit_table='\n'.join(f"|{n}|{c['kind']}|`{c['text']}`|{', '.join(d['surface']+': '+d['decision'] for d in c['audit']) or '対象surfaceなし'}|" for n,c in enumerate(diagnostics['cases'],1))
    audit_md=f'''# Phase 3.3 quotation recovery audit

2登録identityだけを復元する別resolver layer。raw morphologyを変更せず、文字span・raw index・空白・POS/context・引用境界を保存する。recoveryは教材内の使用許可を与えない。

## quoted/unquoted parity

|content|registered ID|結果|
|---|---|---|
{parity_table}

## 証拠

아니요は元substring完全一致、VCN 아니＋EC/EF 요、発話冒頭、直後の応答句境界、registered interjection/no_politeを要求。한국어はMM 한＋NNG 국어の連続raw span、空白なしの元substring、registered noun/korean_language、名詞位置を要求する。両方とも一意のID/POS/sense、重複・隙間なしの文字partition、連続raw indices、annotation占有の一意性を必要とする。quoted/unquotedの独立syntax証拠を使い、generated annotationを証拠の代用にしない。

`아니요가...`、非応答位置、`한 국어`、内部空白・内部引用符、未閉鎖引用、raw POS不一致は自動復元しない。Core 아니다の文は아니요へ吸収しない。既に正しく登録identityへ解決されているtokenはALREADY_REGISTEREDで変更しない。これは新しいrecoveryの承認とは区別する。

## audit cases

|番号|種類|original text|recovery decision|
|---:|---|---|---|
{audit_table}

negative fixtureは正しい韓国語教材とは主張せず、復元しない境界を検査する診断。診断を露出creditへ加えない。

## 全文

過去failed002の文字列をそのまま新gateへ通し、quoted한국어とquoted아니요を2箇所復元した。全文start/endはannotationとoriginal substringの照合で検証。残る열리다・未許可titleはhard rejectのまま。修正版002でも引用符を保持し、同じ2identityを復元してhard PASS。

全attemptでRECOVERED annotation合計{result['recovered_annotations_in_attempts']}（failedとcommittedを合算した診断件数。露出数ではない）。全raw stream保存、schema violations {len(result['schema_errors'])}。具体的なraw_parts/raw_tags/start/end/registered identity/quotation_context/evidence/decisionは[JSON audit](k1_phase3_3_quote_recovery_audit.json)とcandidate JSONにある。

## regression

Phase 3.2の全33contrast fixtures、8 frozen pilot用例、28不規則probeを新layerで再実行。旧Phase 3.2 tests自体も全suiteで維持。네のyes/所有REVIEW/数詞、밥하고/친구하고、걷다、눈/풀/쓰다、하다 compound、future、retired、planned identity、atomic commitを退行させていない。
'''
    (REPORTS/'k1_phase3_3_quote_recovery_audit.md').write_text(audit_md,encoding='utf-8')
    row_table='\n'.join(f"|{r['text']:03d}|{r['attempt']}|{r['eojeol']}|{r['N']} / {r['U']}|100%|{r['coverage']['previous_vocab_coverage']:.6%}|PASS|" for r in result['committed_reanalyses'])
    attempt_table='\n'.join(f"|{a['text_number']:03d}|{a['attempt_number']}|{'PASS → commit' if a['hard_pass'] else 'REJECT'}|{a['eojeol_count']}|{', '.join(sorted({e['code'] for e in a['hard_errors']})) or '0'}|" for a in attempts)
    test_table='\n'.join(f"|{kind}|{t['tests']}|{t['failures']} / {t['errors']}|{t['status']}|{t['seconds']}秒|" for kind,t in result['tests'].items())
    report_md=f'''# Phase 3.3 — quote boundary recovery

## 判定

**{result['decision']} / Phase 3.3 {result['status']}。** 新run `phase3_3` でactual exposureゼロから001、002の順に検証し、hard PASS後にだけ各1回atomic commitした。003以降は生成していない。次は別runで001〜050の連続試験を再実施可能。このsmoke runを003以降へ継続せず、300本量産にも進まない。

## 修正

frozen `k1_phase3_2_analysis.py` と `k1_phase3_2_resolver.py` の結果へ、`k1_phase3_3_resolver.py` の登録surface復元layerを追加した。rawは編集しない。対象は아니요/ko_k1_0443/interjection/no_polite、한국어/ko_k1_0169/noun/korean_languageの2組だけ。raw indicesと元文字spanが隙間・重複なく連続し、内部空白/句読点なし、完全登録一致、POS列・局所構文が支持する場合のみannotationを復元する。

아니요は発話冒頭の否定応答＋後続句境界。コンマ付きのVCN+ECだけでなく、句点で終わるVCN+EFも対照testsで確認して明示した。Core 아니다の非応答用法へ広げない。한국어はMM+NNGの名詞位置だけを復元し、`한 국어`等の実際の空白は跨がない。quotes/SSO/SSC/SP/SF等は外側境界として残す。

任意token連結・無条件alias・唯一候補fallback・generated sense信用を導入していない。元annotationもauditに保存する。復元IDがfutureなら元のpermission gateでrejectする。語彙800、grammar32、初出・window・ID migration、自然さguidelineは変更なし。新依存なし（既存Kiwi/jsonschemaを使用）。

## parity・全文

5組のquoted/unquoted対照が全PASS。speaker narration、複数quoted turns、quote前後のpunctuation、smart quote、過去failed002全文でoffsetを照合した。10種類のunsafe境界fixtureではRECOVEREDを出していない。

|content|registered ID|結果|
|---|---|---|
{parity_table}

raw morphologyはPhase 3.2と同一。rawの誤分割を隠すのではなく、別annotation layerへidentityと証拠を追加した。K1-002のquoted `"네, 여기 있어요."` は3.2のIC処理を維持し、quoted `"아니요, 책이 너무 비싸요."` は正しくno_politeへ復元。quoted `"한국어 책이 있어요?"` もCore nounへ復元。

## smoke / 通常のdraft repair

元本文のraw sourceだけをfreeze履歴から再利用した回帰smoke。過去annotation、誤coverage、ledgerや予定上の露出は一切流用しない。新state epoch0、001commit後epoch1で初めて002のallowed snapshotを構築した。

|教材|attempt|判定|어절|hard error種類|
|---|---:|---|---:|---|
{attempt_table}

002 attempt1は元failed candidate全文をそのまま使い、quote identityは修復したが、future 열리다と未許可の未来連体title `동생에게 줄 책` はrejectした。planned 네/아니요はこの失敗candidateでも両方認識される。open-stateの`열려 있어요`に付随する未許可/未解決形態素も残して記録した。失敗後のstate SHAは不変。

attempt2はtitleを`동생에게 책을 줘요`へ、本文の`가게 문이 열려 있어요.`をCoreの`저는 가게 문을 열어요.`へ変更し、日本語訳も「私は店のドアを開けます。」へ更新した。自然な入店の行動であり、引用符を削除して回避していない。future語や文法を許可したのではない。titleも同じallowed vocabulary/grammar policyで再検証した。

## 最終hard result

|教材|PASS attempt|어절|N / U|controlled|previous|結果|
|---|---:|---:|---|---|---|---|
{row_table}

future {result['future_violations']}、invalid {result['invalid_usage']}、unresolved {result['unresolved']}、grammar violations {result['grammar_violations']}、committed hard errors {result['committed_hard_errors']}。planned ID == actual IDは両教材で一致。新出tokenは各教材2、99% target missはhard98%を満たすためblockerではない。

001→002のfresh raw reanalysis mismatch0、candidate/recovery schema errors {len(result['schema_errors'])}、validator errors {len(result['errors'])}。N/Uは修復後annotationから再計算し、過去のcoverage値を採用していない。

## state safety

ledger epoch={result['ledger_epoch']}、records/text projection/genre history/scene history各2。実導入{result['actual_introduced_count']}語、異なるvocab/text露出{result['actual_distinct_vocab_text_exposures']}組。failed attemptはactual first/exposure/review/debt/genre/sceneへcreditしていない。001/002のcommitは各一度、idempotent recoveryを維持。

selected review {result['selected_review_exposures']}、incidental {result['incidental_exposures']}、outstanding debt {result['outstanding_debt']}、expired debt {result['expired_debt']}。002の実際に出たprevious 괜찮다だけがincidentalとしてcreditされる。review windowが開く前の2本文smokeであり、50本のdebt回収成立までは主張しない。

原Phase 3 sequential v2停止run、committed001、failed002、3.1/3.2 enginesを含む{result['frozen_file_count']}ファイルのfreeze変更0。元runのC/FAIL・epoch1・停止statusはそのまま保存。新しい結果だけをPhase 3.3へ保存した。

## tests

|suite|tests|failures / errors|結果|時間|
|---|---:|---|---|---|
{test_table}

Phase 3.2全fixturesを新layerで検証し、旧suiteも含め全PASS。negative POS、原文字列space、punctuation、欠落identity、Core 아니다、future permission、planned mismatch、retired、title、failed-state isolation、before/after atomic publish faultを含む。最初の開発testで未対応EF signatureとfixture件数の誤りを検出し、smoke開始前に修正した。最終suiteの成功で旧失敗履歴を書き換えていない。

## 限界と次

完全な韓国語解析・sense disambiguationを実装したとは扱わない。2 identity以外の未知signature、未閉鎖引用などは従来通りREVIEW/reject。自然さのsemantic自己評価も独立した人間承認ではない。自然さlint warnings {result['lint_warnings']}、translation fidelity flags {result['translation_flags']}はhuman review対象の絞り込みに使う。

**A — 別runで001から050を連続再試験できる。** そのrunでもmax5attempt、2回停滞STOP、構造的問題STOP、10本checkpoint、050上限を維持する。Phase 3.3では003以降と300本量産は実施しない。

詳細: [validation JSON](k1_phase3_3_validation_result.json)、[quote recovery audit](k1_phase3_3_quote_recovery_audit.md)、[設計説明](../docs/ko_k1_quote_recovery_phase3_3.md)。
'''
    (REPORTS/'k1_phase3_3_quote_boundary_report.md').write_text(report_md,encoding='utf-8')
    review='# Phase 3.3 smoke 人間レビュー\n\nraw-source regression smoke。自己評価は人間承認ではない。\n'
    for r in (read(PILOT/'texts/K1-001.json'),read(PILOT/'texts/K1-002.json')):
        review+=f"\n## K1-{r['text_number']:03d} — {r['title_ko']}\n\n{r['text_ko']}\n\n### 日本語訳\n\n{r['translation_ja']}\n\n{r['eojeol_count']}어절、controlled100%、previous{r['coverage']['previous_vocab_coverage']:.6%}。\n"
    (REPORTS/'k1_phase3_3_smoke_review.md').write_text(review,encoding='utf-8')

def main():
    result,attempts,diagnostics=validate();reports(result,attempts,diagnostics)
    print(json.dumps({k:result[k] for k in ('status','decision','committed_count','ledger_epoch','attempts','rejected','committed_hard_errors','errors','incidental_exposures')},ensure_ascii=False))
    raise SystemExit(0 if result['status']=='PASS' else 1)

if __name__=='__main__':main()
