"""Isolated zero-state 001..003 smoke; candidate contract covers 001..050."""
import argparse
from copy import deepcopy
import json
from k1_phase3_4_gate import CandidateGate, StructuralStop, read, write, ROOT
from k1_phase3_retry import stagnant_errors
from k1_phase3 import sha

PILOT=ROOT/'pilot/ko/k1/phase3_4'
LEDGER=ROOT/'state/phase3_4_smoke_exposure_ledger.json'
REPORTS=ROOT/'reports'
FREEZE=REPORTS/'k1_phase3_4_input_freeze.json'

def freeze():
    if FREEZE.exists():return
    old=read(REPORTS/'k1_phase3_sequential_v3_input_freeze.json')
    manifest=read(REPORTS/'k1_phase3_sequential_v3_artifact_manifest.json')
    expected=dict(old['files'],**manifest['files'])
    bad=[p for p,h in expected.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    if bad:raise StructuralStop('Frozen prior history changed: '+str(bad))
    paths=set(expected)|{'reports/k1_phase3_sequential_v3_input_freeze.json',
                        'reports/k1_phase3_sequential_v3_artifact_manifest.json'}
    paths|={'scripts/k1_phase3_4.py','scripts/k1_phase3_4_gate.py','scripts/k1_phase3_4_resolver.py',
            'scripts/build_k1_phase3_4_schemas.py'}
    paths|={p.relative_to(ROOT).as_posix() for p in (ROOT/'config/languages/ko/k1/phase3_4').glob('*.json')}
    write(FREEZE,dict(phase='3.4',files={p:sha(ROOT/p) for p in sorted(paths)}))

def freeze_errors():
    return [p for p,h in read(FREEZE)['files'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]

class SmokeGate(CandidateGate):
    def __init__(self,run_dir=PILOT,ledger_path=LEDGER,**kwargs):
        super().__init__(run_dir,ledger_path,max_text=3,**kwargs)
    def _submit_locked(self,source):
        path,result=super()._submit_locked(source)
        if not result['hard_pass'] and result['attempt_number']>=2:
            previous=read(path.with_name(f"K1-{result['text_number']:03d}-attempt-{result['attempt_number']-1:02d}.json"))
            stagnant=stagnant_errors(previous,result)
            if stagnant:self.reject_run(dict(type='same_hard_error_twice_without_improvement',
                text=result['text_number'],attempt=result['attempt_number'],errors=stagnant))
        return path,result

def source_from_pairs(path):
    source=read(path)
    if 'pairs' in source:
        pairs=source.pop('pairs')
        source['sentences']=[p[0] for p in pairs]
        source['translations_ja']=[p[1] for p in pairs]
    return source

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['init','submit','status']);p.add_argument('--source');a=p.parse_args()
    g=SmokeGate()
    if a.action=='init':freeze();g.initialize()
    if freeze_errors():
        g.reject_run(dict(type='frozen_input_changed',files=freeze_errors()));raise StructuralStop('Freeze mismatch')
    if a.action=='submit':
        source=source_from_pairs(a.source)
        path,result=g.submit(source)
        if result['hard_pass']:result=g.commit(path)
        print(json.dumps(dict(text=result['text_number'],attempt=result['attempt_number'],hard_pass=result['hard_pass'],
            eojeol=result.get('eojeol_count'),coverage=result.get('coverage'),errors=result['hard_errors'],
            invalid=result.get('invalid_usage_ids'),unresolved=result.get('unresolved_tokens'),
            uri_recoveries=[d for d in result.get('uri_recovery_audit',[]) if d['decision']!='ALREADY_REGISTERED'],
            control=read(g.control)),ensure_ascii=False))
    state=g.load()
    print(json.dumps(dict(epoch=state['epoch'],last_committed_text=state['last_committed_text'],
        control=read(g.control),outstanding_debt=len(state['review_debt'])),ensure_ascii=False))

if __name__=='__main__':main()
