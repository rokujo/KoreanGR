"""Phase 3.5 only: sealed zero-state smoke boundary 001..005."""
from k1_phase3_5_gate import CandidateGate, StructuralStop, ROOT, read, write
from k1_phase3_retry import stagnant_errors
from k1_phase3 import sha

PILOT=ROOT/'pilot/ko/k1/phase3_5'
LEDGER=ROOT/'state/phase3_5_smoke_exposure_ledger.json'
FREEZE=ROOT/'reports/k1_phase3_5_input_freeze.json'

def freeze_errors():
    return [p for p,h in read(FREEZE)['files'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]

class SmokeGate(CandidateGate):
    def __init__(self,run_dir=PILOT,ledger_path=LEDGER,**kwargs):
        super().__init__(run_dir,ledger_path,max_text=5,**kwargs)
    def _submit_locked(self,source):
        path,result=super()._submit_locked(source)
        semantic=[e for e in result['hard_errors'] if e['code'].startswith('semantic_grammar_')]
        if semantic:
            self.reject_run(dict(type='semantic_grammar_stop',text=result['text_number'],errors=semantic))
        elif not result['hard_pass'] and result['attempt_number']>=2:
            previous=read(path.with_name(f"K1-{result['text_number']:03d}-attempt-{result['attempt_number']-1:02d}.json"))
            stagnant=stagnant_errors(previous,result)
            if stagnant:self.reject_run(dict(type='same_hard_error_twice_without_improvement',text=result['text_number'],errors=stagnant))
        return path,result
    def run_one(self,text,generator):
        """Honor a semantic STOP before asking an author for another draft.

        The generic bounded retry loop is suitable for ordinary draft errors;
        this phase's semantic STOP is stronger. Never overwrite its reason.
        """
        feedback=None
        for attempt in range(1,self.max_attempts+1):
            if read(self.control)['status']!='running':return None
            try:
                snapshot=self.snapshot(text)
                source=generator(snapshot,feedback,attempt)
                path,result=self.submit(source)
                if result['hard_pass']:return self.commit(path)
            except Exception as exc:
                if read(self.control)['status']=='running':
                    self.reject_run(dict(type='structural_failure',reason=str(exc)))
                raise StructuralStop(str(exc)) from exc
            if read(self.control)['status']!='running':return None
            feedback=result
        return None

def submit(source):
    g=SmokeGate()
    if freeze_errors():raise StructuralStop('Frozen history changed')
    write(PILOT/'sources'/f"K1-{source['text_number']:03d}-attempt-01.json",source)
    path,result=g.submit(source)
    if result['hard_pass']:result=g.commit(path)
    return result
