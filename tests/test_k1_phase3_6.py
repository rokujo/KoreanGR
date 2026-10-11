import sys
from pathlib import Path
import tempfile
import unittest
from copy import deepcopy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase3 import ROOT,files,read
from k1_phase2_3 import make_kiwi
from k1_phase3_4_resolver import analyze as raw_previous
from k1_phase3_6_resolver import analyze
from k1_phase3_6 import ProductionGate,freeze_errors
from k1_phase3_6_gate import StructuralStop,construction_errors

REVIEW=dict(naturalness='PASS',translation_fidelity='PASS',review_word_integration='PASS',reason='Regression fixture approval only, not corpus human approval.')

class ProductionLiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=files();cls.k=make_kiwi()
        cls.source=read(ROOT/'pilot/ko/k1/phase3_5/sources/K1-001-attempt-01.json')

    def gate(self,d):
        g=ProductionGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);g.initialize();return g

    def test_frozen_history(self):self.assertEqual([],freeze_errors())

    def test_drink_scope_and_raw_preservation(self):
        sentence='저는 물을 받고 마셔요.'
        for scope,text in [('sentence',sentence),('quoted','"'+sentence+'"'),
                           ('paragraph','오늘은 학교에 가요. '+sentence+' 저는 책을 읽어요.'),
                           ('full',' '.join(self.source['sentences'][:10])+sentence+' '.join(self.source['sentences'][10:]))]:
            a=analyze(text,self.f,1,kiwi=self.k,scope=scope)
            b=raw_previous(text,self.f,1,kiwi=self.k,scope=scope)
            self.assertEqual(a['raw_morphology'],b['raw_morphology'])
            recovered=[x for x in a['annotations'] if x['lemma']=='마시다']
            self.assertEqual(1,len(recovered));self.assertFalse(a['unresolved_tokens'])
            for x in a['drink_recovery_audit']:
                self.assertEqual('PASS',x['decision']);self.assertEqual('마셔요',text[x['start']:x['end']])

    def test_drink_normal_form_unchanged(self):
        for text in ('저는 물을 마셔요.','저는 물을 받아요. 저는 물을 마셔요.'):
            a=analyze(text,self.f,1,kiwi=self.k)
            self.assertFalse(a['drink_recovery_audit'])
            self.assertTrue(any(x['lemma']=='마시다' for x in a['annotations']))

    def test_no_global_drink_alias(self):
        for text in ('받고 마셔요.','책을 받고 마셔요.','하지 마세요.','물을 받고 마세요.','물을 받고 마셔요가 있어요.'):
            a=analyze(text,self.f,1,kiwi=self.k)
            self.assertFalse(a['drink_recovery_audit'])
        a=analyze('책을 받고 마셔요.',self.f,1,intents=[dict(lemma='마시다',pos='verb',sense='drink')],kiwi=self.k)
        self.assertFalse(a['drink_recovery_audit'])

    def test_semantic_role_fail_warning_not_coverage(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d);src=deepcopy(self.source)
            src['sentences'].insert(3,'사진을 선물로 주고 싶어요.')
            src['translations_ja'].insert(3,'写真を贈り物として渡したいです。')
            p,r=g.submit(src)
            self.assertTrue(r['hard_pass'],r['hard_errors'])
            self.assertTrue(any(c['grammar_id']=='ko_k1_g30' and c['decision']=='FAIL' for c in r['semantic_grammar_warnings']))
            self.assertEqual(1,r['coverage']['controlled_vocab_coverage'])
            g.approve(p,REVIEW);g.commit(p);self.assertEqual(1,g.load()['epoch'])

    def test_basic_semantic_reviews_do_not_block(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d);src=deepcopy(self.source)
            src['sentences'].append('어머니에게 사진을 받아요.')
            src['translations_ja'].append('母から写真を受け取ります。')
            p,r=g.submit(src)
            self.assertTrue(r['semantic_grammar_warnings']);self.assertTrue(r['hard_pass'])
            self.assertFalse(any(e['code'].startswith('semantic_grammar') for e in r['hard_errors']))

    def test_explicit_unapproved_forms(self):
        for text in ('가지 않아요.','친구는 먹고 싶어해요.','선물로서 줘요.','연필으로써 써요.'):
            self.assertTrue(construction_errors(text,'body'))
        for text in ('사진을 선물로 줘요.','학교에서 집으로 와요.','어머니에게 사진을 받아요.'):
            self.assertFalse(construction_errors(text,'body'))

    def test_future_and_failed_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d);before=g.ledger.read_bytes();src=deepcopy(self.source)
            src['sentences'][0]='친구도 집에 들어오고 싶어요.'
            p,r=g.submit(src)
            self.assertFalse(r['hard_pass']);self.assertTrue(any(x['reason']=='future_expansion' for x in r['invalid_usage_ids']))
            self.assertNotIn('ko_k1_0386',r['incidental_previous_vocab_ids'])
            self.assertEqual(before,g.ledger.read_bytes())

    def test_post_mechanical_author_approval_required(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d);p,r=g.submit(self.source)
            self.assertTrue(r['hard_pass'])
            with self.assertRaises(FileNotFoundError):g._commit_locked(p)
            self.assertEqual(0,g.load()['epoch'])

    def test_atomic_commit_and_replay_once(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d);p,r=g.submit(self.source);g.approve(p,REVIEW);before=g.ledger.read_bytes()
            with self.assertRaises(OSError):g.commit(p,fault_at='before_publish')
            self.assertEqual(before,g.ledger.read_bytes())
            with self.assertRaises(OSError):g.commit(p,fault_at='after_publish')
            self.assertEqual(1,g.load()['epoch']);g.commit(p);self.assertEqual(1,g.load()['epoch'])

    def test_callback_gets_only_actual_snapshot_before_draft(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d);seen=[]
            def author(snap,feedback,attempt):
                seen.append(snap)
                self.assertEqual(302,len(snap['entries']))
                self.assertFalse(any(x['lemma']=='물어보다' for x in snap['entries']))
                return deepcopy(self.source)
            g.run_one(1,author,lambda r:REVIEW)
            self.assertEqual(1,len(seen));self.assertEqual(1,g.load()['epoch'])

    def test_planned_identity_gate_not_relaxed(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d);src=deepcopy(self.source)
            src['sentences']=[s.replace('괜찮아요','좋아요') for s in src['sentences']]
            p,r=g.submit(src);self.assertFalse(r['hard_pass'])
            self.assertTrue(any(e['code']=='planned_new_not_present' for e in r['hard_errors']))

    def test_title_has_same_policy(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d);src=deepcopy(self.source);src['title_ko']='들어오는 친구'
            _,r=g.submit(src);self.assertFalse(r['hard_pass']);self.assertTrue(any(e['code']=='title_permission' for e in r['hard_errors']))

    def test_same_error_stagnation_stops(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d);src=deepcopy(self.source);src['sentences']=src['sentences'][:10];src['translations_ja']=src['translations_ja'][:10]
            g.submit(src);g.submit(src)
            self.assertEqual('stopped',read(g.control)['status']);self.assertEqual(0,g.load()['epoch'])

    def test_numerical_bounds(self):
        with tempfile.TemporaryDirectory() as d:
            g=self.gate(d)
            with self.assertRaises(StructuralStop):g.snapshot(11)

