"""POS/context, grouping, temporal licensing and transaction regression."""
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
from k1_phase3_2_analysis import ALIAS_AUDIT, choose_entry, identity_candidate, morphology
from k1_phase3_2_resolver import analyze
from k1_phase3_2_gate import CandidateGate, StructuralStop, read, build_snapshot
from k1_phase3_retry import draft_from_pairs
from k1_phase3_1 import smoke_source

ROOT=Path(__file__).resolve().parents[1]

class BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=files();cls.f['_allowed_vocab']=cls.f['core_vocab.json']+cls.f['expansion_vocab.json'];cls.kiwi=make_kiwi()
    def test_contrast_fixtures(self):
        for c in read(ROOT/'tests/fixtures/k1_phase3_2_boundaries.json')['cases']:
            with self.subTest(case=c['id']):
                a=analyze(c['text'],self.f,255,(),(),(),self.kiwi)
                rows={(x['lemma'],x['pos'],x['sense']) for x in a['annotations'] if x['vocab_id']}
                lemmas={r[0] for r in rows}
                review=bool(a['unresolved_tokens'] or any(d.get('requires_candidate_review') for d in a['resolver_decisions']))
                self.assertEqual('REVIEW' if review else 'PASS',c['expected_status'],a)
                for row in c.get('required',[]):self.assertIn(tuple(row),rows)
                for row in c.get('forbidden',[]):self.assertNotIn(tuple(row),rows)
                for lemma in c.get('required_lemmas',[]):self.assertIn(lemma,lemmas)
                for lemma in c.get('forbidden_lemmas',[]):self.assertNotIn(lemma,lemmas)
                self.assertTrue(set(c.get('required_grammar',[]))<=set(a['grammar_used']))
                self.assertEqual(a['raw_morphology'],morphology(c['text'],self.kiwi))
                indices=[i for x in a['annotations'] for i in x['morph_indices']]
                self.assertEqual(len(indices),len(set(indices)),'Each raw index represented once')
    def test_audit_covers_all_frozen_aliases(self):
        from k1_pilot_analysis import ALIASES
        self.assertEqual({x['surface']:x['old_target'] for x in ALIAS_AUDIT},ALIASES)
        self.assertEqual(len(ALIAS_AUDIT),12)
    def test_unique_entry_does_not_override_pos(self):
        e=next(x for x in self.f['core_vocab.json'] if x['lemma']=='너')
        raw=[dict(form='네',tag='IC',start=0,length=1)]
        self.assertIsNone(choose_entry([e],'IC','너',None,raw,0))
    def test_possessive_alias_requires_np_and_nominal_evidence(self):
        text='네 책';raw=[dict(form='네',tag='NP',start=0,length=1),dict(form='책',tag='NNG',start=2,length=1)]
        self.assertEqual(identity_candidate(raw,0,text),('너','contracted_possessive',True))
        raw[0]['tag']='IC';self.assertFalse(identity_candidate(raw,0,text)[2])
    def test_numeral_alias_cannot_cross_punctuation(self):
        raw=[dict(form='네',tag='MM',start=0,length=1),dict(form=',',tag='SP',start=1,length=1),dict(form='사람',tag='NNG',start=3,length=2)]
        self.assertFalse(identity_candidate(raw,0,'네, 사람')[2])
    def test_generated_sense_cannot_override_context(self):
        a=analyze('눈이 와요.',self.f,255,(),(),(),self.kiwi)
        self.assertIn('snow',{x['sense'] for x in a['annotations']})
        from k1_phase3_2_analysis import analyze as raw_analyze
        b=raw_analyze('눈이 와요.',self.f,255,(),{'눈':'eye'},self.kiwi)
        self.assertTrue(b['unresolved_tokens'])
    def test_no_sense_default_without_positive_evidence(self):
        a=analyze('풀이 있어요.',self.f,255,(),(),(),self.kiwi)
        self.assertTrue(a['unresolved_tokens'])
    def test_existing_constrained_walk_retained(self):
        text='공원까지 친구하고 걸어요.'
        i=dict(sentence=text,surface='걸어요',vocab_id='ko_k1_0186',lemma='걷다',pos='verb',sense='walk')
        a=analyze(text,self.f,1,(),[i],['walk'],self.kiwi)
        self.assertFalse(a['unresolved_tokens']);self.assertTrue(any(d['status']=='RESOLVED' for d in a['resolver_decisions']))
    def test_hang_is_not_walk(self):
        text='가방을 벽에 걸어요.'
        i=dict(sentence=text,surface='걸어요',vocab_id='ko_k1_0186',lemma='걷다',pos='verb',sense='walk')
        a=analyze(text,self.f,1,(),[i],['walk'],self.kiwi)
        self.assertFalse(any(x['lemma']=='걷다' and x['vocab_id'] for x in a['annotations']))
        self.assertTrue(any(d.get('requires_candidate_review') for d in a['resolver_decisions']))
    def test_frozen_phase23_regression_sentences(self):
        for c in read(ROOT/'tests/fixtures/k1_phase3_2_frozen_regressions.json')['cases']:
            with self.subTest(source=c['source'],text=c['text']):
                self.assertIn(c['text'],read(ROOT/c['source'])['text_ko'])
                a=analyze(c['text'],self.f,255,(),(),(),self.kiwi)
                self.assertFalse(a['unresolved_tokens'],a)
                matches=[x for x in a['annotations'] if x['lemma']==c['lemma'] and x['vocab_id']]
                self.assertTrue(matches)
                if 'sense' in c:self.assertEqual(matches[0]['sense'],c['sense'])
                if 'grammar' in c:self.assertIn(c['grammar'],a['grammar_used'])
    def test_frozen_phase31_irregular_probes(self):
        from k1_phase3_1 import PROBES
        for lemma,text,kind in PROBES:
            with self.subTest(lemma=lemma,kind=kind):
                e=next(x for x in self.f['core_vocab.json']+self.f['expansion_vocab.json'] if x['lemma']==lemma and x['pos'] in ('verb','adjective'))
                intents=[dict(sentence=text,surface='걸었어요' if kind.endswith('past') else '걸어요',lemma=e['lemma'],pos=e['pos'],sense=e['sense'],vocab_id=e['id'])] if lemma=='걷다' else []
                a=analyze(text,self.f,255,(),intents,['walk'] if lemma=='걷다' else [],self.kiwi)
                self.assertFalse(a['unresolved_tokens'],a)
                self.assertIn(e['id'],{x['vocab_id'] for x in a['annotations']})

class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.f=files();cls.kiwi=make_kiwi()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)
        self.g=CandidateGate(self.path/'run',self.path/'ledger.json',f=self.f,kiwi=self.kiwi)
        self.g.initialize();self.initial=self.g.ledger.read_bytes()
    def tearDown(self):self.tmp.cleanup()
    def source1(self):return draft_from_pairs(ROOT/'pilot/ko/k1/phase3_retry/sources/K1-001-attempt-01.json')
    def source2(self):return draft_from_pairs(ROOT/'pilot/ko/k1/phase3_retry/sources/K1-002-attempt-01.json')
    def test_original_rice_candidate_passes_and_state_unchanged_until_commit(self):
        p,r=self.g.submit(self.source1());self.assertTrue(r['hard_pass'],r['hard_errors'])
        self.assertEqual(self.initial,self.g.ledger.read_bytes());self.g.commit(p)
        self.assertEqual(self.g.load()['epoch'],1)
    def test_actual_permission_only_and_two_smoke_transactions(self):
        p,_=self.g.submit(self.source1());self.g.commit(p);before=self.g.ledger.read_bytes()
        snap=self.g.snapshot(2);self.assertEqual(Counter(x['role'] for x in snap['entries']),dict(core=300,previous_expansion=2,current_new_expansion=2))
        p,r=self.g.submit(self.source2());self.assertTrue(r['hard_pass'],r['hard_errors']);self.assertEqual(before,self.g.ledger.read_bytes())
        self.assertEqual(set(r['planned_new_vocab_ids']),set(r['actual_new_vocab_ids']))
        self.assertEqual(r['coverage']['new_tokens_U'],2);self.assertEqual(r['coverage']['controlled_vocab_coverage'],1)
        self.g.commit(p);once=self.g.ledger.read_bytes();self.g.commit(p);self.assertEqual(once,self.g.ledger.read_bytes())
        self.assertEqual(self.g.load()['epoch'],2)
        self.assertEqual(sum(e['actual_exposure_count'] for e in self.g.load()['entries']),4)
    def test_future_vocab_reject_not_incidental(self):
        source=self.source1();source['sentences'][0]='친구도 집에 들어오고 싶어요.'
        _,r=self.g.submit(source);self.assertFalse(r['hard_pass']);self.assertTrue(any(e['code']=='future_expansion' for e in r['hard_errors']))
        self.assertNotIn('ko_k1_0386',r['incidental_previous_vocab_ids']);self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_retired_identity_reject(self):
        source=self.source1();source['generated_intents']=[dict(vocab_id='ko_k1_0603',lemma='찍다',pos='verb',sense='stamp')]
        _,r=self.g.submit(source);self.assertFalse(r['hard_pass']);self.assertTrue(any(e['code']=='retired_id_or_sense' for e in r['hard_errors']))
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_planned_new_identity_gate_not_relaxed(self):
        p,_=self.g.submit(self.source1());self.g.commit(p);before=self.g.ledger.read_bytes();source=self.source2()
        source['sentences']=[s.replace('네,','너,') for s in source['sentences']]
        _,r=self.g.submit(source);self.assertFalse(r['hard_pass']);self.assertTrue(any(e['code']=='planned_new_not_present' for e in r['hard_errors']))
        self.assertEqual(before,self.g.ledger.read_bytes())
    def test_old_ne_identity_bug_still_rejected_by_unchanged_gate(self):
        p,_=self.g.submit(self.source1());self.g.commit(p);before=self.g.ledger.read_bytes()
        import k1_phase3_2_gate as gate_module
        original=gate_module.analyze
        def emulate_old_bug(*args,**kwargs):
            a=original(*args,**kwargs)
            for x in a['annotations']:
                if x['vocab_id']=='ko_k1_0442':x.update(lemma='너',pos='pronoun',sense='you_informal',vocab_id='ko_k1_0003',role='core')
            return a
        with patch.object(gate_module,'analyze',side_effect=emulate_old_bug):
            _,r=self.g.submit(self.source2())
        self.assertFalse(r['hard_pass']);self.assertTrue(any(e['code']=='planned_new_not_present' for e in r['hard_errors']))
        self.assertEqual(before,self.g.ledger.read_bytes())
    def test_retry_isolation_then_commit(self):
        bad=self.source1();bad['sentences'][0]='친구도 집에 들어오고 싶어요.'
        _,r=self.g.submit(bad);self.assertFalse(r['hard_pass']);self.assertEqual(self.initial,self.g.ledger.read_bytes())
        p,r=self.g.submit(self.source1());self.assertTrue(r['hard_pass']);self.g.commit(p)
        state=self.g.load();self.assertEqual(state['epoch'],1);self.assertEqual(len(state['genre_history']),1)
        self.assertFalse(any(e['vocab_id']=='ko_k1_0386' and e['actual_texts'] for e in state['entries']))
    def test_atomic_crash_before_publish(self):
        p,r=self.g.submit(self.source1());self.assertTrue(r['hard_pass'])
        with self.assertRaises(OSError):self.g.commit(p,fault_at='before_publish')
        self.assertEqual(self.initial,self.g.ledger.read_bytes());self.g.commit(p);self.assertEqual(self.g.load()['epoch'],1)
    def test_atomic_crash_after_publish_recovery_once(self):
        p,r=self.g.submit(self.source1());self.assertTrue(r['hard_pass'])
        with self.assertRaises(OSError):self.g.commit(p,fault_at='after_publish')
        once=self.g.ledger.read_bytes();self.g.recover();self.g.commit(p);self.assertEqual(once,self.g.ledger.read_bytes())
    def test_003_boundary(self):
        with self.assertRaises(StructuralStop):self.g.snapshot(3)
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_wrong_pos_unique_dictionary_candidate_rejected(self):
        source=self.source1()
        import k1_phase3_2_analysis as parser
        original=parser.identity_candidate
        def corrupt(raw,index,text):
            result=original(raw,index,text)
            return ('너','invalid_test_alias',True) if raw[index]['form']=='동생' else result
        with patch.object(parser,'identity_candidate',side_effect=corrupt):
            _,r=self.g.submit(source)
        self.assertFalse(r['hard_pass']);self.assertEqual(self.initial,self.g.ledger.read_bytes())

if __name__=='__main__':unittest.main()
