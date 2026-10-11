"""Independent fresh raw replay in temporary state; actual ledger is read-only."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import tempfile
import re
from jsonschema import Draft202012Validator
from k1_phase3_4 import SmokeGate, PILOT, LEDGER, REPORTS, FREEZE, freeze_errors
from k1_phase3_4_gate import read, write, ROOT, digest, StructuralStop
from k1_phase3 import sha
from k1_phase3_2_analysis import morphology

# The first smoke is immutable diagnostic history. Final validation targets
# the explicitly separate corrected zero-state smoke, never its credit.
INITIAL_PILOT=PILOT
PILOT=ROOT/'pilot/ko/k1/phase3_4_corrected_smoke'
LEDGER=ROOT/'state/phase3_4_corrected_smoke_exposure_ledger.json'

def grammar_meaning_issues(text):
    """One observed restricted reading; not a full particle sense resolver."""
    if not re.search(r'선물로\s',text):
        return []
    return [dict(type='grammar_semantic_restriction',grammar='ko_k1_g30',surface='선물로',
                 reason='Role/as-a-gift meaning outside frozen instrumental/directional meanings')]


def validate():
    g=SmokeGate(PILOT,LEDGER);state=g.load();before=LEDGER.read_bytes();rows=state['committed_records'];errors=[]
    attempts=[read(p) for p in sorted((PILOT/'candidates').glob('*.json'))]
    initial=read(PILOT/'initial_state.json')
    if initial['epoch'] or initial['committed_records'] or any(e['actual_first_text'] is not None or e['actual_texts'] for e in initial['entries']):
        errors.append('Initial actual state not zero')
    reanalyses=[]
    keys=('annotations','raw_morphology','coverage','actual_new_vocab_ids','actual_review_vocab_ids',
          'incidental_previous_vocab_ids','invalid_usage_ids','grammar_used','uri_recovery_audit','quote_recovery_audit')
    with tempfile.TemporaryDirectory() as temporary:
        p=Path(temporary);replay=SmokeGate(p/'run',p/'ledger.json',f=g.f,kiwi=g.kiwi);replay.initialize()
        if replay.load()!=initial:errors.append('Replay initial state differs from actual zero-state snapshot')
        for row in rows:
            prior_bytes=replay.ledger.read_bytes()
            path,fresh=replay.submit(row['source'])
            if replay.ledger.read_bytes()!=prior_bytes:errors.append('Replay candidate changed state before commit')
            differences=[key for key in keys if fresh.get(key)!=row.get(key)]
            if not fresh['hard_pass'] or differences:errors.append(dict(type='fresh_reanalysis',text=row['text_number'],errors=fresh['hard_errors'],mismatches=differences))
            if fresh['hard_pass']:replay.commit(path)
            if row['planned_new_vocab_ids']!=row['actual_new_vocab_ids']:errors.append('Planned actual identity mismatch')
            if row['raw_morphology']!=morphology(row['text_ko'],g.kiwi):errors.append('Original raw morphology changed')
            # This narrow observed construction is not an instrumental/tool
            # use of g30. ID-only grammar enumeration cannot establish senses.
            errors += [dict(issue,text=row['text_number']) for issue in grammar_meaning_issues(row['text_ko'])]
            reanalyses.append(dict(text=row['text_number'],attempt=row['attempt_number'],hard_pass=fresh['hard_pass'],
                mismatches=differences,eojeol=row['eojeol_count'],coverage=fresh.get('coverage'),
                planned_ids=row['planned_new_vocab_ids'],actual_ids=row['actual_new_vocab_ids'],
                uri_recoveries=sum(a['decision']=='RECOVERED' for a in row.get('uri_recovery_audit',[])),
                quote_recoveries=sum(a['decision']=='RECOVERED' for a in row.get('quote_recovery_audit',[]))))
        if replay.load()!=state:errors.append('Replay actual ledger/history/exposure/debt reconstruction differs')
    schema=Draft202012Validator(read(ROOT/'config/languages/ko/k1/phase3_4/candidate.schema.json'))
    source_schema=Draft202012Validator(read(ROOT/'config/languages/ko/k1/phase3_4/source.schema.json'))
    schema_errors=[]
    for a in attempts:
        schema_errors += [dict(text=a['text_number'],error=e.message) for e in schema.iter_errors(a)]
        schema_errors += [dict(text=a['text_number'],source_error=e.message) for e in source_schema.iter_errors(a['source'])]
        copy=deepcopy(a);expected=copy.pop('candidate_digest')
        if digest(copy)!=expected:errors.append('Candidate digest mismatch')
        if a['ledger_sha_before_evaluation']!=a['ledger_sha_after_evaluation']:errors.append('Actual candidate state mutation')
        for recovery in a.get('uri_recovery_audit',[]):
            if recovery['decision']=='RECOVERED' and not all(recovery['context_evidence'].values()):errors.append('Incomplete uri recovery evidence')
            if recovery['permission_granted']:errors.append('Recovery granted vocabulary permission')
    if schema_errors:errors.append(dict(schema_errors=schema_errors))
    cardinality=(len(g.f['core_vocab.json']),len(g.f['expansion_vocab.json']),len(g.f['grammar.json']))
    tiers=dict(Counter(e['tier'] for e in g.f['expansion_vocab.json']))
    if cardinality!=(300,500,32) or tiers!={'E1':200,'E2':200,'E3':100}:errors.append('Frozen data cardinality changed')
    if state['epoch']!=3 or state['last_committed_text']!=3 or [r['text_number'] for r in rows]!=[1,2,3]:errors.append('Smoke commit sequence incomplete')
    if len(state['genre_history'])!=3 or len(state['scene_history'])!=3:errors.append('History transaction count mismatch')
    if len(list((PILOT/'texts').glob('*.json')))!=3 or any(p.name.startswith('K1-004') for p in PILOT.rglob('*.json')):errors.append('Smoke boundary/projection error')
    for entry in state['entries']:
        actual=[r['text_number'] for r in rows if entry['vocab_id'] in r['actual_new_vocab_ids']+r['actual_review_vocab_ids']+r['incidental_previous_vocab_ids']]
        if entry['actual_texts']!=actual or entry['actual_exposure_count']!=len(actual):errors.append('Exposure actual-text reconstruction mismatch')
        if entry['incidental_exposure_count']!=sum(entry['vocab_id'] in r['incidental_previous_vocab_ids'] for r in rows):errors.append('Incidental credit mismatch')
    try:g.snapshot(4);errors.append('Control allowed text 4')
    except StructuralStop:pass
    if read(g.control)['status']!='completed' or read(g.control)['max_text']!=3:errors.append('Smoke control not completed at 3')
    if freeze_errors():errors.append(dict(frozen_changes=freeze_errors()))
    tests={label:read(REPORTS/f'k1_phase3_4_{label}_test_result.json') for label in ('all','focused')}
    if any(t['status']!='PASS' or t['failures'] or t['errors'] for t in tests.values()):errors.append('Regression suites failed')
    audit=read(REPORTS/'k1_phase3_4_uri_context_audit.json')
    forward=read(REPORTS/'k1_phase3_4_forward_schema_audit.json')
    if not audit['all_pass'] or not forward['all_pass']:errors.append('Diagnostic audit failure')
    if before!=LEDGER.read_bytes():errors.append('Validation modified actual ledger')
    failed=[a for a in attempts if not a['hard_pass']]
    if any(a['candidate_digest']==r['commit_id'] for a in failed for r in rows):errors.append('Rejected attempt credited')
    warnings=Counter(w['rule_id'] for r in rows for w in r['naturalness']['lint_warnings'])
    result=dict(phase='3.4',status='PASS' if not errors else 'FAIL',decision='A' if not errors else 'B',errors=errors,
        core_count=cardinality[0],expansion_count=cardinality[1],total_count=800,grammar_count=cardinality[2],tiers=tiers,
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
        outstanding_debt=state['review_debt'],expired_debt=state['expired_review_debt'],
        uri_recoveries=sum(d['decision']=='RECOVERED' for r in rows for d in r['uri_recovery_audit']),
        active_resolver_reviews=sum(d.get('requires_candidate_review',False) for r in rows for d in r['resolver_decisions']),
        initial_actual_state_zero=True,old_credit_imported=False,failed_candidates_credited=False,
        validation_state_unchanged=True,raw_morphology_preserved=True,
        active_smoke_run='phase3_4_corrected_smoke',
        first_smoke_post_semantic_failure=read(REPORTS/'k1_phase3_4_post_semantic_failure.json'),
        first_smoke_credit_imported=False,
        forward_schema_positive_count=len(forward['positive']),forward_schema_negative_count=len(forward['negative']),
        schema_errors=schema_errors,uri_scope_audit_pass=audit['all_pass'],tests=tests,
        frozen_file_count=len(read(FREEZE)['files']),frozen_input_violations=freeze_errors(),
        lint_warnings_by_category=dict(warnings),translation_flags=sum(len(r['translation_fidelity_flags']) for r in rows),
        semantic_flags=sum(len(r['naturalness']['semantic_review']['flags']) for r in rows),
        semantics_are_not_independent_human_gold=True,generation_beyond_003=False,
        provenance={'001':'Frozen raw-source regression, newly evaluated in zero-state run',
                    '002':'Frozen failed raw-source regression, newly evaluated after actual 001 commit',
                    '003':'Fresh photo-present scene, author draft 2 repaired before final zero-state smoke commit'})
    write(REPORTS/'k1_phase3_4_validation_result.json',result)
    return result,rows,audit,forward


def reports(result,rows,audit,forward):
    table='\n'.join(f"|{r['text_number']:03d}|{r['attempt_number']}|{r['eojeol_count']}|{r['coverage']['denominator_N']} / {r['coverage']['new_tokens_U']}|100%|{r['coverage']['previous_vocab_coverage']:.6%}|" for r in rows)
    scope_table='\n'.join(f"|{c['scope']}|{', '.join(d['raw_pos']+' → '+d['decision'] for d in c['uri_audit'])}|{'PASS' if c['passed'] else 'FAIL'}|" for c in audit['cases'])
    test_table='\n'.join(f"|{name}|{t['tests']}|{t['failures']} / {t['errors']}|{t['status']}|" for name,t in result['tests'].items())
    debt_table='\n'.join(f"|{d['vocab_id']}|{d['window_index']}|{d['window']['from']}〜{d['window']['to']}|" for d in result['outstanding_debt'])
    uri=f'''# Phase 3.4 — 우리の文脈依存POS揺れ対策

**{result['decision']} / Phase 3.4 {result['status']}。** 新しいactual stateゼロから001→002→003をhard PASS後に各1回だけcommitした。004以降・300本量産は行っていない。

最終判定の対象は `phase3_4_corrected_smoke`。最初の `phase3_4` smokeは003の生成文「사진을 선물로 주고 싶어요」に、文法30の手段・方向限定を超える「プレゼントとして」の用法があった。自動grammar ID判定と作者semantic reviewが見落とし、003をmechanical PASSとしてcommitした。最終の用法監査で発見し、そのrunをpost-semantic FAILとして停止した。元ledgerと本文は書き換えず、最初の自動PASS reportsは `reports/phase3_4_initial_smoke_post_review/` へ履歴コピーした。

これは新たなraw lexical identity崩壊ではなく、作者draftの文法用法誤りとID-only validatorの既知の意味判定限界である。元runのcreditを一切使わず、さらに別のzero-state smokeを作り、003を `저는 어머니에게 사진을 주고 싶어요.` に直して再検証した。以下のPASS値はその最終clean runだけの値。初回runの不適切なcreditを成功実績へ合算しない。particle senseの人間確認を省かず、既知の危険句선물로はsupplemental final validatorでも検出する。

## 原因と修正

元v3の自然な引用 `"우리 집에 올 거예요?"` は短文ではNP、段落と全文ではNNGだった。Core `우리 / ko_k1_0004 / pronoun / we` とのPOS不一致を旧gateがREVIEW・未解決としてrejectした判断を維持する。

新 `k1_phase3_4_resolver.py` は承認済み3.3 resolverの後段に置く。rawを保存し、元文字spanとcontext evidenceに基づくannotationだけを別layerで復元する。無条件NNG→pronoun alias、単文結果の全文rawへの上書き、generated annotationのみの採用はしない。

対象headは既存Core 집/home・학교/school・가족/familyの3語に限定。NNG時はexact 우리の単一raw span、空白、raw NNGのexact head、登録ID/POS/sense、우리へのparticleなし、直前400文字以内のraw NP speaker/group anchor＋主格/主題/添加particle、一意なannotation span、引用境界を要求する。全根拠が揃った場合だけRECOVERED。동네/E2・교실/Coreは今回の追加headに入れない。

raw NPの通常のweは維持する一方、`우리 안 / 우리 밖 / 우리에서` はnoun読みを否定できずREVIEWへ送る。これによりrawがNPであることだけでもCore pronounを自動承認しない。NNGで話者根拠のない短文や任意の名詞もREVIEW。正しい用法の一部を拒否するfalse negativeを許容する。

## Scope・contrast audit

|scope|raw POSとresolver decision|期待に対する結果|
|---|---|---|
{scope_table}

paragraph / full textのNNGをそのまま保存し、同じCore pronoun identityへ復元した。span offset49 / 238、raw index・前後tokens・following noun・raw話者anchor・quotation context・元annotationを[JSON audit](k1_phase3_4_uri_context_audit.json)に保存。noun対照で他のtokenも未解決になる場合があるが、우리そのものをREVIEWにすることを独立確認した。negative fixtureを自然な教材とは扱わない。

3.3 quote recoveryは変更しない。네 / 아니요 / 한국어の5組quoted/unquoted parity、複数quoted turns、punctuation、全文・paragraph、raw spanの保存を新layerで再実行。Phase 3.2の33境界fixtures、8 frozen用例、28不規則probe（걷다限定resolver含む）も通った。future/retired・planned identity・failed isolation・atomic fault・二回停滞STOPのgateは維持した。

## Smokeと再解析

001/002は元v3のraw本文のみを回帰candidateとして使用した。旧annotation・coverage・ledger/creditをimportせず、001実commit後のsnapshotだけを002に渡した。003は001/002実commit後に新規作成した家族写真の誕生日プレゼント場面。予定新出이 / 그は各1token、네の応答は実導入済み語のincidental露出。

|教材|PASS attempt|어절|N / U|controlled|previous|
|---|---:|---:|---|---|---|
{table}

3本ともplanned IDs == actual IDs、future0 / invalid0 / unresolved0 / grammar違反0 / hard errors0。99% targetはいずれもmissするがhard98%を満たしblockerではない。003は151어절でdraft soft target130〜150を1어절上回るが、hard120〜180内なので不自然な削除・paddingを行わない。

別のtemporary zero-stateへraw sourceだけを順に再投入し、全annotation・raw・coverage・review/incidental・uri/quote auditの差分0、最終state完全一致を確認した。この再解析は本runへのcreditではない。candidate評価前後のledger SHAは全件一致。epoch3、records/texts/genre/scene history各3。validation処理でも実ledger byte不変。旧runの状態・本文・失敗結果を含むfreeze {result['frozen_file_count']}ファイルの変更0。

actual導入{result['actual_introduced_count']}語、異なるvocab/text実露出{result['actual_distinct_vocab_text_exposures']}組、incidental {result['incidental_exposures']}、selected review {result['selected_review_exposures']}。003で初めてreview windowが開いた2語は未消化debtとして記録し、creditしない。期限切れ0、数学的回収不能0。3本smokeは50本運用のdebt回収や多様性の成功証明ではない。

|debt語ID|window index|期限範囲|
|---|---:|---|
{debt_table}

## Tests・自然さ・限界

|suite|tests|failures / errors|結果|
|---|---:|---|---|
{test_table}

validator errors {len(result['errors'])}、schema errors {len(result['schema_errors'])}。active resolver REVIEW0。自然さlintは {result['lint_warnings_by_category']}、translation flags {result['translation_flags']}、semantic flags {result['semantic_flags']}。쓰다は공책・写真の裏へ名前を書くwrite義の文脈として確認する。自己評価とraw解析は独立した人間の言語自然さ承認ではない。初回003でID-only grammar checkが十分でなかったことも、post-semantic failure記録に保持する。

有限の文脈resolverであり、一般的な韓国語POS/sense disambiguationを完成したとは扱わない。語彙800・文法32・schedule/window・ID migration・自然さguidelineは変更なし。追加依存なし。

**A：別runの実績ゼロから001〜050連続試験を再実施可能。** 今回は003で終了し、004以降へ続けない。次runにもmax5attempt・2回停滞STOP・構造STOP・10本checkpoint・050上限を引き継ぐ。300本量産許可ではない。

[validation結果](k1_phase3_4_validation_result.json) / [forward schema report](k1_phase3_4_forward_schema_report.md) / [人間レビュー本文](k1_phase3_4_smoke_review.md) / [設計説明](../docs/ko_k1_uri_context_phase3_4.md)
'''
    (REPORTS/'k1_phase3_4_uri_context_report.md').write_text(uri,encoding='utf-8')
    schema=f'''# Phase 3.4 — 001〜050 forward candidate schema

**{result['status']}。** 元v3のschemaはsmoke用 `^K1-00[12]$` を残して003〜050を拒否した。この更新漏れは旧停止runを変更せず、新versionで修正した。

## 契約と実行上限

新builderはgeneric `^K1-[0-9]{{3}}$` 形式を `$defs` に置き、run契約の001〜050 enumとtext_number 1〜50を組み合わせる。さらにIDとtext_numberが一致する条件を50件設定した。candidate全体にhard PASSのcoverage・length等の既存Schema条件も残す。source Schemaの教材範囲も1〜50。gateはoutput candidateも保存前にSchema検証する。

schemaは50まで受理するが、本smokeのcontrolは `max_text=3`。003 commit後にcompletedとなり、snapshot004を拒否する。text004を生成して境界検査することはしない。将来の100等のrunはbuilderのrange引数で別契約を生成する設計であり、smoke regexをコピーしない。100番のsynthetic Schema testは実本文生成ではない。

## JSON Schema contract test

- 全50 ID：001〜050を、hard-PASS candidateの実データ形を持つobjectで検証して50/50受理。
- 指定negative8件：K1-000 / K1-051 / K1-099 / K1-300 / K1-01 / K1-1 / KO-K1-001 / K2-001をcandidate objectとして8/8拒否。
- ID/番号不一致、controlled coverage不足も拒否。
- 本smokeの実003 candidateがSchemaを通り、予定이・그を本文中で解析してhard PASS・commit。

regexだけの検査ではなく、Draft202012Validatorによる全candidate object validation。詳細は[Schema audit JSON](k1_phase3_4_forward_schema_audit.json)。

## Metadata監査

scene17値は正式 `vocab_review_windows.json.scene_catalog` から継承し、追加なし。weatherはtag/genreであってscene値ではなくnatureへ対応する。元v3のweather format rejectは正しい境界として維持する。

以前genreは任意の非空文字列だった。新source Schemaは人間指定のPhase 3 genre候補と既存承認済みpilot labelを合わせた19値に限定：{', '.join(forward['genres'])}。friendsとfriendshipは既存labelの互換性を保持する。genre quota・scene taxonomyの変更はしない。未知genreと未登録sceneはformat rejectし、retry可能。

これらmetadata enumはレビュー・監視のtaxonomyであり、語彙許可や意味identityの代用ではない。scene/hard grammar/vocab gateは別途実行する。

## 結果

full{result['tests']['all']['tests']} / focused{result['tests']['focused']['tests']} tests PASS。最終clean smokeのactual candidate/source Schema違反0、001〜003 commit済み。run upper bound3と契約upper bound50を分離するtests PASS。最初のsmokeの003で見落とした文法意味制限違反はuri reportとpost-semantic failureに記録し、元creditを引き継がない。旧engines・schemas・停止結果を変更していない。

[우리 report](k1_phase3_4_uri_context_report.md) / [validation JSON](k1_phase3_4_validation_result.json)
'''
    (REPORTS/'k1_phase3_4_forward_schema_report.md').write_text(schema,encoding='utf-8')
    review='# Phase 3.4 smoke — 人間レビュー\n\n001/002はraw source回帰、003は新規場面。自己評価は人間承認の代替ではない。\n'
    for row in rows:
        review+=f"\n## K1-{row['text_number']:03d} — {row['title_ko']}\n\n{row['text_ko']}\n\n### 日本語訳\n\n{row['translation_ja']}\n\n{row['eojeol_count']}어절 / controlled100% / previous{row['coverage']['previous_vocab_coverage']:.6%} / hard PASS / planned = actual {', '.join(row['actual_new_vocab_ids'])}。\n\n"
        review+=f"Review: {row['actual_review_vocab_ids']}。Incidental: {row['incidental_previous_vocab_ids']}。\n\n"
        review+='\n'.join(f"- {w['rule_id']}: {w['surface']} — {w['reason']}" for w in row['naturalness']['lint_warnings']) or 'Warningなし。'
        review+='\n'
    (REPORTS/'k1_phase3_4_smoke_review.md').write_text(review,encoding='utf-8')
    (PILOT/'README.md').write_text(
        '# Phase 3.4 smoke\n\nNew zero actual state; completed only K1-001..003. max_text=3; candidate schema contract=001..050.\n\n'
        '001/002 raw sources were replayed to exercise frozen failures, without prior annotation or credit. 003 is fresh. '
        'Candidate journals never credit exposure. Three hard-PASS commits publish once each. No K1-004+ generated.\n\n'
        'Schemas and uri context overlay: config/languages/ko/k1/phase3_4/. '
        'Authoritative ledger: state/phase3_4_smoke_exposure_ledger.json.\n',encoding='utf-8')
    write(ROOT/'state/phase3_4_corrected_smoke_run_state.json',dict(result['control'],epoch=result['ledger_epoch'],last_committed_text=3))
    write(ROOT/'state/phase3_4_smoke_run_state.json',dict(read(INITIAL_PILOT/'run_control.json'),epoch=3,last_committed_text=3,
        status_scope='Initial automated smoke; stopped after semantic grammar review. Its credit is excluded from the corrected smoke.'))
    paths={p for p in REPORTS.glob('k1_phase3_4*') if p.is_file()}
    paths|={p for p in PILOT.rglob('*') if p.is_file()}
    paths|={p for p in INITIAL_PILOT.rglob('*') if p.is_file()}
    paths|={p for p in (REPORTS/'phase3_4_initial_smoke_post_review').rglob('*') if p.is_file()}
    paths|={p for p in (ROOT/'config/languages/ko/k1/phase3_4').glob('*') if p.is_file()}
    paths|={p for p in (ROOT/'state').glob('phase3_4*.json') if p.is_file()}
    paths|={ROOT/p for p in ('scripts/k1_phase3_4.py','scripts/k1_phase3_4_gate.py','scripts/k1_phase3_4_resolver.py',
        'scripts/build_k1_phase3_4_schemas.py','scripts/audit_k1_phase3_4.py','scripts/validate_k1_phase3_4.py',
        'scripts/run_k1_phase3_4_tests.py','tests/test_k1_phase3_4.py','tests/fixtures/k1_phase3_4_uri_scope.json',
        'docs/ko_k1_uri_context_phase3_4.md')}
    manifest=REPORTS/'k1_phase3_4_artifact_manifest.json';paths.discard(manifest)
    write(manifest,dict(phase='3.4',decision=result['decision'],files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths)}))


if __name__=='__main__':
    result,rows,audit,forward=validate();reports(result,rows,audit,forward)
    print(json.dumps({k:result[k] for k in ('status','decision','committed_count','ledger_epoch','attempts','rejected',
        'committed_hard_errors','errors','incidental_exposures','uri_recoveries','frozen_file_count')},ensure_ascii=False))
    raise SystemExit(0 if result['status']=='PASS' else 1)
