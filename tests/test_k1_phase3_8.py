import sys,tempfile,unittest,json
from copy import deepcopy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from k1_phase3 import ROOT,files,read
from k1_phase2_3 import make_kiwi
from k1_phase3_8 import ProductionGate
from k1_phase3_8_analysis import analyze
from k1_phase3_8_sense import policies,sense_checks,basic_family_usages

class SensePolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.f=files();cls.k=make_kiwi()

    def test_approved_meal_time_family_same_id(self):
        probes=[('아침이에요.','ko_k1_0072','morning_time'),('아침에 학교에 가요.','ko_k1_0072','morning_time'),('아침을 먹어요.','ko_k1_0072','breakfast_meal'),('아침을 먹고 학교에 가요.','ko_k1_0072','breakfast_meal'),('저녁이에요.','ko_k1_0074','evening_time'),('오늘 저녁에 집에 가요.','ko_k1_0074','evening_time'),('내일 아침에 학교에 가요.','ko_k1_0072','morning_time'),('집에서 가족하고 저녁을 먹을 거예요.','ko_k1_0074','dinner_meal')]
        for text,i,fn in probes:
            with self.subTest(text=text):
                a=analyze(text,self.f,5,kiwi=self.k);u=basic_family_usages(text,a)
                self.assertTrue(any(x['vocab_id']==i and x['function']==fn for x in u),u)
                self.assertFalse(any(x['decision']=='FAIL' for x in sense_checks(text,a)))

    def test_each_restriction_has_source_positive_negative(self):
        vs={x['id']:x for name in ('core_vocab.json','expansion_vocab.json') for x in self.f[name]}
        for e in policies()['explicit_restricted_senses.json']['entries']:
            with self.subTest(id=e['vocab_id']):
                self.assertEqual(vs[e['vocab_id']]['notes'],e['source']['notes'])
                # Adversarial fixture for a falsely assigned canonical identity.
                # This is NOT trusting author intention: rejection needs the
                # independent original local negative pattern as well as ID.
                def fixture(text):
                    lo=text.index(e['lemma'][:-1] if e['lemma'].endswith('다') and e['lemma']!='들다' else e['lemma']) if e['lemma'] in text else 0
                    return {'annotations':[dict(vocab_id=e['vocab_id'],surface=text[lo:lo+1],start=lo,end=lo+1,sense=e['allowed_sense'])]}
                self.assertFalse(any(x['decision']=='FAIL' for x in sense_checks(e['positive_example'],fixture(e['positive_example']))))
                self.assertTrue(any(x['decision']=='FAIL' for x in sense_checks(e['negative_example'],fixture(e['negative_example']))))

    def test_no_new_restriction_for_other_words(self):
        p=policies();ids={e['vocab_id'] for e in p['explicit_restricted_senses.json']['entries']}
        self.assertNotIn('ko_k1_0072',ids);self.assertNotIn('ko_k1_0074',ids)
        self.assertEqual(2,len(p['basic_sense_families.json']['entries']))
        a=analyze('사진을 찍어요.',self.f,1,kiwi=self.k)
        self.assertFalse(any(x['decision']=='FAIL' for x in sense_checks('사진을 찍어요.',a)))
        self.assertFalse(sense_checks('집에 가요.',analyze('집에 가요.',self.f,1,kiwi=self.k)))

    def test_future_still_rejected(self):
        from k1_phase3_8_gate import permission_issues
        with tempfile.TemporaryDirectory() as d:
            g=ProductionGate(Path(d)/'r',Path(d)/'s',kiwi=self.k);g.initialize()
            a=analyze('저 사람을 봐요.',self.f,1,kiwi=self.k)
            self.assertTrue(any(x['reason']=='future_expansion' for x in permission_issues(a,g.snapshot(1),self.f)))

    def test_local_repeated_failures_do_not_credit_or_stop_before_five(self):
        old=read(ROOT/'pilot/ko/k1/phase3_6c/candidates/K1-001-attempt-01.json')['source']
        with tempfile.TemporaryDirectory() as d:
            g=ProductionGate(Path(d)/'r',Path(d)/'s',kiwi=self.k);g.initialize();before=g.ledger.read_bytes()
            short=deepcopy(old);short['sentences']=short['sentences'][:3];short['translations_ja']=short['translations_ja'][:3]
            for n in range(4):
                _,c=g.submit(short);self.assertFalse(c['hard_pass']);self.assertEqual('running',read(g.control)['status']);self.assertEqual(before,g.ledger.read_bytes())
            _,c=g.submit(short);self.assertFalse(c['hard_pass']);self.assertEqual('stopped',read(g.control)['status']);self.assertEqual(before,g.ledger.read_bytes())

    def test_scope_pos_comparison_lexical_indices_both_sides(self):
        text='저는 일을 하고 갈 거예요.'
        a=analyze(text,self.f,1,kiwi=self.k,scope='full_candidate')
        for x in a['scope_diagnostics']:
            self.assertFalse(set(x['diagnostic_raw_pos']) & {'EF','ETM','EC','EP'})
        self.assertIn('ko_k1_0002',{x['canonical_vocab_id'] for x in a['canonical_lexical_map']})

    def test_snapshot_policies_and_raw_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            g=ProductionGate(Path(d)/'r',Path(d)/'s',kiwi=self.k);g.initialize();s=g.snapshot(1)
            self.assertEqual(2,len(s['basic_sense_families']));self.assertTrue(s['explicit_restricted_senses'])
            self.assertEqual(800,len(self.f['core_vocab.json'])+len(self.f['expansion_vocab.json']))
            self.assertEqual(32,len(self.f['grammar.json']))

if __name__=='__main__':unittest.main()
