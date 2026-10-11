"""Preserve validation regressions and reject corrupted Phase 1.2 plans."""
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
from k1_schedule import text_load_rows,load_statistics,build_exposure_plan
DATA=ROOT/'config/languages/ko/k1'

class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base={p.name:json.loads(p.read_text(encoding='utf-8')) for p in DATA.glob('*.json')}

    def fixture(self,mutate):
        data=copy.deepcopy(self.base);mutate(data)
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            for name,value in data.items():
                (folder/name).write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
            return validator.validate(folder)

    def test_current_data(self):
        r=validator.validate(DATA)
        self.assertTrue(r['ok'],r['errors']);s=r['summary']
        self.assertEqual((s['core'],s['expansion'],s['total']),(300,500,800))
        self.assertEqual(s['tiers'],{'E1':200,'E2':200,'E3':100})
        self.assertEqual(s['introduction_capacity'],dict(assigned=500,slots=550,slack=50,
            period_counts={'0':22,'1':6,'2':247},last_introduction=255,consolidation_new_entries=0))
        self.assertEqual(s['grammar'],32)
        self.assertEqual(s['replacements'],dict(adopted=7,pending=0))
        self.assertEqual(s['exposure_plan']['planned_entry_text_pairs'],3000)
        self.assertEqual(s['exposure_plan']['min_distinct_texts'],6)
        self.assertEqual(s['exposure_plan']['concentration_warning_count'],0)

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
            ('missing controlled',lambda d:d['profile.json'].pop('controlled_vocab_coverage_hard_min'),'required property'),
            ('missing previous',lambda d:d['profile.json'].pop('previous_vocab_coverage_target'),'required property'),
            ('coverage type',lambda d:d['profile.json'].update(previous_vocab_coverage_hard_min='0.98'),'not of type'),
            ('coverage bool',lambda d:d['profile.json'].update(previous_vocab_coverage_target=True),'not of type'),
            ('coverage above range',lambda d:d['profile.json'].update(previous_vocab_coverage_target=1.01),'greater than'),
            ('coverage below range',lambda d:d['profile.json'].update(previous_vocab_coverage_target=-0.01),'less than'),
            ('controlled below100',lambda d:d['profile.json'].update(controlled_vocab_coverage_hard_min=.99),'was expected'),
            ('old ratio key',lambda d:d['profile.json'].update(known_vocab_ratio=.99),'Additional properties'),
            ('token cap drift',lambda d:d['profile.json']['new_vocab'].update(first_text_new_lemma_token_soft_max=6),'was expected'),
            ('grammar metadata drift',lambda d:d['profile.json'].update(grammar_count=29),'was expected'),
            ('added grammar replaced',lambda d:d['grammar.json'][29].update(form='와/과'),'Added grammar'),
            ('unapplied replacement',lambda d:d['expansion_replacement_proposals.json'].update(applied=False),'was expected'),
            ('retired ID reused',lambda d:d['expansion_vocab.json'][-1].update(id='ko_k1_0800'),'Active ID set'),
            ('migration reuse',lambda d:d['id_migration.json']['id_policy'].update(reuse_retired_ids=True),'Immutable ID'),
            ('candidate identity',lambda d:d['k2_candidates.json']['entries'][0].update(sense='wrong'),'ledger identity'),
            ('duplicate schedule intro',lambda d:d['introduction_schedule.json']['rows'][1]['entry_ids'].__setitem__(0,d['introduction_schedule.json']['rows'][0]['entry_ids'][0]),'Duplicate scheduled'),
            ('wrong schedule text',lambda d:d['introduction_schedule.json']['rows'][0].update(text=2),'ordered 1..300'),
            ('missing schedule intro',lambda d:d['introduction_schedule.json']['rows'][0]['entry_ids'].pop(),'every Expansion'),
            ('too many schedule entries',lambda d:d['introduction_schedule.json']['rows'][0]['entry_ids'].append(d['expansion_vocab.json'][-1]['id']),'too long'),
            ('slack wrong',lambda d:d['profile.json']['feasibility'].update(slack_slots=0),'Slack slot'),
            ('missing exposure',lambda d:d['vocab_exposure_schedule.json']['entries'].pop(),'too short'),
            ('short reviews',lambda d:d['vocab_exposure_schedule.json']['entries'][0]['review_texts'].pop(),'too short'),
            ('duplicate reviews',lambda d:d['vocab_exposure_schedule.json']['entries'][0]['review_texts'].__setitem__(1,d['vocab_exposure_schedule.json']['entries'][0]['review_texts'][0]),'non-unique'),
            ('review outside300',lambda d:d['vocab_exposure_schedule.json']['entries'][0]['review_texts'].__setitem__(-1,301),'greater than'),
            ('review at first',lambda d:d['vocab_exposure_schedule.json']['entries'][0]['review_texts'].__setitem__(0,d['vocab_exposure_schedule.json']['entries'][0]['first_introduction_text']),'review before or at'),
            ('first mismatch',lambda d:d['vocab_exposure_schedule.json']['entries'][0].update(first_introduction_text=2),'first introduction disagrees'),
            ('missing long',lambda d:d['vocab_exposure_schedule.json']['entries'][0].update(review_texts=[3,9,15,20,25]),'missing long-distance'),
            ('incorrect load',lambda d:d['vocab_exposure_schedule.json']['texts'][0].update(review_vocab_count=99),'load/index mismatch'),
            ('incorrect stats',lambda d:d['vocab_exposure_schedule.json']['statistics']['all_texts'].update(max=99),'statistics mismatch'),
        ]
        for name,mutate,expected in cases:
            with self.subTest(name=name):
                result=self.fixture(mutate);self.assertFalse(result['ok'])
                self.assertIn(expected,'\n'.join(result['errors']))

    def test_globally_impossible_windows(self):
        def change(d):
            for e in d['expansion_vocab.json']:
                if e['tier']=='E1':e.update(introduced_from=1,introduced_to=30)
        r=self.fixture(change);self.assertFalse(r['ok'])
        self.assertIn('infeasible','\n'.join(r['errors']))

    def test_duplicate_json_key_and_nan(self):
        for content in ('{"id":1,"id":2}','[NaN]'):
            with self.subTest(content=content),tempfile.TemporaryDirectory() as temp:
                folder=Path(temp)
                for name,value in self.base.items():
                    (folder/name).write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
                (folder/'core_vocab.json').write_text(content,encoding='utf-8')
                r=validator.validate(folder);self.assertFalse(r['ok'])
                self.assertTrue(any('Duplicate JSON' in e or 'Non-JSON' in e for e in r['errors']))

    def test_consolidation_zone_is_empty(self):
        for target in (276,300):
            with self.subTest(text=target):
                def change(d):
                    entry=d['introduction_schedule.json']['rows'][0]['entry_ids'].pop()
                    d['introduction_schedule.json']['rows'][target-1]['entry_ids'].append(entry)
                r=self.fixture(change);self.assertFalse(r['ok'])
                self.assertIn('consolidation zone','\n'.join(r['errors']))

    def test_preserved_identities_and_promotions(self):
        old=ROOT/'reports/phase1_1_snapshot/config/languages/ko/k1'
        before={e['id']:e for e in json.loads((old/'expansion_vocab.json').read_text(encoding='utf-8'))}
        after={e['id']:e for e in self.base['expansion_vocab.json']}
        migrations=self.base['id_migration.json']['mappings'];retired={m['old_id'] for m in migrations}
        self.assertEqual(len(before.keys()&after.keys()),493)
        for vid in before.keys()-retired:
            self.assertEqual((before[vid]['rank'],validator.key(before[vid])),(after[vid]['rank'],validator.key(after[vid])))
            self.assertEqual(before[vid]['tier'],after[vid]['tier'])
        for m in migrations:
            self.assertNotIn(m['old_id'],after)
            self.assertEqual(after[m['new_id']]['rank'],before[m['old_id']]['rank'])
            self.assertNotEqual(m['old_id'],m['new_id'])
        by_lemma={e['lemma']:e for e in after.values()}
        for lemma,tier in {'잠깐':'E1','어떻다':'E1','기억하다':'E2','부모':'E2','딸기':'E2','사촌':'E3','고추':'E3'}.items():
            self.assertEqual(by_lemma[lemma]['tier'],tier)
        self.assertIn('未知の成人男性への直接呼びかけを無条件に生成しない',by_lemma['아저씨']['notes'])
        self.assertEqual(self.base['grammar.json'],json.loads((old/'grammar.json').read_text(encoding='utf-8')))
        for name in ('core_vocab.source.json','core_vocab.json','proper_names.json'):
            self.assertEqual((DATA/name).read_bytes(),(old/name).read_bytes())

    def test_scheduler_with_reserved_slots(self):
        rows=self.base['introduction_schedule.json']['rows']
        capacities={r['text']:len(r['entry_ids']) for r in rows if r['text']<=275}
        witness,failure=validator.introduction_assignment(self.base['expansion_vocab.json'],275,2,capacities,True)
        self.assertIsNone(failure);self.assertEqual(witness,rows[:275])
        entries=[{**e,'introduced_from':1,'introduced_to':275} for e in self.base['expansion_vocab.json']]
        witness,failure=validator.introduction_assignment(entries,275,2,{t:0 for t in range(250,276)})
        self.assertIsNone(witness);self.assertIsNotNone(failure)

    def test_schedule_deterministic(self):
        schedule=build_exposure_plan(self.base['expansion_vocab.json'],self.base['introduction_schedule.json']['rows'])
        self.assertEqual(schedule,self.base['vocab_exposure_schedule.json'])

    def test_load_concentration_detected(self):
        def concentrate(d):
            plan=d['vocab_exposure_schedule.json']
            for e in plan['entries']:e['review_texts'][-1]=300
            plan['texts']=text_load_rows(d['expansion_vocab.json'],plan['entries'],20)
            plan['statistics']=load_statistics(plan['texts'])
        r=self.fixture(concentrate)
        self.assertTrue(r['ok'],r['errors'])
        self.assertGreater(r['summary']['exposure_plan']['concentration_warning_count'],0)
        self.assertTrue(any('LOAD: 300' in w for w in r['warnings']))

if __name__=='__main__':unittest.main()
