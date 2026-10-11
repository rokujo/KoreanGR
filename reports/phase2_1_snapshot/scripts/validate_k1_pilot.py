"""Pilot validator. Structural acceptance is conditional on annotation hypotheses.

Does not change any Phase 1.2 file. A semantic schedule conflict is an overall
FAIL even when the licensed-language checks pass. Naturalness is never certified.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
from jsonschema import Draft202012Validator
from select_k1_pilot import ROOT,load_inputs,select
from k1_pilot_analysis import analyze,make_kiwi
from lexical_coverage import evaluate_lexical_tokens
from validate_k1_vocab import load_json

PILOT=ROOT/'pilot/ko/k1'

def check_freeze():
    manifest=json.loads((ROOT/'reports/k1_phase2_input_freeze.json').read_text(encoding='utf-8'))
    errors=[]
    for section in ('files','implementation_files','test_files'):
        for relative,digest in manifest[section].items():
            if hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()!=digest:errors.append('Frozen input changed: '+relative)
    return errors

def text_metrics(text):
    sentences=[s.strip() for s in re.split(r'(?<=[.!?])(?:["”]?\s+|$)',text) if s.strip()]
    sizes=[sum(bool(re.search(r'[가-힣A-Za-z0-9]',w)) for w in s.split()) for s in sentences]
    return dict(eojeol_count=sum(sizes),sentence_count=len(sizes),max_sentence_eojeol=max(sizes,default=0),
                sentence_eojeol_counts=sizes,preferred_sentence_outliers=[i+1 for i,n in enumerate(sizes) if not 4<=n<=7])

def token_stream(annotations):
    result=[]
    for a in annotations:
        if a['role']=='grammar_function':result.append(dict(kind='grammar',id=a['grammar_id']))
        elif a['role']=='proper_name':result.append(dict(kind='proper_name',id=a['lemma']))
        elif a['role']=='frozen_exception':result.append(dict(kind='exception',id=a['exception_id']))
        elif a['vocab_id']:result.append(dict(kind='vocab',id=a['vocab_id']))
        else:result.append(dict(kind='unknown',id=a['surface']))
    return result

def inspect_record(record,files,kiwi):
    t=record['text_number'];errors=[];warnings=[]
    expected_row=files['vocab_exposure_schedule.json']['texts'][t-1]
    vocab={e['id']:e for e in files['core_vocab.json']+files['expansion_vocab.json']}
    expansion={e['id']:e for e in files['expansion_vocab.json']}
    first={e['vocab_id']:e['first_introduction_text'] for e in files['vocab_exposure_schedule.json']['entries']}
    expected=analyze(record['text_ko'],files,t,expected_row['review_vocab_ids'],record.get('sense_overrides'),kiwi)
    # Re-tokenize the raw body. This verifies reconstruction/normalization rules,
    # not the intended sense or native-speaker judgement.
    if record['raw_morphology']!=expected['raw_morphology']:errors.append('Raw morphology no longer matches body')
    if record['annotations']!=expected['annotations']:errors.append('Annotation hypotheses do not match raw/rule normalization')
    if record['grammar_used']!=expected['grammar_used']:errors.append('Grammar metadata differs from recognized raw spans')
    if record['annotation_review_required']!=expected['annotation_review_required']:errors.append('Ambiguity ledger mismatch')
    if record['unresolved_tokens']!=expected['unresolved_tokens']:errors.append('Unresolved ledger mismatch')
    used={a['vocab_id'] for a in record['annotations'] if a['vocab_id']}
    retired={m['old_id'] for m in files['id_migration.json']['mappings']}
    if used&retired:errors.append('Retired ID used')
    if used-vocab.keys():errors.append('Unknown vocabulary ID')
    if any(vid in first and first[vid]>t for vid in used):errors.append('Future Expansion used')
    for a in record['annotations']:
        if not 0<=a['start']<a['end']<=len(record['text_ko']) or record['text_ko'][a['start']:a['end']]!=a['surface']:
            errors.append('Annotation surface/offset mismatch')
        if a['vocab_id'] in vocab:
            e=vocab[a['vocab_id']]
            if (a['lemma'],a['pos'],a['sense'])!=(e['lemma'],e['pos'],e['sense']):errors.append('Vocabulary identity mismatch')
    actual_new=sorted(used&{vid for vid,n in first.items() if n==t})
    actual_review=sorted(used&set(expected_row['review_vocab_ids']))
    extra=sorted(vid for vid in used&expansion.keys() if first[vid]<t and vid not in expected_row['review_vocab_ids'])
    for name,value in [('scheduled_new_vocab_ids',expected_row['new_vocab_ids']),('scheduled_review_vocab_ids',expected_row['review_vocab_ids']),
                       ('actually_used_new_vocab_ids',actual_new),('actually_used_review_vocab_ids',actual_review),('extra_previous_vocab_ids',extra)]:
        if record[name]!=value:errors.append(name+' mismatch')
    coverage=evaluate_lexical_tokens(token_stream(record['annotations']),t,files)
    metrics=text_metrics(record['text_ko']);p=files['profile.json']
    length_pass=p['length']['min_eojeol']<=metrics['eojeol_count']<=p['length']['max_eojeol']
    sentence_pass=metrics['max_sentence_eojeol']<=p['sentence_length']['hard_max_eojeol']
    grammar_pass=not any(x['type']=='unapproved_or_unresolved_grammar' for x in expected['annotation_review_required'])
    grammar_pass=grammar_pass and set(record['grammar_used'])<={g['id'] for g in files['grammar.json']}
    missing_new=set(expected_row['new_vocab_ids'])-set(actual_new)
    missing_review=set(expected_row['review_vocab_ids'])-set(actual_review)
    conflicts=record['semantic_schedule_conflicts']
    if {c['vocab_id'] for c in conflicts}!=missing_review|missing_new:errors.append('Missing scheduled word/conflict ledger mismatch')
    if len({c['vocab_id'] for c in conflicts})!=len(conflicts):errors.append('Duplicate semantic conflict')
    for c in conflicts:
        if c['vocab_id'] not in first:
            errors.append('Unknown conflict vocabulary ID');continue
        if not c['reason'] or not c['proposed_text_candidates']:errors.append('Conflict requires reason and move candidates')
        for destination in c['proposed_text_candidates']:
            if not first[c['vocab_id']]<destination<=300 or destination==t:errors.append('Invalid proposed review destination')
    schedule_pass=not missing_new and not missing_review
    if missing_new:errors.append('Scheduled new vocabulary missing')
    if t>=276 and actual_new:errors.append('New vocabulary in fast zone')
    for field in ('eojeol_count','sentence_count','max_sentence_eojeol'):
        if record[field]!=metrics[field]:errors.append(field+' mismatch')
    expected_coverage=dict(denominator_N=coverage['N'],new_tokens_U=coverage['U'],
        controlled_vocab_coverage=coverage['controlled_vocab_coverage'],previous_vocab_coverage=coverage['previous_vocab_coverage'],
        target_99_met=coverage['previous_vocab_coverage'] is not None and coverage['previous_vocab_coverage']>=.99)
    if record['coverage']!=expected_coverage:errors.append('Coverage metadata mismatch')
    title_analysis=analyze(record['title_ko'],files,t,[],record.get('sense_overrides'),kiwi)
    title_coverage=evaluate_lexical_tokens(token_stream(title_analysis['annotations']),t,files)
    if not title_coverage['controlled_vocab_coverage']==1 or title_analysis['unresolved_tokens']:errors.append('Title vocabulary/grammar requires resolution')
    if not record['translation_ja']:errors.append('Japanese translation missing')
    flags=dict(vocab_pass=coverage['ok'] and not errors,grammar_pass=grammar_pass,length_pass=length_pass,
        sentence_length_pass=sentence_pass,schedule_pass=schedule_pass,naturalness_review_required=True)
    if record['validation']!=flags:errors.append('Validation flag metadata mismatch')
    errors.extend(coverage['errors']);warnings.extend(coverage['warnings'])
    if not grammar_pass:errors.append('Unresolved or unapproved grammar/content span')
    if not length_pass:errors.append('Length outside 120..180 eojeol')
    if not sentence_pass:errors.append('Sentence exceeds hard maximum')
    if metrics['preferred_sentence_outliers']:warnings.append('Some sentences outside preferred 4..7 eojeol')
    language_status='FAIL' if errors else 'PASS' if expected_coverage['target_99_met'] else 'PASS_WITH_TARGET_MISS'
    status='FAIL' if language_status=='FAIL' or not schedule_pass else language_status
    return dict(id=record['id'],text_number=t,status=status,language_status=language_status,errors=errors,warnings=warnings,
        coverage=expected_coverage,validation=flags,metrics=metrics,scheduled_expansion_count=len(expected_row['new_vocab_ids'])+len(expected_row['review_vocab_ids']),
        used_scheduled_expansion_count=len(actual_new)+len(actual_review),missing_new_vocab_ids=sorted(missing_new),missing_review_vocab_ids=sorted(missing_review),
        semantic_schedule_conflicts=conflicts,annotation_ambiguity_occurrences=len(expected['annotation_review_required']),
        annotation_ambiguity_types=len({(x['type'],x['lemma']) for x in expected['annotation_review_required']}),
        unresolved_token_count=len(expected['unresolved_tokens']),title_annotation_review_required=title_analysis['annotation_review_required'])

def validate(pilot_dir=PILOT):
    files=load_inputs();freeze=check_freeze();schema=json.loads((PILOT/'pilot_text.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema);selected=select(files);kiwi=make_kiwi();results=[];errors=list(freeze)
    paths=sorted((pilot_dir/'texts').glob('K1-*.json'))
    numbers=[]
    for path in paths:
        try:record=load_json(path)
        except (OSError,ValueError) as exc:errors.append(f'{path.name}: {exc}');continue
        issues=list(Draft202012Validator(schema).iter_errors(record))
        if issues:errors.extend(f'{path.name}: {e.message}' for e in issues);continue
        numbers.append(record['text_number'])
        if record['id']!=f"K1-{record['text_number']:03}" or path.stem!=record['id']:errors.append('Text number/ID/file mismatch')
        results.append(inspect_record(record,files,kiwi))
    if numbers!=selected['text_numbers']:errors.append('Pilot set differs from data-derived selection')
    counts=dict(Counter(r['status'] for r in results))
    return dict(ok=not errors and all(r['status']!='FAIL' for r in results),frozen_input_integrity='PASS' if not freeze else 'FAIL',
        errors=errors,text_count=len(results),counts={k:counts.get(k,0) for k in ('PASS','FAIL','PASS_WITH_TARGET_MISS')},
        language_counts=dict(Counter(r['language_status'] for r in results)),
        hard_error_texts=sum(bool(r['errors']) for r in results),schedule_conflict_texts=sum(bool(r['semantic_schedule_conflicts']) for r in results),
        semantic_schedule_conflict_count=sum(len(r['semantic_schedule_conflicts']) for r in results),results=results,
        limits=['Annotation hypotheses and Kiwi morphology are not independent sense truth.','Naturalness and translation require human review.','Earlier introductions are simulated from the frozen schedule, not delivered texts.'])

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--pilot-dir',type=Path,default=PILOT);parser.add_argument('--json',action='store_true');parser.add_argument('--save',action='store_true')
    args=parser.parse_args();result=validate(args.pilot_dir)
    if args.save:(ROOT/'reports/k1_phase2_pilot_validation_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else json.dumps({k:v for k,v in result.items() if k!='results'},ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['ok'] else 1)
