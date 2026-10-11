import sys,unittest,tempfile
from pathlib import Path
from copy import deepcopy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase3 import ROOT,read,files
from k1_phase2_3 import make_kiwi
from k1_phase3_7_analysis import analyze,segments
from k1_phase3_7 import ProductionGate
from k1_phase3_7_gate import permission_issues

class SentenceCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k=make_kiwi();cls.f=files();cls.f['_allowed_vocab']=cls.f['core_vocab.json']+cls.f['expansion_vocab.json']

    def test_segmentation_quote_and_offsets(self):
        text='친구가 말해요.\n"저는 시간이 있어요." "네. 여기 있어요."'
        ss=segments(text)
        self.assertEqual(4,len(ss))
        self.assertEqual('"저는 시간이 있어요."',ss[1][2])
        for lo,hi,s in ss:self.assertEqual(s,text[lo:hi])

    def test_pronoun_topic_not_future_determiner(self):
        for text in ('"저는 일을 하고 갈 거예요."','"저는 시간이 있어서 기다릴 거예요."','제가 가요.','저도 가요.'):
            a=analyze(text,self.f,1,kiwi=self.k)
            self.assertIn('ko_k1_0002',{x['canonical_vocab_id'] for x in a['canonical_lexical_map']})
            self.assertNotIn('ko_k1_0446',{x['canonical_vocab_id'] for x in a['canonical_lexical_map']})

    def test_true_determiner_and_future_not_authorized(self):
        a=analyze('저 사람을 봐요.',self.f,1,kiwi=self.k)
        self.assertIn('ko_k1_0446',{x['vocab_id'] for x in a['annotations']})
        with tempfile.TemporaryDirectory() as d:
            g=ProductionGate(Path(d)/'r',Path(d)/'s',kiwi=self.k);g.initialize()
            self.assertTrue(any(x['reason']=='future_expansion' for x in permission_issues(a,g.snapshot(1),self.f)))

    def test_ne_contrast(self):
        for text in ('네.','"네, 여기 있어요."'):
            self.assertIn('ko_k1_0442',{x['vocab_id'] for x in analyze(text,self.f,2,kiwi=self.k)['annotations']})
        for text in ('네 책.','네 가방.','네 사람이 와요.'):
            self.assertNotIn('ko_k1_0442',{x['vocab_id'] for x in analyze(text,self.f,2,kiwi=self.k)['annotations']})

    def test_uri_contrast(self):
        for text in ('우리는 한국어를 배워요.','우리 집에 가요.'):
            self.assertIn('ko_k1_0004',{x['vocab_id'] for x in analyze(text,self.f,7,kiwi=self.k)['annotations']})
        a=analyze('우리 안에 개가 있어요.',self.f,7,kiwi=self.k)
        self.assertTrue(a['unresolved_tokens'] or any(x.get('requires_candidate_review') for x in a['resolver_decisions']))

    def test_existing_resolvers(self):
        for text,lemma in [('"아니요."','아니요'),('"한국어 책이 있어요?"','한국어'),('물을 마셔요.','마시다'),('밥하고 국을 먹어요.','밥')]:
            self.assertIn(lemma,{x['lemma'] for x in analyze(text,self.f,7,kiwi=self.k)['annotations']})
        text='공원까지 친구하고 걸어요.'
        intent=dict(sentence=text,surface='걸어요',vocab_id='ko_k1_0186',lemma='걷다',pos='verb',sense='walk')
        self.assertIn('걷다',{x['lemma'] for x in analyze(text,self.f,7,(),[intent],['walk'],self.k)['annotations']})

    def test_historical_failed001_can_pass_with_warnings(self):
        old=read(ROOT/'pilot/ko/k1/phase3_6c/candidates/K1-001-attempt-01.json')
        with tempfile.TemporaryDirectory() as d:
            g=ProductionGate(Path(d)/'r',Path(d)/'s',kiwi=self.k);g.initialize()
            before=g.ledger.read_bytes();p,c=g.submit(old['source'])
            self.assertTrue(c['hard_pass'],c['hard_errors']);self.assertEqual(before,g.ledger.read_bytes())
            self.assertEqual(1,c['coverage']['controlled_vocab_coverage'])
            self.assertTrue(any(x['id_disagreement'] for x in c['scope_diagnostics']))
            self.assertEqual('running',read(g.control)['status'])
            g.approve(p,dict(naturalness='PASS',translation_fidelity='PASS',review_word_integration='PASS',reason='regression-only'))
            g.commit(p);self.assertEqual(1,g.load()['epoch'])

    def test_raw_streams_not_overwritten(self):
        old=read(ROOT/'pilot/ko/k1/phase3_6c/candidates/K1-001-attempt-01.json')
        a=analyze(old['text_ko'],self.f,1,kiwi=self.k,scope='full_candidate')
        from k1_phase3_6c_resolver import analyze as prior
        full=prior(old['text_ko'],self.f,1,kiwi=self.k,scope='full_diagnostic')
        self.assertEqual(full['raw_morphology'],a['full_text_diagnostic']['raw_morphology'])
        for x in a['canonical_lexical_map']:
            self.assertEqual(x['surface'],old['text_ko'][x['start']:x['end']])

    def test_unknown_and_retired_evidence_still_rejected(self):
        a=analyze('도장을 찍어요.',self.f,1,kiwi=self.k)
        self.assertTrue(a['unresolved_tokens'] or any(x.get('requires_candidate_review') for x in a['resolver_decisions']))

if __name__=='__main__':unittest.main()
