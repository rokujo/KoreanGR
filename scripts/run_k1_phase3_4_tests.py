"""Phase 3.4 logs only; never overwrite any frozen phase's test results."""
import argparse
import time
import unittest
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--focused',action='store_true');a=p.parse_args()
    label='focused' if a.focused else 'all';pattern='test_k1_phase3_4.py' if a.focused else 'test*.py'
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern=pattern)
    path=ROOT/f'reports/k1_phase3_4_{label}_test_log.txt';start=time.monotonic()
    with path.open('w',encoding='utf-8',newline='\n') as stream:
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    metadata=dict(command='python -B scripts/run_k1_phase3_4_tests.py'+(' --focused' if a.focused else ''),
        tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        seconds=round(time.monotonic()-start,3),status='PASS' if result.wasSuccessful() else 'FAIL',
        log=path.relative_to(ROOT).as_posix(),exit_code=0 if result.wasSuccessful() else 1)
    (ROOT/f'reports/k1_phase3_4_{label}_test_result.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(metadata,ensure_ascii=False));raise SystemExit(metadata['exit_code'])

if __name__=='__main__':main()
