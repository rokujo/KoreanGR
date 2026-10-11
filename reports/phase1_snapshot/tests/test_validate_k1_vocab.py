"""Reject corrupted fixtures, including interval-capacity failures invisible to schemas."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validator',ROOT/'scripts/validate_k1_vocab.py')
validator=importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
DATA=ROOT/'config/languages/ko/k1'

class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base={p.name:json.loads(p.read_text(encoding='utf-8')) for p in DATA.glob('*.json')}

    def fixture(self, mutate):
        data=copy.deepcopy(self.base)
        mutate(data)
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            for name,value in data.items():
                (folder/name).write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
            return validator.validate(folder)

    def test_current_data(self):
        result=validator.validate(DATA)
        self.assertTrue(result['ok'],result['errors'])
        self.assertEqual(result['summary']['total'],800)
        self.assertEqual(result['summary']['introduction_capacity']['assigned'],500)
        self.assertEqual(result['summary']['introduction_capacity']['slack'],0)
        self.assertTrue(result['warnings'])

    def test_invalid_fixtures(self):
        cases=[
            ('core count',lambda d:d['core_vocab.json'].pop(),'Core count'),
            ('expansion count',lambda d:d['expansion_vocab.json'].pop(),'Expansion count'),
            ('duplicate id',lambda d:d['expansion_vocab.json'][0].update(id=d['core_vocab.json'][0]['id']),'Duplicate ID'),
            ('duplicate rank',lambda d:d['expansion_vocab.json'][0].update(rank=1),'Duplicate rank'),
            ('overlap',lambda d:d['expansion_vocab.json'][0].update(**{k:d['core_vocab.json'][0][k] for k in ('lemma','pos','sense')}),'Core/Expansion overlap'),
            ('tier count',lambda d:d['expansion_vocab.json'][0].update(tier='E2'),'Tier counts'),
            ('missing field',lambda d:d['expansion_vocab.json'][0].pop('gloss_ja'),'required property'),
            ('invalid POS',lambda d:d['expansion_vocab.json'][0].update(pos='particle'),'not one of'),
            ('rank bool',lambda d:d['expansion_vocab.json'][0].update(rank=True),'not of type'),
            ('reverse interval',lambda d:d['expansion_vocab.json'][0].update(introduced_from=99,introduced_to=98),'start exceeds end'),
            ('late interval',lambda d:d['expansion_vocab.json'][0].update(introduced_to=251),'greater than'),
            ('null exposure',lambda d:d['expansion_vocab.json'][0].update(target_exposures=None),'not of type'),
            ('short exposure',lambda d:d['expansion_vocab.json'][0].update(target_exposures=5),'less than'),
            ('tag syntax',lambda d:d['expansion_vocab.json'][0].update(tags=['Daily Life']),'does not match'),
            ('tag duplicate',lambda d:d['expansion_vocab.json'][0].update(tags=['food','food']),'non-unique'),
            ('extra property',lambda d:d['expansion_vocab.json'][0].update(typo=True),'Additional properties'),
            ('grammar count',lambda d:d['grammar.json'].pop(),'too short'),
            ('grammar missing example',lambda d:d['grammar.json'][0].pop('example'),'required property'),
            ('proper name counted',lambda d:d['core_vocab.json'][40].update(lemma='한국'),'proper name'),
            ('profile max drift',lambda d:d['profile.json']['new_vocab'].update(max=3),'was expected'),
            ('exception backdoor',lambda d:d['lexical_exceptions.json']['policy'].update(license_constituents=True),'was expected'),
        ]
        for name,mutate,expected in cases:
            with self.subTest(name=name):
                result=self.fixture(mutate)
                self.assertFalse(result['ok'])
                self.assertIn(expected,'\n'.join(result['errors']))

    def test_globally_impossible_windows(self):
        def change(data):
            for e in data['expansion_vocab.json']:
                if e['tier']=='E1':e.update(introduced_from=1,introduced_to=30)
        result=self.fixture(change)
        self.assertFalse(result['ok'])
        self.assertIn('infeasible','\n'.join(result['errors']))

    def test_duplicate_json_key_and_nan(self):
        for content in ('{"id":1,"id":2}','[NaN]'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as temp:
                folder=Path(temp)
                for name,value in self.base.items():
                    (folder/name).write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
                (folder/'core_vocab.json').write_text(content,encoding='utf-8')
                result=validator.validate(folder)
                self.assertFalse(result['ok'])
                self.assertTrue(any('Duplicate JSON' in e or 'Non-JSON' in e for e in result['errors']))

if __name__=='__main__':
    unittest.main()
