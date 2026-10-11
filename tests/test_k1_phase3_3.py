"""Quotation parity, exact evidence negatives, frozen regressions, atomic smoke."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from copy import deepcopy
from collections import Counter
import tempfile
import unittest
from unittest.mock import patch
from k1_phase3 import files
from k1_phase2_3 import make_kiwi
from k1_phase3_2_analysis import morphology
from k1_phase3_2_resolver import analyze as old_analyze
from k1_phase3_3_resolver import analyze, recover_registered_surfaces
from k1_phase3_3 import SmokeGate, replay_source, PILOT
from k1_phase3_3_gate import read, ROOT, StructuralStop

class RecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=files();cls.f['_allowed_vocab']=cls.f['core_vocab.json']+cls.f['expansion_vocab.json'];cls.kiwi=make_kiwi()
        cls.fixture=read(ROOT/'tests/fixtures/k1_phase3_3_quote_parity.json')
    def analyze(self,text):return analyze(text,self.f,2,(),(),(),self.kiwi)
    def assert_raw_spans(self,text,a):
        self.assertEqual(a['raw_morphology'],morphology(text,self.kiwi))
        ids=[i for x in a['annotations'] for i in x['morph_indices']]
        self.assertEqual(len(ids),len(set(ids)))
        for x in a['annotations']:self.assertEqual(text[x['start']:x['end']],x['surface'])
    def test_quoted_unquoted_parity(self):
        for p in self.fixture['parity_pairs']:
            plain=self.analyze(p['content']);quoted=self.analyze('"'+p['content']+'"')
            with self.subTest(content=p['content']):
                for a in (plain,quoted):
                    self.assertFalse(a['unresolved_tokens'],a)
                    self.assertIn(p['identity'],{x['vocab_id'] for x in a['annotations']})
                identity=lambda a:[(x['lemma'],x['pos'],x['sense'],x['vocab_id']) for x in a['annotations'] if x['vocab_id']]
                self.assertEqual(identity(plain),identity(quoted))
                self.assert_raw_spans(p['content'],plain);self.assert_raw_spans('"'+p['content']+'"',quoted)
    def test_paragraph_multiple_turns_and_offsets(self):
        for text in self.fixture['paragraphs']:
            with self.subTest(text=text):
                a=self.analyze(text);self.assertFalse(a['unresolved_tokens'],a);self.assert_raw_spans(text,a)
                self.assertIn('ko_k1_0443',{x['vocab_id'] for x in a['annotations']})
    def test_no_unsafe_reassembly(self):
        for text in self.fixture['no_recovery']:
            with self.subTest(text=text):
                a=self.analyze(text);self.assertFalse(any(d['decision']=='RECOVERED' for d in a['quote_recovery_audit']),a)
                self.assert_raw_spans(text,a)
    def test_core_anida_not_absorbed(self):
        for text in self.fixture['unchanged_anida']:
            a=self.analyze(text);self.assertIn('ko_k1_0041',{x['vocab_id'] for x in a['annotations']})
            self.assertNotIn('ko_k1_0443',{x['vocab_id'] for x in a['annotations']})
    def test_audit_full_evidence(self):
        a=self.analyze('"아니요, 책이 너무 비싸요."')
        d=next(d for d in a['quote_recovery_audit'] if d['decision']=='RECOVERED')
        self.assertEqual(d['raw_tags'],['VCN','EC']);self.assertEqual(d['raw_parts'],['아니','요'])
        self.assertEqual((d['start'],d['end']),(1,4));self.assertTrue(all(d['evidence'].values()))
        self.assertFalse(d['permission_granted']);self.assertTrue(d['quotation_context']['inside_balanced'])
    def test_missing_registered_identity_cannot_recover(self):
        text='"아니요, 책이 너무 비싸요."';old=old_analyze(text,self.f,2,(),(),(),self.kiwi)
        f=deepcopy(self.f);f['expansion_vocab.json']=[e for e in f['expansion_vocab.json'] if e['id']!='ko_k1_0443']
        a=recover_registered_surfaces(text,old,f,2)
        self.assertFalse(any(d['decision']=='RECOVERED' for d in a['quote_recovery_audit']))
    def test_raw_pos_mismatch_not_repaired(self):
        text='"한국어 책이 있어요?"';old=old_analyze(text,self.f,2,(),(),(),self.kiwi)
        t=next(r for r in old['raw_morphology'] if r['form']=='한');t['tag']='VV'
        a=recover_registered_surfaces(text,old,self.f,2)
        self.assertFalse(any(d['decision']=='RECOVERED' for d in a['quote_recovery_audit']))
    def test_raw_nonconsecutive_or_overlapping_not_repaired(self):
        text='"한국어 책이 있어요?"';old=old_analyze(text,self.f,2,(),(),(),self.kiwi)
        next(r for r in old['raw_morphology'] if r['form']=='국어')['start']-=1
        a=recover_registered_surfaces(text,old,self.f,2)
        self.assertFalse(any(d['decision']=='RECOVERED' for d in a['quote_recovery_audit']))
    def test_smart_quotes_keep_offsets(self):
        text='친구가 말해요. “아니요, 책이 너무 비싸요.”'
        a=self.analyze(text);self.assertFalse(a['unresolved_tokens'],a);self.assert_raw_spans(text,a)
        self.assertIn('ko_k1_0443',{x['vocab_id'] for x in a['annotations']})
    def test_all_phase32_contrast_fixtures_on_new_layer(self):
        for c in read(ROOT/'tests/fixtures/k1_phase3_2_boundaries.json')['cases']:
            with self.subTest(id=c['id']):
                a=analyze(c['text'],self.f,255,(),(),(),self.kiwi)
                rows={(x['lemma'],x['pos'],x['sense']) for x in a['annotations'] if x['vocab_id']}
                review=bool(a['unresolved_tokens'] or any(d.get('requires_candidate_review') for d in a['resolver_decisions']))
                self.assertEqual('REVIEW' if review else 'PASS',c['expected_status'])
                for r in c.get('required',[]):self.assertIn(tuple(r),rows)
                for r in c.get('forbidden',[]):self.assertNotIn(tuple(r),rows)
                for lemma in c.get('required_lemmas',[]):self.assertIn(lemma,{r[0] for r in rows})
                for lemma in c.get('forbidden_lemmas',[]):self.assertNotIn(lemma,{r[0] for r in rows})
                self.assertTrue(set(c.get('required_grammar',[]))<=set(a['grammar_used']))
                self.assert_raw_spans(c['text'],a)
    def test_frozen_phase23_fixtures_on_new_layer(self):
        for c in read(ROOT/'tests/fixtures/k1_phase3_2_frozen_regressions.json')['cases']:
            a=analyze(c['text'],self.f,255,(),(),(),self.kiwi)
            self.assertFalse(a['unresolved_tokens'],a)
            self.assertTrue(any(x['lemma']==c['lemma'] and x['vocab_id'] for x in a['annotations']))
    def test_irregular_and_limited_walk_on_new_layer(self):
        from k1_phase3_1 import PROBES
        for lemma,text,kind in PROBES:
            e=next(e for e in self.f['core_vocab.json']+self.f['expansion_vocab.json'] if e['lemma']==lemma and e['pos'] in ('verb','adjective'))
            intents=[dict(sentence=text,surface='걸었어요' if kind.endswith('past') else '걸어요',lemma=e['lemma'],pos=e['pos'],sense=e['sense'],vocab_id=e['id'])] if lemma=='걷다' else []
            a=analyze(text,self.f,255,(),intents,['walk'] if lemma=='걷다' else [],self.kiwi)
            self.assertFalse(a['unresolved_tokens'],a);self.assertIn(e['id'],{x['vocab_id'] for x in a['annotations']})

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.kiwi=make_kiwi()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name)
        self.g=SmokeGate(p/'run',p/'state.json',kiwi=self.kiwi);self.g.initialize();self.initial=self.g.ledger.read_bytes()
    def tearDown(self):self.tmp.cleanup()
    def commit1(self):
        _,source=replay_source(1);p,r=self.g.submit(source);self.assertTrue(r['hard_pass'],r['hard_errors']);self.g.commit(p)
    def test_original_full_failed002_identity_fixed_draft_errors_retained(self):
        self.commit1();before=self.g.ledger.read_bytes();_,source=replay_source(2)
        _,r=self.g.submit(source);self.assertFalse(r['hard_pass'])
        self.assertEqual(r['planned_new_vocab_ids'],r['actual_new_vocab_ids'])
        self.assertTrue(any(e['code']=='future_expansion' and e['detail']['lemma']=='열리다' for e in r['hard_errors']))
        self.assertTrue(any(e['code']=='title_permission' for e in r['hard_errors']))
        self.assertFalse(any(x['lemma'] in ('요','국어') for x in r['unresolved_tokens']))
        self.assertEqual(before,self.g.ledger.read_bytes());self.assertEqual(len(r['quote_recovery_audit']),2)
        self.assertTrue(all(d['decision']=='RECOVERED' for d in r['quote_recovery_audit']))
    def test_reject_repair_commit_only_two_transactions(self):
        self.commit1();before=self.g.ledger.read_bytes();_,bad=replay_source(2);self.g.submit(bad)
        self.assertEqual(before,self.g.ledger.read_bytes());_,good=replay_source(2,2);p,r=self.g.submit(good)
        self.assertTrue(r['hard_pass'],r['hard_errors']);self.assertEqual(before,self.g.ledger.read_bytes())
        self.assertEqual(r['coverage']['new_tokens_U'],2);self.assertEqual(r['coverage']['controlled_vocab_coverage'],1)
        self.assertGreaterEqual(r['coverage']['previous_vocab_coverage'],.98)
        self.g.commit(p);once=self.g.ledger.read_bytes();self.g.commit(p);self.assertEqual(once,self.g.ledger.read_bytes())
        state=self.g.load();self.assertEqual(state['epoch'],2);self.assertEqual(len(state['genre_history']),2)
        self.assertFalse(any(e['vocab_id']=='ko_k1_0594' and e['actual_texts'] for e in state['entries']))
        with self.assertRaises(StructuralStop):self.g.snapshot(3)
    def test_recovery_does_not_allow_future_interjection(self):
        _,source=replay_source(1);source['sentences'][0]='"아니요, 책이 너무 비싸요."'
        _,r=self.g.submit(source);self.assertFalse(r['hard_pass'])
        self.assertTrue(any(e['code']=='future_expansion' and e['detail']['vocab_id']=='ko_k1_0443' for e in r['hard_errors']))
        self.assertNotIn('ko_k1_0443',r['incidental_previous_vocab_ids']);self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_planned_identity_gate_unchanged(self):
        self.commit1();_,source=replay_source(2,2)
        source['sentences']=[s.replace('아니요,','아니에요,') for s in source['sentences']]
        before=self.g.ledger.read_bytes();_,r=self.g.submit(source)
        self.assertFalse(r['hard_pass']);self.assertTrue(any(e['code']=='planned_new_not_present' for e in r['hard_errors']))
        self.assertEqual(before,self.g.ledger.read_bytes())
    def test_retired_intent_and_future_title_rejected(self):
        _,source=replay_source(1);source['title_ko']='친구가 들어와요'
        source['generated_intents']=[dict(vocab_id='ko_k1_0603',lemma='찍다',pos='verb',sense='stamp')]
        _,r=self.g.submit(source);self.assertFalse(r['hard_pass'])
        self.assertTrue(any(e['code']=='retired_id_or_sense' for e in r['hard_errors']))
        self.assertTrue(any(e['code']=='title_permission' for e in r['hard_errors']))
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_future_attributive_title_alone_rejected(self):
        self.commit1();before=self.g.ledger.read_bytes();_,source=replay_source(2,2)
        source['title_ko']='동생에게 줄 책'
        _,r=self.g.submit(source);self.assertFalse(r['hard_pass'])
        self.assertEqual(r['planned_new_vocab_ids'],r['actual_new_vocab_ids'])
        self.assertEqual({e['code'] for e in r['hard_errors']},{'title_permission'})
        self.assertEqual(before,self.g.ledger.read_bytes())
    def test_atomic_fault_before_and_after_publish(self):
        _,source=replay_source(1);p,r=self.g.submit(source);self.assertTrue(r['hard_pass'])
        with self.assertRaises(OSError):self.g.commit(p,fault_at='before_publish')
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
        with self.assertRaises(OSError):self.g.commit(p,fault_at='after_publish')
        once=self.g.ledger.read_bytes();self.g.recover();self.g.commit(p);self.assertEqual(once,self.g.ledger.read_bytes())
        self.assertEqual(self.g.load()['epoch'],1)

if __name__=='__main__':unittest.main()
