"""New adapter safety tests; fixture runs never touch production ledgers."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import tempfile
import unittest
from unittest.mock import patch
from copy import deepcopy
from jsonschema import Draft202012Validator
from k1_phase3_sequential_v3 import SequentialGate, PILOT, similarity
from k1_phase3_sequential_v3_gate import read, ROOT, StructuralStop
from k1_phase2_3 import make_kiwi

class NewRunSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.kiwi=make_kiwi()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name)
        self.g=SequentialGate(p/'run',p/'ledger.json',kiwi=self.kiwi)
        self.g.initialize();self.initial=self.g.ledger.read_bytes()
        self.source=read(ROOT/'pilot/ko/k1/phase3_2/sources/K1-001.json')
    def tearDown(self): self.tmp.cleanup()
    def test_empty_actual_history_and_bounds(self):
        s=self.g.load();self.assertEqual(s['epoch'],0)
        self.assertFalse(any(e['actual_texts'] for e in s['entries']))
        self.assertEqual((self.g.max_text,self.g.max_attempts),(50,5))
    def test_stagnant_twice_preserves_entire_state(self):
        fail=dict(text_number=1,hard_pass=False,hard_errors=[dict(code='length',detail=119)])
        with patch.object(self.g,'evaluate',return_value=fail):
            self.g.submit(self.source);self.g.submit(self.source)
        self.assertEqual(read(self.g.control)['stop']['type'],'same_hard_error_twice_without_improvement')
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_progress_allows_up_to_five_then_stops(self):
        for n in range(115,120):
            with patch.object(self.g,'evaluate',return_value=dict(text_number=1,hard_pass=False,hard_errors=[dict(code='length',detail=n)])):
                self.g.submit(self.source)
        self.assertEqual(read(self.g.control)['stop']['type'],'candidate_retries_exhausted')
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_stop_does_not_call_generator_again(self):
        calls=[]
        def generate(snapshot,feedback,attempt): calls.append(attempt);return self.source
        with patch.object(self.g,'evaluate',return_value=dict(text_number=1,hard_pass=False,hard_errors=[dict(code='length',detail=119)])):
            self.assertIsNone(self.g.run_one(1,generate))
        self.assertEqual(calls,[1,2])
    def test_schema_boundary_50_51(self):
        validator=Draft202012Validator(read(PILOT/'source.schema.json'))
        x=deepcopy(self.source);x['text_number']=50;self.assertFalse(list(validator.iter_errors(x)))
        x['text_number']=51;self.assertTrue(list(validator.iter_errors(x)))
    def test_real_raw_replay_pass_and_atomic_credit_once(self):
        path,result=self.g.submit(self.source);self.assertTrue(result['hard_pass'],result['hard_errors'])
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
        with self.assertRaises(OSError): self.g.commit(path,fault_at='before_publish')
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
        self.g.commit(path);once=self.g.ledger.read_bytes();self.g.commit(path)
        self.assertEqual(once,self.g.ledger.read_bytes());self.assertEqual(self.g.load()['epoch'],1)
    def test_future_never_incidental_or_credited(self):
        x=deepcopy(self.source);x['sentences'][0]='친구도 집에 들어오고 싶어요.'
        _,result=self.g.submit(x);self.assertFalse(result['hard_pass'])
        self.assertTrue(any(e['code']=='future_expansion' for e in result['hard_errors']))
        self.assertNotIn('ko_k1_0386',result['incidental_previous_vocab_ids'])
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_next_snapshot_requires_previous_actual_commit(self):
        with self.assertRaises(StructuralStop): self.g.snapshot(2)
    def test_fingerprint_detects_identical_not_unrelated(self):
        a=self.source['scene_fingerprint'];self.assertEqual(similarity(a,a),1)
        b=dict(goal='other',setting='other',participants=['other'],problem_type='other',resolution_type='other',main_actions=['other'])
        self.assertEqual(similarity(a,b),0)

if __name__=='__main__': unittest.main()
