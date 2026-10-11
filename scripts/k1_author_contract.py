"""Schema-only author retry. Journals are not actual learner state."""
import hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
from k1_phase3_9_gate import ROOT, atomic_write, digest
SCHEMA=ROOT/'config/languages/ko/k1/author_selfcheck.schema.json'
def schema():return json.loads(SCHEMA.read_text(encoding='utf8'))
def template(notes=''):
    s=schema()
    return {**{k:s['properties'][k]['const'] for k in s['required']},'notes':notes}
def errors(raw):
    try:value=json.loads(raw)
    except (json.JSONDecodeError,TypeError) as exc:return None,[{'code':'malformed_json','message':str(exc)}]
    return value,[{'code':e.validator,'path':list(e.absolute_path),'message':e.message} for e in Draft202012Validator(schema()).iter_errors(value)]
def check(path,body,journal_dir,ledger_path):
    """Up to three failed schema submissions. Never writes ledger or run state.

    body includes the complete Korean/translation/title, not just its length.
    Restore the bound body during a contract retry; prose repair is a separate
    later step. Initial success has retry_count=0, one recovered failure=1.
    """
    path=Path(path);folder=Path(journal_dir);folder.mkdir(parents=True,exist_ok=True)
    history_path=folder/'history.json'
    history=json.loads(history_path.read_text(encoding='utf8')) if history_path.exists() else {'failures':0,'body_digest':digest(body),'events':[]}
    before=hashlib.sha256(Path(ledger_path).read_bytes()).hexdigest()
    if history.get('accepted'):raise RuntimeError('Author contract already accepted')
    if history['failures']>=3:return {'accepted':False,'exhausted':True,'retry_count':history['failures'],'errors':[{'code':'AUTHOR_CONTRACT_STRUCTURAL_FAIL'}]}
    if digest(body)!=history['body_digest']:
        return {'accepted':False,'exhausted':False,'retry_count':history['failures'],'errors':[{'code':'same_body_required','message':'Restore Korean, translation and title; repair only self-check JSON.'}]}
    try:raw=path.read_text(encoding='utf8')
    except FileNotFoundError:raw=''
    value,issues=errors(raw)
    if issues:history['failures']+=1
    else:history['accepted']=True
    after=hashlib.sha256(Path(ledger_path).read_bytes()).hexdigest()
    if before!=after:raise RuntimeError('Author contract changed actual state')
    event={'validation_number':len(history['events'])+1,'accepted':not issues,'errors':issues,'raw_selfcheck':raw,'body_digest':history['body_digest'],'ledger_sha_before':before,'ledger_sha_after':after,'state_unchanged':True}
    history['events'].append(event)
    atomic_write(folder/f"validation-{event['validation_number']:02d}.json",event)
    atomic_write(history_path,history)
    return {'accepted':not issues,'exhausted':bool(issues and history['failures']>=3),'retry_count':history['failures'],'errors':issues,'value':value,'state_unchanged':True,'instruction':'Keep Korean, Japanese translation and title unchanged. Re-output only self-check JSON using the supplied schema/template.' if issues else None,'schema_path':str(SCHEMA),'template':template()}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('path');p.add_argument('--notes',default='');a=p.parse_args()
    atomic_write(Path(a.path),template(a.notes))
