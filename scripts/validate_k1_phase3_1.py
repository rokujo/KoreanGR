"""Reparse the three candidates and replay the one authoritative smoke commit."""
from copy import deepcopy
from collections import Counter
from jsonschema import Draft202012Validator
from k1_phase3_1 import RUN_DIR,LEDGER,FREEZE,freeze_errors,REPORTS,ROOT,DATA,read,write
from k1_candidate_gate import CandidateGate,build_snapshot,digest
from k1_phase3 import files
from k1_phase2_3 import make_kiwi

def validate():
    errors=freeze_errors();f=files();g=CandidateGate(RUN_DIR,LEDGER,f=f,kiwi=make_kiwi());state=g.load()
    initial=read(RUN_DIR/'initial_state.json');snap=build_snapshot(f,initial,1)
    saved=read(RUN_DIR/'allowed_vocab_snapshots/K1-001-epoch-0.json')
    if snap!=saved:errors.append('Allowed snapshot differs from actual initial state')
    errors += ['Snapshot schema: '+e.message for e in Draft202012Validator(read(DATA/'phase3_1/allowed_snapshot.schema.json')).iter_errors(saved)]
    candidates=[read(p) for p in sorted((RUN_DIR/'candidates').glob('*.json'))];attempts=[]
    for c in candidates:
        errors += ['Candidate schema: '+e.message for e in Draft202012Validator(read(RUN_DIR/'candidate.schema.json')).iter_errors(c)]
        check=deepcopy(c);value=check.pop('candidate_digest')
        if digest(check)!=value:errors.append('Candidate digest mismatch')
        if c['ledger_sha_before_evaluation']!=c['ledger_sha_after_evaluation']:errors.append('Candidate mutated actual state')
        if c['state_checksum_before']!=initial['state_checksum']:errors.append('Candidate evaluated against noninitial state')
        r=g.evaluate(c['source'],initial,snap)
        for k in ('annotations','raw_morphology','resolver_decisions','hard_errors','hard_pass','coverage','eojeol_count','sentence_prechecks','invalid_usage_ids','incidental_previous_vocab_ids'):
            if r[k]!=c[k]:errors.append('Candidate reanalysis mismatch: '+k)
        attempts.append(dict(attempt=c['attempt_number'],status=c['candidate_status'],eojeol=c['eojeol_count'],
            hard_error_codes=sorted({e['code'] for e in c['hard_errors']}),coverage=c['coverage'],
            invalid_usage_ids=c['invalid_usage_ids'],unresolved_tokens=len(c['unresolved_tokens']),
            state_unchanged=c['ledger_sha_before_evaluation']==c['ledger_sha_after_evaluation'],
            sentence_precheck_failures=[x['sentence'] for x in c['sentence_prechecks'] if not x['passed']],
            resolver_decisions=c['resolver_decisions']))
    committed=[read(p) for p in sorted((RUN_DIR/'texts').glob('*.json'))]
    if len(candidates)>3 or any(c['text_number']!=1 for c in candidates+committed):errors.append('Smoke scope exceeded')
    if len(committed)!=1 or state['epoch']!=1 or state['last_committed_text']!=1:errors.append('Smoke single-commit requirement failed')
    if committed!=state['committed_records']:errors.append('Materialized texts differ from authoritative state')
    if not committed:raise ValueError('No smoke committed text')
    c=committed[0];r=g.evaluate(c['source'],initial,snap)
    if not r['hard_pass']:errors.append('Committed text fails final raw validation')
    for k in ('annotations','raw_morphology','coverage','text_ko','actual_new_vocab_ids','actual_review_vocab_ids','incidental_previous_vocab_ids'):
        if c[k]!=r[k]:errors.append('Committed reanalysis mismatch: '+k)
    if sum(e['actual_exposure_count'] for e in state['entries'])!=2:errors.append('Unexpected credit / failed attempt credit')
    if any(e['actual_texts']!=([1] if e['vocab_id'] in snap['planned_new_vocab_ids'] else []) for e in state['entries']):errors.append('Actual exposure replay mismatch')
    if len(state['genre_history'])!=1 or len(state['scene_history'])!=1:errors.append('Failed attempts changed histories')
    if read(RUN_DIR/'run_control.json')['status']!='completed':errors.append('Smoke controller not completed')
    audit=read(REPORTS/'k1_phase3_1_morphology_audit.json')
    if audit['failed_probes']:errors.append('Morphology regression probes failed')
    result=dict(phase='3.1',pass_=not errors,decision='A' if not errors else 'B',errors=errors,
        phase3_failure_unchanged=not freeze_errors(),candidate_attempts=attempts,committed_count=len(committed),
        generated_text_numbers=[1],not_generated='K1-002 and later',
        hard_result=dict(eojeol=c['eojeol_count'],max_sentence_eojeol=c['max_sentence_eojeol'],coverage=c['coverage'],
            unresolved_content_words=len(c['unresolved_tokens']),invalid_usages=len(c['invalid_usage_ids']),
            future_vocab=0,grammar_violations=0,planned_new_vocab_ids=snap['planned_new_vocab_ids'],actual_new_vocab_ids=c['actual_new_vocab_ids']),
        ledger=dict(epoch=state['epoch'],actual_entry_text_pairs=sum(e['actual_exposure_count'] for e in state['entries']),
            introduced_count=sum(e['actual_first_text'] is not None for e in state['entries']),exposure_distribution=dict(Counter(e['actual_exposure_count'] for e in state['entries'])),
            genre_history_count=len(state['genre_history']),scene_history_count=len(state['scene_history']),review_debt=state['review_debt']),
        morphology_audit=dict(probes=audit['probe_count'],failed=len(audit['failed_probes']),stem_inventory_count=len(audit['stem_candidates']),
            standalone_help_active=audit['inactive_standalone_help']['active']),
        naturalness=dict(lint_warnings=len(c['naturalness']['lint_warnings']),semantic_flags=c['naturalness']['semantic_review']['flags'],human_approved=False),
        limitations='Controlled authored regression smoke. Semantic inference remains conditional; does not demonstrate arbitrary LLM retries or sequential review feasibility.')
    write(REPORTS/'k1_phase3_1_validation_result.json',result)
    return result

if __name__=='__main__':
    r=validate();print(dict(pass_=r['pass_'],errors=r['errors'],hard=r['hard_result'],ledger=r['ledger'],morphology=r['morphology_audit']))
    raise SystemExit(0 if r['pass_'] else 1)
