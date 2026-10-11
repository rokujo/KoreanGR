"""Pilot policy regressions, raw reanalysis, and frozen A/B history separation."""
import sys,unittest
from pathlib import Path
from copy import deepcopy
import tempfile,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase2_2 import *
from validate_k1_phase2_2 import validate,inspect_record
from jsonschema import Draft202012Validator

class Phase22Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files=inputs();cls.kiwi=make_kiwi();cls.result=validate()
        cls.records={r['text_number']:r for r in [read(p) for p in sorted((PILOT/'texts').glob('*.json'))]}
        cls.scenes={s['text_number']:s for s in read(PILOT/'authored_scenes.json')}

    def modified(self,t,sentence):
        scene=deepcopy(self.scenes[t]);text,ja=source_text(scene);scene.pop('sentences',None)
        scene['text_ko']=text+' '+sentence;scene['translation_ja']=ja
        return record(scene,self.files,self.records[t]['scheduler_selection'],self.kiwi)

    def test_all_25_hard_rules_and_separate_groups(self):
        self.assertTrue(self.result['ok'],self.result['errors'])
        self.assertEqual([self.result['groups'][g]['text_count'] for g in ('A','B')],[20,5])
        for r in self.result['results']:
            self.assertFalse(r['errors'],r['id']);self.assertEqual(r['coverage']['controlled_vocab_coverage'],1)
            self.assertGreaterEqual(r['coverage']['previous_vocab_coverage'],.98)

    def test_auxiliary_selection_derived_from_ids(self):
        s=selection(self.files)
        self.assertEqual(s['first_introduction_B'],[20,33,110,111,127])
        self.assertFalse(set(s['comparison_A'])&set(s['first_introduction_B']))
        self.assertEqual(s['comparison_A'],read(ROOT/'pilot/ko/k1/selection.json')['text_numbers'])

    def test_five_first_introductions_one_token_each(self):
        for vid in B_IDS:
            r=next(r for r in self.result['results'] if vid in r['new_token_counts'])
            self.assertEqual(r['group'],'B');self.assertEqual(r['new_token_counts'][vid],1)
            self.assertEqual(r['coverage']['new_tokens_U'],2);self.assertTrue(5<=r['review_count']<=8)

    def test_future_vocabulary_rejected_from_raw(self):
        r=self.modified(20,'세탁기는 집에 있어요.')
        c=inspect_record(r,self.files,self.kiwi)
        self.assertIn('Future Expansion used',c['errors'])

    def test_dynamic_new_token_limit_not_soft_three(self):
        r=self.modified(1,'오늘도 학생이 돼요.')
        c=inspect_record(r,self.files,self.kiwi)
        self.assertEqual(c['coverage']['new_tokens_U'],3)
        self.assertLess(c['coverage']['previous_vocab_coverage'],.98)
        self.assertEqual(c['status'],'FAIL')

    def test_annotation_and_metric_falsification_detected(self):
        r=deepcopy(self.records[110]);r['raw_morphology'][0]['form']='거짓'
        self.assertIn('Raw reanalysis mismatch: raw_morphology',inspect_record(r,self.files,self.kiwi)['errors'])
        r=deepcopy(self.records[20]);r['coverage']['denominator_N']+=1
        self.assertIn('Coverage metadata mismatch',inspect_record(r,self.files,self.kiwi)['errors'])

    def test_repeated_review_one_text_credit(self):
        w=self.files['vocab_review_windows.json'];state=ReviewScheduler(w);e=w['entries'][0];i=e['vocab_id'];first=e['first_introduction_text']
        state.record(first,[i,i]);state.record(first+2,[i,i]);state.record(first+2,[i])
        self.assertEqual(len(state.actual[i]),2)

    def test_sparse_ledger_never_claims_all_300_observed(self):
        ledger=read(PILOT/'exposure_ledger.json')
        self.assertFalse(ledger['full_300_review_history_available']);self.assertFalse(ledger['final_500_by_six_actual_complete'])
        self.assertTrue(ledger['hypothetical_introduction_seeds'])
        self.assertEqual({r['text_number'] for r in ledger['pilot_occurrences']},set(self.records))

    def test_registered_hints_do_not_license_unlisted_word(self):
        a=analyze('저는 친구에게 길을 묻고 있어요.',self.files,246,[],kiwi=self.kiwi)
        c=evaluate_lexical_tokens(token_stream(a['annotations']),246,self.files)
        self.assertFalse(c['ok'])
        a=analyze('저는 걷기를 좋아해요. 저는 가지 않아요.',self.files,246,[],kiwi=self.kiwi)
        self.assertTrue(any(i['type']=='unapproved_or_unresolved_grammar' for i in a['annotation_review_required']))

    def test_compound_fallback_remains_context_review(self):
        r=self.records[246]
        ask=next(e['id'] for e in self.files['expansion_vocab.json'] if e['sense']=='ask')
        self.assertIn(ask,{a['vocab_id'] for a in r['annotations']})
        self.assertTrue(any(i['candidate_id']==ask and i['type']=='compound_grouping' for i in r['annotation_review_required']))
        self.assertTrue(any(g['vocab_id']==ask and g['category']=='requires_grammar_boundary_review' for g in self.result['annotation_triage']['groups']))

    def test_freeze_and_retired_ids_and_fast_zone(self):
        self.assertEqual(check_freeze(),[])
        retired=set(self.files['id_migration.json']['retired_ids'])
        for r in self.records.values():
            self.assertFalse(retired&{a['vocab_id'] for a in r['annotations']})
            if r['text_number']>=256:self.assertEqual(r['scheduled_new_vocab_ids'],[])
        self.assertEqual(len(list((ROOT/'pilot/ko/k1/texts').glob('*.json'))),20)

    def test_schema_and_extra_pilot_number_rejected(self):
        r=deepcopy(self.records[20]);r['group']='C'
        self.assertTrue(list(Draft202012Validator(text_schema()).iter_errors(r)))
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);shutil.copytree(PILOT/'texts',d/'texts')
            r=deepcopy(self.records[20]);r['id']='K1-021';r['text_number']=21
            write(d/'texts/K1-021.json',r)
            result=validate(d)
            self.assertFalse(result['ok']);self.assertIn('Must contain exactly the approved A20+B5',result['errors'])

if __name__=='__main__':unittest.main()
