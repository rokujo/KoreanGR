"""Actual-history accounting and Phase 3 stop/length policy regression tests."""
import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase3 import files,read,DATA,metrics,similarity,debt_rows,accept,initialize,actual_coverage_files
from lexical_coverage import evaluate_lexical_tokens
from k1_review_scheduler import ReviewScheduler
from jsonschema import Draft202012Validator

class SequentialPolicy(unittest.TestCase):
    def state(self):return ReviewScheduler(files()['vocab_review_windows.json'])
    def test_empty_actual_has_no_hypothetical_history(self):
        s=self.state();self.assertFalse(any(s.actual.values()));self.assertFalse(debt_rows(s,1))
    def test_confirmation_required_for_review(self):
        s=self.state();vid=s.new_ids(1)[0]
        with self.assertRaises(ValueError):s.record(3,[vid])
    def test_selection_does_not_credit(self):
        s=self.state();ids=s.new_ids(1);s.record(1,ids)
        s.select(3,['home'],approved_ids=ids)
        self.assertEqual(sum(map(len,s.actual.values())),2)
    def test_same_text_deduplicates(self):
        s=self.state();ids=s.new_ids(1);s.record(1,ids+ids);s.record(1,ids)
        self.assertTrue(all(s.actual[i]=={1} for i in ids))
    def test_close_deadline_after_final_opportunity(self):
        s=self.state();ids=s.new_ids(1);s.record(1,ids)
        end=s.entries[ids[0]]['review_windows'][0]['to']
        self.assertFalse(any(d['deadline_status']=='expired' for d in debt_rows(s,end)))
        self.assertTrue(any(d['deadline_status']=='expired' for d in debt_rows(s,end,close=True)))
        s.record(end,ids)
        self.assertFalse(any(d['deadline_status']=='expired' for d in debt_rows(s,end,close=True)))
    def test_future_record_rejected(self):
        s=self.state()
        with self.assertRaises(ValueError):s.record(1,s.new_ids(20))
    def test_incidental_before_window_does_not_prepay(self):
        s=self.state();ids=s.new_ids(1);s.record(1,ids);s.record(2,ids)
        self.assertEqual(len(s.actual[ids[0]]),2);self.assertFalse(s.credits[ids[0]])
    def test_natural_two_word_not_hard_min(self):
        m=metrics('물이 있어요. 저는 물을 마셔요.')
        self.assertEqual(m['sentence_eojeol_counts'],[2,3]);self.assertEqual(m['preferred_sentence_outliers'],[1])
    def test_profile_only_preference_changed(self):
        f=files()['profile.json'];old=read(DATA/'profile.json')
        for k in old:
            if k not in ('version','status','sentence_length'):self.assertEqual(f[k],old[k])
        self.assertEqual(old['sentence_length']['preferred_min_eojeol'],4)
        self.assertEqual(f['sentence_length']['preferred_min_eojeol'],3)
        self.assertFalse(list(Draft202012Validator(read(DATA/'phase3/profile.schema.json')).iter_errors(f)))
    def test_bad_profile_rejected(self):
        f=files()['profile.json'];f['previous_vocab_coverage_hard_min']=.97
        self.assertTrue(list(Draft202012Validator(read(DATA/'phase3/profile.schema.json')).iter_errors(f)))
    def test_fingerprint_same_goal_not_whole_scene(self):
        a=dict(goal='help',setting='home',participants=['family'],problem_type='weather',resolution_type='stay',main_actions=['read'])
        b=dict(a,goal='buy',setting='shop',problem_type='missing',resolution_type='buy',main_actions=['pay'])
        self.assertEqual(similarity(a,a),1);self.assertLess(similarity(a,b),.85)
    def test_stopped_run_cannot_resume(self):
        with patch('k1_phase3.read',side_effect=[dict(status='stopped'),dict(text_number=2)]):
            with self.assertRaisesRegex(ValueError,'Run stopped'):accept('not_read_from_disk')
    def test_skipping_a_text_rejected(self):
        with patch('k1_phase3.read',side_effect=[dict(status='running',last_committed_text=1),dict(text_number=3)]):
            with self.assertRaisesRegex(ValueError,'next text'):accept('not_read_from_disk')
    def test_051_rejected_even_after_050(self):
        with patch('k1_phase3.read',side_effect=[dict(status='running',last_committed_text=50),dict(text_number=51)]):
            with self.assertRaisesRegex(ValueError,'capped at 050'):accept('not_read_from_disk')
    def test_initialize_cannot_erase_actual_history(self):
        with patch('k1_phase3.RUN') as p:
            p.exists.return_value=True
            with self.assertRaisesRegex(ValueError,'cannot reset'):initialize()
    def test_planned_prior_is_not_actual_prior(self):
        f=files();s=self.state();i=s.new_ids(1)[0]
        tokens=[dict(kind='vocab',id=i)]
        self.assertTrue(evaluate_lexical_tokens(tokens,2,f)['ok'])
        self.assertFalse(evaluate_lexical_tokens(tokens,2,actual_coverage_files(f,s,2,s.new_ids(2)))['ok'])
        s.record(1,s.new_ids(1))
        self.assertTrue(evaluate_lexical_tokens(tokens,2,actual_coverage_files(f,s,2,s.new_ids(2)))['ok'])

if __name__=='__main__':unittest.main()
