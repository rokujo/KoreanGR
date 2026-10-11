import sys,unittest,tempfile,json,inspect,hashlib
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_author_contract import schema,template,errors,check
from k1_phase3 import ROOT,read
from k1_phase3_9a_planner import author_findings,health,proposals
from k1_phase3_9_planner import health as old_health,proposals as old_proposals
from k1_phase3_9_gate import CandidateGate as OldGate
from k1_phase3_9a_gate import CandidateGate as NewGate

class ContractTests(unittest.TestCase):
    def test_existing_keys_migrated_not_invented(self):
        import ast
        nodes=ast.walk(ast.parse((ROOT/'scripts/k1_phase3_9.py').read_text(encoding='utf8')))
        old=next(ast.literal_eval(n.value) for n in nodes if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='required' for t in n.targets))
        self.assertEqual(list(old),schema()['required']);self.assertFalse(errors(json.dumps(template()))[1])
    def test_negative_contracts(self):
        s=template();key=schema()['required'][0]
        variants=[]
        x=deepcopy(s);x.pop(key);variants.append(x)
        x=deepcopy(s);x[key+'x']=x.pop(key);variants.append(x)
        x=deepcopy(s);x['forbidden_extra']='yes';variants.append(x)
        x=deepcopy(s);x[key]='true';variants.append(x)
        x=deepcopy(s);x[key]=False;variants.append(x) # wrong allowed constant; no new enum invented
        x=deepcopy(s);x[key]='PASS';variants.append(x)
        for x in variants:self.assertTrue(errors(json.dumps(x))[1])
        self.assertTrue(errors('{')[1])
        self.assertTrue(errors('[]')[1])
    def test_historical_wrong_keys_recover_same_body(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);ledger=p/'ledger.json';ledger.write_text('{"epoch":0,"credit":0}',encoding='utf8')
            body={'pairs':read(ROOT/'pilot/ko/k1/phase3_9/author/K1-013-pairs.json'),'title':'family meal'}
            callback=p/'self.json';callback.write_text((ROOT/'pilot/ko/k1/phase3_9/author/K1-013-pairs-selfcheck.json').read_text(encoding='utf8'),encoding='utf8')
            before=ledger.read_bytes();a=check(callback,body,p/'journal',ledger)
            self.assertFalse(a['accepted']);self.assertFalse(a['exhausted']);self.assertEqual(1,a['retry_count']);self.assertEqual(before,ledger.read_bytes())
            callback.write_text(json.dumps(template()),encoding='utf8');b=check(callback,body,p/'journal',ledger)
            self.assertTrue(b['accepted']);self.assertEqual(1,b['retry_count']);self.assertEqual(before,ledger.read_bytes())
    def test_max_three_failures(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);ledger=p/'ledger';ledger.write_text('actual state',encoding='utf8');callback=p/'bad';callback.write_text('{',encoding='utf8')
            for n in (1,2,3):
                x=check(callback,{'body':'unchanged'},p/'history',ledger)
                self.assertEqual(n,x['retry_count']);self.assertEqual(n==3,x['exhausted']);self.assertEqual('actual state',ledger.read_text())
    def test_body_translation_title_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);ledger=p/'ledger';ledger.write_text('state');callback=p/'bad';callback.write_text('{}')
            body={'ko':'a','ja':'b','title':'c'};check(callback,body,p/'history',ledger)
            callback.write_text(json.dumps(template()))
            for key in body:
                changed=dict(body);changed[key]='different';r=check(callback,changed,p/'history',ledger)
                self.assertFalse(r['accepted']);self.assertEqual('same_body_required',r['errors'][0]['code']);self.assertEqual(1,r['retry_count'])
            self.assertTrue(check(callback,body,p/'history',ledger)['accepted'])
    def test_controller_recovers_without_candidate_or_credit(self):
        import k1_phase3_9a as controller
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);run=p/'run';ledger=p/'ledger.json';timing=p/'timing.json'
            gate=controller.ProductionGate(run,ledger);gate.initialize();before=ledger.read_bytes();control=gate.control.read_bytes()
            pairs=p/'draft.json';pairs.write_text(json.dumps([['한국어를 읽어요.','read Korean']]),encoding='utf8')
            selfcheck=p/'draft-selfcheck.json';selfcheck.write_text('{}',encoding='utf8')
            timing.write_text(json.dumps({'texts':[{'text_number':1,'phase':'author_draft','phase_start_counter':controller.now(),'stages':{},'attempts':[],'plan':{'title_ko':'한국어','scene_fingerprint':{'main_actions':['read']}}}]}),encoding='utf8')
            with patch.object(controller,'guard',lambda:None),patch.object(controller,'PILOT',run),patch.object(controller,'TIMING',timing),patch.object(controller,'ProductionGate',lambda:gate):
                controller.preflight(pairs)
                self.assertEqual(before,ledger.read_bytes());self.assertEqual(control,gate.control.read_bytes());self.assertFalse(list((run/'candidates').glob('*')))
                selfcheck.write_text(json.dumps(template()),encoding='utf8');controller.preflight(pairs)
                r=read(timing)['texts'][-1];self.assertTrue(r['author_contract_accepted']);self.assertEqual(1,r['author_contract_retry_count']);self.assertEqual([],r['attempts']);self.assertEqual(before,ledger.read_bytes());self.assertEqual(control,gate.control.read_bytes())
    def test_unchanged_mechanical_and_planning(self):
        self.assertEqual(inspect.getsource(OldGate.evaluate),inspect.getsource(NewGate.evaluate));self.assertEqual(inspect.getsource(OldGate._commit_locked),inspect.getsource(NewGate._commit_locked))
        self.assertIs(health,old_health);self.assertIs(proposals,old_proposals)
    def test_observed_gaps_author_only(self):
        self.assertTrue(author_findings('밖에는 비하고 바람이 있어요.'));self.assertFalse(author_findings('밖에는 비가 많이 와요.'))
        self.assertTrue(author_findings('언니는 종이에 말을 써요.'));self.assertFalse(author_findings('언니가 종이에 써요.'))
        self.assertTrue(author_findings('책을 열어요.'));self.assertFalse(author_findings('책을 읽어요.'))

if __name__=='__main__':unittest.main()
