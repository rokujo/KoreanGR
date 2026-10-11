"""Report-only historical replay. No candidate submissions or history edits."""
import tempfile,json,hashlib
from pathlib import Path
from copy import deepcopy
from k1_phase3 import ROOT,read,write,vocab
from k1_phase3_9a import ProductionGate
from k1_phase3_9a_gate import build_snapshot,permission_issues
from k1_phase3_8_analysis import analyze
from k1_phase3_8_sense import sense_checks,basic_family_usages
from k1_author_contract import check,template
from k1_phase3_9a_planner import author_findings
def audit():
    report=[]
    with tempfile.TemporaryDirectory() as d:
        p=Path(d);gate=ProductionGate(p/'gate',p/'ledger.json');gate.initialize();f=gate.f
        for phase,t in [('3_6',2),('3_6b',7),('3_6c',1),('3_7',5)]:
            cp=ROOT/f'pilot/ko/k1/phase{phase}/candidates/K1-{t:03d}-attempt-01.json'
            if not cp.exists():cp=ROOT/f'pilot/ko/k1/phase{phase}/texts/K1-{t:03d}.json'
            old=read(cp);state=read(ROOT/f'state/phase{phase}_production_exposure_ledger.json')
            snap=build_snapshot(f,state,t);vf=deepcopy(f);v=vocab(f);vf['_allowed_vocab']=[v[e['vocab_id']] for e in snap['entries']]
            source=old.get('source',old)
            a=analyze(old['text_ko'],vf,t,intents=source.get('generated_intents',[]),scene_actions=source.get('scene_fingerprint',{}).get('main_actions',[]),kiwi=gate.kiwi,scope='full_candidate')
            report.append(dict(historical_phase=phase,text=t,source=str(cp.relative_to(ROOT)),lexical_violations=permission_issues(a,snap,vf),restricted_violations=[x for x in sense_checks(old['text_ko'],a) if x['decision']=='FAIL'],basic_family_usages=basic_family_usages(old['text_ko'],a),scope_diagnostic_count=sum(x['disagreement'] for x in a['scope_diagnostics']),canonical_authority=a['lexical_authority']))
        for t in (39,47,48):
            cp=ROOT/f'pilot/ko/k1/phase3_8/texts/K1-{t:03d}.json';old=read(cp)
            report.append(dict(historical_phase='3_8',text=t,source=str(cp.relative_to(ROOT)),observed_author_patterns=author_findings(old['text_ko'],t==47),corpus_unchanged=True))
        bad=ROOT/'pilot/ko/k1/phase3_9/author/K1-013-pairs-selfcheck.json';body={'pairs':read(ROOT/'pilot/ko/k1/phase3_9/author/K1-013-pairs.json'),'title':'historical body'}
        callback=p/'selfcheck.json';callback.write_bytes(bad.read_bytes());before=gate.ledger.read_bytes()
        first=check(callback,body,p/'contract',gate.ledger);callback.write_text(json.dumps(template()),encoding='utf8');second=check(callback,body,p/'contract',gate.ledger)
        report.append(dict(historical_phase='3_9',text=13,first_rejected=not first['accepted'],first_exhausted=first['exhausted'],second_accepted=second['accepted'],contract_retry_count=second['retry_count'],same_body=True,state_unchanged=before==gate.ledger.read_bytes(),formal_attempts=0))
    write(ROOT/'reports/k1_phase3_9a_historical_replay.json',dict(report_only=True,rows=report))
    print(json.dumps([dict(historical_phase=x['historical_phase'],text=x['text'],lexical_violations=x.get('lexical_violations'),observed_author_patterns=x.get('observed_author_patterns'),second_accepted=x.get('second_accepted')) for x in report],ensure_ascii=False))
if __name__=='__main__':audit()
