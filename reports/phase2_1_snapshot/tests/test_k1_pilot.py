"""Pilot regressions: raw/annotation disagreement and frozen-policy boundaries."""
import copy
import json
from pathlib import Path
import sys
import unittest
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from select_k1_pilot import load_inputs,select
from validate_k1_pilot import validate,inspect_record,check_freeze,token_stream
from k1_pilot_analysis import analyze,make_kiwi
from lexical_coverage import evaluate_lexical_tokens

class PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files=load_inputs();cls.selection=select(cls.files);cls.kiwi=make_kiwi()
        cls.records={int(p.stem[-3:]):json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'pilot/ko/k1/texts').glob('K1-*.json')}
        cls.schema=json.loads((ROOT/'pilot/ko/k1/pilot_text.schema.json').read_text(encoding='utf-8'))

    def test_dataset_and_freeze(self):
        r=validate();self.assertFalse(r['ok']) # Declared conflicts are not silently PASS.
        self.assertFalse(r['errors']);self.assertFalse(check_freeze())
        self.assertEqual(r['text_count'],20);self.assertEqual(r['hard_error_texts'],0)
        self.assertGreater(r['schedule_conflict_texts'],0)
        self.assertTrue(all(x['coverage']['controlled_vocab_coverage']==1 for x in r['results']))
        self.assertTrue(all(x['coverage']['previous_vocab_coverage']>=.98 for x in r['results']))

    def test_all_adoptions_and_medium_firsts_selected(self):
        first={e['vocab_id']:e['first_introduction_text'] for e in self.files['vocab_exposure_schedule.json']['entries']}
        ids={m['new_id'] for m in self.files['id_migration.json']['mappings']}
        ids|={e['id'] for e in self.files['expansion_vocab.json'] if e['confidence']=='medium'}
        for vid in ids:
            self.assertIn(first[vid],self.selection['text_numbers'])
            self.assertIn(vid,self.records[first[vid]]['actually_used_new_vocab_ids'])
        self.assertEqual({len(r['scheduled_new_vocab_ids']) for r in self.records.values()},{0,1,2})

    def test_selection_reads_changed_schedule(self):
        f=copy.deepcopy(self.files);m=f['id_migration.json']['mappings'][0]
        e=next(e for e in f['vocab_exposure_schedule.json']['entries'] if e['vocab_id']==m['new_id'])
        e['first_introduction_text']+=1
        self.assertEqual(select(f)['selection_keys']['replacement:'+m['new_lemma']],e['first_introduction_text'])

    def test_false_metric_cannot_pass(self):
        record=copy.deepcopy(self.records[1]);record['coverage']['previous_vocab_coverage']=1
        r=inspect_record(record,self.files,self.kiwi)
        self.assertEqual(r['language_status'],'FAIL');self.assertIn('Coverage metadata mismatch',r['errors'])

    def test_retired_and_future_ids(self):
        future=next(e for e in self.files['expansion_vocab.json'] if e['id']=='ko_k1_0801')
        for vid,expected in [('ko_k1_0773','Retired ID used'),(future['id'],'Future Expansion used')]:
            record=copy.deepcopy(self.records[1]);a=next(a for a in record['annotations'] if a['vocab_id'])
            a['vocab_id']=vid
            r=inspect_record(record,self.files,self.kiwi)
            self.assertEqual(r['language_status'],'FAIL');self.assertIn(expected,r['errors'])

    def test_content_cannot_be_deleted_from_annotation(self):
        record=copy.deepcopy(self.records[1]);i=next(i for i,a in enumerate(record['annotations']) if a['vocab_id']);record['annotations'].pop(i)
        r=inspect_record(record,self.files,self.kiwi)
        self.assertIn('Annotation hypotheses do not match raw/rule normalization',r['errors'])

    def test_unlisted_raw_grammar(self):
        for text in ['저는 책을 읽지 않아요.','저는 책 읽기를 좋아해요.','저는 친구와 같이 가요.',
                     '저는 친구보다 빨리 가요.','저는 걸으면서 책을 읽어요.']:
            with self.subTest(text=text):
                a=analyze(text,self.files,299,[],kiwi=self.kiwi)
                self.assertTrue(a['unresolved_tokens'],a)
        a=analyze('저는 책을 읽어 보고 싶어요.',self.files,299,[],kiwi=self.kiwi)
        self.assertFalse(a['unresolved_tokens'],a['unresolved_tokens'])
        self.assertIn('ko_k1_g18',a['grammar_used'])

    def test_schema_required_and_grammar_range(self):
        for change in [lambda r:r.pop('translation_ja'),lambda r:r['grammar_used'].append('ko_k1_g33')]:
            r=copy.deepcopy(self.records[1]);change(r)
            self.assertTrue(list(Draft202012Validator(self.schema).iter_errors(r)))

    def test_conflict_cannot_be_silently_removed(self):
        r=copy.deepcopy(next(r for r in self.records.values() if r['semantic_schedule_conflicts']))
        r['semantic_schedule_conflicts']=[];r['validation']['schedule_pass']=True
        result=inspect_record(r,self.files,self.kiwi)
        self.assertEqual(result['status'],'FAIL')
        self.assertIn('Missing scheduled word/conflict ledger mismatch',result['errors'])

    def test_proper_and_frozen_expression_limits(self):
        a=analyze('한국은 정말 좋은 나라예요.',self.files,1,[],kiwi=self.kiwi)
        self.assertFalse(a['unresolved_tokens']);self.assertTrue(any(x['role']=='proper_name' for x in a['annotations']))
        for text,ok in [('안녕하세요.',True),('안녕하세요. 안녕하세요. 안녕하세요.',False),('우주선은 여기 있어요.',False)]:
            a=analyze(text,self.files,1,[],kiwi=self.kiwi)
            self.assertEqual(evaluate_lexical_tokens(token_stream(a['annotations']),1,self.files)['ok'],ok)

if __name__=='__main__':unittest.main()
