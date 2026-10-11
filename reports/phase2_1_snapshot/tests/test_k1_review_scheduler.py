"""Phase 2.1 regressions: honest exposure accounting and semantic/deadline gates."""
import copy
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from k1_review_scheduler import ReviewScheduler, capacity_dry_run, make_windows
from k1_annotation_triage import classify
from build_k1_phase2_1 import DATA, load, read
from validate_k1_phase2_1 import validate


def small(first=1):
    return {'entries': [{'vocab_id': 'ko_k1_0301', 'first_introduction_text': first,
                        'review_windows': make_windows(first), 'scene_affinity': ['home'],
                        'semantic_domain': 'people_social'}]}


class SchedulerTests(unittest.TestCase):
    def test_all_frozen_inputs_and_23_replays(self):
        result = validate()
        self.assertTrue(result['ok'], result['errors'])
        self.assertEqual(result['counts']['total'], 800)
        self.assertEqual(result['conflict_replay']['count'], 23)
        self.assertEqual(result['conflict_replay']['scheduler_selected_provisional_scenes'], 22)
        self.assertFalse(result['conflict_replay']['actual_prose_verified'])
        self.assertFalse(result['mass_generation_approved'])

    def test_unique_six_actual_texts_not_tokens(self):
        scheduler = ReviewScheduler(small())
        for t in (1, 3, 7, 26, 67, 121):
            scheduler.record(t, ['ko_k1_0301', 'ko_k1_0301'])
            scheduler.record(t, ['ko_k1_0301'])
        self.assertTrue(scheduler.audit(300, final=True)['ok'])
        self.assertEqual(len(scheduler.actual['ko_k1_0301']), 6)

    def test_repeated_single_text_cannot_finish(self):
        scheduler = ReviewScheduler(small())
        scheduler.record(1, ['ko_k1_0301'])
        for _ in range(10):
            scheduler.record(3, ['ko_k1_0301'])
        self.assertFalse(scheduler.audit(300, final=True)['ok'])

    def test_selection_is_not_exposure(self):
        scheduler = ReviewScheduler(small())
        scheduler.record(1, ['ko_k1_0301'])
        result = scheduler.select(3, ['home'], ['ko_k1_0301'])
        self.assertEqual(len(result['selected_reviews']), 1)
        self.assertEqual(scheduler.actual['ko_k1_0301'], {1})
        self.assertFalse(result['selection_is_observation'])
        self.assertEqual(scheduler.scene_candidates(1)['new_vocab_ids'], ['ko_k1_0301'])
        self.assertEqual(scheduler.scene_candidates(3)['candidate_scenes'], ['home'])

    def test_window_expiry_is_debt_then_oldest_single_credit(self):
        scheduler = ReviewScheduler(small())
        scheduler.record(1, ['ko_k1_0301'])
        interim = scheduler.audit(30)
        self.assertTrue(interim['ok'])
        self.assertTrue(any(w['type'] == 'expired_window_debt' for w in interim['warnings']))
        chosen = scheduler.select(30, ['home'], ['ko_k1_0301'])['selected_reviews'][0]
        self.assertTrue(chosen['carry_debt'])
        scheduler.record(30, ['ko_k1_0301'])
        self.assertEqual(scheduler.credits['ko_k1_0301'], {0: 30})
        self.assertTrue(any(w['type'] == 'final_quota_no_longer_feasible'
                            for w in scheduler.audit(299)['warnings']))

    def test_no_prepayment_of_unopened_window(self):
        scheduler = ReviewScheduler(small())
        scheduler.record(1, ['ko_k1_0301'])
        scheduler.record(2, ['ko_k1_0301'])
        self.assertFalse(scheduler.credits['ko_k1_0301'])
        self.assertEqual(len(scheduler.actual['ko_k1_0301']), 2)

    def test_semantic_veto_overrides_urgent_deadline(self):
        scheduler = ReviewScheduler(small())
        scheduler.record(1, ['ko_k1_0301'])
        selected = scheduler.select(300, ['home'], ['ko_k1_0301'], ['ko_k1_0301'])
        self.assertFalse(selected['selected_reviews'])
        self.assertEqual(selected['excluded'][0]['reason'], 'semantic_veto')

    def test_tags_without_positive_realization_do_not_pass(self):
        scheduler = ReviewScheduler(small())
        scheduler.record(1, ['ko_k1_0301'])
        self.assertFalse(scheduler.select(3, ['home'])['selected_reviews'])
        self.assertFalse(scheduler.select(3, ['food'], ['ko_k1_0301'])['selected_reviews'])

    def test_future_retired_and_nonchronological_events_rejected(self):
        scheduler = ReviewScheduler(small(10))
        for t, ids in ((9, ['ko_k1_0301']), (11, ['ko_k1_0301']), (10, ['ko_k1_0773'])):
            with self.assertRaises(ValueError):
                scheduler.record(t, ids)
        scheduler.record(10, ['ko_k1_0301'])
        with self.assertRaises(ValueError):
            scheduler.record(9, [])
        for t in (0, 301, True):
            with self.assertRaises(ValueError):
                scheduler.record(t, [])

    def test_final_missing_introduction_detected(self):
        scheduler = ReviewScheduler(small())
        result = scheduler.audit(300, final=True)
        self.assertFalse(result['ok'])
        self.assertIn('unconfirmed_introduction', {e['type'] for e in result['errors']})
        with self.assertRaises(ValueError):
            scheduler.audit(299, final=True)
        with self.assertRaises(ValueError):
            scheduler.audit(301)

    def test_capacity_and_last_25_have_no_new_words(self):
        windows = read(DATA / 'vocab_review_windows.json')
        proof = capacity_dry_run(windows, 10)
        self.assertTrue(proof['complete'])
        self.assertEqual(sum(len(r['reviews']) for r in proof['rows']), 2500)
        self.assertFalse(capacity_dry_run(windows, 8)['complete'])
        scheduler = ReviewScheduler(windows)
        self.assertTrue(all(not scheduler.new_ids(t) for t in range(276, 301)))

    def test_late_introduction_preserves_five_distinct_windows(self):
        windows = make_windows(255)
        self.assertEqual(len(windows), 5)
        self.assertEqual(windows[-1]['to'], 300)
        self.assertTrue(all(w['from'] <= w['to'] for w in windows))
        self.assertTrue(all(a['to'] < b['from'] for a, b in zip(windows, windows[1:])))
        with self.assertRaises(ValueError):
            make_windows(276)

    def test_schema_disallows_exact_reviews_and_policy_drift(self):
        windows = read(DATA / 'vocab_review_windows.json')
        validator = Draft202012Validator(read(DATA / 'vocab_review_windows.schema.json'))
        self.assertFalse(list(validator.iter_errors(windows)))
        broken = copy.deepcopy(windows)
        broken['entries'][0]['review_texts'] = [3, 4, 5, 6, 7]
        self.assertTrue(list(validator.iter_errors(broken)))
        broken = copy.deepcopy(windows)
        broken['policy']['previous_vocab_coverage_hard_min'] = .97
        self.assertTrue(list(validator.iter_errors(broken)))

    def test_ambiguity_triage_preserves_269_and_detects_bad_span(self):
        dry = read(ROOT / 'reports/k1_phase2_1_dry_run.json')
        triage = dry['annotation_triage']
        self.assertEqual(triage['total_occurrences'], 269)
        self.assertLess(triage['total_groups'], 100)
        core, expansion, _, _, records = load()
        vocab = {e['id']: e for e in core + expansion}
        record = copy.deepcopy(records[0])
        issue = record['annotation_review_required'][0]
        a = next(a for a in record['annotations'] if a['start'] == issue['start'])
        a['surface'] = 'bad span'
        category, _ = classify(issue, record, vocab, set())
        self.assertEqual(category, 'true_unresolved')

    def test_cli_dry_run_cannot_be_substituted_for_actual_final(self):
        no_ledger = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/validate_k1_phase2_1.py'),
                                   '--final'], capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(no_ledger.returncode, 0)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / 'empty.json'
            ledger.write_text('[]', encoding='utf-8')
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/validate_k1_phase2_1.py'),
                '--actual-ledger', str(ledger), '--final', '--json'],
                capture_output=True, text=True, encoding='utf-8', timeout=60)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertFalse(report['ok'])
        self.assertEqual(report['actual_entry_text_pairs'], 0)


if __name__ == '__main__':
    unittest.main()
