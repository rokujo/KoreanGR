"""Raw reanalysis and actual-credit replay, distinct from experiment success."""
from collections import Counter
from copy import deepcopy
import json
from jsonschema import Draft202012Validator
from k1_phase3 import (ROOT,DATA,REPORTS,PILOT,RUN,LEDGER,read,write,files,
    records,freeze_errors,metrics,analyze,make_kiwi,vocab,plan,actual_coverage_files)
from k1_review_scheduler import ReviewScheduler
from validate_k1_pilot import token_stream
from lexical_coverage import evaluate_lexical_tokens
from k1_naturalness_lint import lint,translation_lint

def validate():
    f=files();errors=freeze_errors();v=vocab(f)
    core=f['core_vocab.json'];exp=f['expansion_vocab.json']
    if (len(core),len(exp),len(v))!=(300,500,800):errors.append('Vocabulary count mismatch')
    if Counter(e['tier'] for e in exp)!=Counter(E1=200,E2=200,E3=100):errors.append('Tier count mismatch')
    if len(f['grammar.json'])!=32:errors.append('Grammar count mismatch')
    if len({(e['lemma'],e['pos'],e['sense']) for e in core+exp})!=800:errors.append('Identity collision')
    errors += [e.message for e in Draft202012Validator(read(DATA/'phase3/profile.schema.json')).iter_errors(f['profile.json'])]
    for name,schema_name in [('core_vocab.json','vocab.schema.json'),('expansion_vocab.json','vocab.schema.json'),
                             ('vocab_review_windows.json','vocab_review_windows.schema.json')]:
        errors += [name+': '+e.message for e in Draft202012Validator(read(DATA/schema_name)).iter_errors(f[name])]
    retired={m['old_id'] for m in f['id_migration.json']['mappings']}
    if retired&v.keys():errors.append('Retired IDs active')
    replacements={'ko_k1_0808':'닦다','ko_k1_0809':'붙이다','ko_k1_0810':'공','ko_k1_0811':'그림','ko_k1_0812':'들다'}
    if any(v[i]['lemma']!=lemma for i,lemma in replacements.items()):errors.append('Five replacements not preserved')
    if v['ko_k1_0812']['sense']!='hold_lift_by_hand':errors.append('Restricted 들다 identity changed')
    if not any(e['lemma']=='찍다' and e['sense']=='take_photo' for e in core):errors.append('Core photo 찍다 missing')
    recs=records();run=read(RUN);s=ReviewScheduler(f['vocab_review_windows.json']);kiwi=make_kiwi()
    attempts=[read(p) for p in sorted((PILOT/'failed_attempts').glob('*.json'))] if (PILOT/'failed_attempts').exists() else []
    body_results=[]
    for r in recs+attempts:
        t=r['text_number'];accepted=r in recs
        errors += [f'Body schema {t}: '+e.message for e in Draft202012Validator(read(PILOT/'text.schema.json')).iter_errors(r)]
        if t!=s.last_recorded_text+1:errors.append('Non-sequential body: '+str(t))
        a=analyze(r['text_ko'],f,t,r['selected_review_vocab_ids'],r.get('sense_overrides',{}),kiwi)
        for key in ('annotations','raw_morphology','grammar_used','annotation_review_required','unresolved_tokens'):
            if a[key]!=r[key]:errors.append(f'Raw reanalysis mismatch {t}: {key}')
        if any(r[k]!=value for k,value in metrics(r['text_ko']).items()):errors.append(f'Metrics mismatch {t}')
        used={x['vocab_id'] for x in a['annotations'] if x['vocab_id']};expids=set(s.entries);new=s.new_ids(t)
        actual_new=sorted(used&set(new));actual_review=sorted(used&set(r['selected_review_vocab_ids']))
        inc=sorted((used&expids)-set(new)-set(r['selected_review_vocab_ids']))
        if (r['planned_new_vocab_ids'],r['actual_new_vocab_ids'],r['actual_review_vocab_ids'],r['incidental_previous_vocab_ids'])!=(new,actual_new,actual_review,inc):
            errors.append(f'Actual usage metadata mismatch {t}')
        source=read(PILOT/'sources'/f'K1-{t:03d}.json');proposal=plan(source,s,f)
        if proposal!=r['selection_trace']:errors.append(f'Scheduler selection mismatch {t}')
        cf=actual_coverage_files(f,s,t,new)
        cov=evaluate_lexical_tokens(token_stream(a['annotations']),t,cf)
        if any(r['coverage'][k]!=cov[j] for k,j in [('denominator_N','N'),('new_tokens_U','U'),('controlled_vocab_coverage','controlled_vocab_coverage'),('previous_vocab_coverage','previous_vocab_coverage')]):errors.append(f'Coverage mismatch {t}')
        if lint(r['text_ko'],a['annotations'],retired)!=r['naturalness']['lint_warnings']:errors.append(f'Lint mismatch {t}')
        if translation_lint([(p['ko'],p['ja']) for p in r['translation_pairs']])!=r['translation_fidelity_flags']:errors.append(f'Translation lint mismatch {t}')
        missing=set(new)-set(actual_new)
        future=sorted(i for i in used&expids if s.entries[i]['first_introduction_text']>t)
        unconfirmed=sorted(i for i in used&expids if i not in new and not s.actual[i])
        unlicensed=sorted(set(a['grammar_used'])-{g['id'] for g in f['grammar.json']})
        unresolved_grammar=[x for x in a['unresolved_tokens'] if any(a['raw_morphology'][j]['tag'].startswith(('J','E','VX')) for j in x['morph_indices'])]
        body_results.append(dict(text=t,accepted=accepted,eojeol=r['eojeol_count'],coverage=r['coverage'],
            future_expansion_ids=future,unconfirmed_prior_ids=unconfirmed,missing_planned_new_ids=sorted(missing),
            unlicensed_grammar_ids=unlicensed,unresolved_grammar_tokens=unresolved_grammar,
            unresolved_content_tokens=[x for x in a['unresolved_tokens'] if x not in unresolved_grammar],
            retired_ids=sorted(used&retired),hard_errors=r['validation']['hard_errors']))
        if accepted:
            if cov['errors'] or a['unresolved_tokens'] or future or unconfirmed or missing or unlicensed or used&retired or not 120<=r['eojeol_count']<=180 or r['max_sentence_eojeol']>10:errors.append(f'Invalid accepted body {t}')
            s.record(t,actual_new+actual_review+inc)
        elif run['status']!='stopped':errors.append('Failing attempt did not stop run')
    if recs and [r['text_number'] for r in recs]!=list(range(1,len(recs)+1)):errors.append('Accepted sequence not contiguous')
    if run['last_committed_text']!=len(recs):errors.append('Run cursor mismatch')
    if run['status']=='stopped' and any(r['text_number']>run['stop']['text'] for r in recs+attempts):errors.append('Generated beyond stop')
    if any(r['text_number']>50 for r in recs+attempts):errors.append('Beyond Phase 3 limit')
    ledger=read(LEDGER)
    if len(ledger['entries'])!=500:errors.append('Ledger does not cover all active Expansion')
    for e in ledger['entries']:
        i=e['vocab_id'];xs=sorted(s.actual[i])
        if e['actual_texts']!=xs or e['actual_exposure_count']!=len(xs):errors.append('Exposure/silent-credit mismatch '+i)
        if e['actual_first_text']!=(min(xs) if xs else None):errors.append('Actual-first mismatch '+i)
        if e['incidental_exposure_count']!=sum(i in r['incidental_previous_vocab_ids'] for r in recs):errors.append('Incidental mismatch '+i)
        if e['selected_review_exposure_count']!=sum(i in r['actual_review_vocab_ids'] for r in recs):errors.append('Selected-review mismatch '+i)
        if e['paid_review_windows']!={str(k):n for k,n in s.credits[i].items()}:errors.append('Review payment mismatch '+i)
    if ledger['actually_introduced_vocab']!=[e['vocab_id'] for e in ledger['entries'] if e['actual_first_text'] is not None]:errors.append('Actually-introduced list mismatch')
    result=dict(phase='3',validator_integrity_errors=sorted(set(errors)),validator_integrity_pass=not errors,
        experiment_pass=run['status']=='completed' and len(recs)==50 and not errors,
        run_status=run['status'],stop=run['stop'],accepted_count=len(recs),failed_attempt_count=len(attempts),
        vocabulary_counts=dict(core=len(core),expansion=len(exp),total=len(v),tiers=dict(Counter(e['tier'] for e in exp))),
        grammar_count=len(f['grammar.json']),body_results=body_results,
        accepted_review_debt=ledger['review_debt'],actual_credit_pairs=sum(map(len,s.actual.values())),
        limitations='Raw reanalysis is reproducible, not independent semantic gold; failed body never credited.')
    write(REPORTS/'k1_phase3_run_integrity_validation.json',result)
    return result

if __name__=='__main__':
    r=validate();print(json.dumps({k:v for k,v in r.items() if k!='body_results'},ensure_ascii=False,indent=2))
    raise SystemExit(0 if r['validator_integrity_pass'] else 1)
