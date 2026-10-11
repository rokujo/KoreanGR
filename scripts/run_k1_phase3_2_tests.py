"""Explicit runner stream avoids PowerShell native stderr/redirection status."""
import argparse
import time
import unittest
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--focused',action='store_true');args=parser.parse_args()
    pattern='test_k1_phase3_2.py' if args.focused else 'test*.py'
    name='focused' if args.focused else 'all'
    path=ROOT/f'reports/k1_phase3_2_{name}_test_log.txt'
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern=pattern)
    start=time.monotonic()
    with path.open('w',encoding='utf-8',newline='\n') as stream:
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    metadata=dict(command='python -B scripts/run_k1_phase3_2_tests.py'+(' --focused' if args.focused else ''),
        tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        seconds=round(time.monotonic()-start,3),status='PASS' if result.wasSuccessful() else 'FAIL',
        log=path.relative_to(ROOT).as_posix(),exit_code=0 if result.wasSuccessful() else 1)
    destination=ROOT/f'reports/k1_phase3_2_{name}_test_result.json'
    destination.write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not args.focused:(ROOT/'reports/k1_phase3_2_test_result.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(metadata,ensure_ascii=True))
    raise SystemExit(metadata['exit_code'])

if __name__=='__main__':main()
