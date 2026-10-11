"""Full test evidence in new files; do not overwrite frozen failure reports."""
import io,time,unittest
from k1_phase3 import ROOT,REPORTS,write

if __name__=='__main__':
    stream=io.StringIO();start=time.monotonic()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT/'tests')))
    (REPORTS/'k1_phase3_1_test_log.txt').write_text(stream.getvalue(),encoding='utf-8')
    write(REPORTS/'k1_phase3_1_test_result.json',dict(command='python -B scripts/run_k1_phase3_1_tests.py',tests_run=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),ok=result.wasSuccessful(),seconds=round(time.monotonic()-start,3),
        initial_candidate_tests=dict(tests=30,failures=1,errors=15,
            cause='Duplicate grammar_used output keyword and VV-I prefix handling bug in new code; fixed implementation, no rule relaxation.',
            corrected_before_smoke=dict(tests=30,failures=0,errors=0,seconds=44.199)),log='reports/k1_phase3_1_test_log.txt'))
    print(f'Tests {result.testsRun}; failures {len(result.failures)}; errors {len(result.errors)}')
    raise SystemExit(0 if result.wasSuccessful() else 1)
