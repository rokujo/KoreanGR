"""Check the preserved Phase 1 history and write complete Phase 1.1 diffs/results.

JSON paths use RFC 6901 pointers. Patch includes every tracked file modification/addition.
The generated change JSON/patch exclude themselves to avoid circular content hashes.
"""
from collections import Counter
import difflib
import hashlib
import json
from pathlib import Path
import sys

from validate_k1_vocab import validate

ROOT=Path(__file__).resolve().parents[1]
SNAPSHOT=ROOT/'reports/phase1_snapshot'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pointer(part):
    return str(part).replace('~','~0').replace('/','~1')

def json_diff(before,after,path=''):
    result=[]
    if isinstance(before,dict) and isinstance(after,dict):
        for key in sorted(before.keys() | after.keys()):
            child=path+'/'+pointer(key)
            if key not in before:result.append(dict(path=child,change='added',after=after[key]))
            elif key not in after:result.append(dict(path=child,change='removed',before=before[key]))
            else:result.extend(json_diff(before[key],after[key],child))
    elif isinstance(before,list) and isinstance(after,list):
        for index in range(max(len(before),len(after))):
            child=path+'/'+str(index)
            if index>=len(before):result.append(dict(path=child,change='added',after=after[index]))
            elif index>=len(after):result.append(dict(path=child,change='removed',before=before[index]))
            else:result.extend(json_diff(before[index],after[index],child))
    elif type(before) is not type(after) or before!=after:
        result.append(dict(path=path,change='changed',before=before,after=after))
    return result

def main():
    manifest=json.loads((SNAPSHOT/'manifest.json').read_text(encoding='utf-8'))['files']
    for relative,expected in manifest.items():
        if sha(SNAPSHOT/relative)!=expected:
            raise RuntimeError(f'Phase 1 history was changed: {relative}')
    result=validate(ROOT/'config/languages/ko/k1')
    if not result['ok']:
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 1
    (ROOT/'reports/k1_vocab_validation_result_phase1_1.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    paths=set(manifest)
    for folder,extension in [('config','.json'),('scripts','.py'),('tests','.py')]:
        paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/folder).rglob('*')
                     if p.is_file() and p.suffix==extension and '__pycache__' not in p.parts)
    paths.update(['reports/k1_vocab_design_report_phase1_1.md','reports/k1_vocab_validation_result_phase1_1.json'])
    files=[];patch=[]
    for relative in sorted(paths):
        old=SNAPSHOT/relative;new=ROOT/relative
        old_exists=old.exists();new_exists=new.exists()
        if not new_exists:raise RuntimeError(f'Expected Phase 1.1 file missing: {relative}')
        old_text=old.read_text(encoding='utf-8') if old_exists else ''
        new_text=new.read_text(encoding='utf-8')
        change='unchanged' if old_exists and old.read_bytes()==new.read_bytes() else 'changed' if old_exists else 'added'
        record=dict(file=relative,change=change,
                    before_sha256=sha(old) if old_exists else None,after_sha256=sha(new))
        if new.suffix=='.json' and change!='unchanged':
            record['json_changes']=json_diff(json.loads(old_text),json.loads(new_text)) if old_exists else [dict(path='',change='added',after=json.loads(new_text))]
        files.append(record)
        if change!='unchanged':
            patch.extend(difflib.unified_diff(old_text.splitlines(keepends=True),new_text.splitlines(keepends=True),
                         fromfile='phase1/'+relative if old_exists else '/dev/null',tofile='phase1_1/'+relative))
    report=dict(from_phase='1',to_phase='1.1',snapshot_integrity='PASS',
                coverage='All original 17 files plus current config JSON, scripts, tests, and Phase 1.1 report/result. Generated diff artifacts exclude themselves.',
                summary=dict(Counter(f['change'] for f in files)),files=files)
    (ROOT/'reports/k1_vocab_changes_phase1_1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'reports/k1_vocab_changes_phase1_1.patch').write_text(''.join(patch),encoding='utf-8')
    print('Snapshot integrity: PASS (17 files)')
    print('Validator: PASS; errors=0; warnings='+str(len(result['warnings'])))
    print('File changes: '+json.dumps(report['summary']))
    return 0

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
