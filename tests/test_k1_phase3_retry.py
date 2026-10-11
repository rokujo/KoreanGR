"""New run budget/stagnation regressions; no historical artifact writes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import tempfile
import unittest
from unittest.mock import patch
from copy import deepcopy
from k1_phase3_retry import SequentialGate, stagnant_errors
from k1_candidate_gate import StructuralStop, read
from k1_phase3 import files
from k1_phase3_1 import smoke_source
from k1_phase2_3 import make_kiwi

class ProgressSignatureTests(unittest.TestCase):
    def length(self,n):return dict(hard_errors=[dict(code='length',detail=n)])
    def test_equal_length_error_stagnates(self):self.assertTrue(stagnant_errors(self.length(119),self.length(119)))
    def test_worse_length_stagnates(self):self.assertTrue(stagnant_errors(self.length(119),self.length(118)))
    def test_improving_length_does_not_stagnate(self):self.assertFalse(stagnant_errors(self.length(118),self.length(119)))
    def test_different_error_is_not_stagnation(self):self.assertFalse(stagnant_errors(self.length(119),dict(hard_errors=[dict(code='planned_new_not_present',detail=['a'])])))
    def test_repeated_future_count_improves(self):
        e=dict(code='future_expansion',detail=dict(vocab_id='a'))
        self.assertFalse(stagnant_errors(dict(hard_errors=[e,e]),dict(hard_errors=[e])))
    def test_same_future_identity_stagnates(self):
        e=dict(hard_errors=[dict(code='future_expansion',detail=dict(vocab_id='a'))])
        self.assertTrue(stagnant_errors(e,e))
    def test_coverage_progress_is_measured(self):
        def c(n):return dict(coverage=dict(controlled_vocab_coverage=n),hard_errors=[dict(code='coverage_or_token_policy',detail='controlled_vocab_coverage below hard 100%')])
        self.assertFalse(stagnant_errors(c(.98),c(.99)))
        self.assertTrue(stagnant_errors(c(.99),c(.99)))

class RetryRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.kiwi=make_kiwi();cls.f=files()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)
        self.g=SequentialGate(self.path/'run',self.path/'ledger.json',f=self.f,kiwi=self.kiwi)
        self.g.initialize();self.initial=self.g.ledger.read_bytes()
        self.source=smoke_source(self.g.snapshot(1),dict(hard_errors=[dict(code='length')]),3)
    def tearDown(self):self.tmp.cleanup()
    def test_five_attempt_budget(self):self.assertEqual(read(self.g.control)['max_attempts'],5)
    def test_six_attempt_budget_refused(self):
        with self.assertRaises(ValueError):SequentialGate(self.path/'other',self.path/'other.json',kiwi=self.kiwi,max_attempts=6)
    def test_two_equal_failures_stop_with_zero_state_change(self):
        with patch.object(self.g,'evaluate',return_value=dict(text_number=1,hard_pass=False,hard_errors=[dict(code='length',detail=119)])):
            self.g.submit(self.source);self.assertEqual(read(self.g.control)['status'],'running')
            self.g.submit(self.source)
        self.assertEqual(read(self.g.control)['stop']['type'],'same_hard_error_twice_without_improvement')
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_five_improving_failures_stop_on_budget(self):
        for n in range(115,120):
            with patch.object(self.g,'evaluate',return_value=dict(text_number=1,hard_pass=False,hard_errors=[dict(code='length',detail=n)])):
                self.g.submit(self.source)
            self.assertEqual(read(self.g.control)['status'],'stopped' if n==119 else 'running')
        self.assertEqual(read(self.g.control)['stop']['type'],'candidate_retries_exhausted')
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_real_pass_commits_exactly_once(self):
        p,r=self.g.submit(self.source);self.assertTrue(r['hard_pass'],r['hard_errors'])
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
        self.g.commit(p);once=self.g.ledger.read_bytes();self.g.commit(p)
        self.assertEqual(once,self.g.ledger.read_bytes());self.assertEqual(self.g.load()['epoch'],1)
    def test_stopped_run_cannot_accept_next_candidate(self):
        self.g.reject_run(dict(type='analyzer_structural_failure'))
        with self.assertRaises(StructuralStop):self.g.submit(self.source)
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_run_one_stops_after_two_stagnant_attempts(self):
        calls=[]
        def generator(snapshot,feedback,attempt):calls.append(attempt);return self.source
        with patch.object(self.g,'evaluate',return_value=dict(text_number=1,hard_pass=False,hard_errors=[dict(code='length',detail=119)])):
            self.assertIsNone(self.g.run_one(1,generator))
        self.assertEqual(calls,[1,2]);self.assertEqual(read(self.g.control)['stop']['type'],'same_hard_error_twice_without_improvement')
        self.assertEqual(self.initial,self.g.ledger.read_bytes())

if __name__=='__main__':unittest.main()
