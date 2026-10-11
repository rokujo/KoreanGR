"""Separate 001/002 smoke, approved history untouched, raw source replay only."""
import argparse
from copy import deepcopy
import json
from k1_phase3_3_gate import CandidateGate, StructuralStop, read, write, ROOT
from k1_phase3_sequential_v2 import draft_from_pairs
from k1_phase3_retry import stagnant_errors
from k1_phase3 import sha

PILOT=ROOT/'pilot/ko/k1/phase3_3'
LEDGER=ROOT/'state/phase3_3_smoke_exposure_ledger.json'
FREEZE=ROOT/'reports/k1_phase3_3_input_freeze.json'

def freeze():
    if FREEZE.exists(): return
    old=read(ROOT/'reports/k1_phase3_sequential_v2_input_freeze.json')
    manifest=read(ROOT/'reports/k1_phase3_sequential_v2_artifact_manifest.json')
    expected=dict(old['files'],**manifest['files'])
    bad=[p for p,h in expected.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    if bad: raise StructuralStop('Frozen prior history changed: '+str(bad))
    paths=set(expected)|{'reports/k1_phase3_sequential_v2_input_freeze.json','reports/k1_phase3_sequential_v2_artifact_manifest.json'}
    paths |= {'scripts/k1_phase3_3_resolver.py','scripts/k1_phase3_3_gate.py','scripts/k1_phase3_3.py',
              'pilot/ko/k1/phase3_3/source.schema.json','pilot/ko/k1/phase3_3/candidate.schema.json'}
    write(FREEZE,dict(phase='3.3',files={p:sha(ROOT/p) for p in sorted(paths)}))

def freeze_errors():
    return [p for p,h in read(FREEZE)['files'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]

class SmokeGate(CandidateGate):
    def __init__(self,run_dir=PILOT,ledger_path=LEDGER,**kwargs):
        super().__init__(run_dir,ledger_path,max_text=2,**kwargs)
    def _submit_locked(self,source):
        path,result=super()._submit_locked(source)
        if not result['hard_pass'] and result['attempt_number']>=2:
            old=read(path.with_name(f"K1-{result['text_number']:03d}-attempt-{result['attempt_number']-1:02d}.json"))
            stagnant=stagnant_errors(old,result)
            if stagnant: self.reject_run(dict(type='same_hard_error_twice_without_improvement',text=result['text_number'],errors=stagnant))
        return path,result

def replay_source(text,attempt=1):
    origin=ROOT/f'pilot/ko/k1/phase3_sequential_v2/sources/K1-{text:03d}-attempt-{2 if text==1 else 1:02d}.json'
    source=draft_from_pairs(origin)
    source['notes']='Phase 3.3 raw-source regression smoke; no prior analysis, coverage, state or exposure credit imported.'
    if text==2 and attempt==2:
        source['title_ko']='동생에게 책을 줘요'
        source['sentences'][6]='저는 가게 문을 열어요.'
        source['translations_ja'][6]='私は店のドアを開けます。'
    return origin,source

def smoke():
    freeze()
    if freeze_errors(): raise StructuralStop('Frozen history/engine mismatch')
    g=SmokeGate();g.initialize();provenance=[]
    for text in (1,2):
        for attempt in range(1,6):
            if read(g.control)['status']!='running': return dict(status='FAIL',control=read(g.control))
            origin,source=replay_source(text,attempt)
            write(PILOT/'sources'/f'K1-{text:03d}-attempt-{attempt:02d}.json',source)
            before=sha(LEDGER);path,result=g.submit(source)
            if sha(LEDGER)!=before: raise StructuralStop('Rejected/evaluated candidate changed actual state')
            provenance.append(dict(text=text,attempt=attempt,raw_source=origin.relative_to(ROOT).as_posix(),source_sha=sha(origin),
                ledger_sha_before_evaluation=before,ledger_sha_after_evaluation=sha(LEDGER),
                candidate_path=path.relative_to(ROOT).as_posix(),hard_pass=result['hard_pass']))
            write(PILOT/'smoke_provenance.json',provenance)
            if result['hard_pass']:
                final=g.commit(path)
                print(json.dumps(dict(text=text,attempt=attempt,committed=True,eojeol=final['eojeol_count'],coverage=final['coverage'],
                                      planned=final['planned_new_vocab_ids'],actual=final['actual_new_vocab_ids']),ensure_ascii=False))
                break
            if text==2 and attempt==1:
                # Identity repair must work even while unrelated draft problems
                # remain hard failures. Do not weaken future/title gates.
                if result['planned_new_vocab_ids']!=result['actual_new_vocab_ids'] or any(
                    a['lemma'] in ('요','국어') for a in result['unresolved_tokens']):
                    g.reject_run(dict(type='quote_recovery_structural_failure',text=text,errors=result['hard_errors']))
                    return dict(status='FAIL',errors=result['hard_errors'])
                print(json.dumps(dict(text=text,attempt=attempt,rejected=True,errors=result['hard_errors'],state_unchanged=True),ensure_ascii=False))
                continue
            g.reject_run(dict(type='unexpected_smoke_failure',text=text,errors=result['hard_errors']))
            return dict(status='FAIL',errors=result['hard_errors'])
    return dict(status='PASS',committed=g.load()['last_committed_text'],generation_beyond_002=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['smoke','freeze']);a=p.parse_args()
    result=smoke() if a.action=='smoke' else dict(errors=freeze_errors())
    print(json.dumps(result,ensure_ascii=False))
    if result.get('status')=='FAIL' or result.get('errors'): raise SystemExit(1)

if __name__=='__main__':main()
