"""Reanalyse raw pilot bodies; hard language QA remains conditional on sense hypotheses."""
import argparse,sys
from collections import Counter
from jsonschema import Draft202012Validator
from k1_phase2_2 import *

def inspect_record(rec,files,kiwi):
    errors=[];warnings=[];t=rec['text_number'];vocab=vocab_map(files)
    first={i:r['text'] for r in files['introduction_schedule.json']['rows'] for i in r['entry_ids']}
    new=sorted(i for i,n in first.items() if n==t);reviews=rec['scheduled_review_vocab_ids']
    expected=analyze(rec['text_ko'],files,t,reviews,rec.get('sense_overrides'),kiwi)
    for k in ('annotations','raw_morphology','annotation_review_required','unresolved_tokens','grammar_used'):
        if rec[k]!=expected[k]:errors.append('Raw reanalysis mismatch: '+k)
    if rec['scheduled_new_vocab_ids']!=new:errors.append('Frozen introduction IDs mismatch')
    if len(reviews)!=len(set(reviews)):errors.append('Duplicate review IDs')
    used={a['vocab_id'] for a in expected['annotations'] if a['vocab_id']}
    retired=set(files['id_migration.json']['retired_ids'])
    if used&retired:errors.append('Retired vocabulary used')
    if used-vocab.keys():errors.append('Unregistered vocabulary ID')
    if any(i in first and first[i]>t for i in used):errors.append('Future Expansion used')
    if set(new)-used:errors.append('Scheduled new lemma missing')
    actual_new=sorted(used&set(new));actual_review=sorted(used&set(reviews))
    extra=sorted(i for i in used if i in first and first[i]<t and i not in reviews)
    for k,val in [('actually_used_new_vocab_ids',actual_new),('actually_used_review_vocab_ids',actual_review),('extra_previous_vocab_ids',extra)]:
        if rec[k]!=val:errors.append(k+' mismatch')
    if any(i not in first or first[i]>=t for i in reviews):errors.append('Invalid/current/future review ID')
    if t>=256 and actual_new:errors.append('New vocabulary in consolidation zone')
    for a in expected['annotations']:
        if not 0<=a['start']<a['end']<=len(rec['text_ko']) or rec['text_ko'][a['start']:a['end']]!=a['surface']:errors.append('Invalid annotation span')
        if a['vocab_id'] in vocab and any(a[k]!=vocab[a['vocab_id']][k] for k in ('lemma','pos','sense')):errors.append('Annotation identity mismatch')
    coverage=evaluate_lexical_tokens(token_stream(expected['annotations']),t,files)
    c=dict(denominator_N=coverage['N'],new_tokens_U=coverage['U'],controlled_vocab_coverage=coverage['controlled_vocab_coverage'],
           previous_vocab_coverage=coverage['previous_vocab_coverage'],target_99_met=coverage['previous_vocab_coverage'] is not None and coverage['previous_vocab_coverage']>=.99)
    if rec['coverage']!=c:errors.append('Coverage metadata mismatch')
    errors+=coverage['errors'];warnings+=coverage['warnings']
    grammar_pass=not any(x['type'] in ('unapproved_or_unresolved_grammar','unaccounted_morpheme') for x in expected['annotation_review_required'])
    if expected['unresolved_tokens']:errors+=['Unresolved: '+a['lemma'] for a in expected['unresolved_tokens']]
    if not grammar_pass:errors.append('Unlisted or unresolved grammar')
    if set(expected['grammar_used'])-{g['id'] for g in files['grammar.json']}:errors.append('Unregistered grammar ID')
    metrics=text_metrics(rec['text_ko']);p=files['profile.json']
    length_pass=p['length']['min_eojeol']<=metrics['eojeol_count']<=p['length']['max_eojeol']
    sentence_pass=metrics['max_sentence_eojeol']<=p['sentence_length']['hard_max_eojeol']
    if not length_pass:errors.append('Length outside 120..180 eojeol')
    if not sentence_pass:errors.append('Sentence over hard maximum 10')
    if metrics['preferred_sentence_outliers']:warnings.append('Sentences outside preferred 4..7 eojeol')
    for k in ('eojeol_count','sentence_count','max_sentence_eojeol'):
        if rec[k]!=metrics[k]:errors.append('Metric mismatch: '+k)
    if len(actual_new)>2:errors.append('More than two new lemmas')
    if coverage['U']>3:warnings.append('New-token soft maximum 3 exceeded')
    missing=set(reviews)-used
    if {c['vocab_id'] for c in rec['semantic_schedule_conflicts']}!=missing:errors.append('Semantic conflict ledger mismatch')
    schedule_pass=not missing and set(new)<=used
    if not 5<=len(actual_review)<=8:warnings.append('Review soft target 5..8 missed; naturalness takes priority')
    flags=dict(vocab_pass=coverage['ok'],grammar_pass=grammar_pass,length_pass=length_pass,sentence_length_pass=sentence_pass,
               schedule_pass=schedule_pass,naturalness_review_required=True)
    if rec['validation']!=flags:errors.append('Validation flag mismatch')
    title=analyze(rec['title_ko'],files,t,[],rec.get('sense_overrides'),kiwi)
    title_coverage=evaluate_lexical_tokens(token_stream(title['annotations']),t,files)
    if not title_coverage['ok'] or title['unresolved_tokens'] or any(x['type'] in ('unapproved_or_unresolved_grammar','unaccounted_morpheme') for x in title['annotation_review_required']):errors.append('Title unlicensed vocabulary/grammar')
    if not rec['translation_ja'].strip():errors.append('Missing translation')
    status='FAIL' if errors else 'PASS' if c['target_99_met'] else 'PASS_WITH_TARGET_MISS'
    active_expansion=used&first.keys()
    recent=[i for i in active_expansion if 0<=t-first[i]<p['exposure_policy']['recent_window_texts']]
    recent_e3=[i for i in recent if vocab[i]['tier']=='E3']
    return dict(id=rec['id'],text_number=t,group=rec['group'],status=status,errors=errors,warnings=warnings,
        coverage=c,metrics=metrics,review_count=len(actual_review),selected_review_count=len(reviews),new_lemma_count=len(actual_new),
        scheduled_expansion_count=len(new)+len(reviews),extra_previous_count=len(extra),actual_expansion_count=len(active_expansion),
        recently_introduced_expansion_count=len(recent),recently_introduced_E3_count=len(recent_e3),validation=flags,
        semantic_schedule_conflicts=rec['semantic_schedule_conflicts'],annotation_ambiguity_occurrences=len(expected['annotation_review_required']),
        unresolved_token_count=len(expected['unresolved_tokens']),new_token_counts=dict(Counter(a['vocab_id'] for a in expected['annotations'] if a['vocab_id'] in new)))

def validate(pilot_dir=PILOT):
    files=inputs();kiwi=make_kiwi();errors=check_freeze();selected=selection(files)
    schema=read(PILOT/'pilot_text.schema.json');Draft202012Validator.check_schema(schema)
    scenes=read(PILOT/'authored_scenes.json');by_number={s['text_number']:s for s in scenes};records=[];results=[]
    if len(scenes)!=25 or len(by_number)!=25:errors.append('Authored source must contain exactly 25 distinct texts')
    for path in sorted((Path(pilot_dir)/'texts').glob('K1-*.json')):
        try:rec=read(path)
        except (OSError,ValueError) as exc:errors.append(str(exc));continue
        issues=list(Draft202012Validator(schema).iter_errors(rec))
        if issues:errors.extend(path.name+': '+i.message for i in issues);continue
        if rec['id']!=path.stem or rec['id']!=f"K1-{rec['text_number']:03}":errors.append('Number/ID/filename mismatch')
        if rec['group']!=('B' if rec['text_number'] in selected['first_introduction_B'] else 'A'):errors.append('A/B group mismatch')
        records.append(rec);results.append(inspect_record(rec,files,kiwi))
    numbers=[r['text_number'] for r in records]
    if numbers!=selected['all_text_numbers'] or sorted(by_number)!=selected['all_text_numbers']:errors.append('Must contain exactly the approved A20+B5')
    if read(PILOT/'selection.json')!=selected:errors.append('Selection not derived from frozen input')
    by_record={r['text_number']:r for r in records}
    if set(numbers)==set(by_number):
        def verify_plan(scene,proposal):
            rec=by_record[scene['text_number']]
            if rec['scheduler_selection']!=proposal or rec['scheduled_review_vocab_ids']!=[r['vocab_id'] for r in proposal['selected_reviews']]:errors.append(rec['id']+': Scheduler replay mismatch')
            if rec['scene_affinity']!=scene['scene']:errors.append(rec['id']+': Scene metadata mismatch')
            if source_text(scene)!=(rec['text_ko'],rec['translation_ja']):errors.append(rec['id']+': Authored source mismatch')
            return rec
        _,ledger=state_steps(files,scenes,verify_plan)
        if read(PILOT/'exposure_ledger.json')!=ledger:errors.append('Hypothetical/observed ledger mismatch')
    ambiguity=annotation_triage(records,files)
    groups={}
    for group in ('A','B'):
        rows=[r for r in results if r['group']==group];counts=Counter(r['status'] for r in rows)
        groups[group]={'text_count':len(rows),'counts':{s:counts[s] for s in ('PASS','PASS_WITH_TARGET_MISS','FAIL')},
            'hard_error_texts':sum(bool(r['errors']) for r in rows),'semantic_schedule_conflict_count':sum(len(r['semantic_schedule_conflicts']) for r in rows),
            'mean_eojeol':sum(r['metrics']['eojeol_count'] for r in rows)/len(rows) if rows else 0,
            'previous_coverage_min':min((r['coverage']['previous_vocab_coverage'] or 0 for r in rows),default=0),
            'review_soft_target_met':sum(5<=r['review_count']<=8 for r in rows)}
    return dict(phase='2.2',ok=not errors and all(r['status']!='FAIL' for r in results),errors=errors,
        frozen_input_integrity='PASS' if not check_freeze() else 'FAIL',groups=groups,results=results,annotation_triage=ambiguity,
        naturalness_human_approved=False,mass_generation_approved=False,
        limitations=['Raw morphology and reproducible annotations are not independent sense truth.',
          'Sparse pilot assumes scheduled earlier introductions, not a delivered 300-text history.',
          '5..8 reviews is soft; first text has no possible review; target99 misses are not blockers if hard98 passes.',
          'Full 500 by six distinct actual exposures is not proven by 25 texts.'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--json',action='store_true');p.add_argument('--save',action='store_true');a=p.parse_args()
    result=validate()
    if a.save:write(REPORTS/'k1_phase2_2_validation_result.json',result)
    sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(result if a.json else {k:v for k,v in result.items() if k not in ('results','annotation_triage')},ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['ok'] else 1)
