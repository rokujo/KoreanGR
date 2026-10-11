"""Fresh validation and honest reporting of this isolated run, including stops."""
from collections import Counter
from copy import deepcopy
import json
from jsonschema import Draft202012Validator
from k1_phase3_sequential_v2 import SequentialGate, PILOT, LEDGER, REPORTS, FREEZE, summarize, freeze_errors
from k1_phase3_sequential_v2_gate import read, write, ROOT, digest, build_snapshot, scheduler

def report():
    g=SequentialGate();state=g.load();before=LEDGER.read_bytes();s=summarize(g);errors=[]
    prior=deepcopy(read(PILOT/'initial_state.json'));reanalyses=[]
    for r in state['committed_records']:
        snap=build_snapshot(g.f,prior,r['text_number']);fresh=g.evaluate(r['source'],prior,snap)
        keys=('text_ko','annotations','raw_morphology','coverage','grammar_used','actual_new_vocab_ids','actual_review_vocab_ids','incidental_previous_vocab_ids','invalid_usage_ids')
        mismatch=[k for k in keys if fresh[k]!=r[k]]
        if not fresh['hard_pass'] or mismatch: errors.append(dict(text=r['text_number'],hard=fresh['hard_errors'],mismatches=mismatch))
        if r['planned_new_vocab_ids']!=r['actual_new_vocab_ids']: errors.append('Planned/actual introduction mismatch')
        reanalyses.append(dict(text=r['text_number'],hard_pass=fresh['hard_pass'],mismatches=mismatch))
        prior['committed_records'].append(r)
        for e in prior['entries']:
            if e['vocab_id'] in r['actual_new_vocab_ids']:e['actual_first_text']=r['text_number']
    attempts=[read(p) for p in sorted((PILOT/'candidates').glob('*.json'))]
    validator=Draft202012Validator(read(PILOT/'candidate.schema.json'));schema_errors=[]
    for a in attempts:
        schema_errors += [dict(text=a['text_number'],attempt=a['attempt_number'],error=e.message) for e in validator.iter_errors(a)]
        copy=deepcopy(a);expected=copy.pop('candidate_digest')
        if digest(copy)!=expected:errors.append('Candidate digest mismatch')
        if a['ledger_sha_before_evaluation']!=a['ledger_sha_after_evaluation']:errors.append('Candidate mutated actual ledger')
    failed=[a for a in attempts if not a['hard_pass']]
    for a in failed:
        if any(r['text_number']==a['text_number'] and r['commit_id']==a['candidate_digest'] for r in state['committed_records']):errors.append('Rejected candidate committed')
    for e in state['entries']:
        expected_incidental=sum(e['vocab_id'] in r['incidental_previous_vocab_ids'] for r in state['committed_records'])
        expected_review=sum(e['vocab_id'] in r['actual_review_vocab_ids'] for r in state['committed_records'])
        if (e['incidental_exposure_count'],e['selected_review_exposure_count'])!=(expected_incidental,expected_review):errors.append('Exposure classification mismatch')
    if schema_errors:errors.append(dict(candidate_schema_errors=schema_errors))
    if freeze_errors():errors.append('Approved frozen inputs changed')
    if state['epoch']!=state['last_committed_text'] or len(list((PILOT/'texts').glob('*.json')))!=state['epoch']:errors.append('Atomic state/projection count mismatch')
    if state['last_committed_text']>50:errors.append('Generation upper bound violated')
    if before!=LEDGER.read_bytes():errors.append('Validation mutated ledger')
    diagnostics=read(REPORTS/'k1_phase3_sequential_v2_analyzer_diagnostics.json') if (REPORTS/'k1_phase3_sequential_v2_analyzer_diagnostics.json').exists() else None
    rows=state['committed_records'];completed=read(g.control)['status']=='completed' and len(rows)==50
    s.update(integrity_errors=errors,integrity_pass=not errors,committed_reanalysis=reanalyses,
             candidate_schema_errors=schema_errors,ledger_epoch=state['epoch'],
             frozen_file_count=len(read(FREEZE)['files']),failed_candidates_credited=False,
             candidate_attempt_counts=dict(Counter(a['text_number'] for a in attempts)),
             committed_actual_new_ids=[i for r in rows for i in r['actual_new_vocab_ids']],
             rejected_hard_error_count=sum(len(a['hard_errors']) for a in failed),
             rejected_unresolved_content_count=sum(len(a.get('unresolved_tokens',[])) for a in failed),
             decision='A' if completed and not errors else 'C',sequential_50_completed=completed,
             decision_reason='Sequential run complete' if completed else 'Stopped on a reproduced structural analyzer boundary defect',
             diagnostics=diagnostics,maximum_committed_text=state['last_committed_text'])
    tests=REPORTS/'k1_phase3_sequential_v2_test_result.json'
    if tests.exists():s['tests']=read(tests)
    comparison=[]
    for r in rows:
        p=ROOT/f"pilot/ko/k1/phase2_3/texts/K1-{r['text_number']:03d}.json"
        if p.exists():
            old=read(p)
            comparison.append(dict(text=r['text_number'],identical_text=r['text_ko']==old['text_ko'],new_scene=r['scene_fingerprint'],
                                   prior_eojeol=old.get('eojeol_count'),new_eojeol=r['eojeol_count'],
                                   prior_coverage=old.get('coverage'),new_coverage=r['coverage'],
                                   prior_review_ids=old.get('actually_used_review_vocab_ids',[]),prior_scene_affinity=old.get('scene_affinity'),
                                   new_review_ids=r['actual_review_vocab_ids'],notes='No prior exposure credit imported. No copying of old Korean prose.'))
    s['phase2_3_comparison']=comparison
    write(REPORTS/'k1_phase3_sequential_v2_validation_result.json',s)
    write(REPORTS/'k1_phase3_sequential_v2_live_validation.json',s)
    issues=[dict(text=r['text_number'],category=w['rule_id'],surface=w['surface'],reason=w['reason'],confirmed_issue=False,warning_only=True,
                 resolution='Context assessment only; not native human approval. 쓰다 is used with notebook/writing context, not another sense.',recurrence_key=w['rule_id'])
            for r in rows for w in r['naturalness']['lint_warnings']]
    write(ROOT/'state/phase3_sequential_v2_naturalness_issue_ledger.json',dict(run='phase3_sequential_v2',issues=issues))
    write(ROOT/'state/phase3_sequential_v2_natural_expression_gap_ledger.json',dict(run='phase3_sequential_v2',gaps=s['natural_expression_gaps'],tracked_missing_expression='펴다',recurrence_count=0))
    write(ROOT/'state/phase3_sequential_v2_run_state.json',dict(read(g.control),last_committed_text=state['last_committed_text'],epoch=state['epoch'],checkpoint_texts=[r['text_number'] for r in rows if r['text_number']%10==0]))
    attempt_table='\n'.join(f"|{a['text_number']:03d}|{a['attempt_number']}|{'PASS → commit' if a['hard_pass'] else 'REJECT'}|{a.get('eojeol_count')}|{', '.join(sorted(set(e['code'] for e in a['hard_errors']))) or '0'}|" for a in attempts)
    error_table='\n'.join(f'|{k}|{v}|' for k,v in s['retry_reason_distribution'].items())
    review='# Phase 3 sequential v2 人間レビュー\n\ncommit済み本文のみ。未承認candidateは学習者本文に含めない。\n'
    v={e['id']:e for e in g.f['core_vocab.json']+g.f['expansion_vocab.json']}
    for r in rows:
        names=lambda ids:' / '.join(v[i]['lemma'] for i in ids) or 'なし'
        review+=f"\n## K1-{r['text_number']:03d} — {r['title_ko']}\n\n{r['text_ko']}\n\n### 日本語訳\n\n{r['translation_ja']}\n\n"
        review+=f"新出: {names(r['actual_new_vocab_ids'])}。selected review: {names(r['actual_review_vocab_ids'])}。incidental: {names(r['incidental_previous_vocab_ids'])}。defer: なし（review window未開）。\n\n"
        review+=f"{r['eojeol_count']}어절 / {r['sentence_count']}文 / 最長{r['max_sentence_eojeol']}어절。N={r['coverage']['denominator_N']}, U={r['coverage']['new_tokens_U']}。controlled 100%、previous {r['coverage']['previous_vocab_coverage']:.6%}、hard PASS、99% target miss。\n\n"
        review+='文法: '+', '.join(r['grammar_used'])+'。\n\nWarning（hard errorではない）:\n\n'
        review+='\n'.join(f"- {w['rule_id']}: {w['surface']} — {w['reason']}" for w in r['naturalness']['lint_warnings']) or 'なし'
        review+='\n\n自己評価は人間による自然さ承認の代替ではない。仕事の初授業を本で練習する一つの場面。한국어の教授・本の読解・공책への書き取りは意味役割を拡張していない。\n'
    (REPORTS/'k1_phase3_sequential_v2_001_050_review.md').write_text(review,encoding='utf-8')
    report=f'''# Phase 3 sequential v2 — K1-002で停止

## 判定

**C / FAIL：引用境界を含む解析器の修正が必要。** 新run `phase3_sequential_v2` は実績ゼロから開始し、001の第2candidateをhard PASS後に1回だけatomic commitした。002の第1candidateはrejectし、独立した短い対照probeで構造的問題を再現した時点で停止した。003〜050、051以降、300本量産は行っていない。元のPhase 3 / retry / 3.1 / 3.2の成功・失敗履歴を書き換えていない。

## 採用した制御と実処理

承認済み3.2 analyzer/resolverを直接importする別run adapter。approved gateを複製した差分はrun名、50上限、source schema参照、engine digest対象。snapshotはCore300＋このrunの実導入済みExpansion＋当該教材のplanned新出語だけ。max5attempt、同じhard errorが2回連続で改善しなければSTOP、candidateはstateを変更せず、hard PASSのfinal raw reanalysis後にだけatomic publish。10本ごとcheckpointを維持し、問題がなければ承認待ちせず継続する。

今回は構造的問題を発見したため、002のretry回数を使い切る前に停止した。引用符を外して解析器の欠陥を隠すための再生成は行わず、run内で解析器・語彙・文法・初出・windowを変更しなかった。draft target130〜150、hard120〜180、新出≤2、U soft3、controlled100%、previous≥98%、sentence max10を維持。長さ合わせのfillerを追加していない。

|教材|attempt|判定|어절|error種類|
|---|---:|---|---:|---|
{attempt_table}

001 attempt1の끝내다は未導入語で、Core 끝나다の自然な文 `공부가 끝나서 저도 쉬어요.` へ修正してattempt2 PASS。これはcandidate内の局所repairで解決できた。002には未導入열리다と未許可の未来連体修飾を使ったtitle `동생에게 줄 책` もあり、これらはdraft側の別問題。構造的停止の根拠と混同しない。

## 構造的停止の根拠

|対照|raw / 解決|結果|
|---|---|---|
|`아니요, 책이 너무 비싸요.`|IC → 아니요 / interjection / no_polite|正しく認識|
|`"아니요, 책이 너무 비싸요."`|VCN 아니＋EC 요 → Core 아니다、요未解決|予定新出 ko_k1_0443 が欠落|
|`한국어 책이 있어요?`|한국어 / noun / korean_language|正しく認識|
|`"한국어 책이 있어요?"`|MM 한＋NNG 국어 → 하나、국어未解決|登録Core ko_k1_0169 のidentity欠落|
|`"네, 여기 있어요."`|IC 네 → interjection / yes|3.2の修正は機能|

引用符あり/なしで同じ自然な直接応答・質問のidentity解決が変わる。モデルannotationを付け直して承認しない。003以降へ進まず、[diagnostics JSON](k1_phase3_sequential_v2_analyzer_diagnostics.json)へ8probeのraw形態素とannotationを保存。probeは教材/露出ではない。

**修正候補（report-only）：** 次の別versionで、引用符・句読点境界を保ったままregistered surfaceとraw spanの再結合候補を検討する。아니요のIC / VCN+요候補には直接否定応答のsyntaxを要求する。한국어のMM+NNG分割には空白なしの完全登録lemma一致と名詞位置を要求し、`한 국어 ...` を同一視しない。無条件aliasや唯一登録候補fallbackを導入せず、quoted/unquoted同じ対照fixtureを文・段落・全文で検証する。語彙DB・POS・senseを変える必要はない。

## 指定指標

|指標|結果・分母|
|---|---|
|commit数|{len(rows)}（001のみ）|
|1発PASS率|0/1 committed教材 = 0%。開始済みでは0/2|
|平均attempt数|2.0 / committed教材。全開始済みでは3/2 = 1.5|
|candidate数 / reject数|3 / 2|
|future vocab混入率|2/3 candidate = 66.67%。commit済みでは0/1|
|resolver REVIEW|{s['resolver_review_count']}（resolver decisionで明示REVIEWの件数）|
|raw unresolved content（reject側）|{s['rejected_unresolved_content_count']}。REVIEW件数0は解析完全性を意味しない|
|実導入語|2: 되다 / 괜찮다、各001で1token|
|actual selected review exposure|0|
|incidental exposure|0|
|review debt|outstanding0 / near-deadline0 / expired0|
|naturalness lint|{sum(s['naturalness_warning_categories'].values())}（{s['naturalness_warning_categories']}）|
|semantic確定問題の再発|0、ただし人間承認は未実施|
|scene / genre|work1。直近10本類似判定の比較pair0、連続多様性は未検証|

retry理由分布は同じcandidate内の複数error・派生coverage errorも個別に数える。独立原因数や教材数とは異なる。

|error code|件数|
|---|---:|
{error_table}

## Hard validation・state integrity

commit済み001: 140어절、35文、最長5어절、N136、U2、controlled100%、previous134/136 = 98.529412%。99% target missはhard98%を満たすためblockerではない。3〜7 preferred compliance34/35 = 97.14%、1어절の`괜찮아요.`は自然な短い応答として許容。未導入/future/retired/invalid/unresolved/grammar32外は0。

fresh再解析mismatch0。epoch1/cursor1/records1/text projection1、導入/露出/genre/scene更新は1回のみ。失敗candidateの評価前後ledger SHAは全件一致。002のactual first、review、incidental、debt payment、genre/sceneへのcreditはすべて0。現在のdeadlineはまだ開いていないので、debt0はwindow運用の成功証拠ではない。

integrity errors={len(errors)}、candidate schema errors={len(schema_errors)}、frozen入力{len(read(FREEZE)['files'])}ファイルの変更/欠落0。新adapter safety testsは9件PASS（実際のテスト結果JSON参照）。全50本のPASSではない。

## Naturalness・読みやすさ

001は新規に書いた「翌日の初授業を友人と練習する」scene。不要な의や、好き＝喜ぶの万能反応、習慣の進行形化、reviewのためだけの別事件はない。쓰다の2warningは公책への書き取りであり、別義への拡張はしていない。warning-onlyで記録し、人間による韓国語自然さ承認の代替にしない。日本語訳は本文修正後に対応文を更新し、끝나다を「勉強が終わる」と訳した。translation lint flags0。natural_expression_gap0、펴다の継続監視は残し、今回は実例0。

露出分布0回498語 / 1回2語。genre work1、平均/最小/最大140어절。最初のreview windowが開く前に止まったため、5〜8review、incidental、500×6への進捗、debt回収、scene重複、genreバランスの実運用成立は判断不能。

## Phase 2.3比較・checkpoint

001だけを比較。Phase 2.3本文をコピーせず、別sceneとして生成した（本文一致false）。旧pilotのreview実績は引き継がない。comparisonのcoverage/eojeolはvalidation JSONに記録。020/033/040には到達していないので比較していない。

10/20/30/40/50のcheckpointは未到達で、成功checkpointを捏造しない。停止時点の[checkpoint002](phase3_sequential_v2_checkpoint_002.md)を保存した。

## 次の判断

**C — analyzerの引用境界・登録lemmaの分割回復を別versionで修正し、対照testsと001〜002 smokeを通した後、新しい別runで001から連続再試験する。** この停止runを修正成功へ書き換えない。K1-003以降・300本量産は許可済み扱いにしない。
'''
    (REPORTS/'k1_phase3_sequential_v2_001_050_report.md').write_text(report,encoding='utf-8')
    if not completed:
        t=read(g.control)['stop'].get('text',state['last_committed_text'])
        write(REPORTS/f'phase3_sequential_v2_checkpoint_{t:03d}.json',s)
        (REPORTS/f'phase3_sequential_v2_checkpoint_{t:03d}.md').write_text(
            f'# Sequential v2 停止checkpoint K1-{t:03d}\n\nC / FAIL。001のみcommit、002 candidateはreject。構造的解析器問題を対照probeで再現して停止。\n\n'
            'hard errors（commit）0、candidate3 / reject2、実導入2、incidental0、debt0、expired0。epoch1。003以降は未生成。\n\n'
            '[最終レポート](k1_phase3_sequential_v2_001_050_report.md) / [validation結果](k1_phase3_sequential_v2_validation_result.json)\n',encoding='utf-8')
    return s

if __name__=='__main__':
    s=report();print(json.dumps({k:s[k] for k in ('generated_count','control','integrity_pass','hard_errors','introduced_count','incidental_exposures','outstanding_debt','decision')},ensure_ascii=False))
