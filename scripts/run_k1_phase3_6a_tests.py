"""Run once before production and once after 010. Never writes old results."""
from pathlib import Path
import json
import sys
import time
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase3 import ROOT,write

if __name__=='__main__':
    label=sys.argv[1]
    if label not in ('pre','post'):raise ValueError('pre or post required')
    log=ROOT/f'reports/k1_phase3_6a_{label}_regression.log'
    result_file=ROOT/f'reports/k1_phase3_6a_{label}_regression.json'
    if result_file.exists():raise RuntimeError('Preserve test history; do not silently rerun')
    start=time.perf_counter()
    with log.open('w',encoding='utf-8') as stream:
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT/'tests')))
    record=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),seconds=time.perf_counter()-start,success=result.wasSuccessful())
    write(result_file,record);print(json.dumps(record));sys.exit(0 if result.wasSuccessful() else 1)
