"""Regression risks from human language review, plus frozen pilot integrity."""
import unittest,sys
from pathlib import Path
from copy import deepcopy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase2_3 import *
from k1_naturalness_lint import lint,semantic_review,CHECKS,translation_lint,sentences
from k1_phase2_2 import analyze
from k1_review_scheduler import ReviewScheduler

class Phase23(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files=inputs();cls.kiwi=make_kiwi()
        cls.records={r['text_number']:r for p in (PILOT/'texts').glob('*.json') for r in [read(p)]}

    def rules(self,text):return {r['rule_id'] for r in lint(text)}

    def test_all_25_hard_conditions_and_same_numbers(self):
        self.assertEqual(sorted(self.records),selection(self.files)['all_text_numbers'])
        for t,r in self.records.items():
            hard=inspect_record(r,self.files,self.kiwi)
            self.assertEqual(hard['errors'],[],r['id'])
            self.assertEqual(r['coverage']['controlled_vocab_coverage'],1)
            self.assertGreaterEqual(r['coverage']['previous_vocab_coverage'],.98)

    def test_freeze_all_old_artifacts(self):self.assertEqual(frozen_errors(),[])

    def test_guideline_contract_and_ten_categories(self):
        data=read(DATA/'naturalness_guidelines.json');schema=read(DATA/'naturalness_guidelines.schema.json')
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(data)),[])
        self.assertEqual(len({r['category'] for r in data['rules']}),10)
        self.assertIn('avoid literal Japanese-style genitive chaining',data['rules'][0]['preferred_strategy'])
        self.assertFalse(data['model_or_regex_is_final_approval'])

    def test_genitives_are_not_globally_banned(self):
        self.assertIn('nat_genitive_overuse',self.rules('학교의 학생은 수업의 시간을 알아요.'))
        self.assertNotIn('nat_genitive_overuse',self.rules('친구의 이름을 알아요.'))
        self.assertNotIn('nat_genitive_overuse',self.rules('버스 번호를 봐요.'))

    def test_four_dangerous_argument_patterns(self):
        for text in ['친구는 책을 물어봐요.','친구의 이름을 말해요.','무거운 가방을 받아요.','친구에게 의자를 줘요.']:
            self.assertIn('nat_verb_argument_frame',self.rules(text))
        # A risk can be a genuine information question/transfer; it remains a warning.
        self.assertTrue(all(r['severity']=='warning' for r in lint('친구의 가방을 받아요.')))

    def test_vague_reaction_vs_actual_preference(self):
        self.assertIn('nat_vague_positive_reaction',self.rules('약속을 아주 좋아해요.'))
        self.assertNotIn('nat_vague_positive_reaction',self.rules('친구는 영화를 좋아해요.'))

    def test_filler_repetition_and_offsets(self):
        text='오늘은 쉬어요.\n 먼저 물을 마셔요. 먼저 밥을 먹어요.'
        rows=lint(text);self.assertTrue(any(r['rule_id']=='nat_filler_adverb' for r in rows))
        for row in rows:self.assertEqual(text[row['start']:row['end']],row['surface'])

    def test_habit_vs_genuine_progressive(self):
        self.assertIn('nat_habit_vs_progressive',self.rules('친구는 자주 공부하고 있어요.'))
        self.assertNotIn('nat_habit_vs_progressive',self.rules('친구는 지금 공부하고 있어요.'))

    def test_reference_candidates_are_not_automatic_errors(self):
        ws=lint('가방이 있어요. 이것을 들어요.')
        self.assertIn('nat_reference_clarity',{w['rule_id'] for w in ws})
        self.assertTrue(all(w['severity']=='warning' for w in ws))

    def test_restricted_context_and_retired_stamp_candidates(self):
        for text in ['마음에 들어요.','종이에는 자리가 없어요.','도장을 찍어요.']:
            self.assertIn('nat_restricted_sense',self.rules(text))
        self.assertNotIn('nat_restricted_sense',self.rules('가방을 들어요.'))
        # Context screening instead relies on annotations for apparently good holds.
        r=self.records[110];ws=lint(r['text_ko'],r['annotations'])
        self.assertTrue(any(w['rule_id']=='nat_restricted_sense' for w in ws))

    def test_translation_does_not_repair_positive_reaction(self):
        self.assertTrue(translation_lint([['좋아해요.','喜びます。']]))
        self.assertEqual(translation_lint([['좋아해요.','好きです。'],['웃어요.','笑います。']]),[])
        self.assertTrue(translation_lint([['웃어요.','うれしいです。']]))

    def test_semantic_review_requires_evidence_and_never_approves(self):
        with self.assertRaises(ValueError):semantic_review({})
        evidence={k:dict(verdict='YES',reason='Context checked') for k in CHECKS}
        self.assertFalse(semantic_review(evidence)['human_approved'])
        evidence['plausible_actions']['verdict']='NO'
        self.assertIn('plausible_actions',semantic_review(evidence)['flags'])
        evidence['plausible_actions']['verdict']='maybe'
        with self.assertRaises(ValueError):semantic_review(evidence)

    def test_five_new_words_one_token_at_first(self):
        for t,vid in [(20,'ko_k1_0808'),(33,'ko_k1_0810'),(110,'ko_k1_0812'),(111,'ko_k1_0811'),(127,'ko_k1_0809')]:
            r=self.records[t]
            self.assertEqual(sum(a['vocab_id']==vid for a in r['annotations']),1)
            self.assertLessEqual(r['coverage']['new_tokens_U'],3)

    def test_new_receipt_and_charger_each_once(self):
        r=self.records[255]
        self.assertEqual(r['coverage']['new_tokens_U'],2)
        self.assertFalse(any(w['rule_id']=='nat_scene_plausibility' for w in r['naturalness_lint']))
        self.assertNotIn('직원에게 휴대폰',r['text_ko'])
        self.assertNotIn('내일 여행의 이야기를',r['text_ko'])

    def test_review_defer_no_credit_and_positive_gate(self):
        scenes=read(PILOT/'authored_scenes.json');ledger=read(PILOT/'exposure_ledger.json')
        for s in scenes:
            for veto in s['review_gate_vetoes']:
                entries=[e for e in self.files['expansion_vocab.json'] if e['lemma']==veto['lemma']]
                ids={e['id'] for e in entries}
                self.assertNotIn(veto['lemma'],s['review_candidates'])
                self.assertFalse(ids&set(self.records[s['text_number']]['scheduled_review_vocab_ids']))
                self.assertFalse(any(o['text_number']==s['text_number'] and o['vocab_id'] in ids for o in ledger['pilot_occurrences']))

    def test_scheduler_deadline_never_overrides_semantic_veto(self):
        w=read(DATA/'vocab_review_windows.json');state=ReviewScheduler(w)
        e=w['entries'][0];vid=e['vocab_id'];state.record(e['first_introduction_text'],[vid])
        t=e['review_windows'][0]['to']
        p=state.select(t,e['scene_affinity'],approved_ids=[vid],veto_ids=[vid])
        self.assertFalse(p['selected_reviews'])
        self.assertTrue(any(x['vocab_id']==vid and x['reason']=='semantic_veto' for x in p['excluded']))
        self.assertEqual(len(state.actual[vid]),1)

    def test_direct_speech_does_not_license_new_grammar(self):
        r=self.records[33]
        self.assertTrue(r['validation']['grammar_pass'])
        bad=analyze('친구가 말해요. “책을 읽지 않아요.”',self.files,299,[],kiwi=self.kiwi)
        self.assertTrue(bad['unresolved_tokens'] or any(i['type']=='unapproved_or_unresolved_grammar' for i in bad['annotation_review_required']))

    def test_future_word_insertion_rejected(self):
        r=deepcopy(self.records[1]);r['text_ko']+=' 충전기가 있어요.'
        errors=inspect_record(r,self.files,self.kiwi)['errors']
        self.assertIn('Future Expansion used',errors)

    def test_annotation_sense_forgery_rejected(self):
        r=deepcopy(self.records[110]);a=next(a for a in r['annotations'] if a['vocab_id']=='ko_k1_0812');a['sense']='like'
        self.assertIn('Raw reanalysis mismatch: annotations',inspect_record(r,self.files,self.kiwi)['errors'])

    def test_future_registered_compound_hint_not_new_licensing(self):
        a=analyze('친구는 내일 책을 꼭 가져올 거예요.',self.files,85,[],kiwi=self.kiwi)
        self.assertEqual(a['unresolved_tokens'],[])
        self.assertTrue(any(x['lemma']=='가져오다' for x in a['annotations']))
        bad=analyze('도장을 찍어요.',self.files,299,[],kiwi=self.kiwi)
        self.assertTrue(bad['unresolved_tokens'])

    def test_new_translation_alignment_and_source_hash(self):
        scenes=read(PILOT/'authored_scenes.json')
        for s in scenes:
            r=self.records[s['text_number']]
            self.assertEqual([k for k,j in s['aligned_translation']],[k for _,k in sentences(r['text_ko'])])
            self.assertEqual(r['translation_fidelity']['korean_sha256'],sha256_text(r['text_ko']))
            self.assertFalse(r['translation_fidelity']['human_approved'])

if __name__=='__main__':unittest.main()
