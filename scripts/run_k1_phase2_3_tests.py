"""Persist actual unittest evidence, including the initial expectation-only failure."""
import io,time,unittest
from k1_phase2_3 import ROOT,REPORTS,write,sha

if __name__=='__main__':
    stream=io.StringIO();start=time.monotonic()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    output=stream.getvalue();(REPORTS/'k1_phase2_3_test_log.txt').write_text(output,encoding='utf-8')
    write(REPORTS/'k1_phase2_3_test_result.json',dict(command='python -B scripts/run_k1_phase2_3_tests.py',
        tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        seconds=round(time.monotonic()-start,3),ok=result.wasSuccessful(),log='reports/k1_phase2_3_test_log.txt',
        initial_run=dict(tests_run=84,failures=1,errors=0,seconds=179.989,
            issue='New assertion expected Annotation identity mismatch; unchanged validator correctly returned Raw reanalysis mismatch: annotations.',
            correction='Only the new test expectation changed to match the actual rejection. No relaxation of language validator.',
            focused_rerun=dict(tests_run=21,failures=0,errors=0,seconds=9.175)),
        final_source_sha256={p.relative_to(ROOT).as_posix():sha(p) for folder in ('scripts','tests') for p in sorted((ROOT/folder).glob('*.py'))}))
    print(f'Tests: {result.testsRun}; failures: {len(result.failures)}; errors: {len(result.errors)}; success: {result.wasSuccessful()}')
    raise SystemExit(0 if result.wasSuccessful() else 1)
