"""Read-only ledger verification and reporting of the isolated stopped run."""
from collections import Counter
from copy import deepcopy
import json
from jsonschema import Draft202012Validator
from k1_phase3_sequential_v3 import (
    SequentialGate, PILOT, LEDGER, REPORTS, FREEZE, summarize, freeze_errors,
)
from k1_phase3_sequential_v3_gate import read, write, ROOT, digest, build_snapshot
from k1_phase3 import sha


def report():
    gate = SequentialGate()
    state = gate.load()
    before = LEDGER.read_bytes()
    result = summarize(gate)
    errors = []
    initial = read(PILOT / 'initial_state.json')
    if initial['epoch'] != 0 or initial['committed_records'] or any(
        e['actual_first_text'] is not None or e['actual_exposure_count']
        for e in initial['entries']
    ):
        errors.append('Initial state was not zero actual experience')

    prior = deepcopy(initial)
    reanalyses = []
    keys = ('text_ko', 'annotations', 'raw_morphology', 'coverage', 'grammar_used',
            'actual_new_vocab_ids', 'actual_review_vocab_ids',
            'incidental_previous_vocab_ids', 'invalid_usage_ids')
    for row in state['committed_records']:
        fresh = gate.evaluate(row['source'], prior, build_snapshot(gate.f, prior, row['text_number']))
        mismatches = [key for key in keys if fresh[key] != row[key]]
        if not fresh['hard_pass'] or mismatches:
            errors.append(dict(text=row['text_number'],errors=fresh['hard_errors'],mismatches=mismatches))
        if row['planned_new_vocab_ids'] != row['actual_new_vocab_ids']:
            errors.append('Planned/actual identity mismatch')
        reanalyses.append(dict(text=row['text_number'],hard_pass=fresh['hard_pass'],mismatches=mismatches))
        # This stopped run has one commit; replay never writes actual state.
        prior['committed_records'].append(row)
        for entry in prior['entries']:
            if entry['vocab_id'] in row['actual_new_vocab_ids']:
                entry['actual_first_text'] = row['text_number']

    attempts = [read(path) for path in sorted((PILOT / 'candidates').glob('*.json'))]
    schema = read(PILOT / 'candidate.schema.json')
    validator = Draft202012Validator(schema)
    schema_errors = []
    for attempt in attempts:
        schema_errors += [dict(text=attempt['text_number'],attempt=attempt['attempt_number'],error=e.message)
                          for e in validator.iter_errors(attempt)]
        copy = deepcopy(attempt)
        expected = copy.pop('candidate_digest')
        if digest(copy) != expected:
            errors.append('Candidate digest mismatch')
        if attempt['ledger_sha_before_evaluation'] != attempt['ledger_sha_after_evaluation']:
            errors.append('Candidate modified authoritative state')
    if schema_errors:
        errors.append(dict(candidate_schema_errors=schema_errors))
    rows = state['committed_records']
    failed = [a for a in attempts if not a['hard_pass']]
    for attempt in failed:
        if any(row['commit_id'] == attempt['candidate_digest'] for row in rows):
            errors.append('Rejected attempt received commit credit')
        path = PILOT / 'failed_attempts' / f"K1-{attempt['text_number']:03d}-attempt-{attempt['attempt_number']:02d}.json"
        if not path.exists() or read(path) != attempt:
            errors.append('Rejected attempt journal/projection mismatch')
    for entry in state['entries']:
        incidental = sum(entry['vocab_id'] in r['incidental_previous_vocab_ids'] for r in rows)
        selected = sum(entry['vocab_id'] in r['actual_review_vocab_ids'] for r in rows)
        actual_texts = [r['text_number'] for r in rows if entry['vocab_id'] in
                        r['actual_new_vocab_ids'] + r['actual_review_vocab_ids'] + r['incidental_previous_vocab_ids']]
        if (entry['incidental_exposure_count'], entry['selected_review_exposure_count']) != (incidental, selected):
            errors.append('Exposure role credit mismatch')
        if entry['actual_texts'] != actual_texts or entry['actual_exposure_count'] != len(actual_texts):
            errors.append('Distinct actual exposure credit mismatch')
    if freeze_errors():
        errors.append('Approved input/history changed')
    if state['epoch'] != len(rows) or state['last_committed_text'] != len(rows):
        errors.append('Commit cursor/epoch mismatch')
    if len(list((PILOT / 'texts').glob('*.json'))) != len(rows):
        errors.append('Committed projection count mismatch')
    if any(a['text_number'] > 2 for a in attempts):
        errors.append('Generated after structural stop')
    if before != LEDGER.read_bytes():
        errors.append('Reporting/reanalysis modified actual ledger')

    # The copied smoke schema's ID pattern also needs correction in a NEXT
    # version before a 50-text run. Do not edit this run's pinned artifacts.
    id_validator = Draft202012Validator(schema['properties']['id'])
    forward_schema_rejections = [f'K1-{n:03d}' for n in range(1, 51)
                                 if not id_validator.is_valid(f'K1-{n:03d}')]
    diagnostic = read(REPORTS / 'k1_phase3_sequential_v3_analyzer_diagnostics.json')
    diagnostic_summary = []
    for probe in diagnostic['probes']:
        diagnostic_summary.append(dict(
            name=probe['name'],
            raw_uri=[t for t in probe['raw_morphology'] if t['form'] == '우리'],
            unresolved=probe['unresolved'],
        ))
    result.update(
        decision='C', sequential_50_completed=False,
        decision_reason='Confirmed full-text/paragraph lexical POS identity instability; stop before K1-002 commit',
        integrity_errors=errors, integrity_pass=not errors,
        initial_actual_state_zero=True, candidate_schema_errors=schema_errors,
        committed_reanalysis=reanalyses, ledger_epoch=state['epoch'],
        actual_commit_transactions=len(rows), failed_candidates_credited=False,
        maximum_committed_text=state['last_committed_text'], maximum_candidate_text=2,
        frozen_file_count=len(read(FREEZE)['files']),
        candidate_attempt_counts=dict(Counter(a['text_number'] for a in attempts)),
        rejected_hard_error_count=sum(len(a['hard_errors']) for a in failed),
        rejected_unresolved_content_count=sum(len(a.get('unresolved_tokens', [])) for a in failed),
        raw_analyzed_candidates=sum('raw_morphology' in a for a in attempts),
        raw_analyzed_future_contaminated_candidates=sum(bool(a.get('invalid_usage_ids')) and
            any(x['reason'] == 'future_expansion' for x in a.get('invalid_usage_ids', [])) for a in attempts),
        diagnostics=diagnostic_summary,
        tests=read(REPORTS / 'k1_phase3_sequential_v3_test_result.json'),
        forward_candidate_schema_rejections=forward_schema_rejections,
        forward_schema_revision_applied=False,
        ten_text_checkpoints_reached=[],
    )
    comparison = []
    for row in rows:
        old_path = ROOT / f"pilot/ko/k1/phase2_3/texts/K1-{row['text_number']:03d}.json"
        if old_path.exists():
            old = read(old_path)
            comparison.append(dict(text=row['text_number'],identical_text=row['text_ko'] == old['text_ko'],
                prior_eojeol=old.get('eojeol_count'),new_eojeol=row['eojeol_count'],
                prior_coverage=old.get('coverage'),new_coverage=row['coverage'],
                new_scene=row['scene_fingerprint'],prior_review_ids=old.get('actually_used_review_vocab_ids', []),
                new_review_ids=row['actual_review_vocab_ids'],prior_credit_imported=False))
    result['phase2_3_comparison'] = comparison
    write(REPORTS / 'k1_phase3_sequential_v3_validation_result.json', result)
    write(REPORTS / 'k1_phase3_sequential_v3_live_validation.json', result)

    issues = [dict(text=r['text_number'],category=w['rule_id'],surface=w['surface'],reason=w['reason'],
                   confirmed_issue=False,warning_only=True,resolution='공책に答えを書く文脈。別義を認可しない。人間による自然さ承認は別途必要。',
                   recurrence_key=w['rule_id']) for r in rows for w in r['naturalness']['lint_warnings']]
    write(ROOT / 'state/phase3_sequential_v3_naturalness_issue_ledger.json',dict(run='phase3_sequential_v3',issues=issues))
    write(ROOT / 'state/phase3_sequential_v3_natural_expression_gap_ledger.json',
          dict(run='phase3_sequential_v3',gaps=result['natural_expression_gaps'],tracked_missing_expression='펴다',recurrence_count=0))
    write(ROOT / 'state/phase3_sequential_v3_run_state.json',dict(read(gate.control),
          last_committed_text=state['last_committed_text'],epoch=state['epoch'],checkpoint_texts=[]))

    vocab = {e['id']:e for e in gate.f['core_vocab.json'] + gate.f['expansion_vocab.json']}
    review = '# Phase 3 sequential v3 — commit済み本文の人間レビュー\n\n未commitの002 candidateは教材本文に含めない。\n'
    for row in rows:
        names = lambda ids: ' / '.join(vocab[i]['lemma'] for i in ids) or 'なし'
        review += f"\n## {row['id']} — {row['title_ko']}\n\n{row['text_ko']}\n\n### 日本語訳\n\n{row['translation_ja']}\n\n"
        review += f"新出: {names(row['actual_new_vocab_ids'])}。Selected review: {names(row['actual_review_vocab_ids'])}。Incidental: {names(row['incidental_previous_vocab_ids'])}。Defer: なし（review window未開）。\n\n"
        review += f"{row['eojeol_count']}어절 / {row['sentence_count']}文 / 最長{row['max_sentence_eojeol']}어절。N={row['coverage']['denominator_N']}, U={row['coverage']['new_tokens_U']}。Controlled 100%、previous {row['coverage']['previous_vocab_coverage']:.6%}。Hard PASS、99% target miss。\n\n"
        review += '使用文法: ' + ', '.join(row['grammar_used']) + '\n\n'
        review += '\n'.join(f"- {w['rule_id']}: {w['surface']} — {w['reason']}" for w in row['naturalness']['lint_warnings'])
        review += '\n\n自己評価は人間による自然さ・日本語訳確認の代替ではない。授業で難しい問題を理解する一つの場面。ゆっくりした説明・再読は問題への対応であり、語数の埋め草ではない。\n'
    (REPORTS / 'k1_phase3_sequential_v3_001_050_review.md').write_text(review,encoding='utf-8')

    table = '\n'.join(f"|{a['text_number']:03d}|{a['attempt_number']}|{'PASS → commit' if a['hard_pass'] else 'REJECT'}|{a.get('eojeol_count','解析前') }|{', '.join(sorted({e['code'] for e in a['hard_errors']})) or '0'}|" for a in attempts)
    reasons = '\n'.join(f'|{k}|{v}|' for k,v in result['retry_reason_distribution'].items())
    row = rows[0]
    cov = row['coverage']
    body = f'''# Phase 3 sequential v3 — K1-002で構造的STOP

## 結果

**C / FAIL：解析器の追加修正が必要。** 承認済みPhase 3.1〜3.3を採用し、別run `phase3_sequential_v3` を実績ゼロから開始した。001のattempt2だけをhard PASS・最終再解析後にatomic commitした。002のattempt2で全文と単文のPOS解決が変わる構造問題を独立再現し、停止した。003〜050を生成していない。051以降・300本量産も行っていない。

旧3.3の001/002やledgerのcreditは流用しない。新しい本文と訳を作成し、このrunの001実績だけを002snapshotへ含めた。過去の成功・停止履歴はfreeze照合で変更なし。

## Candidate gateと処理履歴

Core300＋実導入済みExpansion＋当該教材planned newだけをsnapshot化。max5attempt、同じhard errorが2回連続で改善しなければSTOP、analyzer構造問題でSTOPを維持。candidate評価はledgerを変更しない。hard PASSの最終再解析後だけcommitする。新adapterのsafety testsは9件PASS、failures0/errors0。

|教材|attempt|結果|어절|hard error code|
|---|---:|---|---:|---|
{table}

001初稿の `이야기해요` は未登録 `이야기하다`。`이야기를 해요` に修正してCore noun＋하다で自然に表現できた。DB・意味・文法を拡張していない。002初稿はscene enumにない `weather` により解析前のformat reject。登録scene `nature` へmetadataだけを修正した。002の次稿は登録Core `우리` のPOS identityを全文解析で失った。異なるエラーなので「同じhard errorが2回停滞」は発動せず、構造問題の即時STOPが発動した。attempt上限を使い切るまで構造問題を隠す再生成は行わない。

## 構造的STOPの独立再現

問題の文は `"우리 집에 올 거예요?"`。登録identityは `우리 / pronoun / we / ko_k1_0004`。

|解析スコープ|raw POS|identity/結果|
|---|---|---|
|引用符なし単文|NP|Core pronounとして解決|
|引用符あり単文|NP|Core pronounとして解決|
|短い話者叙述＋引用|NP|Core pronounとして解決|
|candidate内の該当段落|NNG（offset49）|未解決・REVIEW|
|candidate全文|NNG（offset238）|未解決・REVIEW|
|全文から引用符を除いた診断用対照|NP|未解決0|

短いquoted/unquoted probeのparityは通るが、段落と全文で失敗する。sentence16のprecheckはPASSした。したがって「引用符を付けると必ず失敗」ではなく、引用を含むより長い局所文脈でraw POSが不安定になる問題。raw morphologyを保存し、誤POSを唯一の登録候補へ無条件fallbackしなかったため、gateが安全にrejectした。引用符除去は診断だけであり、本文を改変して解析問題を回避・commitしていない。

11probeのraw span・annotation・REVIEWを[diagnostics JSON](k1_phase3_sequential_v3_analyzer_diagnostics.json)に保存。probesは教材でも露出creditでもない。`우리 안에 개가 있어요.` は曖昧な対照で、rawがNPになるため、これだけで「檻」義の正しい拒否を実証したとは扱わない。Coreのpronoun以外を自動許可しない。

既存3.3の `네 / yes` と `아니요 / no_polite` はquoted formを含め正しく認識された。002の予定新出 `ko_k1_0442 / ko_k1_0443` はactual identityと一致したが、別のCore identityの未解決を理由に本文全体をrejectした。

## 指定指標

|指標|結果・分母|
|---|---|
|commit数|1本（001のみ）|
|1発PASS率|0/1 committed = 0%。開始済み教材ベースも0/2。一般化できる標本数ではない|
|平均attempt数|2.0 / committed教材。開始済み教材ベース4/2 = 2.0|
|全candidate / reject|4 / 3|
|future vocab混入|raw解析済み0/3。全journalのfuture検出0/4（1件はformat rejectで未解析）|
|commit済みfuture/invalid|0 / 0|
|resolver REVIEW|{result['resolver_review_count']}（candidate resolver decisionsのREVIEW数）|
|reject側unresolved content|{result['rejected_unresolved_content_count']}。commit側0|
|review / incidental実露出|0 / 0|
|review debt|outstanding0 / near-deadline0 / expired0|
|実導入Expansion|2語：되다 / 괜찮다、各001の1token|
|実露出分布|0回498語、1回2語|
|自然さlint|2件、`nat_restricted_sense`（答えを書く쓰다の文脈）|
|confirmed semantic issue / 再発|0 / 0。ただし人間承認は未実施|
|natural_expression_gap|commit本文0。펴다は継続追跡、今回実例0|
|genre / scene|school1、比較pair0。連続多様性は検証できない|

retry理由はerror code出現数であり、coverageの派生errorも数える。独立原因数や教材数とは異なる。

|error code|件数|
|---|---:|
{reasons}

## Hard validation・coverage

commit済み001: {row['eojeol_count']}어절、{row['sentence_count']}文、最長{row['max_sentence_eojeol']}어절。N={cov['denominator_N']}、U={cov['new_tokens_U']}、controlled100%、previous {cov['denominator_N']-cov['new_tokens_U']}/{cov['denominator_N']} = {cov['previous_vocab_coverage']:.6%}。99% target missはhard98%を満たすためblockerではない。preferred3〜7の達成率は{result['sentence_preferred_compliance']:.2%}、hard max違反0。文法32外・future・retired・invalid・未解決はすべて0。

002 attempt2は135어절、N130、U2、controlled129/130 = 99.230769%、previous127/130 = 97.692308%。未解決1tokenをcontrolledにもpreviousにもcreditしていない。identityが未解決のまま `(N-U)/N` を使ってhard PASSとは扱わない。hard coverage違反として保存した。

fresh raw reanalysisで001のannotation・identity・coverageの差分0。candidate評価前後のledger SHAは全4件一致。failed attemptは導入・露出・review/debt・genre・sceneへcreditしない。epoch1 / cursor1 / record1 / text projection1。報告処理でもledger byte不変。integrity errors={len(errors)}、実journal schema errors={len(schema_errors)}、freeze {result['frozen_file_count']}ファイルの変更・欠落0。

Core300 / Expansion500 / Total800 / tiers200/200/100 / grammar32、初出予定・review windows・coverage・ID migration・意味制限・自然さguidelineを変更していない。review windowが開く前の停止なので、debt0やincidental0はwindow運用成功の証拠ではない。

## 自然さ・訳・比較・checkpoint

001は韓国語の授業で難しい問題を理解して答えを書く場面。意味のないreview文、不要な의、習慣への進行形、좋아하다の万能反応は使用していない。천천히は難しい問題への説明の速さとして使う。쓰다の2warningは공책に答えを書く文脈として記録し、別義を認可しない。semantic self-reviewのYESと訳lint flags0は人間レビューの代替ではない。

Phase 2.3の001と本文は一致せず、新規sceneを生成した。旧本文のcoverage/어절/reviewとの差はvalidation JSONの `phase2_3_comparison` に保存。020/033/040へは未到達。10/20/30/40/50のcheckpointは未到達で作らず、停止時点の[checkpoint002](phase3_sequential_v3_checkpoint_002.md)を保存した。

## 次の修正候補（report-only）

1. 別analyzer versionで、Core `우리` のpronoun/NNG境界を原文字列・POS・名詞修飾位置・発話目的・引用境界・前後の人物参照から限定解決する。NNG→pronounのglobal aliasは不可。「檻」等の別senseを予算内へ追加しない。
2. 短文だけでなく、実段落と全文のquoted/unquoted identity parityをfixture化する。rawを保存し、単文解析が正しいという証拠だけで全文の誤POSを上書きしない。証拠不足はREVIEWを維持する。
3. 別run adapter作成時にcandidate schemaのID pattern更新を見落とした。複製元smoke schemaの `^K1-00[12]$` が残り、003〜050の48IDを拒否することを診断した。今回保存した001/002 journalはschema PASSだが、次の50本run前に50ID全域のpositive/negative contract testが必要。このrunのpinned schemaは書き換えない。

**C：analyzer境界とforward schemaの修正・対照tests・001〜002 smoke後、別の実績ゼロrunで連続試験をやり直す。** この停止runを成功に書き換えず、003以降や300本量産へ進まない。
'''
    (REPORTS / 'k1_phase3_sequential_v3_001_050_report.md').write_text(body,encoding='utf-8')
    write(REPORTS / 'phase3_sequential_v3_checkpoint_002.json', result)
    (REPORTS / 'phase3_sequential_v3_checkpoint_002.md').write_text(
        '# Sequential v3 停止checkpoint K1-002\n\n'
        'C / FAIL。001のみcommit、002は2candidateともreject。全文・段落でCore 우리のPOS identity喪失を再現したため構造的STOP。\n\n'
        'commit hard errors0、candidate4/reject3、実導入2、review0/incidental0/debt0/expired0、epoch1。003以降未生成。10本checkpoint未到達。\n\n'
        '[最終レポート](k1_phase3_sequential_v3_001_050_report.md) / [validation結果](k1_phase3_sequential_v3_validation_result.json)\n',encoding='utf-8')
    (PILOT / 'README.md').write_text(
        '# Phase 3 sequential v3\n\n'
        'Approved Phase 3.3 runtime, zero actual experience, separate state. STOP at K1-002; only K1-001 committed.\n\n'
        'sources/ and candidates/ retain all four attempts. failed_attempts/ has three rejects; texts/ has only the single hard-PASS commit. '
        'allowed_vocab_snapshots/ is derived solely from this run. initial_state.json is zero actual experience. '
        'Authoritative ledger: state/phase3_sequential_v3_001_050_exposure_ledger.json.\n\n'
        'Never resume this stopped run by changing its frozen engine, schemas, or ledger. '
        'The preserved schema ID pattern also requires a new-version fix before a future 50-text test.\n',encoding='utf-8')

    paths = set()
    for pattern in ('k1_phase3_sequential_v3*', 'phase3_sequential_v3_checkpoint_*'):
        paths.update(p for p in REPORTS.glob(pattern) if p.is_file())
    paths.update(p for p in PILOT.rglob('*') if p.is_file())
    paths.update(p for p in (ROOT / 'state').glob('phase3_sequential_v3*.json'))
    paths.update(ROOT / p for p in (
        'scripts/k1_phase3_sequential_v3.py', 'scripts/k1_phase3_sequential_v3_gate.py',
        'scripts/diagnose_k1_phase3_sequential_v3.py', 'scripts/report_k1_phase3_sequential_v3.py',
        'tests/test_k1_phase3_sequential_v3.py',
    ))
    manifest = REPORTS / 'k1_phase3_sequential_v3_artifact_manifest.json'
    paths.discard(manifest)
    write(manifest,dict(run='phase3_sequential_v3',decision='C',
          files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths)}))
    return result


if __name__ == '__main__':
    result = report()
    print(json.dumps({key:result[key] for key in (
        'generated_count','control','integrity_pass','hard_errors','introduced_count',
        'incidental_exposures','outstanding_debt','decision','frozen_file_count',
    )},ensure_ascii=False))
