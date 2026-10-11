"""Verify preserved Phase 1/1.1 history without overwriting historical reports.

JSON paths use RFC 6901 pointers. Patch includes every tracked file modification/addition.
The generated change JSON/patch exclude themselves to avoid circular content hashes.
"""
import hashlib
import json
from pathlib import Path
import sys


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
    # Historical reports must never be replaced by results for the current phase.
    return audit_history()

def audit_history():
    import subprocess
    for phase,folder in [('1','phase1_snapshot'),('1.1','phase1_1_snapshot')]:
        snapshot=ROOT/'reports'/folder
        manifest=json.loads((snapshot/'manifest.json').read_text(encoding='utf-8'))['files']
        for relative,expected in manifest.items():
            if sha(snapshot/relative)!=expected:
                raise RuntimeError(f'Phase {phase} history was changed: {relative}')
        completed=subprocess.run([sys.executable,'-B',str(snapshot/'scripts/validate_k1_vocab.py'),
                                  '--data-dir',str(snapshot/'config/languages/ko/k1'),'--json'],
                                 capture_output=True,text=True,encoding='utf-8',check=True)
        result=json.loads(completed.stdout)
        if not result['ok']:raise RuntimeError(f'Archived Phase {phase} validation failed')
        print(f'Phase {phase}: snapshot integrity PASS ({len(manifest)} files); archived validator PASS')
    print('Historical reports/results preserved; use audit_phase1_2_changes.py for current data.')
    return 0

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
