"""Active microrevision regressions, alongside historical Phase 1.2/2/2.1 suites."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_k1_phase2_1A import BASE, DATA, EXCHANGES, digest, history_errors, read
from validate_k1_phase2_1A import resolve_vocab, validate
from lexical_coverage import evaluate_lexical_tokens
from k1_annotation_triage import classify


class RevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = {p.name: read(p) for p in DATA.glob('*.json')}
        cls.first = {vid: r['text'] for r in cls.files['introduction_schedule.json']['rows'] for vid in r['entry_ids']}
        cls.examples_result = validate(DATA, check_examples=True)

    def fixture(self, mutation):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            for p in DATA.glob('*.json'):
                shutil.copy2(p, folder / p.name)
            data = copy.deepcopy(self.files)
            mutation(data)
            for name, value in data.items():
                if value != self.files[name]:
                    (folder / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            window = read(folder / 'vocab_review_windows.json')
            for path in window['source']:
                if path.startswith('config/languages/ko/k1/'):
                    window['source'][path] = digest(folder / Path(path).name)
            (folder / 'vocab_review_windows.json').write_text(json.dumps(window, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            return validate(folder)

    def test_active_revision_and_short_examples(self):
        result = self.examples_result
        self.assertTrue(result['ok'], result['errors'])
        self.assertEqual(result['summary']['total'], 800)
        self.assertEqual(result['summary']['tiers'], {'E1': 200, 'E2': 200, 'E3': 100})
        examples = result['summary']['lexical_gap_examples']
        self.assertEqual(len(examples), 5)
        self.assertTrue(all(2 <= len(e['sentences']) <= 3 and e['ok'] for e in examples))
        self.assertTrue(all(e['coverage']['controlled_vocab_coverage'] == 1 for e in examples))
        self.assertTrue(result['summary']['phase2_2_can_proceed'])
        self.assertFalse(result['summary']['mass_generation_approved'])

    def test_all_five_new_ids_and_no_aliases(self):
        expansion = {e['id']: e for e in self.files['expansion_vocab.json']}
        for old, new, lemma, pos, sense, gloss, tier, *_ in EXCHANGES:
            self.assertNotIn(old, expansion)
            self.assertEqual((expansion[new]['lemma'], expansion[new]['tier']), (lemma, tier))
            self.assertEqual(resolve_vocab(lemma, pos, sense, self.files), new)
        migration = self.files['id_migration.json']
        self.assertEqual(migration['id_policy']['next_id_sequence'], 813)
        self.assertFalse(migration['aliases'])
        self.assertEqual(len(self.files['k2_candidates.json']['entries']), 12)

    def test_photo_sense_kept_stamp_rejected(self):
        identity = resolve_vocab('찍다', 'verb', 'take_photo', self.files)
        self.assertIn(identity, {e['id'] for e in self.files['core_vocab.json']})
        with self.assertRaises(ValueError):
            resolve_vocab('찍다', 'verb', 'stamp', self.files)

    def test_hold_lift_does_not_license_other_senses(self):
        self.assertEqual(resolve_vocab('들다', 'verb', 'hold_lift_by_hand', self.files), 'ko_k1_0812')
        for sense in ('cost', 'like', 'grow_old', 'enter', 'other_dictionary_senses'):
            with self.subTest(sense=sense), self.assertRaises(ValueError):
                resolve_vocab('들다', 'verb', sense, self.files)
        group = next(e for e in self.examples_result['summary']['lexical_gap_examples'] if e['key'] == 'holding_lifting')
        issues = [i for i in group['annotation_review_required'] if i['type'] == 'restricted_sense_context_review']
        self.assertEqual(len(issues), 2)
        vocab = {e['id']: e for e in self.files['core_vocab.json'] + self.files['expansion_vocab.json']}
        record = {'annotations': group['generated_annotations'], 'text_ko': ' '.join(group['sentences']),
                  'raw_morphology': group['raw_morphology']}
        category, _ = classify(issues[0], record, vocab, set(group['grammar_used']))
        self.assertEqual(category, 'requires_lexical_sense_review')

    def test_first_dates_reassessed_early_within_tier(self):
        old = {vid: r['text'] for r in read(BASE / 'introduction_schedule.json')['rows'] for vid in r['entry_ids']}
        for source, new, *_ in EXCHANGES:
            self.assertLess(self.first[new], old[source])
        self.assertEqual([self.first[x] for x in ('ko_k1_0808', 'ko_k1_0810', 'ko_k1_0812', 'ko_k1_0811', 'ko_k1_0809')],
                         [20, 33, 110, 111, 127])
        rows = self.files['introduction_schedule.json']['rows']
        self.assertTrue(all(not r['entry_ids'] for r in rows[255:]))
        self.assertEqual(max(self.first.values()), 255)

    def test_coverage_uses_introduction_not_historical_reviews(self):
        core = {'kind': 'vocab', 'id': self.files['core_vocab.json'][0]['id']}
        new = {'kind': 'vocab', 'id': 'ko_k1_0808'}
        self.assertFalse(evaluate_lexical_tokens([core] * 99 + [new], 19, self.files)['ok'])
        introduced = evaluate_lexical_tokens([core] * 99 + [new], 20, self.files)
        self.assertTrue(introduced['ok']); self.assertEqual(introduced['U'], 1)
        for old, *_ in EXCHANGES:
            self.assertFalse(evaluate_lexical_tokens([core] * 99 + [{'kind': 'vocab', 'id': old}], 300, self.files)['ok'])

    def test_categories_soft_and_large_skew_warns(self):
        def skew(data):
            movable = [e for e in data['expansion_vocab.json'] if e['category'] == 'food_nature'][:30]
            for e in movable:
                e['category'] = 'places_objects'
        result = self.fixture(skew)
        self.assertTrue(result['ok'], result['errors'])
        self.assertTrue(any(w.startswith('CATEGORY:') for w in result['warnings']))

    def test_identity_tier_coverage_and_migration_corruption(self):
        cases = [
            lambda d: d['expansion_vocab.json'][0].update(id='ko_k1_0363'),
            lambda d: d['expansion_vocab.json'][0].update(tier='E2'),
            lambda d: d['id_migration.json']['id_policy'].update(next_id_sequence=808),
            lambda d: d['id_migration.json']['aliases'].append({'old': 'ko_k1_0603', 'new': 'ko_k1_0809'}),
            lambda d: d['profile.json'].update(previous_vocab_coverage_hard_min=.97),
            lambda d: d['grammar.json'].pop(),
            lambda d: next(e for e in d['expansion_vocab.json'] if e['id'] == 'ko_k1_0812').update(sense='cost'),
            lambda d: d['id_migration.json']['mappings'][-1].update(old_sense='cost'),
            lambda d: d['id_migration.json']['mappings'][-1].pop('old_rank'),
            lambda d: d['k2_candidates.json']['entries'][-1].update(former_category='food_nature'),
            lambda d: d['k2_candidates.json']['entries'][-1].pop('former_tier'),
            lambda d: d['expansion_replacement_proposals.json']['entries'][-1].update(source_sense='cost'),
            lambda d: d['lexical_gap_checks.json']['groups'].pop(),
        ]
        for index, mutation in enumerate(cases):
            with self.subTest(index=index):
                self.assertFalse(self.fixture(mutation)['ok'])

    def test_future_intro_and_retired_window_rejected(self):
        def late(data):
            rows = data['introduction_schedule.json']['rows']
            rows[255]['entry_ids'] = [rows[0]['entry_ids'].pop()]
        self.assertFalse(self.fixture(late)['ok'])
        def retired(data):
            data['vocab_review_windows.json']['entries'][0]['vocab_id'] = 'ko_k1_0603'
        self.assertFalse(self.fixture(retired)['ok'])
        def reversed_window(data):
            data['vocab_review_windows.json']['entries'][0]['review_windows'][0]['to'] = 1
        self.assertFalse(self.fixture(reversed_window)['ok'])

    def test_freeze_preserved_and_original_20_numbers_kept(self):
        self.assertFalse(history_errors())
        selection = read(ROOT / 'pilot/ko/k1/selection.json')['text_numbers']
        self.assertEqual(selection, [1, 40, 85, 103, 150, 170, 180, 184, 189, 190, 193, 234, 242, 246, 252, 254, 255, 276, 284, 299])
        self.assertEqual(len(list((ROOT / 'pilot/ko/k1/texts').glob('K1-*.json'))), 20)


if __name__ == '__main__':
    unittest.main()
