"""Report-only historical replay; no old files/state/credit are changed."""
from pathlib import Path
from copy import deepcopy
import tempfile,json
from k1_phase3 import ROOT,read,write
from k1_phase3_8 import ProductionGate
from k1_phase3_8_gate import seal,build_snapshot
from k1_phase2_3 import make_kiwi

def run():
    k=make_kiwi();rows=[]
    for phase,n in [('3_6',2),('3_6b',7),('3_6c',1),('3_7',5)]:
        paths=sorted((ROOT/f'pilot/ko/k1/phase{phase}/candidates').glob(f'K1-{n:03d}-attempt-*.json'))
        old=read(paths[-1]);previous=read(ROOT/f'state/phase{phase}_production_exposure_ledger.json')
        with tempfile.TemporaryDirectory() as d:
            g=ProductionGate(Path(d)/'r',Path(d)/'s',kiwi=k);g.initialize()
            # Hypothetical historical state, only in memory, explicitly not
            # this run's actual introductions or permission credit.
            state=deepcopy(previous);state['committed_records']=state['committed_records'][:n-1]
            state['input_digest']=g.load()['input_digest'];state=seal(state)
            snap=build_snapshot(g.f,state,n)
            result=g.evaluate(old['source'],state,snap)
            rows.append(dict(historical_phase=phase,text=n,source=str(paths[-1].relative_to(ROOT)),hard_pass=result['hard_pass'],hard_errors=result['hard_errors'],coverage=result['coverage'],canonical_lexical_map=result['canonical_lexical_map'],scope_disagreements=[x for x in result['scope_diagnostics'] if x['disagreement']],credit=False))
    write(ROOT/'reports/k1_phase3_8_regression_replay.json',dict(rows=rows,report_only=True))
    print(json.dumps([dict(phase=r['historical_phase'],passed=r['hard_pass'],errors=r['hard_errors'],disagreements=len(r['scope_disagreements'])) for r in rows],ensure_ascii=False))

if __name__=='__main__':run()
