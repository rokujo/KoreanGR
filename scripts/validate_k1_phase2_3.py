"""Hard QA and nonauthoritative naturalness warnings are deliberately separate."""
import argparse,sys,json
from collections import Counter
from statistics import mean
from k1_phase2_3 import *
from k1_naturalness_lint import sentences
from validate_k1_phase2_1A import validate as validate_inputs

def validate(pilot_dir=PILOT):
    errors=frozen_errors();files=inputs();kiwi=make_kiwi()
    db=validate_inputs(DATA,False)
    errors+=['K1 inputs: '+e for e in db['errors']]
    schema=read(PILOT/'pilot_text.schema.json');Draft202012Validator.check_schema(schema)
    gs=read(DATA/'naturalness_guidelines.schema.json');Draft202012Validator.check_schema(gs)
    errors+=['Guideline schema: '+e.message for e in Draft202012Validator(gs).iter_errors(read(DATA/'naturalness_guidelines.json'))]
    scenes=read(PILOT/'authored_scenes.json');sources={s['text_number']:s for s in scenes}
    records=[];results=[];selected=selection(files);numbers=selected['all_text_numbers']
    for path in sorted((pilot_dir/'texts').glob('K1-*.json')):
        r=read(path);t=r['text_number'];records.append(r)
        hard=inspect_record(r,files,kiwi)
        issues=list(Draft202012Validator(schema).iter_errors(r))
        hard['errors']+=['Schema: '+i.message for i in issues]
        if path.stem!=r['id'] or r['id']!=f'K1-{t:03}':hard['errors'].append('Filename/number mismatch')
        s=sources.get(t)
        if not s:hard['errors'].append('Missing source')
        else:
            if s['text_ko']!=r['text_ko'] or s['translation_ja']!=r['translation_ja']:hard['errors'].append('Source/body mismatch')
            pairs=s.get('aligned_translation',[])
            if [k for k,j in pairs]!=[k for _,k in sentences(r['text_ko'])]:hard['errors'].append('Translation Korean alignment mismatch')
            if ' '.join(j for k,j in pairs)!=r['translation_ja']:hard['errors'].append('Translation Japanese alignment mismatch')
            if r['translation_ja'].startswith('DRAFT'):hard['errors'].append('Pending translation')
            if r['translation_fidelity']['flags']!=translation_lint(pairs):hard['errors'].append('Translation warning metadata mismatch')
            if r['naturalness_semantic_review']!=second_pass(s,r):hard['errors'].append('Semantic second-pass metadata mismatch')
        if r['translation_fidelity']['korean_sha256']!=sha256_text(r['text_ko']):hard['errors'].append('Translation refers to stale Korean body')
        warnings=lint(r['text_ko'],r['annotations'],files['id_migration.json']['retired_ids'])
        if r['naturalness_lint']!=warnings:hard['errors'].append('Naturalness warning metadata mismatch')
        if r['naturalness_semantic_review']['human_approved'] or r['translation_fidelity']['human_approved']:hard['errors'].append('Unsubstantiated human approval')
        hard['naturalness_warnings']=warnings
        hard['semantic_review_flags']=r['naturalness_semantic_review']['flags']
        hard['translation_fidelity_flags']=r['translation_fidelity']['flags']
        hard['natural_expression_gaps']=r['natural_expression_gaps']
        hard['status']='FAIL' if hard['errors'] else 'PASS' if r['coverage']['target_99_met'] else 'PASS_WITH_TARGET_MISS'
        results.append(hard)
    if [r['text_number'] for r in records]!=numbers or sorted(sources)!=numbers or len(scenes)!=25:errors.append('Must have exactly frozen A20+B5, no new pilot numbers')
    by_number={r['text_number']:r for r in records}
    if set(by_number)==set(sources):
        def replay(scene,proposal):
            r=by_number[scene['text_number']]
            if r['scheduler_selection']!=proposal:errors.append(r['id']+': Scheduler replay mismatch')
            if r['scheduled_review_vocab_ids']!=[e['vocab_id'] for e in proposal['selected_reviews']]:errors.append(r['id']+': Review selection mismatch')
            return r
        _,ledger=state_steps(files,scenes,replay);ledger['phase']='2.3'
        if read(PILOT/'exposure_ledger.json')!=ledger:errors.append('Actual/assumed exposure ledger mismatch')
    modified=0;defer=[]
    vocab={e['id']:e for e in files['core_vocab.json']+files['expansion_vocab.json']}
    for r in records:
        old=read(ROOT/'pilot/ko/k1/phase2_2/texts'/f"{r['id']}.json")
        modified+=old['text_ko']!=r['text_ko']
        # Includes already unpaid old selection as well as words withdrawn by the semantic gate.
        for vid in sorted((set(old['scheduled_review_vocab_ids'])|set(r['scheduled_review_vocab_ids']))-set(r['actually_used_review_vocab_ids'])-set(r['extra_previous_vocab_ids'])):
            w=next(e for e in files['vocab_review_windows.json']['entries'] if e['vocab_id']==vid)
            defer.append(dict(text_number=r['text_number'],vocab_id=vid,lemma=vocab[vid]['lemma'],
                cause='Natural scene gate or omitted/unmatched review; no occurrence credit.',
                previously_unpaid=vid not in old['actually_used_review_vocab_ids'],
                review_windows=w['review_windows'],next_opportunities=[x for x in w['review_windows'] if x['to']>r['text_number']],
                resolution='Dynamic semantically compatible later scene; retain debt, not an exact reassignment or promised observation.'))
    groups={}
    for g in ('A','B'):
        rows=[r for r in results if r['group']==g];c=Counter(r['status'] for r in rows)
        groups[g]=dict(text_count=len(rows),counts={s:c[s] for s in ('PASS','PASS_WITH_TARGET_MISS','FAIL')},
          mean_eojeol=mean(r['metrics']['eojeol_count'] for r in rows),previous_coverage_min=min(r['coverage']['previous_vocab_coverage'] for r in rows),
          review_soft_target_met=sum(5<=r['review_count']<=8 for r in rows))
    warning_counts=Counter(w['rule_id'] for r in results for w in r['naturalness_warnings'])
    summary=dict(modified_texts=modified,translations_reauthored=len(records),hard_errors=len(errors)+sum(len(r['errors']) for r in results),
        controlled_coverage_violations=sum(r['coverage']['controlled_vocab_coverage']!=1 for r in results),
        previous_hard_violations=sum((r['coverage']['previous_vocab_coverage'] or 0)<.98 for r in results),
        grammar_violations=sum(not r['validation']['grammar_pass'] for r in results),
        unresolved_tokens=sum(r['unresolved_token_count'] for r in results),naturalness_warnings=sum(warning_counts.values()),
        naturalness_warning_categories=dict(warning_counts),semantic_review_flags=sum(len(r['semantic_review_flags']) for r in results),
        semantic_review_flagged_texts=sum(bool(r['semantic_review_flags']) for r in results),
        translation_fidelity_flags=sum(len(r['translation_fidelity_flags']) for r in results),natural_expression_gaps=sum(len(r['natural_expression_gaps']) for r in results),
        current_selected_review_conflicts=sum(len(r['semantic_schedule_conflicts']) for r in results),deferred_review_count=len(defer))
    return dict(phase='2.3',ok=summary['hard_errors']==0,errors=errors,summary=summary,groups=groups,
        language_input_counts={k:db['summary'][k] for k in ('core','expansion','total','tiers','grammar')},
        frozen_input_integrity='PASS' if not frozen_errors() else 'FAIL',results=results,deferred_reviews=defer,
        annotation_triage=annotation_triage(records,files),naturalness_human_approved=False,
        phase3_recommendation='Conditional limited sequential 50-text validation; retain contextual human review and all warnings/debt. No 300-text authorization.',
        mass_generation_approved=False,limitations=['Rule-based reanalysis reproduces hypotheses, not independent sense gold.',
          'Warning counts are candidate occurrences, not proven errors. Semantic/translation YES is author screening, not human approval.',
          'Sparse A20/B5 assumptions are not a delivered sequential corpus; final 500 × six actual exposures are unproven.',
          'Two new tokens with N < 200 can miss target99 without blocking hard98.'])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--save',action='store_true');parser.add_argument('--json',action='store_true');a=parser.parse_args()
    result=validate()
    if a.save:write(REPORTS/'k1_phase2_3_validation_result.json',result)
    sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(result if a.json else {k:v for k,v in result.items() if k not in ('results','annotation_triage','deferred_reviews')},ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['ok'] else 1)
