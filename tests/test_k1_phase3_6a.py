import sys
from pathlib import Path
import unittest
import tempfile
from copy import deepcopy
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase3 import ROOT,files,read
from k1_phase2_3 import make_kiwi
from k1_phase3_6_resolver import analyze as previous
from k1_phase3_6a_resolver import analyze,focused_scope_parity
from k1_phase3_6a import ProductionGate,freeze_errors
from k1_phase3_6a_gate import StructuralStop

REVIEW=dict(naturalness='PASS',translation_fidelity='PASS',review_word_integration='PASS',reason='Regression fixture approval only, not human corpus approval.')

class NeResponseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=files();cls.k=make_kiwi()
        cls.failed=read(ROOT/'pilot/ko/k1/phase3_6/candidates/K1-002-attempt-01.json')
        cls.first=read(ROOT/'pilot/ko/k1/phase3_6/texts/K1-001.json')['source']

    def test_positive_probes(self):
        for s in ('네.','"네."','네, 여기 있어요.','"네, 여기 있어요."','네, 저녁에 만나요.','"네, 저녁에 만나요."'):
            with self.subTest(s=s):
                a=analyze(s,self.f,2,kiwi=self.k)
                self.assertTrue(any(x['vocab_id']=='ko_k1_0442' for x in a['annotations']))
                self.assertFalse(any(x['vocab_id']=='ko_k1_0003' for x in a['annotations']))

    def test_possessive_and_numeral_contrasts(self):
        for s in ('네 책','네 가방','네 사람이 와요.'):
            a=analyze(s,self.f,2,kiwi=self.k)
            self.assertFalse(any(x['vocab_id']=='ko_k1_0442' for x in a['annotations']))
            self.assertFalse(any(r['decision']=='RECOVERED' for r in a['ne_response_recovery_audit']))

    def test_original_failed_full_raw_reproduction(self):
        s=self.failed['text_ko'];a=analyze(s,self.f,2,kiwi=self.k,scope='full_fixture')
        baseline=previous(s,self.f,2,kiwi=self.k)
        self.assertEqual(baseline['raw_morphology'],a['raw_morphology'])
        at=s.index('네,')
        self.assertEqual(['ko_k1_0442'],[x['vocab_id'] for x in a['annotations'] if x['start']==at and x['vocab_id']])
        rows=[r for r in a['ne_response_recovery_audit'] if r['start']==at]
        self.assertEqual('RECOVERED',rows[0]['decision']);self.assertTrue(all(rows[0]['evidence'].values()))
        self.assertEqual(['너','의'],rows[0]['raw_parts']);self.assertEqual(['NP','JKG'],rows[0]['raw_tags'])
        self.assertNotIn('ko_k1_g29',a['grammar_used'])

    def test_scope_parity_full_fixture(self):
        s=self.failed['text_ko'];sentences=self.failed['source']['sentences']
        short=[analyze(x,self.f,2,kiwi=self.k,scope='sentence') for x in sentences]
        full=analyze(s,self.f,2,kiwi=self.k,scope='full')
        rows=focused_scope_parity(s,full,sentences,short,self.f,2,['ko_k1_0442','ko_k1_0443'],kiwi=self.k)
        self.assertFalse(any(r['structural_defect'] for r in rows))
        ne=[r for r in rows if r['surface']=='네']
        self.assertEqual(1,len(ne));self.assertEqual('RECOVERED_SAFE',ne[0]['decision'])

    def test_missing_short_evidence_not_accepted(self):
        real=previous(self.failed['text_ko'],self.f,2,kiwi=self.k)
        def fake(text,*args,**kwargs):
            if text==self.failed['text_ko']:return deepcopy(real)
            return dict(annotations=[],raw_morphology=[],resolver_decisions=[],unresolved_tokens=[],annotation_review_required=[],grammar_used=[])
        with patch('k1_phase3_6a_resolver.previous_analyze',side_effect=fake):
            a=analyze(self.failed['text_ko'],self.f,2,kiwi=self.k)
        self.assertFalse(any(r['decision']=='RECOVERED' for r in a['ne_response_recovery_audit']))
        self.assertTrue(any(r.get('requires_candidate_review') for r in a['resolver_decisions']))

    def test_annotation_not_authority(self):
        a=analyze('네 책',self.f,2,intents=[dict(vocab_id='ko_k1_0442',lemma='네',pos='interjection',sense='yes')],kiwi=self.k)
        self.assertFalse(any(x['vocab_id']=='ko_k1_0442' for x in a['annotations']))

    def test_registered_vs_registered_mismatch_detection(self):
        text='"네, 여기 있어요."'
        good=analyze(text,self.f,2,kiwi=self.k)
        bad=deepcopy(good);bad['ne_response_recovery_audit']=[]
        for x in bad['annotations']:
            if x['vocab_id']=='ko_k1_0442':x.update(vocab_id='ko_k1_0003',lemma='너',pos='pronoun',sense='you_informal')
        rows=focused_scope_parity(text,bad,[text],[good],self.f,2,['ko_k1_0442'],kiwi=self.k)
        self.assertTrue(any(r['type']=='SCOPE_IDENTITY_MISMATCH' and r['structural_defect'] for r in rows))

    def test_other_recoveries_and_drink_preserved(self):
        for s,target in [('"아니요, 책이 비싸요."','ko_k1_0443'),('"한국어 책이 있어요?"','ko_k1_0169'),
                         ('"우리 집에 올 거예요?"','ko_k1_0004')]:
            a=analyze(s,self.f,2,kiwi=self.k)
            self.assertTrue(any(x['vocab_id']==target for x in a['annotations']))
        a=analyze('저는 물을 받고 마셔요.',self.f,2,kiwi=self.k)
        self.assertTrue(any(x['lemma']=='마시다' for x in a['annotations']));self.assertFalse(a['unresolved_tokens'])

    def test_historical_freeze(self):self.assertFalse(freeze_errors())

    def test_new_gate_full_fixture_and_atomic_state(self):
        with tempfile.TemporaryDirectory() as d:
            g=ProductionGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);g.initialize()
            p,c=g.submit(self.first);self.assertTrue(c['hard_pass'],c['hard_errors']);g.approve(p,REVIEW);g.commit(p)
            before=g.ledger.read_bytes();p,c=g.submit(self.failed['source'])
            self.assertEqual(before,g.ledger.read_bytes());self.assertTrue(c['hard_pass'],c['hard_errors'])
            self.assertEqual(c['planned_new_vocab_ids'],c['actual_new_vocab_ids'])
            self.assertEqual(2,c['coverage']['new_tokens_U']);self.assertEqual(1,c['coverage']['controlled_vocab_coverage'])
            self.assertGreaterEqual(c['coverage']['previous_vocab_coverage'],.98)
            g.approve(p,REVIEW);g.commit(p);self.assertEqual(2,g.load()['epoch'])
            g.commit(p);self.assertEqual(2,g.load()['epoch'])

    def test_unresolved_parity_stops_without_credit(self):
        with tempfile.TemporaryDirectory() as d:
            g=ProductionGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);g.initialize();before=g.ledger.read_bytes()
            with patch('k1_phase3_6a_gate.focused_scope_parity',return_value=[dict(type='SCOPE_IDENTITY_MISMATCH',structural_defect=True)]):
                p,c=g.submit(self.first)
            self.assertFalse(c['hard_pass']);self.assertEqual('stopped',read(g.control)['status'])
            self.assertEqual(before,g.ledger.read_bytes())

    def test_future_response_not_licensed_by_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            g=ProductionGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);g.initialize()
            src=deepcopy(self.first);src['sentences'].append('"네."');src['translations_ja'].append('「はい。」')
            _,c=g.submit(src);self.assertFalse(c['hard_pass'])
            self.assertTrue(any(x['vocab_id']=='ko_k1_0442' and x['reason']=='future_expansion' for x in c['invalid_usage_ids']))

