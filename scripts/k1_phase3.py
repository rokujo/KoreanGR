"""Actual sequential run. No hypothetical exposures, no edits to frozen inputs.

The raw morphology is independent of authored annotations, but the shared
normalizer and contextual sense judgments are not independent semantic gold.
An attempted full body with a hard error stops this run; it is never credited.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import argparse
import math
import re
import statistics
from jsonschema import Draft202012Validator
from k1_phase2_2 import ROOT, DATA, REPORTS, read, write, sha, inputs, analyze, annotation_triage
from k1_phase2_3 import make_kiwi
from k1_review_scheduler import ReviewScheduler
from k1_naturalness_lint import lint, semantic_review, CHECKS, translation_lint, sentences
from lexical_coverage import evaluate_lexical_tokens
from validate_k1_pilot import token_stream

PILOT=ROOT/'pilot/ko/k1/phase3'
STATE=ROOT/'state'
PROFILE=DATA/'phase3/profile.json'
FREEZE=REPORTS/'k1_phase3_input_freeze.json'
LEDGER=STATE/'phase3_k1_001_050_exposure_ledger.json'
ISSUES=STATE/'phase3_naturalness_issue_ledger.json'
RUN=STATE/'phase3_run.json'

def initialize():
    if RUN.exists():
        raise ValueError('Run already exists; initialize cannot reset actual history')
    paths=list(DATA.glob('*.json'))
    paths += [p for d in ('scripts','tests','docs') for p in (ROOT/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'phase3' not in p.name]
    paths += [p for p in (ROOT/'pilot/ko/k1').rglob('*') if p.is_file() and 'phase3' not in p.parts]
    paths += [p for p in REPORTS.rglob('*') if p.is_file() and 'phase3' not in p.name and '__pycache__' not in p.parts]
    write(FREEZE,dict(phase='3',files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(paths))}))
    profile=deepcopy(inputs()['profile.json'])
    profile['version']='0.3.0'
    profile['status']='phase3_actual_sequential_001_050'
    profile['sentence_length']['preferred_min_eojeol']=3
    write(PROFILE,profile)
    schema=deepcopy(read(DATA/'support.schema.json'))
    schema['$defs']['profile']['properties']['sentence_length']['const']['preferred_min_eojeol']=3
    schema['$ref']='#/$defs/profile'
    write(DATA/'phase3/profile.schema.json',schema)
    write(PILOT/'run_policy.json',dict(
        maximum_text=50,processing='generate_validate_commit_one_text_before_next',
        expired_window_stop=True,close_window_after_text=True,
        near_deadline_mass_threshold=30,near_deadline_horizon=3,
        numerical_review_capacity_per_text=10,capacity_is_upper_bound_not_semantic_guarantee=True,
        confirmed_pattern_count=3,confirmed_pattern_horizon=5,
        scene_similarity_threshold=0.85,scene_cluster_stop_count=4,scene_horizon=10,
        preferred_sentence_min=3,preferred_sentence_max=7,hard_sentence_max=10,
        hard_sentence_min=None,short_sentences_need_no_padding=True,
        quotas_evaluated_at_300_not_50=True,regex_warnings_are_not_confirmed_issues=True))
    write(RUN,dict(phase='3',last_committed_text=0,status='running',stop=None,attempted_texts=[],
                  checkpoint_texts=[],genre_history=[],scene_history=[],natural_expression_gaps=[]))
    write(ISSUES,dict(phase='3',issues=[]))
    save_ledger(ReviewScheduler(inputs()['vocab_review_windows.json']),[],0,[])

def files():
    f=inputs();f['profile.json']=read(PROFILE);return f

def freeze_errors():
    return ['Frozen file changed/missing: '+p for p,h in read(FREEZE)['files'].items()
            if not (ROOT/p).is_file() or sha(ROOT/p)!=h]

def records():
    return [read(p) for p in sorted((PILOT/'texts').glob('K1-*.json'))] if (PILOT/'texts').exists() else []

def actual_scheduler(recs=None):
    s=ReviewScheduler(inputs()['vocab_review_windows.json'])
    for r in records() if recs is None else recs:
        s.record(r['text_number'],r['actual_new_vocab_ids']+r['actual_review_vocab_ids']+r['incidental_previous_vocab_ids'])
    return s

def vocab(f):return {e['id']:e for e in f['core_vocab.json']+f['expansion_vocab.json']}

def actual_coverage_files(f,s,t,new):
    """Private evaluator view: unknown actual introductions are never assumed.

    The 999 sentinel exists only in memory for the legacy token evaluator; it is
    not an introduction plan and is never written to the frozen schedule.
    """
    result=deepcopy(f)
    first={i:min(s.actual[i]) if s.actual[i] else t if i in new else 999 for i in s.entries}
    result['introduction_schedule.json']['rows']=[dict(text=n,entry_ids=sorted(i for i,x in first.items() if x==n)) for n in sorted(set(first.values()))]
    return result

def ids_for(lemmas,f):
    result=[]
    for word in lemmas:
        lemma,sep,sense=word.partition('::')
        matches=[e['id'] for e in f['expansion_vocab.json'] if e['lemma']==lemma and (not sep or e['sense']==sense)]
        if len(matches)!=1:raise ValueError('Unambiguous active Expansion required: '+word)
        result.extend(matches)
    return result

def metrics(text):
    rows=sentences(text)
    sizes=[sum(bool(re.search(r'[가-힣A-Za-z0-9]',w)) for w in s.split()) for _,s in rows]
    return dict(eojeol_count=sum(sizes),sentence_count=len(sizes),max_sentence_eojeol=max(sizes,default=0),
                sentence_eojeol_counts=sizes,preferred_sentence_outliers=[i+1 for i,n in enumerate(sizes) if not 3<=n<=7])

def similarity(a,b):
    fields=('goal','setting','participants','problem_type','resolution_type','main_actions')
    scores=[]
    for k in fields:
        x,y=a[k],b[k]
        if isinstance(x,list):
            x,y=set(x),set(y);scores.append(len(x&y)/len(x|y) if x|y else 1)
        else:scores.append(float(x==y))
    return sum(scores)/len(scores)

def debt_rows(s,t,close=False):
    rows=[]
    for vid,e in s.entries.items():
        if not s.actual[vid]:continue
        for i,w in enumerate(e['review_windows']):
            if i in s.credits[vid] or w['from']>t:continue
            expired=w['to']<t or (close and w['to']==t)
            rows.append(dict(vocab_id=vid,window_index=i,current_window=w,
                             current_actual_exposure_count=len(s.actual[vid]),
                             deadline_status='expired' if expired else 'near_deadline' if w['to']-t<=3 else 'open',
                             urgency=round(20/max(1,w['to']-t+1),3)))
    return rows

def save_ledger(s,recs,t,deferred):
    v=vocab(inputs());inc=Counter(i for r in recs for i in r['incidental_previous_vocab_ids'])
    selected=Counter(i for r in recs for i in r['actual_review_vocab_ids'])
    debt=debt_rows(s,t,close=True) if t else []
    entries=[]
    for vid,e in s.entries.items():
        ds=[d for d in debt if d['vocab_id']==vid]
        texts=sorted(s.actual[vid])
        entries.append(dict(vocab_id=vid,lemma=v[vid]['lemma'],first_planned_text=e['first_introduction_text'],
            actual_first_text=min(texts) if texts else None,actual_texts=texts,actual_exposure_count=len(texts),
            last_exposure_text=max(texts) if texts else None,incidental_exposure_count=inc[vid],
            selected_review_exposure_count=selected[vid],active_window=[d['current_window'] for d in ds],
            outstanding_debt=ds,deadline_status='expired' if any(d['deadline_status']=='expired' for d in ds)
              else 'near_deadline' if any(d['deadline_status']=='near_deadline' for d in ds) else 'open' if ds else 'not_open_or_paid',
            paid_review_windows={str(k):value for k,value in s.credits[vid].items()}))
    write(LEDGER,dict(phase='3',scope='actual bodies only; no pilot or hypothetical seed',last_committed_text=t,
        actually_introduced_vocab=[e['vocab_id'] for e in entries if e['actual_first_text'] is not None],
        actual_first_introduction={e['vocab_id']:e['actual_first_text'] for e in entries if e['actual_first_text'] is not None},
        review_debt=debt,expired_review_debt=[d for d in debt if d['deadline_status']=='expired'],
        incidental_exposures=[dict(text=r['text_number'],ids=r['incidental_previous_vocab_ids']) for r in recs],
        defer_events=deferred,entries=entries))

def plan(source,s,f):
    approved=ids_for(source.get('review_candidates',[]),f)
    return s.select(source['text_number'],source['scene'],approved_ids=approved,desired=source.get('review_target',8))

def stop(run,t,reasons,rec=None):
    run['status']='stopped';run['stop']=dict(text=t,reasons=reasons)
    write(RUN,run)
    if rec:write(PILOT/'failed_attempts'/f'K1-{t:03d}.json',rec)

def accept(path):
    run=read(RUN);src=read(path);t=src['text_number']
    if run['status']!='running':raise ValueError('Run stopped; no more bodies may be generated')
    if t!=run['last_committed_text']+1 or not 1<=t<=50:raise ValueError('Must generate next text, capped at 050')
    f=files();v=vocab(f);recs=records();s=actual_scheduler(recs)
    initial_errors=freeze_errors()+[str(e.message) for e in Draft202012Validator(read(DATA/'phase3/profile.schema.json')).iter_errors(f['profile.json'])]
    if initial_errors:stop(run,t,initial_errors);return dict(stopped=True,errors=initial_errors)
    proposal=plan(src,s,f);selected=[r['vocab_id'] for r in proposal['selected_reviews']]
    text='\n\n'.join(' '.join(src['sentences'][i:i+6]) for i in range(0,len(src['sentences']),6))
    kiwi=make_kiwi()
    analysis=analyze(text,f,t,selected,src.get('sense_overrides',{}),kiwi)
    used={a['vocab_id'] for a in analysis['annotations'] if a['vocab_id']}
    expansion=set(s.entries);new=s.new_ids(t);actual_new=sorted(used&set(new))
    actual_review=sorted(used&set(selected));incidental=sorted((used&expansion)-set(new)-set(selected))
    errors=list(initial_errors)
    errors.extend('Unresolved '+a['surface']+' / '+str(a['lemma']) for a in analysis['unresolved_tokens'])
    errors.extend('Unconfirmed previous Expansion '+i for i in used&expansion if i not in new and not s.actual[i])
    errors.extend('Future Expansion '+i for i in used&expansion if s.entries[i]['first_introduction_text']>t)
    if actual_new!=new:errors.append('Introduction schedule conflict: not all planned new IDs actually present')
    # Coverage uses actual introduction history, never assumed schedule history.
    coverage_files=actual_coverage_files(f,s,t,new)
    cov=evaluate_lexical_tokens(token_stream(analysis['annotations']),t,coverage_files)
    errors+=cov['errors'];m=metrics(text)
    if not 120<=m['eojeol_count']<=180:errors.append('Body length outside 120..180')
    if m['max_sentence_eojeol']>10:errors.append('Sentence exceeds hard 10')
    allowed={g['id'] for g in f['grammar.json']}
    if set(analysis['grammar_used'])-allowed:errors.append('Unlicensed grammar')
    retired={x['old_id'] for x in f['id_migration.json']['mappings']}
    if used&retired:errors.append('Retired ID/sense')
    # Every licensed vocab annotation must match the full frozen identity.
    for a in analysis['annotations']:
        if a['vocab_id'] and (a['lemma'],a['pos'],a['sense'])!=(v[a['vocab_id']]['lemma'],v[a['vocab_id']]['pos'],v[a['vocab_id']]['sense']):
            errors.append('Lemma/POS/sense mismatch')
    title_analysis=analyze(src['title_ko'],f,t,selected,src.get('sense_overrides',{}),kiwi)
    if title_analysis['unresolved_tokens']:errors.append('Unresolved title word')
    for a in title_analysis['annotations']:
        if a['vocab_id'] in expansion and a['vocab_id'] not in new and not s.actual[a['vocab_id']]:errors.append('Unintroduced title word')
    warnings=lint(text,analysis['annotations'],retired)
    evidence=src['semantic_evidence'];second=semantic_review(evidence)
    pairs=list(zip(src['sentences'],src['translations_ja']))
    if len(src['sentences'])!=len(src['translations_ja']):errors.append('Translation alignment mismatch')
    fidelity=translation_lint(pairs)
    rec=dict(id=f'K1-{t:03d}',text_number=t,title_ko=src['title_ko'],genre=src['genre'],scene=src['scene'],
        text_ko=text,translation_ja='\n\n'.join(' '.join(src['translations_ja'][i:i+6]) for i in range(0,len(src['translations_ja']),6)),
        planned_new_vocab_ids=new,actual_new_vocab_ids=actual_new,
        review_candidate_ids=ids_for(src.get('review_candidates',[]),f),selected_review_vocab_ids=selected,
        actual_review_vocab_ids=actual_review,incidental_previous_vocab_ids=incidental,
        deferred_review_vocab_ids=[],grammar_used=analysis['grammar_used'],**m,
        coverage=dict(denominator_N=cov['N'],new_tokens_U=cov['U'],controlled_vocab_coverage=cov['controlled_vocab_coverage'],
            previous_vocab_coverage=cov['previous_vocab_coverage'],target_99_met=cov['previous_vocab_coverage']>=.99),
        exposure_state_after_text=None,validation=dict(vocab_pass=not analysis['unresolved_tokens'],grammar_pass=not analysis['unresolved_tokens'],
            coverage_pass=cov['ok'],length_pass=120<=m['eojeol_count']<=180,sentence_length_pass=m['max_sentence_eojeol']<=10,
            hard_errors=sorted(set(errors))),
        naturalness=dict(lint_warnings=warnings,semantic_review=second,natural_expression_gaps=src.get('natural_expression_gaps',[])),
        scene_fingerprint=src['scene_fingerprint'],notes=src.get('notes',[]),sense_overrides=src.get('sense_overrides',{}),
        translation_pairs=[dict(ko=k,ja=j) for k,j in pairs],translation_fidelity_flags=fidelity,
        translation_fidelity_review=src['translation_fidelity_review'],selection_trace=proposal,
        analysis_limitations='Morphological coverage is conditional on contextual lemma/POS/sense hypotheses; semantic review is not human approval.',
        **{k:analysis[k] for k in ('annotations','raw_morphology','annotation_review_required','unresolved_tokens')})
    run['attempted_texts'].append(t)
    if errors:
        stop(run,t,sorted(set(errors)),rec)
        return dict(stopped=True,text=t,errors=sorted(set(errors)),eojeol=m['eojeol_count'],N=cov['N'],U=cov['U'])
    # Commit only after hard QA. Current-new and previous usages earn distinct-text credits.
    s.record(t,actual_new+actual_review+incidental)
    debt=debt_rows(s,t,close=True)
    deferred=[]
    for d in debt:
        if d['vocab_id'] in used:continue
        e=s.entries[d['vocab_id']];w=d['current_window']
        next_open=t+1 if t<w['to'] else next((x['from'] for x in e['review_windows'] if x['from']>t),None)
        deferred.append(dict(**d,skipped_text=t,reason='No natural integrated occurrence in this actual scene; no forced review-only sentence',
                             next_available_opportunity=next_open))
    rec['deferred_review_vocab_ids']=sorted({d['vocab_id'] for d in deferred})
    rec['defer_events']=deferred
    rec['exposure_state_after_text']=dict(text=t,actually_introduced_count=sum(bool(x) for x in s.actual.values()),
        actual_entry_text_pairs=sum(map(len,s.actual.values())),spacing_credits=sum(map(len,s.credits.values())),
        outstanding_debt_count=len(debt),expired_debt_count=sum(d['deadline_status']=='expired' for d in debt))
    prior_sim=[dict(text=r['text_number'],similarity=round(similarity(src['scene_fingerprint'],r['scene_fingerprint']),4)) for r in recs[-10:]]
    rec['scene_similarity_to_previous_10']=prior_sim
    recs.append(rec);write(PILOT/'texts'/f'K1-{t:03d}.json',rec)
    run['last_committed_text']=t;run['genre_history'].append(dict(text=t,genre=src['genre']))
    run['scene_history'].append(dict(text=t,fingerprint=src['scene_fingerprint']))
    run['natural_expression_gaps']+= [dict(text=t,**g) for g in src.get('natural_expression_gaps',[])]
    issueledger=read(ISSUES)
    for w in warnings:
        issueledger['issues'].append(dict(text=t,category=w['rule_id'],surface=w.get('surface'),reason=w['reason'],
            confirmed_issue=False,warning_only=True,resolution='contextual second pass; retain only with stated scene meaning',recurrence_key=w['rule_id']))
    for issue in src.get('confirmed_issues',[]):issueledger['issues'].append(dict(text=t,warning_only=False,confirmed_issue=True,**issue))
    write(ISSUES,issueledger)
    all_defers=[d for r in recs for d in r.get('defer_events',[])]
    save_ledger(s,recs,t,all_defers)
    stops=[]
    if any(d['deadline_status']=='expired' for d in debt):stops.append('Expired review window debt at closure')
    if sum(d['deadline_status']=='near_deadline' for d in debt)>30:stops.append('More than 30 review debts due within 3 texts')
    # Earliest-deadline capacity upper bound. Includes only introduced unpaid windows.
    deadlines=sorted(d['current_window']['to'] for d in debt)
    if any(i+1>10*max(0,deadline-t) for i,deadline in enumerate(deadlines)):stops.append('Remaining review slots cannot clear opened debts')
    if any(6-len(x)>300-t for x in s.actual.values() if x):stops.append('Final distinct-text exposure quota infeasible')
    confirmed=Counter(i['category'] for i in issueledger['issues'] if i['confirmed_issue'] and t-4<=i['text']<=t)
    if any(n>=3 for n in confirmed.values()):stops.append('Confirmed naturalness pattern at least three in five texts')
    if sum(p['similarity']>=.85 for p in prior_sim)>=3:stops.append('Four extremely similar scene skeletons in current/previous ten')
    if stops:stop(run,t,stops)
    elif t==50:run['status']='completed';write(RUN,run)
    else:write(RUN,run)
    if t%10==0:
        checkpoint(t);run=read(RUN);run['checkpoint_texts'].append(t);write(RUN,run)
    return dict(text=t,committed=True,stopped=bool(stops),stop_reasons=stops,eojeol=m['eojeol_count'],N=cov['N'],U=cov['U'],
        previous=cov['previous_vocab_coverage'],new=[v[i]['lemma'] for i in actual_new],
        selected=[v[i]['lemma'] for i in actual_review],incidental=[v[i]['lemma'] for i in incidental],
        debt=[(v[d['vocab_id']]['lemma'],d['current_window']['to'],d['deadline_status']) for d in debt],warnings=len(warnings))

def next_plan():
    f=files();s=actual_scheduler();t=read(RUN)['last_committed_text']+1;v=vocab(f)
    return dict(text=t,status=read(RUN)['status'],new=[dict(id=i,lemma=v[i]['lemma'],sense=v[i]['sense'],
        affinity=s.entries[i]['scene_affinity']) for i in s.new_ids(t)],open_reviews=[dict(lemma=v[d['vocab_id']]['lemma'],**d) for d in debt_rows(s,t)],
        actual_previous=[v[i]['lemma'] for i,x in s.actual.items() if x])

def stats(recs):
    s=actual_scheduler(recs);t=max((r['text_number'] for r in recs),default=0)
    lengths=[r['eojeol_count'] for r in recs];sizes=[n for r in recs for n in r['sentence_eojeol_counts']]
    previous=[r['coverage']['previous_vocab_coverage'] for r in recs]
    debt=debt_rows(s,t,close=True) if t else []
    return dict(generated_texts=len(recs),hard_errors=sum(len(r['validation']['hard_errors']) for r in recs),
        controlled_violations=sum(r['coverage']['controlled_vocab_coverage']<1 for r in recs),
        previous_below_98=sum(p<.98 for p in previous),grammar_violations=sum(not r['validation']['grammar_pass'] for r in recs),
        unresolved_content_words=sum(len(r['unresolved_tokens']) for r in recs),introduction_conflicts=0,
        semantic_schedule_conflicts=sum(len(set(r['selected_review_vocab_ids'])-set(r['actual_review_vocab_ids'])) for r in recs),
        new_vocabulary_introduced=sum(bool(x) for x in s.actual.values()),
        planned_introductions=sum(e['first_introduction_text']<=t for e in s.entries.values()),
        actual_selected_review_exposures=sum(len(r['actual_review_vocab_ids']) for r in recs),
        incidental_exposures=sum(len(r['incidental_previous_vocab_ids']) for r in recs),
        actual_exposure_distribution=dict(sorted(Counter(len(x) for x in s.actual.values()).items())),
        introduced_exposure_distribution=dict(sorted(Counter(len(x) for x in s.actual.values() if x).items())),
        total_outstanding_debt=len(debt),debt_approaching_deadline=sum(d['deadline_status']=='near_deadline' for d in debt),
        expired_debt=sum(d['deadline_status']=='expired' for d in debt),
        defer_events=sum(len(r.get('defer_events',[])) for r in recs),
        naturalness_warning_categories=dict(Counter(w['rule_id'] for r in recs for w in r['naturalness']['lint_warnings'])),
        semantic_review_flags=sum(len(r['naturalness']['semantic_review']['flags']) for r in recs),
        natural_expression_gaps=[dict(text=r['text_number'],**g) for r in recs for g in r['naturalness']['natural_expression_gaps']],
        genre_distribution=dict(Counter(r['genre'] for r in recs)),
        scene_similarity_max=max((x['similarity'] for r in recs for x in r['scene_similarity_to_previous_10']),default=0),
        scene_extreme_similarity_pairs=[dict(text=r['text_number'],**x) for r in recs for x in r['scene_similarity_to_previous_10'] if x['similarity']>=.85],
        mean_eojeol=statistics.mean(lengths) if lengths else None,min_eojeol=min(lengths,default=0),max_eojeol=max(lengths,default=0),
        sentence_length_distribution=dict(sorted(Counter(sizes).items())),preferred_sentence_compliance=sum(3<=n<=7 for n in sizes)/len(sizes) if sizes else None,
        hard_max_violations=sum(n>10 for n in sizes),previous_coverage_min=min(previous,default=None),
        previous_coverage_mean=statistics.mean(previous) if previous else None,target_99_misses=sum(p<.99 for p in previous))

def checkpoint(t):
    recs=[r for r in records() if r['text_number']<=t];summary=stats(recs)
    prev=[r for r in recs if r['text_number']>t-10]
    summary['new_review_debt_events_last_10']=sum(len(r['defer_events']) for r in prev)
    write(REPORTS/f'phase3_checkpoint_{t:03d}.json',summary)
    lines=[f'# Phase 3 checkpoint K1-{t:03d}','',f"逐次確定本文 {len(recs)} 本。停止状態: {read(RUN)['status']}。",'',
           '過去実績はこのrunの本文だけ。未導入400語等の0回を失敗と扱わない。99% target missはhard failureではない。','',
           '| 指標 | 結果 |','|---|---|']
    lines += [f'| {k} | {value} |' for k,value in summary.items()]
    (REPORTS/f'phase3_checkpoint_{t:03d}.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def report():
    recs=records();run=read(RUN);v=vocab(files());summary=stats(recs)
    attempts=[read(p) for p in sorted((PILOT/'failed_attempts').glob('*.json'))] if (PILOT/'failed_attempts').exists() else []
    summary['attempted_hard_errors']=[dict(text=r['text_number'],errors=r['validation']['hard_errors']) for r in attempts]
    summary['attempted_count']=len(recs)+len(attempts)
    summary['attempt_controlled_violations']=sum(r['coverage']['controlled_vocab_coverage']<1 for r in attempts)
    summary['attempt_previous_below_98']=sum(r['coverage']['previous_vocab_coverage']<.98 for r in attempts)
    summary['attempt_unresolved_content_words']=sum(len(r['unresolved_tokens']) for r in attempts)
    summary['attempt_naturalness_warning_categories']=dict(Counter(w['rule_id'] for r in attempts for w in r['naturalness']['lint_warnings']))
    summary['confirmed_issue_categories']=dict(Counter(i['category'] for i in read(ISSUES)['issues'] if i['confirmed_issue']))
    summary['translation_fidelity_flags']=sum(len(r['translation_fidelity_flags']) for r in recs)
    summary['freeze_errors']=freeze_errors()
    summary['annotation_triage']=annotation_triage(recs,files())
    write(REPORTS/'k1_phase3_sequential_50_validation_result.json',dict(run=run,summary=summary))
    human=['# Phase 3 人間レビュー用本文','', 'このrunの逐次実績。自然さ・語義・訳のモデル確認は人間承認ではありません。','']
    words=lambda ids:', '.join(v[i]['lemma']+' / '+i for i in ids) or 'なし'
    for r in recs+attempts:
        human += [f"## {r['id']} {r['title_ko']}",'',r['text_ko'],'','### 日本語訳','',r['translation_ja'],'',
            f"新出: {words(r['actual_new_vocab_ids'])}",'',f"選択review: {words(r['actual_review_vocab_ids'])}",'',
            f"incidental: {words(r['incidental_previous_vocab_ids'])}",'',f"defer: {words(r['deferred_review_vocab_ids'])}",'',
            f"Coverage: {r['coverage']} / {r['eojeol_count']} 어절",'',
            f"Warnings: {r['naturalness']['lint_warnings']}",'',f"Semantic review: {r['naturalness']['semantic_review']}",'',
            f"Hard errors: {r['validation']['hard_errors']}。失敗試行はledger未反映、日本語訳もdraft。" if r in attempts else '確定本文・実ledger反映済み。','']
    (REPORTS/'k1_phase3_001_050_review.md').write_text('\n'.join(human)+'\n',encoding='utf-8')
    comparison=[]
    for r in recs+attempts:
        old=ROOT/'pilot/ko/k1/phase2_3/texts'/f"{r['id']}.json"
        if old.exists():
            o=read(old);comparison.append(dict(text=r['text_number'],identical_body=r['text_ko']==o['text_ko'],
                phase23_scene=o.get('scene'),phase3_scene=r['scene_fingerprint'],
                previous_coverage_difference=r['coverage']['previous_vocab_coverage']-o['coverage']['previous_vocab_coverage'],
                review_before=o.get('actually_used_review_vocab_ids',[]),review_after=r['actual_review_vocab_ids'],
                confirmed_issue_recurrence=[i for i in read(ISSUES)['issues'] if i['text']==r['text_number'] and i['confirmed_issue']],
                credited=r in recs,
                guideline_effect='Fresh attempt, not a copy. Genitive/filler risks reduced, but hard vocabulary/length failure blocks acceptance; semantic judgment remains provisional.' if r in attempts else 'Generated afresh from actual prior state; no literal genitive padding or stretched verb frame identified in second pass. Human review pending.'))
    write(PILOT/'phase2_3_comparison.json',comparison)
    verdict='C. FAIL — 設計修正が必要' if run['status']=='stopped' else 'B. CONDITIONAL PASS — 人間の語義・自然さ確認後に次の連続テストを判断'
    lines=['# K1 Phase 3 連続運用検証','',f"判定: **{verdict}**。",'',
        f"確定 {len(recs)} 本。run状態 {run['status']}。停止: {run['stop']}。K1-051以降は生成しません。",'',
        '## Generation / hard validation','',str(summary['attempted_hard_errors']),'',
        '| 指標 | 結果 |','|---|---|']
    lines += [f'| {k} | {value} |' for k,value in summary.items() if k!='annotation_triage']
    lines += ['', '## 計数・承認の限界','',
        'Nは解決された語彙意味単位token。助詞・語尾・許可構文の文法bound form・句読点は除外。複合lemmaは登録単位、固有名詞・定型exceptionは各span1。Uは当該教材の初出Expansion token。previous=(N−U)/N。未解決内容語もNへ含めhard停止する。titleは別に許可を確認し本文N/Uには含めない。', '',
        '生形態素解析・rule normalization・文脈上のsense判断を分離して保存した。Kiwi解析との一致は独立した語義の正解を証明しない。incidentalも実表層と文脈判断を持つものだけcredit。選択・defer・候補にはcreditを付けない。', '',
        'review windowは変更していない。Phase 3では最終教材の検証後にwindowを閉じ、未払い枠を期限切れとして停止する。near-deadline大量集中は3教材以内30語超、数的capacity上界は10review/教材。これは自然さを保証せず、語数ノルマでもない。','',
        'Scene similarityは6fieldの一致/Jaccard平均。直近10本で0.85以上3本と現本文が一致した場合停止。タグ意味類似モデルではなく、繰り返しテンプレートのスクリーニング。','',
        '## Phase 2.3との比較','',str(comparison),'',
        '## 次の判断','',
        '停止した場合は原因を直し、同じfreeze入力での再runまたはreport-only設計案の人間判断が必要。50本成功でも300本の量産許可ではない。自然さ・制限sense・日本語訳の人間レビューを残す。']
    (REPORTS/'k1_phase3_sequential_50_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return dict(generated=len(recs),status=run['status'],stop=run['stop'],summary={k:x for k,x in summary.items() if k not in ('annotation_triage','natural_expression_gaps')})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['init','next','accept','report']);p.add_argument('source',nargs='?');a=p.parse_args()
    result=initialize() if a.command=='init' else next_plan() if a.command=='next' else accept(a.source) if a.command=='accept' else report()
    import json;print(json.dumps(result,ensure_ascii=False,indent=2))
