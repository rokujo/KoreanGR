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
from k1_phase3_4_resolver import analyze, recover_uri
from k1_phase3_3_resolver import recover_registered_surfaces
from k1_phase3_4 import SmokeGate, source_from_pairs, PILOT
from k1_phase3_4_gate import read, ROOT, StructuralStop, CandidateGate
from jsonschema import Draft202012Validator
from build_k1_phase3_4_schemas import contracts

class QuoteRegressionTests(unittest.TestCase):
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


class UriTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=files();cls.f['_allowed_vocab']=cls.f['core_vocab.json']+cls.f['expansion_vocab.json'];cls.kiwi=make_kiwi()
    def analyze(self,text,scope='fixture'):
        return analyze(text,self.f,2,(),(),(),self.kiwi,scope=scope)
    def check_raw(self,text,a):
        self.assertEqual(a['raw_morphology'],morphology(text,self.kiwi))
        indices=[i for x in a['annotations'] for i in x['morph_indices']]
        self.assertEqual(len(indices),len(set(indices)))
        for annotation in a['annotations']:
            self.assertEqual(text[annotation['start']:annotation['end']],annotation['surface'])
    def test_positive_collocations(self):
        for text in ('우리 집에 가요.','우리 학교에 가요.','우리 가족이 와요.','"우리 집에 올 거예요?"'):
            with self.subTest(text=text):
                a=self.analyze(text)
                self.assertIn('ko_k1_0004',{x['vocab_id'] for x in a['annotations']})
                self.assertFalse(a['unresolved_tokens']);self.check_raw(text,a)
    def test_scope_parity_and_raw_pos_instability_preserved(self):
        cases=read(ROOT/'tests/fixtures/k1_phase3_4_uri_scope.json')['scope_cases']
        for case in cases:
            with self.subTest(scope=case['scope']):
                a=self.analyze(case['text'],case['scope']);self.check_raw(case['text'],a)
                self.assertFalse(a['unresolved_tokens'],a)
                for row in a['uri_recovery_audit']:
                    self.assertIn(row['decision'],('RECOVERED','ALREADY_REGISTERED'))
                if case['scope'] in ('candidate_paragraph','candidate_full_text'):
                    row=next(row for row in a['uri_recovery_audit'] if row['decision']=='RECOVERED')
                    self.assertEqual(row['raw_pos'],'NNG');self.assertTrue(all(row['context_evidence'].values()))
                    self.assertEqual(row['registered_id'],'ko_k1_0004');self.assertFalse(row['permission_granted'])
                    self.assertTrue(row['original_annotation']);self.assertTrue(row['speaker_anchors'])
    def test_noun_sense_contrasts_are_review_even_raw_np(self):
        for text in ('우리 안에 개가 있어요.','우리에서 사람이 나와요.','우리 밖에 사람이 있어요.'):
            with self.subTest(text=text):
                a=self.analyze(text);self.check_raw(text,a)
                self.assertNotIn('ko_k1_0004',{x['vocab_id'] for x in a['annotations']})
                self.assertTrue(any(d.get('requires_candidate_review') for d in a['resolver_decisions']))
    def forced_nng(self,text):
        old=old_analyze(text,self.f,2,(),(),(),self.kiwi)
        raw=next(r for r in old['raw_morphology'] if r['form']=='우리');raw['tag']='NNG'
        return recover_uri(text,old,self.f,'synthetic_raw_contrast')
    def test_nng_without_discourse_or_with_arbitrary_head_is_review(self):
        for text in ('우리 집에 가요.','저는 여기에 있어요. 우리 책을 읽어요.'):
            with self.subTest(text=text):
                a=self.forced_nng(text)
                self.assertNotIn('ko_k1_0004',{x['vocab_id'] for x in a['annotations'] if x['surface']=='우리'})
                self.assertTrue(any(d['decision']=='REVIEW' for d in a['uri_recovery_audit']))
    def test_speaker_anchor_supports_only_licensed_heads(self):
        for text in ('저는 여기에 있어요. 우리 집에 가요.','저는 학생이에요. 우리 학교에 가요.','저는 집에 있어요. 우리 가족이 와요.'):
            with self.subTest(text=text):
                a=self.forced_nng(text);self.assertTrue(any(d['decision']=='RECOVERED' for d in a['uri_recovery_audit']))
    def test_generated_intent_cannot_replace_raw_context(self):
        text='우리 안에 개가 있어요.'
        intent=[dict(surface='우리',lemma='우리',vocab_id='ko_k1_0004',pos='pronoun',sense='we',sentence=text)]
        a=analyze(text,self.f,2,(),intent,(),self.kiwi)
        self.assertNotIn('ko_k1_0004',{x['vocab_id'] for x in a['annotations']})
    def test_missing_registered_identity_or_bad_span_cannot_recover(self):
        fixture=read(ROOT/'tests/fixtures/k1_phase3_4_uri_scope.json')['scope_cases']
        text=next(c['text'] for c in fixture if c['scope']=='candidate_paragraph')
        old=old_analyze(text,self.f,2,(),(),(),self.kiwi)
        f=deepcopy(self.f);f['core_vocab.json']=[e for e in f['core_vocab.json'] if e['id']!='ko_k1_0004']
        a=recover_uri(text,old,f)
        self.assertFalse(any(d['decision']=='RECOVERED' for d in a['uri_recovery_audit']))
        next(r for r in old['raw_morphology'] if r['form']=='우리' and r['tag']=='NNG')['length']=1
        a=recover_uri(text,old,self.f)
        self.assertFalse(any(d['decision']=='RECOVERED' for d in a['uri_recovery_audit']))


class ForwardSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=read(ROOT/'pilot/ko/k1/phase3_sequential_v3/candidates/K1-001-attempt-02.json')
        cls.candidate,cls.source=contracts()
        cls.validator=Draft202012Validator(cls.candidate)
    def test_all_fifty_actual_candidate_objects(self):
        for t in range(1,51):
            with self.subTest(text=t):
                obj=deepcopy(self.template);obj.update(id=f'K1-{t:03d}',text_number=t)
                self.assertEqual(list(self.validator.iter_errors(obj)),[])
    def test_all_negative_ids_as_candidate_objects(self):
        for ident in ('K1-000','K1-051','K1-099','K1-300','K1-01','K1-1','KO-K1-001','K2-001'):
            with self.subTest(id=ident):
                obj=deepcopy(self.template);obj['id']=ident
                self.assertTrue(list(self.validator.iter_errors(obj)))
    def test_id_number_mismatch_and_wrong_hard_metrics_rejected(self):
        obj=deepcopy(self.template);obj.update(id='K1-003',text_number=2)
        self.assertFalse(self.validator.is_valid(obj))
        obj=deepcopy(self.template);obj['coverage']['controlled_vocab_coverage']=.99
        self.assertFalse(self.validator.is_valid(obj))
    def test_generated_contract_matches_pinned_json(self):
        path=ROOT/'config/languages/ko/k1/phase3_4'
        self.assertEqual(read(path/'candidate.schema.json'),self.candidate)
        self.assertEqual(read(path/'source.schema.json'),self.source)
    def test_run_range_is_generated_independently_of_smoke(self):
        schema,_=contracts(100)
        obj=deepcopy(self.template);obj.update(id='K1-100',text_number=100)
        self.assertTrue(Draft202012Validator(schema).is_valid(obj))
        self.assertFalse(self.validator.is_valid(obj))
    def test_metadata_catalog_and_unknown_rejection(self):
        source=source_from_pairs(ROOT/'pilot/ko/k1/phase3_sequential_v3/sources/K1-002-attempt-02.json')
        validator=Draft202012Validator(self.source)
        self.assertTrue(validator.is_valid(source))
        self.assertEqual(self.source['properties']['scene']['items']['enum'],files()['vocab_review_windows.json']['scene_catalog'])
        for field,value in [('scene',['weather']),('genre','unregistered_news_genre')]:
            obj=deepcopy(source);obj[field]=value;self.assertFalse(validator.is_valid(obj))
    def test_observed_particle_role_error_and_allowed_repair(self):
        from validate_k1_phase3_4 import grammar_meaning_issues
        self.assertTrue(grammar_meaning_issues('저는 사진을 선물로 주고 싶어요.'))
        self.assertEqual(grammar_meaning_issues('저는 어머니에게 사진을 주고 싶어요.'),[])
        self.assertEqual(grammar_meaning_issues('저는 버스로 학교에 가요.'),[])


class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.kiwi=make_kiwi()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name)
        self.g=SmokeGate(p/'run',p/'state.json',kiwi=self.kiwi);self.g.initialize();self.initial=self.g.ledger.read_bytes()
    def tearDown(self):self.tmp.cleanup()
    def source(self,t):
        return source_from_pairs(ROOT/f'pilot/ko/k1/phase3_sequential_v3/sources/K1-{t:03d}-attempt-02.json')
    def commit1(self):
        p,r=self.g.submit(self.source(1));self.assertTrue(r['hard_pass'],r['hard_errors']);return self.g.commit(p)
    def test_full_v3_candidate_recovery_commit_identity_and_state(self):
        self.assertFalse(any(e['actual_texts'] for e in self.g.load()['entries']))
        self.commit1();before=self.g.ledger.read_bytes()
        p,r=self.g.submit(self.source(2));self.assertTrue(r['hard_pass'],r['hard_errors'])
        self.assertEqual(before,self.g.ledger.read_bytes())
        self.assertEqual(r['planned_new_vocab_ids'],r['actual_new_vocab_ids'])
        self.assertEqual(r['coverage']['controlled_vocab_coverage'],1)
        self.assertGreaterEqual(r['coverage']['previous_vocab_coverage'],.98)
        self.assertTrue(any(d['decision']=='RECOVERED' for d in r['uri_recovery_audit']))
        self.g.commit(p);once=self.g.ledger.read_bytes();self.g.commit(p);self.assertEqual(once,self.g.ledger.read_bytes())
        self.assertEqual(self.g.load()['epoch'],2)
    def test_failed_candidate_identity_and_permission_credit_isolation(self):
        self.commit1();before=self.g.ledger.read_bytes();source=self.source(2)
        source['sentences'][0]='친구도 집에 들어오고 싶어요.'
        source['generated_intents']=[dict(vocab_id='ko_k1_0603',lemma='찍다',pos='verb',sense='stamp')]
        _,r=self.g.submit(source)
        codes={e['code'] for e in r['hard_errors']}
        self.assertTrue({'future_expansion','retired_id_or_sense'}<=codes)
        self.assertNotIn('ko_k1_0386',r['incidental_previous_vocab_ids'])
        self.assertEqual(before,self.g.ledger.read_bytes())
        self.assertIsNone(next(e for e in self.g.load()['entries'] if e['vocab_id']=='ko_k1_0442')['actual_first_text'])
    def test_planned_identity_missing_is_still_rejected(self):
        self.commit1();source=self.source(2)
        source['sentences']=[s.replace('네, 시간이 있어요.','시간이 있어요.') for s in source['sentences']]
        before=self.g.ledger.read_bytes();_,r=self.g.submit(source)
        self.assertTrue(any(e['code']=='planned_new_not_present' for e in r['hard_errors']))
        self.assertEqual(before,self.g.ledger.read_bytes())
    def test_metadata_fail_then_repair_uses_retry_without_credit(self):
        self.commit1();source=self.source(2);source['scene']=['weather']
        before=self.g.ledger.read_bytes();_,r=self.g.submit(source);self.assertFalse(r['hard_pass'])
        self.assertEqual(before,self.g.ledger.read_bytes())
        p,r=self.g.submit(self.source(2));self.assertTrue(r['hard_pass']);self.assertEqual(r['attempt_number'],2)
        self.g.commit(p);self.assertEqual(self.g.load()['epoch'],2)
    def test_atomic_fault_before_and_after_publish(self):
        p,r=self.g.submit(self.source(1));self.assertTrue(r['hard_pass'])
        with self.assertRaises(OSError):self.g.commit(p,fault_at='before_publish')
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
        with self.assertRaises(OSError):self.g.commit(p,fault_at='after_publish')
        once=self.g.ledger.read_bytes();self.g.recover();self.g.commit(p)
        self.assertEqual(once,self.g.ledger.read_bytes());self.assertEqual(self.g.load()['epoch'],1)
    def test_same_error_stagnation_stop_preserves_actual_state(self):
        source=self.source(1);source['scene']=['weather']
        self.g.submit(source);self.g.submit(source)
        self.assertEqual(read(self.g.control)['status'],'stopped')
        self.assertEqual(self.initial,self.g.ledger.read_bytes())
    def test_control_caps_snapshot_even_when_schema_allows_next(self):
        self.commit1();p,r=self.g.submit(self.source(2));self.g.commit(p)
        self.g.snapshot(3)
        with self.assertRaises(StructuralStop):self.g.snapshot(4)
        self.assertEqual(read(self.g.control)['max_text'],3)

if __name__=='__main__':unittest.main()

