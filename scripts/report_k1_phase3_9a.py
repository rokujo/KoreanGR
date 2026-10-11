"""Report actual credits and window debt; no policy or corpus mutation."""
import json,sys,statistics,math,tempfile
from collections import Counter
from pathlib import Path
from k1_phase3 import ROOT,read,write,similarity
from k1_phase3_9a import ProductionGate,PILOT,TIMING,freeze_errors,locked_code
from k1_phase3_9a_planner import health,author_findings
from k1_phase3_8_sense import sense_checks
def stats(xs):
    return dict(n=len(xs),mean=statistics.mean(xs) if xs else None,median=statistics.median(xs) if xs else None,
        p90=sorted(xs)[math.ceil(.9*len(xs))-1] if xs else None,min=min(xs) if xs else None,max=max(xs) if xs else None)
def collect():
    g=ProductionGate();s=g.load();rows=s['committed_records'];timing=read(TIMING);n=len(rows)
    attempts=[read(p) for p in sorted((PILOT/'candidates').glob('*.json'))]
    elapsed=timing.get('production_end_counter',__import__('time').perf_counter())-timing['production_start_counter']
    stage=Counter()
    for t in timing['texts']:stage.update(t['stages'])
    expired=set();recovered=set();new_expired=set()
    for e in s['entries']:
        ws=next(w['review_windows'] for w in g.f['vocab_review_windows.json']['entries'] if w['vocab_id']==e['vocab_id'])
        for i,w in enumerate(ws):
            paid=e['paid_review_windows'].get(str(i))
            if paid is not None and paid>w['to']:recovered.add((e['vocab_id'],i))
            if (e['actual_first_text'] is not None and w['to']<n and (paid is None or paid>w['to'])):new_expired.add((e['vocab_id'],i))
            if w['to']<n and paid is None and e['actual_first_text'] is not None:expired.add((e['vocab_id'],i))
    checks=[dict(text=r['text_number'],finding=x) for r in rows for x in sense_checks(r['text_ko'],r) if x['decision']=='FAIL']
    integrity=freeze_errors()+locked_code()
    for r in rows:
        if read(PILOT/'texts'/f"{r['id']}.json")!=r:integrity.append('projection:'+r['id'])
    scene=[dict(a=r['text_number'],b=o['text_number'],score=similarity(r['scene_fingerprint'],o['scene_fingerprint'])) for i,r in enumerate(rows) for o in rows[max(0,i-10):i]]
    committed_issues=[dict(text=r['text_number'],finding=x) for r in rows for x in author_findings(r['text_ko'],r['source'].get('pack_intended',False))]
    lens=[len(p.split()) for r in rows for p in r['source']['sentences']]
    h=health(s,n)
    r=dict(phase='3.9a',committed_count=n,completed=n==100 and read(g.control)['status']=='completed',stop=read(g.control).get('stop') or timing.get('stop'),
        total_attempts=len(attempts),formal_first_pass_count=sum(x['attempt_number']==1 for x in rows),
        formal_first_pass_ratio=sum(x['attempt_number']==1 for x in rows)/n if n else None,
        mean_attempts=statistics.mean(x['attempt_number'] for x in rows) if rows else None,
        initial_draft_with_finding=sum(bool(t.get('lexical_preflight',{}).get('findings')) for t in timing['texts']),
        initial_draft_with_future=sum(t.get('lexical_preflight',{}).get('future_count',0)>0 for t in timing['texts']),
        initial_finding_ratio=sum(bool(t.get('lexical_preflight',{}).get('findings')) for t in timing['texts'])/sum('lexical_preflight' in t for t in timing['texts']) if any('lexical_preflight' in t for t in timing['texts']) else None,
        initial_future_ratio=sum(t.get('lexical_preflight',{}).get('future_count',0)>0 for t in timing['texts'])/sum('lexical_preflight' in t for t in timing['texts']) if any('lexical_preflight' in t for t in timing['texts']) else None,
        preflight_completed_count=sum('lexical_preflight' in t for t in timing['texts']),
        author_contract_retry_count=sum(t.get('author_contract_retry_count',0) for t in timing['texts']),
        contract_failures_recovered=sum(t.get('author_contract_retry_count',0) for t in timing['texts'] if t.get('author_contract_accepted')),
        contract_max_exhaustion=(read(g.control).get('stop') or {}).get('type')=='AUTHOR_CONTRACT_STRUCTURAL_FAIL',
        formal_future_findings=[dict(text=a['text_number'],attempt=a['attempt_number'],**x) for a in attempts for x in a.get('invalid_usage_ids',[]) if x['reason']=='future_expansion'],
        retry_error_codes=dict(Counter(e['code'] for a in attempts if not a['hard_pass'] for e in a['hard_errors'])),
        hard_errors=sum(len(x['hard_errors']) for x in rows),committed_future=sum(x['reason']=='future_expansion' for a in rows for x in a['invalid_usage_ids']),
        committed_unresolved=sum(len(a['unresolved_tokens']) for a in rows),planned_mismatch=sum(a['planned_new_vocab_ids']!=a['actual_new_vocab_ids'] for a in rows),
        final_canonical_mismatch=sum(not a.get('final_reanalysis_pass',False) for a in rows),integrity_errors=integrity,
        restricted_false_accepts=checks,failed_state_isolation=all(a['ledger_sha_before_evaluation']==a['ledger_sha_after_evaluation'] for a in attempts),
        semantic_warning_count=sum(len(a['semantic_grammar_warnings']) for a in rows),
        naturalness_warning_categories=dict(Counter(x['rule_id'] for a in rows for x in a['naturalness']['lint_warnings'])),
        confirmed_committed_issues=committed_issues,author_repair_count=sum(any(h['evidence'][k]=='REPAIR' for k in ('naturalness','translation_fidelity','review_word_integration')) for t in timing['texts'] for h in t.get('author_review_history',[])),
        known_gap_occurrences=[dict(text=a['text_number'],**x) for a in rows for x in a['naturalness']['natural_expression_gaps']],
        selected_review=sum(e['selected_review_exposure_count'] for e in s['entries']),incidental=sum(e['incidental_exposure_count'] for e in s['entries']),
        introduced_count=sum(e['actual_first_text'] is not None for e in s['entries']),
        effective_review_credits=sum(len(set(a['actual_new_vocab_ids']+a['actual_review_vocab_ids']+a['incidental_previous_vocab_ids'])) for a in rows),
        effective_credit_distribution=stats([len(set(a['actual_new_vocab_ids']+a['actual_review_vocab_ids']+a['incidental_previous_vocab_ids'])) for a in rows]),
        exposure_distribution=dict(Counter(e['actual_exposure_count'] for e in s['entries'])),outstanding_debt=s['review_debt'],expired_debt=s['expired_review_debt'],
        recovered_expired_count=len(recovered),ever_expired_count=len(new_expired),recovered_expired_windows=sorted(recovered),
        near_deadline_debt=[x for x in s['review_debt'] if 0<=x['window']['to']-n<=3],
        genre_distribution=dict(Counter(a['genre'] for a in rows)),max_scene_similarity=max((x['score'] for x in scene),default=0),
        eojeol=stats([a['eojeol_count'] for a in rows]),sentence_length_distribution=dict(Counter(lens)),
        production_wall_seconds=elapsed,per_text_seconds=stats([t['total_seconds'] for t in timing['texts'] if t.get('committed')]),stage_seconds=dict(stage),
        preflight_repair_fraction=stage['preflight_repair']/elapsed,formal_retry_fraction=stage['retry_repair']/elapsed,
        largest_stage=max(stage,key=stage.get) if stage else None,**h)
    return g,s,rows,timing,r
def checkpoint():
    g,s,rows,timing,r=collect();n=len(rows)
    if n not in (25,50,75,100):raise ValueError('025/050/075/100 only')
    past=[read(ROOT/f'reports/k1_phase3_9a_checkpoint_{j:03d}.json') for j in (25,50,75,100) if j<n and (ROOT/f'reports/k1_phase3_9a_checkpoint_{j:03d}.json').exists()]
    old=past[-1] if past else None
    delta=r['required_future_credit_rate']-old['required_future_credit_rate'] if old else None
    r.update(trajectory='initial' if delta is None else 'rising' if delta>1e-9 else 'falling' if delta<-1e-9 else 'flat',
        newly_expired_since_checkpoint=r['ever_expired_count']-(old['ever_expired_count'] if old else 0),
        recovered_expired_since_checkpoint=r['recovered_expired_count']-(old['recovered_expired_count'] if old else 0))
    r['scheduler_risk']=r['trajectory']=='rising' or r['newly_expired_since_checkpoint']>r['recovered_expired_since_checkpoint']
    write(ROOT/f'reports/k1_phase3_9a_checkpoint_{n:03d}.json',r)
    (ROOT/f'reports/k1_phase3_9a_checkpoint_{n:03d}.md').write_text('# Phase 3.9a checkpoint\n\n'+json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:r[k] for k in ('committed_count','hard_errors','formal_first_pass_ratio','initial_finding_ratio','initial_future_ratio','capped_exposure_progress','required_future_credit_rate','trajectory','scheduler_risk')},ensure_ascii=False))
def finish():
    g,s,rows,timing,r=collect();errors=[]
    # Exactly the frozen atomic commit and canonical reanalysis, new zero-state.
    with tempfile.TemporaryDirectory(prefix='k1_phase3_9a_replay_') as d:
        replay=ProductionGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=g.kiwi);replay.initialize()
        for old in rows:
            p,c=replay.submit(old['source'])
            if not c['hard_pass']:errors.append(dict(text=old['text_number'],errors=c['hard_errors']));break
            ev=read(PILOT/'author_reviews'/f"{old['id']}-attempt-{old['attempt_number']:02d}.json")['evidence']
            replay.approve(p,ev);new=replay.commit(p)
            for k in ('canonical_lexical_map','annotations','coverage','actual_new_vocab_ids','actual_review_vocab_ids','incidental_previous_vocab_ids'):
                if new[k]!=old[k]:errors.append(dict(text=old['text_number'],field=k))
            print('replay',old['text_number'],flush=True)
        if replay.load()['entries']!=s['entries']:errors.append('ledger_entries_mismatch')
    r['ledger_replay_errors']=errors
    r['pre_regression']=read(ROOT/'reports/k1_phase3_9a_pre_regression.json')
    r['post_regression']=read(ROOT/'reports/k1_phase3_9a_post_regression.json')
    r['performance']='GREEN' if r['completed'] and r['per_text_seconds']['median']<=180 else 'YELLOW' if r['completed'] and r['per_text_seconds']['median']<=300 else 'RED' if r['completed'] else 'INCOMPLETE'
    cps=[read(ROOT/f'reports/k1_phase3_9a_checkpoint_{n:03d}.json') for n in (25,50,75,100) if (ROOT/f'reports/k1_phase3_9a_checkpoint_{n:03d}.json').exists()]
    r['checkpoint_trajectory']=[dict(text=c['committed_count'],rate=c['required_future_credit_rate'],trajectory=c['trajectory']) for c in cps]
    healthy=not(r['hard_errors'] or r['integrity_errors'] or errors or r['restricted_false_accepts']) and r['pre_regression']['success'] and r['post_regression']['success']
    verdict='D'
    if r['completed'] and healthy:
        verdict='E' if r['performance']=='RED' else 'C' if r['required_future_credit_rate']>11 or any(c['trajectory']=='rising' for c in cps[1:]) else 'B' if r['confirmed_committed_issues'] or r['initial_future_ratio']>.3 or r['initial_finding_ratio']>.5 else 'A'
    labels=dict(A='READY_FOR_K1_300_CONTINUATION',B='GENERATOR_TUNING',C='SCHEDULER_TUNING',D='STRUCTURAL_FAIL',E='PERFORMANCE_FAIL')
    r.update(verdict=verdict,status=labels[verdict],estimated_300_mean_hours=r['per_text_seconds']['mean']*300/3600 if r['completed'] else None,estimated_300_median_hours=r['per_text_seconds']['median']*300/3600 if r['completed'] else None,
        corpus_candidate_reusable=verdict=='A',continuation_requires_user_confirmation=True)
    write(ROOT/'reports/k1_phase3_9a_validation_result.json',r)
    timing.update(production_wall_seconds=r['production_wall_seconds'],stage_totals_seconds=r['stage_seconds'],per_text_statistics=r['per_text_seconds'])
    write(TIMING,timing)
    fixed={n for n in (1,10,25,50,75,100) if n<=len(rows)};chosen=set(fixed)
    for key in (lambda x:x['attempt_number'],lambda x:len(x['naturalness']['lint_warnings']),lambda x:len(x['actual_review_vocab_ids']),lambda x:len(x['naturalness']['natural_expression_gaps'])):
        for x in sorted(rows,key=key,reverse=True)[:5]:
            if len(chosen)<20:chosen.add(x['text_number'])
    v={e['id']:e for e in g.f['core_vocab.json']+g.f['expansion_vocab.json']}
    human=['# Phase 3.9a human spot review','', 'Author assessment is not independent gold. Fingerprint scores do not establish semantic diversity.','']
    for x in rows:
        if x['text_number'] in chosen:
            human += [f"## {x['id']} — {x['title_ko']}",'',f"{x['eojeol_count']} eojeol; attempts {x['attempt_number']}; new: {' / '.join(v[i]['lemma'] for i in x['actual_new_vocab_ids'])}; review: {' / '.join(v[i]['lemma'] for i in x['actual_review_vocab_ids'])}",f"Warnings {len(x['naturalness']['lint_warnings'])}; semantic diagnostics {len(x['semantic_grammar_warnings'])}",'',x['text_ko'],'',x['translation_ja'],'']
    (ROOT/'reports/k1_phase3_9a_human_spot_review.md').write_text('\n'.join(human)+'\n',encoding='utf8')
    doc=['# Phase 3.9a endurance trial','',f"**{verdict} / {labels[verdict]}** — {len(rows)}/100 committed. No K1-101 or later generated.",'',
      'Mechanical evaluate and atomic commit are byte-identical to Phase 3.8. The new envelope changes only run range/paths/provenance. Prompt and scene presentation were frozen before production. Existing credit/payment rules remain authoritative. Semantic warnings never block production.','',
      'Effective credit includes introductions plus selected and incidental distinct Expansion appearances; previous-only credits are separately recorded per text. Capped progress counts each vocabulary ID at most six times. Repetition beyond six never reduces remaining required credits.','',
      'Timing is live local author/callback wall time, not isolated external API latency. Engineering, pre/post regression, reporting and replay are excluded. Author self-checks are not independent gold. Early review hints can be vetoed; no selection is credited without canonical body occurrence.','',
      f"First pass {r['formal_first_pass_ratio']}; mean attempts {r['mean_attempts']}; contract-only retries {r['author_contract_retry_count']} (recovered {r['contract_failures_recovered']}); initial findings {r['initial_finding_ratio']}; initial future {r['initial_future_ratio']}.",
      f"Capped progress {r['capped_exposure_progress']}/3000; future required rate {r['required_future_credit_rate']}; outstanding {len(r['outstanding_debt'])}; expired {len(r['expired_debt'])}; recovered expired {r['recovered_expired_count']}.",
      f"Timing {r['per_text_seconds']}; wall {r['production_wall_seconds']}; stages {r['stage_seconds']}; performance {r['performance']}.",
      f"300-text serial hours: mean {r['estimated_300_mean_hours']}, median {r['estimated_300_median_hours']}. Later vocabulary load and human quality review are excluded.",
      'No automatic continuation: user confirmation is required before K1-101..300.','', '## Full metrics','', '```json',json.dumps(r,ensure_ascii=False,indent=2),'```']
    (ROOT/'reports/k1_phase3_9a_production_001_100_report.md').write_text('\n'.join(doc)+'\n',encoding='utf8')
    if not r['completed']:(ROOT/'reports/k1_phase3_9a_structural_stop_report.md').write_text('# STOP\n\n'+json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:r[k] for k in ('status','committed_count','total_attempts','formal_first_pass_ratio','required_future_credit_rate','production_wall_seconds')},ensure_ascii=False))
if __name__=='__main__':globals()[sys.argv[1]]()
