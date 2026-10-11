"""Range/report adapter only: frozen gate, zero-state replay on finish only."""
from collections import Counter
from datetime import datetime
from pathlib import Path
import json
import math
import statistics
import tempfile
import sys
import re
from k1_phase3 import ROOT,read,write,similarity
from k1_phase3_6b import ProductionGate,PILOT,LEDGER,TIMING,freeze_errors,locked_code

def stats(xs):
    if not xs:return dict(n=0,min=None,max=None,mean=None,median=None,p90=None)
    return dict(n=len(xs),min=min(xs),max=max(xs),mean=statistics.mean(xs),median=statistics.median(xs),p90=sorted(xs)[math.ceil(.9*len(xs))-1])

def collect():
    gate=ProductionGate();s=gate.load();rows=s['committed_records'];timing=read(TIMING)
    control=read(gate.control);attempts=[read(p) for p in sorted((PILOT/'candidates').glob('*.json'))]
    stages=Counter();retry=Counter()
    for t in timing['texts']:
        stages.update(t.get('stages',{}))
        for a in t['attempts']:
            if not a['hard_pass']:retry.update(e['code'] for e in a['hard_errors'])
    sem=Counter(x['decision'] for r in rows for x in r.get('semantic_grammar_warnings',[]))
    nat=Counter(x['rule_id'] for r in rows for x in r['naturalness']['lint_warnings'])
    scenes=[dict(a=a['text_number'],b=b['text_number'],score=similarity(a['scene_fingerprint'],b['scene_fingerprint'])) for i,a in enumerate(rows) for b in rows[max(0,i-10):i]]
    lengths=[len(x.split()) for r in rows for x in r['source']['sentences']]
    confirmed=[dict(text=t['text_number'],**h) for t in timing['texts'] for h in t.get('author_review_history',[]) if h['evidence']['naturalness']=='REPAIR']
    recurrent={}
    patterns={'recipient_smile':r'\S+에게\s+웃', 'habit_progressive':r'(?:매일|자주|보통)[^.?!]*고\s+있'}
    for key,pattern in patterns.items():
        found=[r['text_number'] for r in rows if re.search(pattern,r['text_ko'])]
        if found:recurrent[key]=dict(texts=found,generator_recurrence_warning=len(found)>=3,confirmed_issue=False)
    wall=timing.get('production_end_counter',__import__('time').perf_counter())-timing['production_start_counter']
    done=len(rows)==50 and control['status']=='completed'
    per=stats([t['total_seconds'] for t in timing['texts'] if t.get('committed')])
    errors=freeze_errors()+locked_code()
    for r in rows:
        if read(PILOT/'texts'/f"{r['id']}.json")!=r:errors.append('text_projection_mismatch:'+r['id'])
    result=dict(phase='3.6b',completed=done,committed_count=len(rows),state_epoch=s['epoch'],stop=control.get('stop') or timing.get('stop'),
        hard_errors=sum(len(r['hard_errors']) for r in rows),integrity_errors=errors,total_attempts=len(attempts),
        first_pass_count=sum(r['attempt_number']==1 for r in rows),first_pass_ratio=sum(r['attempt_number']==1 for r in rows)/len(rows) if rows else None,
        mean_attempts=statistics.mean(r['attempt_number'] for r in rows) if rows else None,attempts=[r['attempt_number'] for r in rows],
        retry_error_codes=dict(retry),rejected_attempts=sum(not a['hard_pass'] for a in attempts),
        future_contaminated_candidates=sum(any(x['reason']=='future_expansion' for x in a.get('invalid_usage_ids',[])) for a in attempts),
        future_in_committed=sum(any(x['reason']=='future_expansion' for x in r['invalid_usage_ids']) for r in rows),
        unresolved_in_committed=sum(len(r['unresolved_tokens']) for r in rows),planned_mismatch=sum(r['planned_new_vocab_ids']!=r['actual_new_vocab_ids'] for r in rows),
        structural_scope_mismatches=sum(x['structural_defect'] for a in attempts for x in a.get('scope_identity_checks',[])),
        resolved_scope_mismatches=sum(x['decision']=='RECOVERED_SAFE' for a in attempts for x in a.get('scope_identity_checks',[])),
        failed_state_isolation=all(a['ledger_sha_before_evaluation']==a['ledger_sha_after_evaluation'] for a in attempts if not a['hard_pass']),
        semantic_warning_count=sum(sem.values()),semantic_warning_distribution=dict(sem),naturalness_warning_count=sum(nat.values()),naturalness_categories=dict(nat),
        author_confirmed_draft_issues=confirmed,confirmed_committed_issues=[],recurring_patterns=recurrent,
        selected_review=sum(e['selected_review_exposure_count'] for e in s['entries']),incidental=sum(e['incidental_exposure_count'] for e in s['entries']),
        introduced_count=sum(e['actual_first_text'] is not None for e in s['entries']),exposure_distribution=dict(Counter(e['actual_exposure_count'] for e in s['entries'])),
        outstanding_debt=s['review_debt'],expired_debt=s['expired_review_debt'],near_deadline_debt=[d for d in s['review_debt'] if d['window']['to']-len(rows)<=2],
        mathematically_unrecoverable=[e['vocab_id'] for e in s['entries'] if e['actual_first_text'] is not None and e['actual_exposure_count']+300-len(rows)<6],
        genre_distribution=dict(Counter(r['genre'] for r in rows)),max_scene_similarity=max((x['score'] for x in scenes),default=0),scene_similarities=scenes,
        eojeol=stats([r['eojeol_count'] for r in rows]),sentence_lengths=dict(Counter(lengths)),preferred_sentence_ratio=sum(3<=x<=7 for x in lengths)/len(lengths) if lengths else None,
        production_wall_seconds=wall,per_text_seconds=per,stage_seconds=dict(stages),
        estimated_300_mean_hours=per['mean']*300/3600 if done else None,estimated_300_median_hours=per['median']*300/3600 if done else None,
        baseline=dict(mean=128.30,median=114.90,p90=163.63,first_pass=.30,mean_attempts=1.9),
        largest_stage=max(stages,key=stages.get) if stages else None,
        engineering_setup_seconds=(datetime.fromisoformat(timing['production_start_utc'])-datetime.fromisoformat(timing['engineering_start_utc'])).total_seconds(),
        pre_regression=read(ROOT/'reports/k1_phase3_6b_pre_regression.json'))
    return gate,s,rows,timing,result

def checkpoint():
    gate,s,rows,timing,r=collect();n=len(rows)
    if n not in (10,20,30,40,50):raise ValueError('Checkpoint only at multiples of ten')
    # load() verifies atomic state checksum; projections/history/engine hashes checked above.
    write(ROOT/f'reports/k1_phase3_6b_checkpoint_{n:03d}.json',r)
    (ROOT/f'reports/k1_phase3_6b_checkpoint_{n:03d}.md').write_text(f'# Phase 3.6b checkpoint {n:03d}\n\n'+json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:r[k] for k in ('committed_count','hard_errors','integrity_errors','first_pass_ratio','selected_review','incidental','max_scene_similarity')},ensure_ascii=False))

def finish():
    gate,s,rows,timing,r=collect();replay_errors=[]
    with tempfile.TemporaryDirectory(prefix='k1_phase3_6b_replay_') as d:
        replay=ProductionGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=gate.kiwi);replay.initialize()
        for old in rows:
            p,c=replay.submit(old['source'])
            if not c['hard_pass']:replay_errors.append(dict(text=old['id'],errors=c['hard_errors']));break
            approval=read(PILOT/'author_reviews'/f"{old['id']}-attempt-{old['attempt_number']:02d}.json")
            replay.approve(p,approval['evidence']);new=replay.commit(p)
            for key in ('raw_morphology','annotations','coverage','actual_new_vocab_ids','actual_review_vocab_ids','incidental_previous_vocab_ids'):
                if new[key]!=old[key]:replay_errors.append(dict(text=old['id'],field=key))
        if replay.load()['entries']!=s['entries']:replay_errors.append('entry_state_mismatch')
    r['ledger_replay_errors']=replay_errors
    post=ROOT/'reports/k1_phase3_6b_post_regression.json';r['post_regression']=read(post) if post.exists() else None
    healthy=not(r['integrity_errors'] or replay_errors or r['hard_errors']) and r['pre_regression']['success'] and bool(r['post_regression'] and r['post_regression']['success'])
    verdict='D'
    if r['mathematically_unrecoverable']:verdict='C'
    elif r['completed'] and healthy:
        verdict='E' if r['per_text_seconds']['median']>300 else 'B' if r['confirmed_committed_issues'] or any(x['generator_recurrence_warning'] for x in r['recurring_patterns'].values()) or r['first_pass_ratio']<.50 or r['mean_attempts']>1.6 else 'A'
    labels=dict(A='READY_FOR_K1_300',B='GENERATOR_TUNING',C='SCHEDULER_ADJUSTMENT',D='STRUCTURAL_FAIL',E='PERFORMANCE_FAIL')
    r.update(verdict=verdict,status=labels[verdict],performance='GREEN' if r['completed'] and r['per_text_seconds']['median']<=180 else 'YELLOW' if r['completed'] and r['per_text_seconds']['median']<=300 else 'RED' if r['completed'] else 'INCOMPLETE',speed_optimization_target='generator' if r['largest_stage'] in ('scene_planning','author_draft','retry_repair') else r['largest_stage'])
    timing.update(production_wall_seconds=r['production_wall_seconds'],stage_totals_seconds=r['stage_seconds'],per_text_statistics=r['per_text_seconds'])
    write(TIMING,timing);write(ROOT/'reports/k1_phase3_6b_validation_result.json',r)
    v={e['id']:e for e in gate.f['core_vocab.json']+gate.f['expansion_vocab.json']}
    def names(ids):return ' / '.join(v[i]['lemma'] for i in ids) or '—'
    chosen={x for x in (1,10,20,30,40,50) if x<=len(rows)}
    chosen.update(x['text_number'] for x in sorted(rows,key=lambda x:len(x['naturalness']['lint_warnings']),reverse=True)[:4])
    chosen.update(x['text_number'] for x in sorted(rows,key=lambda x:x['attempt_number'],reverse=True)[:4])
    human=['# Phase 3.6b human spot review','', 'Author review is not independent gold. Semantic warnings are diagnostics, not error verdicts.','']
    for x in rows:
        if x['text_number'] not in chosen:continue
        human += [f"## {x['id']} — {x['title_ko']}",'',f"{x['eojeol_count']} eojeol; new: {names(x['actual_new_vocab_ids'])}; review: {names(x['actual_review_vocab_ids'])}; attempts: {x['attempt_number']}",f"Naturalness warnings: {json.dumps(x['naturalness']['lint_warnings'],ensure_ascii=False)}; semantic warnings: {len(x['semantic_grammar_warnings'])}",'',x['text_ko'],'',x['translation_ja'],'']
    (ROOT/'reports/k1_phase3_6b_human_spot_review.md').write_text('\n'.join(human)+'\n',encoding='utf-8')
    doc=['# Phase 3.6b Production Trial','',f"Verdict **{verdict}: {labels[verdict]}**. Committed {len(rows)}/50. No text beyond K1-050 was generated.",'',
      'Frozen Phase 3.6a gate, analyzer, resolver, scheduler and policy are reused unchanged. Only the author overlay changes guidance. The new runner changes output paths, runtime max_text to 50 and timing/checkpoint reporting. Semantic role REVIEW/heuristic FAIL remain warnings.', '',
      'Timing measures the live local LLM author and file callback, including reasoning and tool transport. It is not a prerecorded replay or isolated external API latency. Setup, pre-tests, post-tests and report/replay time are outside production wall time. Projections and atomic ledger are checked; final zero-state raw replay is separate.', '',
      f"Stop: {r['stop']}. First-pass {r['first_pass_count']}/{len(rows)}; mean attempts {r['mean_attempts']}; total attempts {r['total_attempts']}.",
      f"Production wall {r['production_wall_seconds']:.2f}s. Per-text statistics: {r['per_text_seconds']}. Stages: {r['stage_seconds']}.",
      f"300 serial estimates: mean {r['estimated_300_mean_hours']}h, median {r['estimated_300_median_hours']}h. Estimates are produced only on completion and do not include final human review or later vocabulary burden.",
      f"Baseline: {r['baseline']}. Optimization target: {r['speed_optimization_target']}.", '',
      f"Selected review {r['selected_review']}; incidental {r['incidental']}; introduced {r['introduced_count']}; outstanding debt {len(r['outstanding_debt'])}; expired {len(r['expired_debt'])}; unrecoverable {len(r['mathematically_unrecoverable'])}.",
      f"Exposure distribution: {r['exposure_distribution']}. Genre distribution: {r['genre_distribution']}. Max recent-ten fingerprint similarity {r['max_scene_similarity']}.",
      f"Semantic warnings {r['semantic_warning_count']}; naturalness warnings {r['naturalness_warning_count']}; author-confirmed draft problems {len(r['author_confirmed_draft_issues'])}; committed problems {len(r['confirmed_committed_issues'])}. Self review is not independent gold.",
      f"Recurring patterns (heuristic, not hard errors): {r['recurring_patterns']}.", '', '## Per-text results','', '| ID | attempts | eojeol | N/U | previous | selected/incidental | seconds |','|---|---:|---:|---|---:|---|---:|']
    for x,t in zip(rows,[t for t in timing['texts'] if t.get('committed')]):
        c=x['coverage'];doc.append(f"| {x['id']} | {x['attempt_number']} | {x['eojeol_count']} | {c['denominator_N']}/{c['new_tokens_U']} | {c['previous_vocab_coverage']:.2%} | {len(x['actual_review_vocab_ids'])}/{len(x['incidental_previous_vocab_ids'])} | {t['total_seconds']:.2f} |")
    doc+=['','## Full diagnostics','', '```json',json.dumps(r,ensure_ascii=False,indent=2),'```']
    (ROOT/'reports/k1_phase3_6b_production_001_050_report.md').write_text('\n'.join(doc)+'\n',encoding='utf-8')
    if not r['completed']:(ROOT/'reports/k1_phase3_6b_structural_stop_report.md').write_text('# STOP\n\n'+json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:r[k] for k in ('status','committed_count','total_attempts','first_pass_ratio','mean_attempts','hard_errors','production_wall_seconds','per_text_seconds','stop')},ensure_ascii=False))

if __name__=='__main__':globals()[sys.argv[1]]()
