"""Isolated 001/002 raw-source smoke; never imports old exposure credit."""
import argparse
from copy import deepcopy
from pathlib import Path
from k1_phase3_2_gate import CandidateGate, StructuralStop, read, write, ROOT
from k1_phase3_retry import draft_from_pairs, stagnant_errors
from k1_phase3 import sha

PILOT=ROOT/'pilot/ko/k1/phase3_2'
LEDGER=ROOT/'state/phase3_2_smoke_exposure_ledger.json'
FREEZE=ROOT/'reports/k1_phase3_2_input_freeze.json'

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
            if stagnant:self.reject_run(dict(type='same_hard_error_twice_without_improvement',text=result['text_number'],errors=stagnant))
        return path,result

def smoke():
    if freeze_errors():raise StructuralStop('Frozen historical artifacts changed')
    g=SmokeGate();g.initialize()
    provenance=[]
    for t in (1,2):
        origin=ROOT/f'pilot/ko/k1/phase3_retry/sources/K1-{t:03d}-attempt-01.json'
        source=draft_from_pairs(origin)
        source['notes']='Phase 3.2 raw-source reanalysis in a new actual state; no prior annotation, coverage or ledger imported.'
        write(PILOT/'sources'/f'K1-{t:03d}.json',source)
        before=sha(LEDGER)
        path,result=g.submit(deepcopy(source))
        if sha(LEDGER)!=before:raise StructuralStop('Candidate mutated state')
        provenance.append(dict(text=t,raw_source=origin.relative_to(ROOT).as_posix(),source_sha=sha(origin),
            prior_state_checksum=result['state_checksum_before'],candidate_path=path.relative_to(ROOT).as_posix(),
            result=result['hard_pass'],ledger_sha_before_candidate=before,ledger_sha_after_candidate=sha(LEDGER)))
        write(PILOT/'smoke_provenance.json',provenance)
        if not result['hard_pass']:
            # These are fixed analyzer regression sources with already audited
            # length/grammar. Unexpected unresolved/identity failure is structural,
            # not justification for erasing the contrast by paraphrasing.
            g.reject_run(dict(type='unexpected_smoke_analysis_failure',text=t,errors=result['hard_errors']))
            return dict(status='FAIL',text=t,errors=result['hard_errors'])
        final=g.commit(path)
        print(__import__('json').dumps(dict(text=t,attempt=result['attempt_number'],hard_pass=True,
            eojeol=final['eojeol_count'],coverage=final['coverage'],actual_new=final['actual_new_vocab_ids']),ensure_ascii=True))
    return dict(status='PASS',committed=g.load()['last_committed_text'],future_generation_permitted=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['smoke','freeze']);a=p.parse_args()
    if a.action=='freeze':
        errors=freeze_errors();print(errors);raise SystemExit(1 if errors else 0)
    else:
        result=smoke();print(result);raise SystemExit(0 if result['status']=='PASS' else 1)

if __name__=='__main__':main()
