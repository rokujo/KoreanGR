"""Numerical and permission-boundary tests using annotations, no learner texts."""
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lexical_coverage import evaluate_lexical_tokens

class CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files={p.name:json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'config/languages/ko/k1').glob('*.json')}
        cls.core=dict(kind='vocab',id=cls.files['core_vocab.json'][0]['id'])
        cls.current=[e['vocab_id'] for e in cls.files['vocab_exposure_schedule.json']['entries'] if e['first_introduction_text']==1]

    def evaluate(self,N,U,text=1):
        tokens=[self.core]*(N-U)+[dict(kind='vocab',id=self.current[i%2]) for i in range(U)]
        return evaluate_lexical_tokens(tokens,text,self.files)

    def test_integer_boundaries(self):
        for N,U,ok,limit in [(99,2,False,1),(100,2,True,2),(149,3,False,2),
                             (150,3,True,3),(250,4,True,5),(100,3,False,2),(100,1,True,2)]:
            with self.subTest(N=N,U=U):
                r=self.evaluate(N,U);self.assertEqual(r['ok'],ok,r)
                self.assertEqual(r['dynamic_hard_new_token_limit'],limit)
                self.assertEqual((r['N'],r['U']),(N,U))
        self.assertTrue(any('soft maximum' in w for w in self.evaluate(250,4)['warnings']))
        self.assertTrue(any('target 99%' in w for w in self.evaluate(100,2)['warnings']))
        self.assertFalse(self.evaluate(100,1)['warnings'])

    def test_repetition_is_tokens_not_unique_lemmas(self):
        r=evaluate_lexical_tokens([self.core]*97+[dict(kind='vocab',id=self.current[0])]*3,1,self.files)
        self.assertEqual((r['U'],r['new_lemma_count']),(3,1));self.assertFalse(r['ok'])

    def test_previous_introduction(self):
        r=self.evaluate(100,20,text=2)
        self.assertTrue(r['ok']);self.assertEqual((r['U'],r['previous_vocab_coverage']),(0,1))

    def test_unknown_future_and_retired(self):
        future=next(e['vocab_id'] for e in self.files['vocab_exposure_schedule.json']['entries'] if e['first_introduction_text']>1)
        for token in [dict(kind='unknown',id='unresolved'),dict(kind='vocab',id=future),dict(kind='vocab',id='ko_k1_0773')]:
            with self.subTest(token=token):
                r=evaluate_lexical_tokens([self.core]*99+[token],1,self.files)
                self.assertFalse(r['ok']);self.assertEqual(r['N'],100)
                self.assertEqual(r['controlled_vocab_coverage'],.99)

    def test_registered_names_and_exact_frozen_forms(self):
        frozen=next(e['id'] for e in self.files['lexical_exceptions.json']['entries'] if e['kind']=='frozen_exception')
        tokens=[dict(kind='proper_name',id='한국'),dict(kind='exception',id=frozen)]
        r=evaluate_lexical_tokens(tokens,1,self.files)
        self.assertTrue(r['ok']);self.assertEqual((r['N'],r['previous_tokens']),(2,2))
        r=evaluate_lexical_tokens([dict(kind='exception',id=frozen)]*3,1,self.files)
        self.assertFalse(r['ok'])
        regular=next(e['id'] for e in self.files['lexical_exceptions.json']['entries'] if e['kind']=='regular_vocab_form')
        r=evaluate_lexical_tokens([self.core]*99+[dict(kind='exception',id=regular)],1,self.files)
        self.assertFalse(r['ok'])

    def test_grammar_exclusion_and_empty_denominator(self):
        grammar=self.files['grammar.json'][0]['id']
        r=evaluate_lexical_tokens([self.core,dict(kind='grammar',id=grammar),dict(kind='punctuation')],1,self.files)
        self.assertTrue(r['ok']);self.assertEqual(r['N'],1)
        r=evaluate_lexical_tokens([self.core,dict(kind='grammar',id='not_authorized')],1,self.files)
        self.assertFalse(r['ok'])
        r=evaluate_lexical_tokens([dict(kind='grammar',id=grammar)],1,self.files)
        self.assertFalse(r['ok']);self.assertIsNone(r['previous_vocab_coverage'])

    def test_invalid_text_number(self):
        for text in (0,301,True,1.5):
            with self.subTest(text=text),self.assertRaises(ValueError):
                evaluate_lexical_tokens([self.core],text,self.files)

if __name__=='__main__':unittest.main()
