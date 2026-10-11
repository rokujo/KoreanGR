"""Candidate safety, A..E regressions, constrained resolver and atomic crash tests."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import unittest
import tempfile
from copy import deepcopy
from unittest.mock import patch
from k1_candidate_gate import CandidateGate,StructuralStop,build_snapshot,read,write,seal,writer_lock
from k1_phase3 import files
from k1_phase3_1 import smoke_source,PROBES
from k1_phase3_1_resolver import walk_evidence,analyze
from k1_phase2_3 import make_kiwi

class CandidateSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.kiwi=make_kiwi();cls.f=files()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)
        self.g=CandidateGate(self.path/'run',self.path/'ledger.json',f=self.f,kiwi=self.kiwi)
        self.g.initialize();self.initial=self.g.ledger.read_bytes();self.snapshot=self.g.snapshot(1)
    def tearDown(self):self.tmp.cleanup()
    def source(self,n=3):
        feedback=None if n==1 else dict(hard_errors=[dict(code='future_expansion' if n==2 else 'length')])
        return smoke_source(self.snapshot,feedback,n)
    def walk(self,sentence='공원까지 친구하고 걸어요.',word='걸어요',intent=True,actions=('walk',)):
        i=dict(sentence=sentence,surface=word,lemma='걷다',pos='verb',sense='walk',vocab_id='ko_k1_0186') if intent else None
        return walk_evidence(sentence,word,i,actions,self.f,{e['vocab_id'] for e in self.snapshot['entries']})
    def test_snapshot_core_and_current_only(self):
        self.assertEqual(len(self.snapshot['entries']),302)
        self.assertEqual(Counter(e['role'] for e in self.snapshot['entries']),dict(core=300,current_new_expansion=2))
        self.assertEqual(len(self.snapshot['allowed_proper_names']),1);self.assertEqual(len(self.snapshot['lexical_exceptions']),5)
    def test_planned_prior_not_actual_prior(self):
        snap=build_snapshot(self.f,self.g.load(),2)
        self.assertNotIn('ko_k1_0373',{e['vocab_id'] for e in snap['entries']})
    def test_case_A_future_reject_and_not_incidental(self):
        _,r=self.g.submit(self.source(1))
        self.assertFalse(r['hard_pass']);self.assertTrue(any(x['vocab_id']=='ko_k1_0386' and x['reason']=='future_expansion' for x in r['invalid_usage_ids']))
        self.assertNotIn('ko_k1_0386',r['incidental_previous_vocab_ids'])
        self.assertEqual(self.g.ledger.read_bytes(),self.initial)
        self.assertEqual(read(self.g.control)['status'],'running')
    def test_case_B_constrained_walk(self):self.assertEqual(self.walk()['status'],'RESOLVED')
    def test_case_C_object_veto_no_walk_alias(self):
        d=self.walk('가방을 벽에 걸어요.')
        self.assertEqual(d['status'],'REVIEW');self.assertFalse(d['evidence']['no_direct_object'])
    def test_no_intent_no_resolve(self):self.assertEqual(self.walk(intent=False)['status'],'REVIEW')
    def test_no_route_no_resolve(self):self.assertEqual(self.walk('친구하고 걸어요.')['status'],'REVIEW')
    def test_no_companion_no_resolve(self):self.assertEqual(self.walk('공원까지 걸어요.')['status'],'REVIEW')
    def test_no_locomotion_scene_no_resolve(self):self.assertEqual(self.walk(actions=['hang'])['status'],'REVIEW')
    def test_invalid_inflection_rejected(self):self.assertEqual(self.walk('공원까지 친구하고 걷어요.','걷어요')['status'],'REVIEW')
    def test_raw_evidence_retained_when_resolved(self):
        f=deepcopy(self.f);f['_allowed_vocab']=f['core_vocab.json']
        sentence='공원까지 친구하고 걸어요.';i=dict(sentence=sentence,surface='걸어요',lemma='걷다',pos='verb',sense='walk',vocab_id='ko_k1_0186')
        a=analyze(sentence,f,1,[],[i],['walk'],self.kiwi)
        self.assertFalse(a['unresolved_tokens']);self.assertIn('ko_k1_0186',{x['vocab_id'] for x in a['annotations']})
        self.assertTrue(a['raw_morphology']);self.assertIn('original_annotation',a['resolver_decisions'][0])
    def test_case_D_119_rejected_without_state_change(self):
        _,r=self.g.submit(self.source(2));self.assertEqual(r['eojeol_count'],119)
        self.assertEqual({e['code'] for e in r['hard_errors']},{'length'})
        self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_case_E_135_valid_and_single_commit(self):
        p,r=self.g.submit(self.source());self.assertTrue(r['hard_pass'],r['hard_errors']);self.assertEqual(r['eojeol_count'],135)
        self.assertEqual(self.g.ledger.read_bytes(),self.initial)
        self.g.commit(p);once=self.g.ledger.read_bytes();self.g.commit(p)
        self.assertEqual(once,self.g.ledger.read_bytes())
        s=self.g.load();self.assertEqual(s['epoch'],1);self.assertEqual(sum(e['actual_exposure_count'] for e in s['entries']),2)
        self.assertEqual(len(s['genre_history']),1);self.assertEqual(len(s['scene_history']),1)
    def test_rejected_cannot_commit(self):
        p,_=self.g.submit(self.source(2))
        with self.assertRaisesRegex(StructuralStop,'Rejected'):self.g.commit(p)
        self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_three_rejections_stop_only_after_budget(self):
        for n in range(3):
            self.g.submit(self.source(2))
            self.assertEqual(read(self.g.control)['status'],'running' if n<2 else 'stopped')
            self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_crash_before_atomic_publish_no_partial_credit(self):
        p,_=self.g.submit(self.source())
        with self.assertRaises(OSError):self.g.commit(p,fault_at='before_publish')
        self.assertEqual(self.g.ledger.read_bytes(),self.initial)
        self.assertFalse((self.g.path/'texts/K1-001.json').exists())
        self.g.commit(p);self.assertEqual(self.g.load()['epoch'],1)
    def test_crash_after_publish_recovers_without_second_credit(self):
        p,_=self.g.submit(self.source())
        with self.assertRaises(OSError):self.g.commit(p,fault_at='after_publish')
        once=self.g.ledger.read_bytes();self.assertEqual(self.g.load()['epoch'],1)
        self.assertFalse((self.g.path/'texts/K1-001.json').exists())
        self.g.recover();self.g.commit(p)
        self.assertEqual(self.g.ledger.read_bytes(),once);self.assertTrue((self.g.path/'texts/K1-001.json').exists())
    def test_tampered_candidate_never_credits(self):
        p,r=self.g.submit(self.source());r['text_ko']+=' 가요.';write(p,r)
        with self.assertRaisesRegex(StructuralStop,'tampered'):self.g.commit(p)
        self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_state_corruption_stops_before_candidate(self):
        s=read(self.g.ledger);s['entries'][0]['actual_exposure_count']=1;write(self.g.ledger,s);bad=self.g.ledger.read_bytes()
        with self.assertRaisesRegex(StructuralStop,'corruption'):self.g.submit(self.source())
        self.assertEqual(read(self.g.control)['status'],'stopped');self.assertEqual(self.g.ledger.read_bytes(),bad)
    def test_analyzer_structural_failure_stops_no_credit(self):
        with patch('k1_candidate_gate.analyze',side_effect=RuntimeError('analyzer unavailable')):
            with self.assertRaises(StructuralStop):self.g.submit(self.source())
        self.assertEqual(read(self.g.control)['status'],'stopped');self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_introduction_contradiction_stops(self):
        self.g.f['vocab_review_windows.json']['entries'][0]['first_introduction_text']+=1
        with self.assertRaises(StructuralStop):self.g.submit(self.source())
        self.assertEqual(read(self.g.control)['status'],'stopped');self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_002_smoke_boundary(self):
        x=self.source();x['text_number']=2
        with self.assertRaises(StructuralStop):self.g.submit(x)
        self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_retired_intent_rejected(self):
        x=self.source();x['generated_intents'].append(dict(vocab_id='ko_k1_0603',lemma='찍다',pos='verb',sense='stamp'))
        _,r=self.g.submit(x);self.assertTrue(any(z['reason']=='retired_id_or_sense' for z in r['invalid_usage_ids']))
        self.assertFalse(r['hard_pass']);self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_unlicensed_grammar_rejected(self):
        x=self.source();x['sentences'][0]='친구는 공원에 가지 않아요.'
        _,r=self.g.submit(x);self.assertFalse(r['hard_pass']);self.assertTrue(r['unresolved_tokens'])
    def test_unknown_proper_name_rejected(self):
        x=self.source();x['sentences'][0]='민수는 공원에 가요.'
        _,r=self.g.submit(x);self.assertFalse(r['hard_pass'])
    def test_target_99_miss_is_not_blocker(self):
        _,r=self.g.submit(self.source());self.assertTrue(r['hard_pass']);self.assertFalse(r['coverage']['target_99_met'])
        self.assertGreaterEqual(r['coverage']['previous_vocab_coverage'],.98)
    def test_semantic_NO_is_candidate_repair_not_immediate_stop(self):
        x=self.source();x['semantic_evidence']['plausible_actions']=dict(verdict='NO',reason='test fixture implausible action')
        _,r=self.g.submit(x);self.assertFalse(r['hard_pass']);self.assertEqual(read(self.g.control)['status'],'running')
    def test_different_pass_candidate_cannot_double_commit(self):
        p1,_=self.g.submit(self.source());p2,_=self.g.submit(self.source())
        self.g.commit(p1);once=self.g.ledger.read_bytes()
        with self.assertRaisesRegex(StructuralStop,'Different committed'):self.g.commit(p2)
        self.assertEqual(once,self.g.ledger.read_bytes())
    def test_auxiliary_after_registered_compound(self):
        f=deepcopy(self.f);f['_allowed_vocab']=f['core_vocab.json']
        a=analyze('친구를 도와주고 싶어요.',f,1,[],[],[],self.kiwi)
        self.assertFalse(a['unresolved_tokens']);self.assertIn('ko_k1_0225',{x['vocab_id'] for x in a['annotations']})
        self.assertIn('ko_k1_g06',a['grammar_used'])
    def test_final_reanalysis_failure_no_credit(self):
        p,r=self.g.submit(self.source());bad=deepcopy(r);bad['hard_pass']=False
        with patch.object(self.g,'evaluate',return_value=bad):
            with self.assertRaisesRegex(StructuralStop,'Final reanalysis'):self.g.commit(p)
        self.assertEqual(read(self.g.control)['status'],'stopped');self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_competing_writer_refused(self):
        with writer_lock(self.g.ledger):
            with self.assertRaisesRegex(StructuralStop,'Concurrent'):self.g.submit(self.source())
        self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_walk_intent_invalid_form_rejects_whole_candidate(self):
        x=self.source();i=x['sentences'].index('공원까지 친구하고 걸어요.')
        x['sentences'][i]='공원까지 친구하고 걷어요.'
        x['generated_intents'][0].update(sentence=x['sentences'][i],surface='걷어요')
        _,r=self.g.submit(x);self.assertFalse(r['hard_pass'])
        self.assertTrue(any(e['code']=='unresolved_context_ambiguity' for e in r['hard_errors']))
    def test_malformed_draft_is_local_rejection(self):
        _,r=self.g.submit(dict(text_number=1,sentences=[]))
        self.assertFalse(r['hard_pass']);self.assertEqual({x['code'] for x in r['hard_errors']},{'candidate_format'})
        self.assertEqual(read(self.g.control)['status'],'running');self.assertEqual(self.g.ledger.read_bytes(),self.initial)
    def test_logical_history_corruption_with_recomputed_checksum(self):
        s=self.g.load();s['genre_history'].append(dict(text=1,genre='not_committed'));write(self.g.ledger,seal(s))
        with self.assertRaisesRegex(StructuralStop,'Genre history'):self.g.submit(self.source())
        self.assertEqual(read(self.g.control)['status'],'stopped')

from collections import Counter
if __name__=='__main__':unittest.main()
