import sys
import unittest
import tempfile
from copy import deepcopy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase3 import files,read,ROOT
from k1_phase2_3 import make_kiwi
from k1_phase3_6a_resolver import analyze as old_analyze
from k1_phase3_6c_resolver import analyze,recover,focused_scope_parity,REGISTRY
from k1_phase3_6c import ProductionGate

class ControlledSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=files();first={i:r['text'] for r in cls.f['introduction_schedule.json']['rows'] for i in r['entry_ids']}
        cls.f['_allowed_vocab']=cls.f['core_vocab.json']+[e for e in cls.f['expansion_vocab.json'] if first[e['id']]<=7]
        cls.k=make_kiwi();cls.failed=read(ROOT/'pilot/ko/k1/phase3_6b/candidates/K1-007-attempt-01.json')

    def test_all_800_classified_without_added_identity(self):
        reg=read(REGISTRY);entries=reg['entries'];v=self.f['core_vocab.json']+self.f['expansion_vocab.json']
        self.assertEqual(800,len(entries));self.assertEqual({e['id'] for e in v},{e['vocab_id'] for e in entries})
        self.assertTrue(all(e['classification'] in ('unique_safe','context_required','morphology_required') for e in entries))
        for e in entries:self.assertEqual([e['lemma']],e['registered_surfaces'])

    def test_failed_007_full_exact_identity_and_raw_preservation(self):
        text=self.failed['text_ko'];old=old_analyze(text,self.f,7,kiwi=self.k);a=analyze(text,self.f,7,kiwi=self.k,scope='full_fixture')
        at=text.index('우리는 한국어');self.assertEqual(old['raw_morphology'],a['raw_morphology'])
        hit=[r for r in a['controlled_surface_recovery_audit'] if r['start']==at][0]
        self.assertEqual('RECOVERED',hit['decision']);self.assertEqual('NNG',hit['raw_parts'][0]['tag'])
        self.assertTrue(all(hit['evidence'].values()));self.assertEqual('ko_k1_0004',[x['vocab_id'] for x in a['annotations'] if x['start']==at][0])
        self.assertFalse(any(x.get('requires_candidate_review') for x in a['resolver_decisions'] if x.get('start')==at))

    def test_sentence_paragraph_full_parity(self):
        c=self.failed;ss=c['source']['sentences'];a=analyze(c['text_ko'],self.f,7,kiwi=self.k)
        short=[analyze(x,self.f,7,kiwi=self.k) for x in ss]
        rows=focused_scope_parity(c['text_ko'],a,ss,short,self.f,7,c['planned_new_vocab_ids'],kiwi=self.k)
        self.assertFalse(any(r['structural_defect'] for r in rows))
        at=c['text_ko'].index('우리는 한국어');self.assertEqual('RECOVERED_SAFE',[r['decision'] for r in rows if r['start']==at][0])

    def test_spatial_noun_contrasts(self):
        for text in ('우리 안에 개가 있어요.','우리 밖에 개가 있어요.','우리에서 나가요.','저는 개를 봐요. 우리는 비싸요.'):
            a=analyze(text,self.f,7,kiwi=self.k)
            self.assertFalse(any(r['decision']=='RECOVERED' for r in a['controlled_surface_recovery_audit'] if r['surface']=='우리'),text)

    def test_existing_uri_modifier(self):
        for text in ('우리 집에 가요.','우리 학교에 가요.','우리 가족이 와요.','"우리 집에 올 거예요?"'):
            a=analyze('저는 친구하고 이야기해요. '+text,self.f,7,kiwi=self.k)
            self.assertTrue(any(x['vocab_id']=='ko_k1_0004' for x in a['annotations']),text)

    def test_ne_no_korean_parity_and_contrasts(self):
        for text,target in [('네.','ko_k1_0442'),('네, 여기 있어요.','ko_k1_0442'),('아니요.','ko_k1_0443'),('아니요, 책이 비싸요.','ko_k1_0443'),('한국어 책이 있어요?','ko_k1_0169')]:
            for content in (text,'"'+text+'"'):
                a=analyze(content,self.f,7,kiwi=self.k);self.assertTrue(any(x['vocab_id']==target for x in a['annotations']))
        for text in ('네 책','네 가방','네 사람이 와요.'):
            a=analyze(text,self.f,7,kiwi=self.k);self.assertFalse(any(x['vocab_id']=='ko_k1_0442' for x in a['annotations']))

    def synthetic(self):
        text='학교에 가요.';a=old_analyze(text,self.f,7,kiwi=self.k)
        x=next(x for x in a['annotations'] if x['lemma']=='학교')
        x.update(vocab_id=None,pos=None,sense=None,role='unresolved');a['raw_morphology'][x['morph_indices'][0]]['tag']='MAG'
        return text,a

    def test_unique_safe_exact_nominal_recovery(self):
        text,a=self.synthetic();before=deepcopy(a['raw_morphology']);b=recover(text,a,self.f,7,kiwi=self.k)
        self.assertEqual(before,b['raw_morphology']);self.assertTrue(any(x['vocab_id'] and x['lemma']=='학교' for x in b['annotations']))
        self.assertTrue(any(r['classification']=='unique_safe' and r['decision']=='RECOVERED' for r in b['controlled_surface_recovery_audit']))

    def test_annotation_conflict_not_overwritten(self):
        text,a=self.synthetic();x=next(x for x in a['annotations'] if x['lemma']=='학교');x['vocab_id']='ko_k1_0001'
        b=recover(text,a,self.f,7,kiwi=self.k);self.assertFalse(any(r['decision']=='RECOVERED' for r in b['controlled_surface_recovery_audit']))

    def test_span_overlap_not_overwritten(self):
        text,a=self.synthetic();x=next(x for x in a['annotations'] if x['lemma']=='학교');x['end']+=1
        b=recover(text,a,self.f,7,kiwi=self.k);self.assertFalse(any(r['decision']=='RECOVERED' for r in b['controlled_surface_recovery_audit']))

    def test_punctuation_whitespace_never_assembled(self):
        for text in ('학 교에 가요.','학"교에 가요.','한 국어 책이 있어요?','아니"요.'):
            a=analyze(text,self.f,7,kiwi=self.k)
            self.assertFalse(any(r['decision']=='RECOVERED' for r in a['controlled_surface_recovery_audit']))

    def test_current_snapshot_only(self):
        f=deepcopy(self.f);f['_allowed_vocab']=[e for e in f['_allowed_vocab'] if e['lemma']!='학교']
        text,a=self.synthetic();b=recover(text,a,f,7,kiwi=self.k)
        self.assertFalse(any(r['surface']=='학교' for r in b['controlled_surface_recovery_audit']))

    def test_future_and_retired_not_recovered(self):
        f=deepcopy(self.f);f['_allowed_vocab']=f['core_vocab.json']
        for text in ('친구가 집에 들어와요.','부엌에서 요리해요.'):
            a=analyze(text,f,1,kiwi=self.k)
            self.assertTrue(all(r['registered_vocab_id'] in {e['id'] for e in f['_allowed_vocab']} for r in a['controlled_surface_recovery_audit']))

    def test_predicate_and_homograph_no_generic_matching(self):
        for text in ('가방을 벽에 걸어요.','네 책','우리에서 나가요.'):
            a=analyze(text,self.f,7,kiwi=self.k)
            self.assertFalse(any(r['decision']=='RECOVERED' for r in a['controlled_surface_recovery_audit']))

    def test_different_registered_ids_still_mismatch(self):
        text='"네, 여기 있어요."';good=analyze(text,self.f,7,kiwi=self.k);bad=deepcopy(good)
        bad['ne_response_recovery_audit']=[];bad['controlled_surface_recovery_audit']=[]
        for x in bad['annotations']:
            if x['vocab_id']=='ko_k1_0442':x.update(vocab_id='ko_k1_0003',lemma='너',pos='pronoun',sense='you_informal')
        rows=focused_scope_parity(text,bad,[text],[good],self.f,7,['ko_k1_0442'],kiwi=self.k)
        self.assertTrue(any(x['structural_defect'] for x in rows))

    def test_new_run_gate_atomic_and_failed_isolation(self):
        # Regression prose is a test fixture, never a production manuscript.
        first=read(ROOT/'pilot/ko/k1/phase3_6b/texts/K1-001.json')['source']
        with tempfile.TemporaryDirectory() as d:
            gate=ProductionGate(Path(d)/'run',Path(d)/'ledger.json',kiwi=self.k);gate.initialize()
            initial=gate.ledger.read_bytes();bad=deepcopy(first);bad['sentences']=bad['sentences'][:2];bad['translations_ja']=bad['translations_ja'][:2]
            p,c=gate.submit(bad);self.assertFalse(c['hard_pass']);self.assertEqual(initial,gate.ledger.read_bytes())
            p,c=gate.submit(first);self.assertTrue(c['hard_pass'],c['hard_errors'])
            gate.approve(p,dict(naturalness='PASS',translation_fidelity='PASS',review_word_integration='PASS',reason='Fixture only'))
            gate.commit(p);gate.commit(p);self.assertEqual(1,gate.load()['epoch'])

if __name__=='__main__':unittest.main()
