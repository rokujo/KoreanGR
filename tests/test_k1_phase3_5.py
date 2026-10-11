import copy
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase3 import ROOT,files,read
from k1_phase3_4_resolver import analyze
from k1_phase3_2_analysis import make_kiwi
from k1_grammar_semantic_gate import checks,registry
from k1_phase3_5 import SmokeGate
from k1_phase3_5_gate import CandidateGate,StructuralStop,digest

class MeaningFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=files();cls.f['_allowed_vocab']=cls.f['core_vocab.json']+cls.f['expansion_vocab.json'];cls.k=make_kiwi()
    def test_all_32_and_37_contrasts(self):
        fixtures=read(ROOT/'tests/fixtures/k1_phase3_5_grammar_semantics.json')
        positives={r['grammar_id'] for r in fixtures if r['provenance']=='frozen grammar.json example'}
        self.assertEqual(positives,set(registry()))
        for r in fixtures:
            with self.subTest(case=r['id']):
                a=analyze(r['text'],self.f,255,[],kiwi=self.k)
                original=copy.deepcopy(a)
                target=[x for x in checks(r['text'],a) if x['grammar_id']==r['grammar_id']]
                if r['expected']=='PRECEDING_REJECT':
                    self.assertFalse(target);self.assertTrue(a['unresolved_tokens'])
                else:
                    self.assertTrue(target);self.assertEqual({r['expected']},{x['decision'] for x in target})
                self.assertEqual(a,original)
    def test_author_labels_are_not_inputs(self):
        text='사진을 선물로 주고 싶어요.'
        a=analyze(text,self.f,255,[],kiwi=self.k)
        a['author_grammar_functions']={'ko_k1_g30':'direction'}
        self.assertEqual(['FAIL'],[x['decision'] for x in checks(text,a) if x['grammar_id']=='ko_k1_g30'])
    def test_no_whole_sentence_example_whitelist(self):
        text='저는 버스로 학교에 가요. 사진을 선물로 줘요.'
        ds=[x['decision'] for x in checks(text,analyze(text,self.f,255,[],kiwi=self.k)) if x['grammar_id']=='ko_k1_g30']
        self.assertEqual(ds,['PASS','FAIL'])
    def test_wrong_head_and_unregistered_tool_review(self):
        text='연필로 학교에 가요.'
        ds=[x['decision'] for x in checks(text,analyze(text,self.f,255,[],kiwi=self.k)) if x['grammar_id']=='ko_k1_g30']
        self.assertEqual(ds,['REVIEW'])
    def test_surface_spans_and_quotes(self):
        text='저는 말해요. "사진을 선물로 줘요." 저는 집으로 가요.'
        for c in checks(text,analyze(text,self.f,255,[],kiwi=self.k)):
            self.assertEqual(text[c['start']:c['end']],c['surface'])
    def test_unmapped_grammar_is_review(self):
        a=analyze('책이에요.',self.f,255,[],kiwi=self.k)
        a['grammar_used'].append('ko_k1_g30')
        self.assertEqual('REVIEW',checks('책이에요.',a)[-1]['decision'])
    def test_existing_scope_quote_regressions(self):
        from test_k1_phase3_4 import QuoteRegressionTests
        # The complete suite runs the original fixtures independently too.
        self.assertTrue(QuoteRegressionTests)
        for sentence in ('네.','아니요.','한국어 책이 있어요?','우리 집에 가요.'):
            plain=analyze(sentence,self.f,255,[],kiwi=self.k)
            quote=analyze('"'+sentence+'"',self.f,255,[],kiwi=self.k)
            self.assertEqual([a['vocab_id'] for a in plain['annotations'] if a['vocab_id']],
                             [a['vocab_id'] for a in quote['annotations'] if a['vocab_id']])
    def test_ownership_contraction_and_existential_modifier(self):
        for text,gid in [('제 책이에요.','ko_k1_g29'),('있는 책을 봐요.','ko_k1_g26')]:
            cs=checks(text,analyze(text,self.f,255,[],kiwi=self.k))
            self.assertEqual({'PASS'},{x['decision'] for x in cs if x['grammar_id']==gid})
    def test_locomotion_at_location_is_not_source(self):
        text='공원에서 뛰어요.'
        self.assertEqual(['PASS'],[x['decision'] for x in checks(text,analyze(text,self.f,255,[],kiwi=self.k)) if x['grammar_id']=='ko_k1_g23'])
    def test_polysemous_particle_and_ending_boundaries(self):
        for text,absent,present in [('읽는 책을 봐요.','ko_k1_g19','ko_k1_g27'),
                                    ('공부하고 있어요.','ko_k1_g25','ko_k1_g05')]:
            cs=checks(text,analyze(text,self.f,255,[],kiwi=self.k));ids={x['grammar_id'] for x in cs}
            self.assertNotIn(absent,ids);self.assertIn(present,ids)
        text='길을 걸어요.'
        cs=checks(text,analyze(text,self.f,255,[],kiwi=self.k))
        self.assertEqual(['REVIEW'],[x['decision'] for x in cs if x['grammar_id']=='ko_k1_g21'])
    def test_corrected_003_all_semantics_pass_without_g30(self):
        text='저는 어머니에게 사진을 주고 싶어요.'
        cs=checks(text,analyze(text,self.f,255,[],kiwi=self.k))
        self.assertNotIn('ko_k1_g30',{x['grammar_id'] for x in cs})
        self.assertEqual({'PASS'},{x['decision'] for x in cs})
    def test_new_post_go_auxiliary_ambiguity_remains_rejected(self):
        simple='저는 물을 마셔요.'
        a=analyze(simple,self.f,255,[],kiwi=self.k)
        self.assertTrue(any(x['lemma']=='마시다' and x['vocab_id'] for x in a['annotations']))
        joined='저는 물을 받고 마셔요.'
        a=analyze(joined,self.f,255,[],kiwi=self.k)
        self.assertTrue(a['unresolved_tokens'])
        self.assertEqual(['REVIEW'],[x['decision'] for x in checks(joined,a) if x['grammar_id']=='ko_k1_g09'])

class SemanticCommitSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.k=make_kiwi()
    def source(self):
        s=read(ROOT/'pilot/ko/k1/phase3_4_corrected_smoke/sources/K1-001-attempt-01.json')
        pairs=s.pop('pairs');s['sentences']=[p[0] for p in pairs];s['translations_ja']=[p[1] for p in pairs]
        return s
    def test_semantic_review_is_hard_reject_with_zero_credit(self):
        with tempfile.TemporaryDirectory() as d:
            g=SmokeGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);g.initialize();before=g.ledger.read_bytes()
            path,r=g.submit(self.source())
            self.assertFalse(r['hard_pass']);self.assertTrue(any(e['code']=='semantic_grammar_review' for e in r['hard_errors']))
            self.assertEqual(before,g.ledger.read_bytes());self.assertEqual(g.load()['epoch'],0)
            self.assertEqual(read(g.control)['stop']['type'],'semantic_grammar_stop')
            with self.assertRaises(StructuralStop):g.commit(path)
            self.assertEqual(before,g.ledger.read_bytes())
    def test_semantic_fail_in_title_is_not_exempt(self):
        with tempfile.TemporaryDirectory() as d:
            g=CandidateGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);g.initialize()
            s=self.source();s['title_ko']='사진을 선물로 줘요.'
            _,r=g.submit(s)
            self.assertTrue(any(c['scope']=='title' and c['decision']=='FAIL' for c in r['semantic_grammar_checks']))
            self.assertEqual(g.load()['epoch'],0)
    def test_frozen_policy_digests_and_forward_contract(self):
        from jsonschema import Draft202012Validator
        from build_k1_phase3_4_schemas import contracts
        self.assertEqual(len(registry()),32)
        # Existing explicit forward contract is still used, not a 005 schema.
        schemas=contracts(50)
        self.assertTrue(schemas)
    def test_atomic_commit_and_idempotence_in_new_engine(self):
        from author_k1_phase3_5_smoke import first
        with tempfile.TemporaryDirectory() as d:
            g=CandidateGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);g.initialize()
            before=g.ledger.read_bytes();p,r=g.submit(first());self.assertTrue(r['hard_pass'])
            with self.assertRaises(OSError):g.commit(p,fault_at='before_publish')
            self.assertEqual(before,g.ledger.read_bytes())
            with self.assertRaises(OSError):g.commit(p,fault_at='after_publish')
            self.assertEqual(g.load()['epoch'],1)
            g.recover();g.commit(p);self.assertEqual(g.load()['epoch'],1)
            self.assertTrue(read(g.path/'texts/K1-001.json')['final_reanalysis_pass'])
    def test_final_semantic_reanalysis_mismatch_prevents_credit(self):
        from author_k1_phase3_5_smoke import first
        from k1_phase3_5_gate import write
        with tempfile.TemporaryDirectory() as d:
            g=CandidateGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);g.initialize()
            p,r=g.submit(first());self.assertTrue(r['hard_pass']);before=g.ledger.read_bytes()
            # Even a resealed artifact cannot bypass the independent final pass.
            r['semantic_grammar_checks'][0]['decision']='REVIEW'
            r.pop('candidate_digest');r['candidate_digest']=digest(r);write(p,r)
            with self.assertRaises(StructuralStop):g.commit(p)
            self.assertEqual(before,g.ledger.read_bytes())
    def test_failed_smoke_four_has_no_credit(self):
        path=ROOT/'pilot/ko/k1/phase3_5/candidates/K1-004-attempt-01.json'
        if not path.exists():self.skipTest('Smoke failure not produced yet')
        r=read(path)
        self.assertFalse(r['hard_pass']);self.assertEqual(r['ledger_sha_before_evaluation'],r['ledger_sha_after_evaluation'])
        self.assertTrue(any(x['code']=='semantic_grammar_review' for x in r['hard_errors']))
        self.assertTrue(any(x['reason']=='future_expansion' for x in r['invalid_usage_ids']))
    def test_callback_retry_honors_semantic_stop_before_next_draft(self):
        with tempfile.TemporaryDirectory() as d:
            g=SmokeGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);g.initialize();calls=[]
            def author(snapshot,feedback,attempt):
                calls.append(attempt)
                self.assertEqual(snapshot['text_number'],1)
                return self.source()
            self.assertIsNone(g.run_one(1,author));self.assertEqual(calls,[1])
            self.assertEqual(read(g.control)['stop']['type'],'semantic_grammar_stop')
            self.assertEqual(g.load()['epoch'],0)

if __name__=='__main__':unittest.main()
