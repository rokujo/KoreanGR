"""Read-only smoke replay, parser audits and separate historical integrity."""
from collections import Counter
from copy import deepcopy
import json
from jsonschema import Draft202012Validator
from k1_phase3_2 import SmokeGate, PILOT, LEDGER, freeze_errors
from k1_phase3_2_gate import read, write, ROOT, build_snapshot, digest
from k1_phase3_2_analysis import ALIAS_AUDIT, LEGACY_DEFAULT_SENSE_AUDIT, morphology
from k1_phase3_2_resolver import analyze
from k1_phase3_1 import PROBES

REPORTS=ROOT/'reports'

def validate():
    g=SmokeGate();state=g.load();before=LEDGER.read_bytes();errors=[]
    if freeze_errors():errors.append(dict(type='freeze',files=freeze_errors()))
    rows=state['committed_records'];v={e['id']:e for e in g.f['core_vocab.json']+g.f['expansion_vocab.json']}
    if [r['text_number'] for r in rows]!=[1,2]:errors.append('Smoke must have only contiguous 001,002')
    if read(g.control)['status']!='completed':errors.append('Smoke control not completed')
    if state['epoch']!=2 or state['last_committed_text']!=2:errors.append('Atomic epoch/cursor mismatch')
    known=set();prior=read(PILOT/'initial_state.json');results=[]
    grammar_ids={e['id'] for e in g.f['grammar.json']}
    for r in rows:
        t=r['text_number'];snapshot=read(PILOT/'allowed_vocab_snapshots'/f'K1-{t:03d}-epoch-{t-1}.json')
        fresh_snapshot=build_snapshot(g.f,prior,t)
        if fresh_snapshot['entries']!=snapshot['entries']:errors.append(dict(text=t,type='allowed_snapshot_identity_mismatch'))
        previous={e['vocab_id'] for e in snapshot['entries'] if e['role']=='previous_expansion'}
        if previous!=known:errors.append(dict(text=t,type='planned_previous_leak'))
        fresh=g.evaluate(r['source'],prior,snapshot)
        mismatches=[k for k in ('text_ko','annotations','raw_morphology','coverage','actual_new_vocab_ids','actual_review_vocab_ids','incidental_previous_vocab_ids','grammar_used') if fresh[k]!=r[k]]
        if not fresh['hard_pass'] or mismatches:errors.append(dict(text=t,type='reanalysis',errors=fresh['hard_errors'],mismatches=mismatches))
        if set(r['grammar_used'])-grammar_ids:errors.append(dict(text=t,type='grammar32'))
        new_ids=set(r['planned_new_vocab_ids'])
        if new_ids!=set(r['actual_new_vocab_ids']):errors.append(dict(text=t,type='planned_new_identity_mismatch'))
        identity_rows=[dict(planned_id=i,lemma=v[i]['lemma'],pos=v[i]['pos'],sense=v[i]['sense'],
            occurrences=[dict(surface=x['surface'],lemma=x['lemma'],pos=x['pos'],sense=x['sense'],vocab_id=x['vocab_id'],
                raw=[r['raw_morphology'][j] for j in x['morph_indices']]) for x in r['annotations'] if x['vocab_id']==i]) for i in sorted(new_ids)]
        results.append(dict(text=t,hard_pass=fresh['hard_pass'],attempt=r['attempt_number'],eojeol=r['eojeol_count'],
            max_sentence_eojeol=r['max_sentence_eojeol'],coverage=r['coverage'],planned_new_ids=sorted(new_ids),
            actual_new_ids=r['actual_new_vocab_ids'],identity_rows=identity_rows,future_count=sum(x['reason']=='future_expansion' for x in r['invalid_usage_ids']),
            invalid_usage=len(r['invalid_usage_ids']),unresolved=len(r['unresolved_tokens']),grammar_violations=len(set(r['grammar_used'])-grammar_ids)))
        known |= new_ids;prior['committed_records'].append(r)
        for e in prior['entries']:
            if e['vocab_id'] in new_ids:e['actual_first_text']=t
    schema=Draft202012Validator(read(PILOT/'candidate.schema.json'));candidate_count=0
    for path in sorted((PILOT/'candidates').glob('*.json')):
        candidate=read(path);candidate_count+=1;check=deepcopy(candidate);expected=check.pop('candidate_digest')
        if digest(check)!=expected:errors.append('Candidate digest mismatch')
        if candidate['ledger_sha_before_evaluation']!=candidate['ledger_sha_after_evaluation']:errors.append('Candidate state mutation')
        errors += [dict(type='schema',file=path.name,error=e.message) for e in schema.iter_errors(candidate)]
    if sorted(p.name for p in (PILOT/'texts').glob('*.json'))!=['K1-001.json','K1-002.json']:errors.append('Unexpected text projection')
    if any(t>2 for e in state['entries'] for t in e['actual_texts']):errors.append('Unexpected exposure beyond 002')
    if sum(e['actual_exposure_count'] for e in state['entries'])!=4:errors.append('Exactly four observed vocab/text exposures expected')
    # Parser-only fixtures do not create exposure credits or pretend prior learning.
    f=deepcopy(g.f);f['_allowed_vocab']=list(v.values());contrasts=[]
    for c in read(ROOT/'tests/fixtures/k1_phase3_2_boundaries.json')['cases']:
        a=analyze(c['text'],f,255,(),(),(),g.kiwi)
        ids={(x['lemma'],x['pos'],x['sense']) for x in a['annotations'] if x['vocab_id']};lemmas={x[0] for x in ids}
        status='REVIEW' if a['unresolved_tokens'] or any(d.get('requires_candidate_review') for d in a['resolver_decisions']) else 'PASS'
        ok=status==c['expected_status'] and all(tuple(row) in ids for row in c.get('required',[])) and not any(tuple(row) in ids for row in c.get('forbidden',[]))
        ok &= all(l in lemmas for l in c.get('required_lemmas',[])) and not any(l in lemmas for l in c.get('forbidden_lemmas',[]))
        ok &= set(c.get('required_grammar',[]))<=set(a['grammar_used'])
        if not ok:errors.append(dict(type='contrast_regression',case=c['id']))
        contrasts.append(dict(id=c['id'],text=c['text'],expected=c['expected_status'],status=status,expectation_met=ok,
            raw=a['raw_morphology'],annotations=a['annotations'],decisions=a['resolver_decisions'],unresolved=a['unresolved_tokens']))
    frozen_examples=[]
    for c in read(ROOT/'tests/fixtures/k1_phase3_2_frozen_regressions.json')['cases']:
        exists=c['text'] in read(ROOT/c['source'])['text_ko'];a=analyze(c['text'],f,255,(),(),(),g.kiwi)
        ok=exists and not a['unresolved_tokens'] and any(x['lemma']==c['lemma'] and x['vocab_id'] for x in a['annotations'])
        if not ok:errors.append(dict(type='frozen_example',source=c['source']))
        frozen_examples.append(dict(**c,exists_in_frozen_source=exists,pass_=ok))
    irregular=[]
    for lemma,text,kind in PROBES:
        e=next(x for x in v.values() if x['lemma']==lemma and x['pos'] in ('verb','adjective'))
        intent=[dict(sentence=text,surface='걸었어요' if kind.endswith('past') else '걸어요',vocab_id=e['id'],lemma=lemma,pos=e['pos'],sense=e['sense'])] if lemma=='걷다' else []
        a=analyze(text,f,255,(),intent,['walk'] if lemma=='걷다' else [],g.kiwi)
        ok=not a['unresolved_tokens'] and e['id'] in {x['vocab_id'] for x in a['annotations']}
        if not ok:errors.append(dict(type='irregular_regression',lemma=lemma,kind=kind))
        irregular.append(dict(lemma=lemma,text=text,kind=kind,pass_=ok))
    if LEDGER.read_bytes()!=before:errors.append('Read-only validator mutated actual state')
    previous_bad=read(ROOT/'pilot/ko/k1/phase3_retry/failed_attempts/K1-002-attempt-01.json')
    grouping=[
        dict(boundary='N + 하고',policy='raw JKB/JC -> g25; missegmented XSV+EC only with explicit food enumeration evidence; otherwise REVIEW'),
        dict(boundary='N + 이랑/랑',policy='not grammar32; REVIEW/reject; not rewritten to 하고'),
        dict(boundary='하다 compound',policy='adjacent NNG/XR + XSV/XSA; full registered lemma + matching verb/adjective POS'),
        dict(boundary='VV + auxiliary',policy='registered exchange/ask prefix with exact surface+raw signature; otherwise grammar09/05/06/18 separately'),
        dict(boundary='registered compound',policy='consecutive raw lexical indices in one eojeol; no EC/punctuation skipping, no productive synonym alias'),
        dict(boundary='bound noun/counter',policy='raw NNB/NNG, registered counter and local numeric evidence; closed grammar constructions explicitly recognized'),
        dict(boundary='quotation',policy='quoted IC response may resolve; frozen expressions exact registered spans; quotation licenses no extra grammar'),
        dict(boundary='punctuation adjacent',policy='punctuation defines context boundaries, never a cross-boundary alias or compound license')]
    audit=dict(alias_count=len(ALIAS_AUDIT),class_counts=dict(Counter(x['classification'] for x in ALIAS_AUDIT)),
        aliases=ALIAS_AUDIT,legacy_default_senses=LEGACY_DEFAULT_SENSE_AUDIT,
        legacy_sense_defaults_used=False,registered_homograph_lemma_count=13,
        additional_pos_bridges=['VV exists/not_exists/necessary -> registered adjective','MM exact 다른 -> adjective + g26','NNG counter after numeric context'],
        unique_entry_fallback='removed; incompatible raw POS yields REVIEW',grouping=grouping,
        contrast_results=contrasts,frozen_examples=frozen_examples,irregular_results=irregular)
    write(REPORTS/'k1_phase3_2_alias_audit.json',audit)
    result=dict(phase='3.2',status='PASS' if not errors else 'FAIL',decision='A' if not errors else 'B',
        errors=errors,smoke=results,committed_count=len(rows),ledger_epoch=state['epoch'],candidate_count=candidate_count,
        candidate_rejections=len(list((PILOT/'failed_attempts').glob('*.json'))),
        previous_failed_002_coverage=previous_bad['coverage'],coverage_recomputed_from_raw=True,
        frozen_files=len(read(ROOT/'reports/k1_phase3_2_input_freeze.json')['files']),frozen_errors=freeze_errors(),
        actual_introduced_ids=sorted(known),actual_exposure_total=sum(e['actual_exposure_count'] for e in state['entries']),
        incidental_exposure_total=sum(e['incidental_exposure_count'] for e in state['entries']),
        outstanding_debt=len(state['review_debt']),expired_debt=len(state['expired_review_debt']),
        state_unchanged_by_validator=True,unresolved_tokens=sum(r['unresolved'] for r in results),
        future_vocab=sum(r['future_count'] or 0 for r in results),invalid_usage=sum(r['invalid_usage'] for r in results),
        grammar_violations=sum(r['grammar_violations'] for r in results),
        naturalness_warnings=sum(len(r['naturalness']['lint_warnings']) for r in rows),
        translation_fidelity_flags=sum(len(r['translation_fidelity_flags']) for r in rows),
        next_001_050_run_possible=not errors,actual_generation_boundary=2,
        limitations=['limited parser, not full sense disambiguation','REVIEW allowed in contrast fixtures but never in committed content','semantic self review is not human approval'])
    test_path=REPORTS/'k1_phase3_2_test_result.json'
    if test_path.exists():result['tests']=read(test_path)
    write(REPORTS/'k1_phase3_2_validation_result.json',result)
    return result,audit

if __name__=='__main__':
    result,_=validate();print(json.dumps({k:result[k] for k in ('status','errors','committed_count','frozen_errors','unresolved_tokens','future_vocab','invalid_usage','grammar_violations')},ensure_ascii=True))
    raise SystemExit(0 if result['status']=='PASS' else 1)
