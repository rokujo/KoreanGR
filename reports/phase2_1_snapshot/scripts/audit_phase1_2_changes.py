"""Validate Phase 1.2, check immutable history, and save complete reviewable diffs."""
from collections import Counter
import difflib
import json
from pathlib import Path
import sys
import argparse
import re
import subprocess
from audit_phase1_1_changes import sha,json_diff
from validate_k1_vocab import validate
ROOT=Path(__file__).resolve().parents[1]
SNAPSHOT=ROOT/'reports/phase1_1_snapshot'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-tests',action='store_true')
    args=parser.parse_args()
    history={}
    for folder in ('phase1_snapshot','phase1_1_snapshot'):
        snapshot=ROOT/'reports'/folder
        manifest=json.loads((snapshot/'manifest.json').read_text(encoding='utf-8'))['files']
        for relative,expected in manifest.items():
            if sha(snapshot/relative)!=expected:raise RuntimeError(f'History changed: {folder}/{relative}')
        history[folder]=dict(status='PASS',files=len(manifest))
    result=validate(ROOT/'config/languages/ko/k1')
    if not result['ok']:
        print(json.dumps(result,ensure_ascii=False,indent=2));return 1
    result['history_integrity']=history
    if args.run_tests:
        completed=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        log=completed.stdout+completed.stderr
        print(log)
        result['tests']=dict(status='PASS' if completed.returncode==0 else 'FAIL',exit_code=completed.returncode,
                             test_methods=int(re.search(r'Ran (\d+) tests',log).group(1)),output=log)
        if completed.returncode:raise RuntimeError('Phase 1.2 regression tests failed')
    (ROOT/'reports/k1_vocab_validation_result_phase1_2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    paths=set(json.loads((SNAPSHOT/'manifest.json').read_text(encoding='utf-8'))['files'])
    for folder in ('config','scripts','tests'):
        paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/folder).rglob('*') if p.suffix in ('.json','.py') and '__pycache__' not in p.parts)
    paths.update(['README.md','reports/k1_vocab_design_report_phase1_2.md','reports/k1_vocab_validation_result_phase1_2.json'])
    records=[];patch=[]
    for relative in sorted(paths):
        before=SNAPSHOT/relative;after=ROOT/relative
        if not after.is_file():raise RuntimeError(f'Missing current file: {relative}')
        previous=before.read_text(encoding='utf-8') if before.is_file() else ''
        current=after.read_text(encoding='utf-8')
        change='unchanged' if before.is_file() and before.read_bytes()==after.read_bytes() else 'changed' if before.is_file() else 'added'
        record=dict(file=relative,change=change,before_sha256=sha(before) if before.is_file() else None,after_sha256=sha(after))
        if after.suffix=='.json' and change!='unchanged':
            record['json_changes']=json_diff(json.loads(previous),json.loads(current)) if before.is_file() else [dict(path='',change='added',after=json.loads(current))]
        records.append(record)
        if change!='unchanged':
            patch.extend(difflib.unified_diff(previous.splitlines(keepends=True),current.splitlines(keepends=True),
                fromfile='phase1_1/'+relative if before.is_file() else '/dev/null',tofile='phase1_2/'+relative))
    report=dict(from_phase='1.1',to_phase='1.2',history_integrity=history,
        coverage='All Phase 1.1 manifest files plus current config/scripts/tests, README and Phase 1.2 report/result; generated diff artifacts exclude themselves.',
        summary=dict(Counter(r['change'] for r in records)),files=records)
    (ROOT/'reports/k1_vocab_changes_phase1_2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'reports/k1_vocab_changes_phase1_2.patch').write_text(''.join(patch),encoding='utf-8')
    print('History integrity: PASS (Phase 1 and Phase 1.1)')
    print(f"Validator: PASS; errors=0; warnings={len(result['warnings'])}; concentration warnings={result['summary']['exposure_plan']['concentration_warning_count']}")
    print('File changes: '+json.dumps(report['summary']))
    return 0

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');raise SystemExit(main())
