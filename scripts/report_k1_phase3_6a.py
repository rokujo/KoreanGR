"""Post-run reports and independent actual-history replay; no old artifact writes."""
from collections import Counter
from datetime import datetime
from pathlib import Path
import json
import math
import statistics
import tempfile
from k1_phase3 import ROOT,read,write,similarity
from k1_phase3_6a import ProductionGate,PILOT,LEDGER,TIMING,freeze_errors,locked_code
from k1_phase3_6a_gate import scheduler


def distribution(values):
    if not values:return dict(n=0,min=None,max=None,mean=None,median=None,p90=None)
    xs=sorted(values)
    return dict(n=len(xs),min=min(xs),max=max(xs),mean=statistics.mean(xs),median=statistics.median(xs),p90=xs[math.ceil(.9*len(xs))-1])


def main():
    gate=ProductionGate();state=gate.load();rows=state['committed_records'];timing=read(TIMING)
    control=read(gate.control);attempts=[read(p) for p in sorted((PILOT/'candidates').glob('*.json'))]
    errors=[]
    if freeze_errors():errors.append('historical_freeze_changed')
    if locked_code():errors.append('benchmark_code_changed')
    # A new zero-state validation replay, never historical planned credit.
    replay_errors=[]
    with tempfile.TemporaryDirectory(prefix='k1_phase3_6a_replay_') as d:
        replay=ProductionGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=gate.kiwi);replay.initialize()
        for r in rows:
            p,c=replay.submit(r['source'])
            if not c['hard_pass']:
                replay_errors.append(dict(text=r['text_number'],errors=c['hard_errors']));break
            original=next(x for x in attempts if x['candidate_digest']==r['commit_id'])
            approval=read(PILOT/'author_reviews'/f"K1-{r['text_number']:03d}-attempt-{r['attempt_number']:02d}.json")
            replay.approve(p,approval['evidence']);result=replay.commit(p)
            for key in ('annotations','raw_morphology','coverage','actual_new_vocab_ids','actual_review_vocab_ids','incidental_previous_vocab_ids'):
                if result[key]!=r[key]:replay_errors.append(dict(text=r['text_number'],field=key))
        if replay.load()['entries']!=state['entries']:replay_errors.append('actual_entry_state_mismatch')
    if replay_errors:errors.append('ledger_replay_failed')
    times=[r['total_seconds'] for r in timing['texts'] if r.get('committed')]
    per_text=distribution(times);complete=len(rows)==10 and control['status']=='completed'
    wall=timing.get('production_end_counter',timing['texts'][-1].get('end_counter',timing['production_start_counter']))-timing['production_start_counter']
    stage=Counter();retry=Counter()
    for t in timing['texts']:
        stage.update(t.get('stages',{}))
        for a in t['attempts']:
            if not a['hard_pass']:retry.update(e['code'] for e in a['hard_errors'])
    semantic=Counter(c['decision'] for r in rows for c in r.get('semantic_grammar_warnings',[]))
    natural=Counter(w['rule_id'] for r in rows for w in r['naturalness']['lint_warnings'])
    sentences=[len(s.split()) for r in rows for s in r['source']['sentences']]
    near=[d for d in state['review_debt'] if d['window']['to']-len(rows)<=2]
    similarity_rows=[dict(a=a['text_number'],b=b['text_number'],score=similarity(a['scene_fingerprint'],b['scene_fingerprint']))
        for i,a in enumerate(rows) for b in rows[max(0,i-10):i]]
    max_similarity=max((r['score'] for r in similarity_rows),default=0)
    confirmed=[h for r in timing['texts'] for h in r.get('author_review_history',[]) if h['evidence']['naturalness']=='REPAIR']
    failed=[r for r in attempts if not r['hard_pass']]
    retry_future=sum(sum(x['reason']=='future_expansion' for x in r.get('invalid_usage_ids',[])) for r in attempts)
    first_pass=sum(r['attempt_number']==1 for r in rows)
    estimate=dict(estimated_300_mean_hours=per_text['mean']*300/3600,estimated_300_median_hours=per_text['median']*300/3600) if complete else None
    performance='GREEN' if complete and per_text['median']<=180 else 'YELLOW' if complete and per_text['median']<=300 else 'RED' if complete else 'INCOMPLETE'
    verdict='C'
    if complete and not errors:
        verdict='B' if confirmed or max_similarity>=.85 else 'D' if per_text['median']>300 else 'A'
    labels=dict(A='PRODUCTION_READY_FOR_50',B='QUALITY_ADJUSTMENT',C='STRUCTURAL_FAIL',D='PERFORMANCE_FAIL')
    result=dict(phase='3.6a',verdict=verdict,status=labels[verdict],completed=complete,committed_count=len(rows),stop=control.get('stop') or timing.get('stop'),
        artifact_integrity_errors=errors,ledger_replay_errors=replay_errors,state_epoch=state['epoch'],
        committed_hard_errors=sum(len(r['hard_errors']) for r in rows),rejected_attempt_count=len(failed),
        candidate_hard_error_distribution=dict(retry),first_attempt_pass_count=first_pass,structural_scope_mismatch_count=sum(x['structural_defect'] for a in attempts for x in a.get('scope_identity_checks',[])),resolved_scope_mismatch_count=sum(x['decision']=='RECOVERED_SAFE' for a in attempts for x in a.get('scope_identity_checks',[])),ne_recovery_count=sum(x['decision']=='RECOVERED' for r in rows for x in r.get('ne_response_recovery_audit',[])),
        first_attempt_pass_ratio=first_pass/len(rows) if rows else None,
        attempts_per_committed_text=[r['attempt_number'] for r in rows],mean_attempts=statistics.mean([r['attempt_number'] for r in rows]) if rows else None,
        total_candidate_attempts=len(attempts),future_contaminated_candidate_count=sum(any(x['reason']=='future_expansion' for x in r.get('invalid_usage_ids',[])) for r in attempts),
        future_usage_occurrences=retry_future,future_in_committed=sum(any(x['reason']=='future_expansion' for x in r['invalid_usage_ids']) for r in rows),
        unknown_unresolved_in_committed=sum(len(r['unresolved_tokens']) for r in rows),planned_identity_mismatch_in_committed=sum(r['planned_new_vocab_ids']!=r['actual_new_vocab_ids'] for r in rows),
        semantic_grammar_warnings=sum(semantic.values()),semantic_warning_distribution=dict(semantic),
        naturalness_warnings=sum(natural.values()),naturalness_warning_distribution=dict(natural),confirmed_language_quality_issues=len(confirmed),
        translation_fidelity_flags=sum(len(r['translation_fidelity_flags']) for r in rows),
        review_debt=state['review_debt'],expired_review_debt=state['expired_review_debt'],near_deadline_debt=near,
        selected_review_exposures=sum(e['selected_review_exposure_count'] for e in state['entries']),
        incidental_exposures=sum(e['incidental_exposure_count'] for e in state['entries']),
        actual_new_introduced=sum(e['actual_first_text'] is not None for e in state['entries']),
        actual_exposure_distribution=dict(Counter(e['actual_exposure_count'] for e in state['entries'])),
        genre_distribution=dict(Counter(r['genre'] for r in rows)),scene_similarities=similarity_rows,max_scene_similarity=max_similarity,
        eojeol_distribution=distribution([r['eojeol_count'] for r in rows]),sentence_length_distribution=dict(Counter(sentences)),
        preferred_sentence_ratio=sum(3<=n<=7 for n in sentences)/len(sentences) if sentences else None,
        production_wall_seconds=wall,per_text_seconds=per_text,stage_seconds=dict(stage),
        estimated_300_mean_hours=estimate['estimated_300_mean_hours'] if estimate else None,
        estimated_300_median_hours=estimate['estimated_300_median_hours'] if estimate else None,
        attempted_text_count=len(timing['texts']),
        attempts_per_attempted_text=[len(t['attempts']) for t in timing['texts']],
        semantic_warnings_all_candidates=sum(len(a.get('semantic_grammar_warnings',[])) for a in attempts),
        failed_attempt_state_unchanged=all(a['ledger_sha_before_evaluation']==a['ledger_sha_after_evaluation'] for a in failed),
        unassigned_between_text_seconds=max(0,wall-sum(r.get('total_seconds',0) for r in timing['texts'])),estimated_300_serial_hours=estimate,performance=performance,
        pre_run_regression=read(ROOT/'reports/k1_phase3_6a_pre_regression.json'),
        post_run_regression=read(ROOT/'reports/k1_phase3_6a_post_regression.json') if (ROOT/'reports/k1_phase3_6a_post_regression.json').exists() else None)
    if not result['pre_run_regression']['success'] or (result['post_run_regression'] and not result['post_run_regression']['success']):
        result['artifact_integrity_errors'].append('regression_failure');result['verdict']='C';result['status']=labels['C']
    top_stage=max(stage,key=stage.get) if stage else None
    result['largest_pipeline_stage']=top_stage
    result['speed_optimization_target']='generator/author callback' if top_stage=='author_draft' else top_stage
    result['total_attempts']=len(attempts)
    result['frozen_history_changes']=freeze_errors()
    result['benchmark_code_changes']=locked_code()
    timing.update(production_wall_seconds=wall,per_text_statistics=per_text,stage_totals_seconds=dict(stage),estimated_300_serial_hours=estimate,
        engineering_before_production_seconds=(datetime.fromisoformat(timing['production_start_utc'])-datetime.fromisoformat(timing['engineering_start_utc'])).total_seconds())
    write(TIMING,timing);write(ROOT/'reports/k1_phase3_6a_validation_result.json',result)
    write(ROOT/'reports/k1_phase3_6a_validation_result.json',result)
    v={e['id']:e for e in gate.f['core_vocab.json']+gate.f['expansion_vocab.json']}
    def names(ids):return '、'.join(v[i]['lemma'] for i in ids) or 'なし'
    human=['# Phase 3.6a 人間抜き取りレビュー用本文','', '作者/LLMによる確認は独立goldではありません。semantic warningは誤文法の判定ではありません。','']
    for r in rows:
        human += [f"## {r['id']} — {r['title_ko']}",'',f"{r['eojeol_count']}어절 / 新出: {names(r['actual_new_vocab_ids'])} / review: {names(r['actual_review_vocab_ids'])} / incidental: {names(r['incidental_previous_vocab_ids'])}",
            f"warnings: semantic {len(r['semantic_grammar_warnings'])}, naturalness {len(r['naturalness']['lint_warnings'])}; controlled 100%, previous {r['coverage']['previous_vocab_coverage']:.2%}",'',r['text_ko'],'',r['translation_ja'],'']
    (ROOT/'reports/k1_phase3_6a_human_review_001_010.md').write_text('\n'.join(human),encoding='utf-8')
    doc=['# Phase 3.6a Production-lite benchmark','',f"判定 **{result['verdict']}: {result['status']}**。commit {len(rows)}/10。K1-011以降は生成していません。",'',
        '## Policy / engineering','',
        '語彙identity・初出・coverage・長さ・grammar32形式・明示的な未許可構文・title・最終再解析・atomic publishをhard検証します。Phase 3.5のsemantic registryは変更せず、PASS/REVIEW/heuristic FAILを診断に使用します。role分類だけでrejectせず、自然な基本用法は作者の文脈レビューで確認します。',
        '既知の물을 받고 마셔요だけを、exact span、말/VX+시/EP+어요/EF、明示的な飲料目的語、받다の接続、登録drink義・正規活用を根拠に復元。rawは保存し、無条件aliasはありません。単文・引用・段落・全文と否定対照を回帰検証しました。',
        '実際の作者はこのLLMであり、snapshot取得後に各本文を作成したローカルfile callbackです。外部モデルAPIの自動運転ベンチマークではありません。作者時間は思考・ファイル転送・ツール待ちを含む実elapsed wall timeで、保存済み本文の高速replayを生成速度として計測していません。',
        f"pre-run engineering/setup {timing['engineering_before_production_seconds']:.1f}s。full pre-suite {result['pre_run_regression']['tests']} tests / {result['pre_run_regression']['seconds']:.1f}s。production開始後のcode/config差分: {locked_code()}。過去freeze差分: {freeze_errors()}。",'',
        '## Generation / validation','',
        f"committed hard errors {result['committed_hard_errors']}、rejected attempts {len(failed)}、unknown/unresolved {result['unknown_unresolved_in_committed']}、planned identity mismatch {result['planned_identity_mismatch_in_committed']}。1発PASS {first_pass}/{len(rows)}、平均attempt {result['mean_attempts']}。future混入candidate {result['future_contaminated_candidate_count']}/{len(attempts)}、committed future 0。retry理由: {dict(retry)}。",'',
        '| Text | attempt | 어절 | N / U | previous | semantic warnings | selected / incidental | seconds |','|---|---:|---:|---|---:|---:|---:|---:|']
    for r,t in zip(rows,[x for x in timing['texts'] if x.get('committed')]):
        c=r['coverage'];doc.append(f"| {r['id']} | {r['attempt_number']} | {r['eojeol_count']} | {c['denominator_N']} / {c['new_tokens_U']} | {c['previous_vocab_coverage']:.2%} | {len(r['semantic_grammar_warnings'])} | {len(r['actual_review_vocab_ids'])} / {len(r['incidental_previous_vocab_ids'])} | {t['total_seconds']:.2f} |")
    doc += ['', '## Throughput','', f"production wall {wall:.2f}s。per text: {json.dumps(per_text)}。性能目安 {performance}。",f"stage totals (s): {json.dumps(dict(stage))}。between-text/controller外のwall {result['unassigned_between_text_seconds']:.2f}sもrun wallへ含めています。",f"300 serial estimate (hours): {json.dumps(estimate)}。mean/medianは各教材の実測totalを基準とします。全run overheadを含むwall/commitベース推定: {wall/len(rows)*300/3600 if complete else '完走前のため算定しない'}h。",'10本の初期E1・ローカル作者経路という小標本です。後期の語彙負荷、人間レビュー、将来のAPI呼び出し待ち、再修正・全300本の最終露出監査を含む納期保証ではありません。','',
        '## Quality / review operation','',f"semantic warnings {sum(semantic.values())}: {dict(semantic)}。これは曖昧分類を含み、語彙coverageとは独立です。naturalness warnings {sum(natural.values())}: {dict(natural)}。作者確認された問題 {len(confirmed)}、translation flags {result['translation_fidelity_flags']}。",f"review selected actual credit {result['selected_review_exposures']}、incidental actual credit {result['incidental_exposures']}、introduced {result['actual_new_introduced']}。outstanding windows {len(state['review_debt'])}、near deadline {len(near)}、expired {len(state['expired_review_debt'])}。creditは確認済み本文のdistinct textのみです。",f"debt詳細: {json.dumps(state['review_debt'],ensure_ascii=False)}。5〜8 reviewはsoftで、初期候補不足の語数達成のために事件を追加しません。",f"genre: {result['genre_distribution']}。max scene fingerprint similarity {max_similarity:.3f}。sentence lengths {result['sentence_length_distribution']}、preferred 3〜7比率 {result['preferred_sentence_ratio']}。",'',
        '## Integrity / next step','',f"zero-state raw replay errors: {replay_errors}。ledger epoch {state['epoch']}。failed candidatesはintroduction/exposure/debt/genre/sceneへcreditされていません。post suite: {result['post_run_regression']}。",'人間抜き取りレビューは別ファイルを使用してください。モデル自己評価とregexを独立した品質保証とは扱いません。',
        '次の001〜050 production trialへ進める。今回の承認は10本のみであり、続きは生成しない。' if result['verdict']=='A' else '50本へ進む前に、この判定で示した一点/作者promptを調整する。今回のrunを成功扱いへ書き換えない。']
    doc += ['', '## Identity parity / next optimization','', f"Unresolved structural scope mismatches: {result['structural_scope_mismatch_count']}; safely converged scope diagnostics: {result['resolved_scope_mismatch_count']}; body NE recoveries: {result['ne_recovery_count']}. Explicit registry/syntax/probe evidence only; raw preserved.",f"Largest stage: {top_stage}; optimization target: {result['speed_optimization_target']}."]
    (ROOT/'reports/k1_phase3_6a_production_benchmark.md').write_text('\n'.join(doc)+'\n',encoding='utf-8')
    checkpoint=['# Phase 3.6a checkpoint K1-010' if complete else '# Phase 3.6a STOP checkpoint','',f"commit {len(rows)}, status {result['status']}",'',json.dumps(result,ensure_ascii=False,indent=2)]
    (ROOT/'reports/k1_phase3_6a_checkpoint_010.md' if complete else ROOT/'reports/k1_phase3_6a_structural_stop_report.md').write_text('\n'.join(checkpoint),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','committed_count','committed_hard_errors','rejected_attempt_count','semantic_grammar_warnings','production_wall_seconds','per_text_seconds','estimated_300_serial_hours','review_debt','incidental_exposures')},ensure_ascii=False))


if __name__=='__main__':main()
