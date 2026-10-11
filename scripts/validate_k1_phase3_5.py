"""Validate new artifacts and replay 001..003 in TEMP state only.

The stopped real run is never resumed/reset. No 005 candidate is generated.
"""
import hashlib
import tempfile
from pathlib import Path
from collections import Counter
from jsonschema import Draft202012Validator
from k1_phase3 import ROOT,read,write,files
from k1_phase3_5 import PILOT,LEDGER,SmokeGate,freeze_errors
from k1_phase3_5_gate import CandidateGate
from k1_grammar_semantic_gate import registry,summarize
from k1_phase3_4_resolver import analyze
from k1_phase3_2_analysis import make_kiwi

def scope_diagnostics(f,k):
    failed=read(PILOT/'candidates/K1-004-attempt-01.json')
    source=failed['source'];sent='저는 물을 받고 마셔요.'
    paragraph=' '.join(source['sentences'][24:30])
    probes={'simple_drinking_control':'저는 물을 마셔요.','split_action_control':'저는 물을 받아요. 저는 물을 마셔요.',
            'sentence':sent,'quoted':'"'+sent+'"','narration_and_quote':'저는 말해요. "'+sent+'"',
            'paragraph':paragraph,'full_candidate':failed['text_ko']}
    result=[]
    for scope,text in probes.items():
        a=analyze(text,f,4,[],kiwi=k,scope=scope)
        hit=text.find('마셔요');raw=[x for x in a['raw_morphology'] if hit<=x['start']<hit+3]
        result.append(dict(scope=scope,text=text,raw_parts=raw,
            registered_identities=[x for x in a['annotations'] if hit<=x['start']<hit+3],
            original_character_span=[hit,hit+3],permission_granted=False))
    write(ROOT/'reports/k1_phase3_5_new_analyzer_scope_audit.json',result)
    return result

def validate():
    f=files();k=make_kiwi();g=SmokeGate(kiwi=k);state=g.load();errors=[]
    reg=registry();schema=read(ROOT/'config/languages/ko/k1/grammar_semantics.schema.json')
    errors += [e.message for e in Draft202012Validator(schema).iter_errors(read(ROOT/'config/languages/ko/k1/grammar_semantics.json'))]
    frozen=freeze_errors();errors+=['Frozen history changed: '+p for p in frozen]
    failures=read(ROOT/'reports/k1_phase3_5_fixture_audit.json')
    errors += ['Fixture failure: '+x['id'] for x in failures if not x['passed']]
    for label in ('all','focused'):
        if read(ROOT/f'reports/k1_phase3_5_{label}_test_result.json')['status']!='PASS':errors.append(label+' tests failed')
    record_checks=[]
    with tempfile.TemporaryDirectory() as d:
        replay=SmokeGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=k);replay.initialize()
        for record in state['committed_records']:
            p,r=replay.submit(record['source'])
            if not r['hard_pass']:errors.append('Committed text replay failed');break
            committed=replay.commit(p)
            keys=('text_ko','annotations','raw_morphology','coverage','grammar_used','semantic_grammar_checks','invalid_usage_ids')
            same=all(committed[x]==record[x] for x in keys)
            if not same:errors.append('Committed reanalysis mismatch')
            record_checks.append(dict(id=record['id'],hard_pass=r['hard_pass'],eojeol=r['eojeol_count'],coverage=r['coverage'],
                semantic=summarize(r['semantic_grammar_checks']),planned_new=r['planned_new_vocab_ids'],actual_new=r['actual_new_vocab_ids'],
                future=len([i for i in r['invalid_usage_ids'] if i['reason']=='future_expansion']),invalid=len(r['invalid_usage_ids']),
                unresolved=len(r['unresolved_tokens']),final_reanalysis_equal=same,
                actual_review=r['actual_review_vocab_ids'],incidental=r['incidental_previous_vocab_ids']))
        equality=replay.load()==state
        if not equality:errors.append('Replay ledger differs from actual committed-only ledger')
        fail=read(PILOT/'candidates/K1-004-attempt-01.json');before=replay.ledger.read_bytes()
        _,rr=replay.submit(fail['source'])
        isolated=before==replay.ledger.read_bytes()
        if rr['hard_pass'] or not isolated:errors.append('Failed candidate isolation broken')
    actual_hash=hashlib.sha256(LEDGER.read_bytes()).hexdigest()
    if actual_hash!=fail['ledger_sha_before_evaluation'] or actual_hash!=fail['ledger_sha_after_evaluation']:errors.append('Failed 004 touched ledger')
    if (state['epoch'],state['last_committed_text'])!=(3,3):errors.append('Unexpected committed extent')
    if list((PILOT/'texts').glob('K1-00[4-9].json')) or (PILOT/'sources/K1-005-attempt-01.json').exists():errors.append('STOP boundary breached')
    full=read(ROOT/'reports/k1_phase3_5_existing_text_audit.json')
    scopes=scope_diagnostics(f,k)
    result=dict(phase='3.5',verdict='C',status='FAIL',reason='004 semantic REVIEW STOP; new raw morphology structural ambiguity and future draft word. 005 not generated.',
        implementation_validation_status='PASS' if not errors else 'FAIL',artifact_errors=errors,
        frozen_vocabulary_counts=dict(core=len(f['core_vocab.json']),expansion=len(f['expansion_vocab.json']),total=len(f['core_vocab.json'])+len(f['expansion_vocab.json']),
            tiers=dict(Counter(e['tier'] for e in f['expansion_vocab.json']))),
        coverage_policy=dict(controlled_hard=f['profile.json']['controlled_vocab_coverage_hard_min'],previous_hard=f['profile.json']['previous_vocab_coverage_hard_min'],previous_target=f['profile.json']['previous_vocab_coverage_target']),
        grammar_count=32,registry_schema_pass=not list(Draft202012Validator(schema).iter_errors(read(ROOT/'config/languages/ko/k1/grammar_semantics.json'))),
        auto_pass_capable_grammar_count=32,local_structural_autocheck_count=sum(e['autocheck']=='hard' for e in reg.values()),
        context_heuristic_grammar_count=sum(e['autocheck']=='heuristic' for e in reg.values()),
        context_review_possible_grammar_count=32,registry_policy_ambiguity_count=sum(bool(e['needs_human_policy']) for e in reg.values()),
        fixture_count=len(failures),fixture_errors=sum(not x['passed'] for x in failures),
        bad_003_detected=next(x['passed'] for x in failures if x['id']=='bad_003'),
        frozen_texts_audited=len(full),frozen_audit_counts=dict(Counter(x['decision'] for c in full for x in c['checks'])),
        frozen_texts_requiring_review=sum(bool(c['review_candidates']) for c in full),
        frozen_audit_fail_candidates=[dict(path=c['path'],sentence=x['sentence'],grammar_id=x['grammar_id'],reason=x['evidence']['reason']) for c in full for x in c['automatic_failures']],
        smoke=dict(committed_count=3,candidate_count=4,attempts_per_text={'001':1,'002':1,'003':1,'004':1},
            results=record_checks,failed_004=dict(semantic=summarize(fail['semantic_grammar_checks']),hard_error_codes=dict(Counter(e['code'] for e in fail['hard_errors'])),
                invalid_usage_ids=fail['invalid_usage_ids'],coverage=fail['coverage'],ledger_unchanged=isolated,
                run_control=read(g.control)),
            zero_state_epoch=read(PILOT/'initial_state.json')['epoch'],replay_entire_ledger_equal=equality,
            outstanding_debt=state['review_debt'],expired_debt=state['expired_review_debt'],
            selected_review_credits=sum(e['selected_review_exposure_count'] for e in state['entries']),
            incidental_credits=sum(e['incidental_exposure_count'] for e in state['entries']),
            actual_introduced=sum(e['actual_first_text'] is not None for e in state['entries']),
            generated_005=False,generated_006_or_later=False),
        tests={label:read(ROOT/f'reports/k1_phase3_5_{label}_test_result.json') for label in ('all','focused')},
        frozen_files_checked=len(read(ROOT/'reports/k1_phase3_5_input_freeze.json')['files']),freeze_errors=frozen,
        limitation='All PASS decisions are bounded evidence rules, not independent Korean semantic gold. Existing text REVIEW flags are not confirmed errors. Corpus audit never grants temporal vocabulary permission or imports credits.')
    write(ROOT/'reports/k1_phase3_5_validation_result.json',result)
    print(dict(verdict=result['verdict'],artifact_errors=len(errors),smoke_committed=3,stopped=4,freeze_errors=len(frozen)))
    return result

if __name__=='__main__':validate()
