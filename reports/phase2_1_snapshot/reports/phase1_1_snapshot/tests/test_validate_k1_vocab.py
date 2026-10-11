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
        self.assertEqual(result['summary']['introduction_capacity']['slack'],50)
        self.assertEqual(result['summary']['introduction_capacity']['slots'],550)
        self.assertEqual(result['summary']['introduction_capacity']['witness_period_counts'],{'0':10,'1':30,'2':235})
        self.assertEqual(result['summary']['introduction_capacity']['consolidation_new_entries'],0)
        self.assertEqual(result['summary']['grammar'],32)
        self.assertEqual(result['summary']['replacement_proposals']['projection']['total'],800)
        self.assertEqual(result['summary']['replacement_proposals']['projection']['tiers'],{'E1':200,'E2':200,'E3':100})
        self.assertFalse(result['summary']['replacement_proposals']['applied'])
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
            ('late interval',lambda d:d['expansion_vocab.json'][0].update(introduced_to=276),'greater than'),
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
            ('missing hard ratio',lambda d:d['profile.json'].pop('hard_min_known_vocab_ratio'),'required property'),
            ('missing target ratio',lambda d:d['profile.json'].pop('target_known_vocab_ratio'),'required property'),
            ('hard ratio type',lambda d:d['profile.json'].update(hard_min_known_vocab_ratio='0.98'),'not of type'),
            ('target ratio type',lambda d:d['profile.json'].update(target_known_vocab_ratio=True),'not of type'),
            ('hard ratio outside range',lambda d:d['profile.json'].update(hard_min_known_vocab_ratio=1.01),'greater than'),
            ('target ratio outside range',lambda d:d['profile.json'].update(target_known_vocab_ratio=-0.01),'less than'),
            ('hard above target',lambda d:d['profile.json'].update(hard_min_known_vocab_ratio=0.995),'was expected'),
            ('token cap drift',lambda d:d['profile.json']['new_vocab'].update(first_text_new_lemma_token_soft_max=6),'was expected'),
            ('grammar metadata drift',lambda d:d['profile.json'].update(grammar_count=29),'was expected'),
            ('grammar32 missing',lambda d:d['grammar.json'].pop(31),'too short'),
            ('added grammar replaced',lambda d:d['grammar.json'][29].update(form='와/과'),'Added grammar'),
            ('replacement applied without review',lambda d:d['expansion_replacement_proposals.json'].update(applied=True),'was expected'),
            ('duplicate schedule intro',lambda d:d['introduction_schedule.json']['rows'][1]['entry_ids'].__setitem__(0,d['introduction_schedule.json']['rows'][0]['entry_ids'][0]),'Duplicate scheduled'),
            ('wrong schedule text',lambda d:d['introduction_schedule.json']['rows'][0].update(text=2),'ordered 1..300'),
            ('missing schedule intro',lambda d:d['introduction_schedule.json']['rows'][0]['entry_ids'].pop(),'every Expansion'),
            ('too many schedule entries',lambda d:d['introduction_schedule.json']['rows'][0]['entry_ids'].append(d['expansion_vocab.json'][-1]['id']),'too long'),
            ('slack metadata wrong',lambda d:d['profile.json']['feasibility'].update(slack_slots=0),'Slack slot'),
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

    def test_consolidation_zone_is_empty(self):
        for target in (276,300):
            with self.subTest(text=target):
                def change(data):
                    entry=data['introduction_schedule.json']['rows'][0]['entry_ids'].pop()
                    data['introduction_schedule.json']['rows'][target-1]['entry_ids'].append(entry)
                result=self.fixture(change)
                self.assertFalse(result['ok'])
                self.assertIn('consolidation zone','\n'.join(result['errors']))

    def test_preserved_identities_and_promotions(self):
        old=ROOT/'reports/phase1_snapshot/config/languages/ko/k1'
        before=json.loads((old/'expansion_vocab.json').read_text(encoding='utf-8'))
        after=self.base['expansion_vocab.json']
        self.assertEqual([(e['id'],e['rank'],validator.key(e)) for e in before],
                         [(e['id'],e['rank'],validator.key(e)) for e in after])
        by_lemma={e['lemma']:e for e in after}
        self.assertEqual(by_lemma['기억하다']['tier'],'E2')
        self.assertEqual(by_lemma['잠깐']['tier'],'E1')
        self.assertEqual(by_lemma['어떻다']['tier'],'E1')
        self.assertEqual(by_lemma['제일']['tier'],'E2')
        self.assertEqual(by_lemma['제일']['confidence'],'high')
        self.assertEqual(by_lemma['가장']['tier'],'E3')
        self.assertEqual(self.base['grammar.json'][:29],json.loads((old/'grammar.json').read_text(encoding='utf-8')))
        self.assertEqual((DATA/'core_vocab.source.json').read_bytes(),(old/'core_vocab.source.json').read_bytes())
        self.assertEqual(self.base['profile.json']['core_decision']['status'],'accepted')
        proposed=self.base['expansion_replacement_proposals.json']
        self.assertFalse(proposed['applied'])
        self.assertEqual(len(proposed['entries']),7)
        for p in proposed['entries']:
            self.assertIn(p['source_lemma'],by_lemma)
            self.assertNotIn(p['candidate']['lemma'],by_lemma)

    def test_scheduler_with_reserved_slots(self):
        result=self.base['introduction_schedule.json']['rows']
        capacities={row['text']:len(row['entry_ids']) for row in result if row['text']<=275}
        witness,failure=validator.introduction_assignment(self.base['expansion_vocab.json'],275,2,capacities,True)
        self.assertIsNone(failure)
        self.assertEqual(witness,result[:275])
        self.assertEqual(len(witness),275)
        self.assertEqual(sum(len(r['entry_ids']) for r in witness),500)
        # 249 double-introduction texts cannot fit 500 entries, even with wide windows.
        entries=[{**e,'introduced_from':1,'introduced_to':275} for e in self.base['expansion_vocab.json']]
        blocked={t:0 for t in range(250,276)}
        witness,failure=validator.introduction_assignment(entries,275,2,blocked)
        self.assertIsNone(witness)
        self.assertIsNotNone(failure)

if __name__=='__main__':
    unittest.main()
