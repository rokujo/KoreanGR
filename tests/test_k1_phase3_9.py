import sys, unittest, inspect
from pathlib import Path
from copy import deepcopy
from jsonschema import Draft202012Validator
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase3 import ROOT,files,read
from k1_phase3_9_planner import author_findings,health,debt_candidates,proposals,contract,GAPS
from k1_phase3_8_gate import CandidateGate as OldGate
from k1_phase3_9_gate import CandidateGate as NewGate

class PresentationOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.f=files()
    def test_mechanical_evaluate_unchanged(self):
        self.assertEqual(inspect.getsource(OldGate.evaluate),inspect.getsource(NewGate.evaluate))
        self.assertEqual(inspect.getsource(OldGate._commit_locked),inspect.getsource(NewGate._commit_locked))
    def test_full_100_schema_contract(self):
        source=read(ROOT/'pilot/ko/k1/phase3_8/texts/K1-001.json')['source']
        for name in ('source.schema.json','candidate.schema.json'):
            schema=read(ROOT/'config/languages/ko/k1/phase3_9'/name)
            original=read(ROOT/'config/languages/ko/k1/phase3_4'/name)
            # Run range only; metadata and hard output contracts remain equal.
            restored=deepcopy(schema);restored['properties']['text_number']['maximum']=50
            if name.startswith('candidate'):restored['properties']['id']['allOf'][1]['enum']=original['properties']['id']['allOf'][1]['enum']
            self.assertEqual(original,restored)
            candidate=read(ROOT/'pilot/ko/k1/phase3_8/candidates/K1-001-attempt-01.json')
            base=source if name.startswith('source') else candidate
            for n in range(1,101):
                x=deepcopy(base);x['text_number']=n
                if not name.startswith('source'):x['id']=f'K1-{n:03d}'
                self.assertFalse(list(Draft202012Validator(schema).iter_errors(x)),n)
            for n in (0,101,300):
                x=deepcopy(base);x['text_number']=n
                self.assertTrue(list(Draft202012Validator(schema).iter_errors(x)))
    def test_known_bad_patterns_not_hard_rules(self):
        self.assertTrue(author_findings('책을 열어요.'))
        self.assertFalse(author_findings('책을 읽어요.'))
        self.assertTrue(author_findings('자전거를 닫아요.'))
        self.assertTrue(author_findings('가방을 만들어요.',True))
        self.assertFalse(author_findings('가방을 만들어요.',False))
        self.assertIn('omit',GAPS['입히다']['strategy']);self.assertIn('omit',GAPS['지우다']['strategy'])
    def test_capped_progress_does_not_count_surplus(self):
        state={'entries':[{'actual_exposure_count':32},{'actual_exposure_count':2}], 'review_debt':[], 'expired_review_debt':[]}
        self.assertEqual(8,health(state,50)['capped_exposure_progress'])
        self.assertEqual(2992/250,health(state,50)['required_future_credit_rate'])
    def test_proposals_are_pure_and_never_include_future(self):
        state=read(ROOT/'pilot/ko/k1/phase3_8/initial_state.json')
        from k1_phase3_8_gate import build_snapshot
        snapshot=build_snapshot(self.f,state,1);before=deepcopy(state)
        p=proposals(self.f,state,snapshot)
        self.assertEqual(before,state);self.assertLessEqual(len(p['scene_candidates']),3)
        self.assertFalse(p['debt_pool']);self.assertFalse(p['selection_is_exposure'])
        c=contract(self.f,snapshot)
        allowed={x['vocab_id'] for x in snapshot['entries']}
        self.assertFalse(allowed & {x['id'] for x in c['FORBIDDEN_FUTURE']})
    def test_debt_bundles_respect_actual_introduction(self):
        state=read(ROOT/'state/phase3_8_production_exposure_ledger.json')
        before=deepcopy(state['entries']);pool=debt_candidates(self.f,state,51)
        actual={e['vocab_id'] for e in state['entries'] if e['actual_first_text'] is not None}
        self.assertTrue(all(e['vocab_id'] in actual for e in pool))
        self.assertEqual(before,state['entries'])
        self.assertTrue(any(x['expired'] for x in pool))

if __name__=='__main__':unittest.main()
