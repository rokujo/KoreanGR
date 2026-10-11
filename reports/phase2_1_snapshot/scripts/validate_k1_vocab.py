"""Phase 1.2 validator: data, immutable ID migration, coverage policy and exposure plan.

Exit 0: data checks pass; 1: invalid; 2: dependency missing. No learner texts generated.
"""
import argparse
from collections import Counter,defaultdict
import json
import math
from pathlib import Path
import sys
import unicodedata

sys.path.insert(0,str(Path(__file__).resolve().parent))
from k1_schedule import introduction_assignment,text_load_rows,load_statistics

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print('Missing jsonschema: python -m pip install -r requirements-dev.txt',file=sys.stderr)
    raise SystemExit(2)

DEFAULT_DIR=Path(__file__).resolve().parents[1]/'config/languages/ko/k1'
CATEGORY_COUNTS={'people_social':40,'places_objects':90,'food_nature':50,'verbs':100,
    'adjectives':65,'adverbs_connectors':50,'time_counters_units':35,'abstract_body_emotion':40,
    'school_work_transport_info':30}
REPLACEMENTS=[('함께','가만히',773),('조부모','아저씨',702),('기차역','시간표',797),
              ('찍히다','충전하다',757),('관계','동갑',710),('정보','충전기',800),('가장','방금',647)]

def unique_object(pairs):
    result={}
    for k,v in pairs:
        if k in result:raise ValueError(f'Duplicate JSON object key: {k}')
        result[k]=v
    return result

def load_json(path):
    def reject(value):raise ValueError(f'Non-JSON numeric constant: {value}')
    return json.loads(path.read_text(encoding='utf-8-sig'),object_pairs_hook=unique_object,parse_constant=reject)

def duplicate_values(values):
    return [v for v,n in Counter(values).items() if n>1]

def key(entry):return entry['lemma'],entry['pos'],entry['sense']

def validate(data_dir):
    errors=[];warnings=[];summary={};files={}
    names=['core_vocab.json','expansion_vocab.json','core_vocab.source.json','grammar.json','profile.json',
           'lexical_exceptions.json','proper_names.json','expansion_replacement_proposals.json',
           'introduction_schedule.json','id_migration.json','k2_candidates.json','vocab_exposure_schedule.json',
           'vocab.schema.json','grammar.schema.json','support.schema.json','vocab_exposure_schedule.schema.json']
    def result():return dict(ok=not errors,errors=errors,warnings=warnings,summary=summary)
    for name in names:
        try:files[name]=load_json(data_dir/name)
        except (OSError,ValueError) as exc:errors.append(f'{name}: {exc}')
    if errors:return result()
    bindings=[('core_vocab.json','vocab.schema.json'),('expansion_vocab.json','vocab.schema.json'),
              ('core_vocab.source.json','vocab.schema.json'),('grammar.json','grammar.schema.json'),
              ('vocab_exposure_schedule.json','vocab_exposure_schedule.schema.json')]
    for name,schema_name in bindings:
        schema=files[schema_name]
        try:Draft202012Validator.check_schema(schema)
        except Exception as exc:errors.append(f'{schema_name}: Invalid schema: {exc}');continue
        for error in Draft202012Validator(schema).iter_errors(files[name]):
            path='/'.join(map(str,error.absolute_path)) or '<root>'
            errors.append(f'{name}:{path}: {error.message}')
    support=files['support.schema.json']
    try:
        Draft202012Validator.check_schema(support)
        for name,definition in [('profile.json','profile'),('lexical_exceptions.json','exceptions'),
                ('proper_names.json','proper_names'),('expansion_replacement_proposals.json','replacement_proposals'),
                ('introduction_schedule.json','introduction_schedule'),('id_migration.json','id_migration'),('k2_candidates.json','k2_candidates')]:
            for error in Draft202012Validator({**support,'$ref':f'#/$defs/{definition}'}).iter_errors(files[name]):
                path='/'.join(map(str,error.absolute_path)) or '<root>'
                errors.append(f'{name}:{path}: {error.message}')
    except Exception as exc:errors.append(f'support.schema.json: {exc}')
    if errors:return result()
    core=files['core_vocab.json'];exp=files['expansion_vocab.json'];all_entries=core+exp
    profile=files['profile.json'];source=files['core_vocab.source.json']
    summary.update(core=len(core),expansion=len(exp),total=len(all_entries),source_core=len(source),
        tiers=dict(Counter(e['tier'] for e in exp)),grammar=len(files['grammar.json']),
        expansion_categories=dict(Counter(e['category'] for e in exp)),
        expansion_pos=dict(Counter(e['pos'] for e in exp)),confidence=dict(Counter(e['confidence'] for e in exp)))
    for label,actual,expected in [('Core',len(core),300),('Expansion',len(exp),500),('Total',len(all_entries),800),('Source Core',len(source),300)]:
        if actual!=expected:errors.append(f'{label} count: {actual}, expected {expected}')
    for label,values in [('ID',[e['id'] for e in all_entries]),('rank',[e['rank'] for e in all_entries]),
                          ('lemma+POS+sense',[key(e) for e in all_entries])]:
        if duplicate_values(values):errors.append(f'Duplicate {label}: {duplicate_values(values)}')
    if set(map(key,core))&set(map(key,exp)):errors.append('Core/Expansion overlap')
    if set(map(key,source))&set(map(key,exp)):errors.append('Original Core/Expansion overlap')
    if any(e['tier']!='core' for e in core):errors.append('Core contains non-core tier')
    if Counter(e['tier'] for e in exp)!=Counter(E1=200,E2=200,E3=100):errors.append('Tier counts must be 200/200/100')
    if Counter(e['category'] for e in exp)!=Counter(CATEGORY_COUNTS):errors.append('Expansion category counts differ from target')
    if [e['rank'] for e in core]!=list(range(1,301)) or [e['rank'] for e in exp]!=list(range(301,801)):
        errors.append('Ranks must be ordered 1..800 (independent of permanent ID)')
    migration=files['id_migration.json'];mappings=migration['mappings']
    active={e['id']:e for e in all_entries};active_exp={e['id']:e for e in exp}
    if len(mappings)!=7:errors.append('ID migration must contain seven mappings')
    if not migration['id_policy']['immutable'] or migration['id_policy']['reuse_retired_ids'] or not migration['id_policy']['id_rank_independent']:
        errors.append('Immutable ID migration policy invalid')
    if migration['id_policy']['next_id_sequence']!=808:errors.append('Next permanent ID sequence must be 808')
    retired_ids={m['old_id'] for m in mappings};new_ids={m['new_id'] for m in mappings}
    if len(retired_ids)!=7 or len(new_ids)!=7 or retired_ids&new_ids:errors.append('ID migration collision')
    expected_ids={f'ko_k1_{n:04}' for n in range(1,801)}-retired_ids|new_ids
    if set(active)!=expected_ids:errors.append('Active ID set does not match permanent-ID migration')
    for n,(old,new,rank) in enumerate(REPLACEMENTS,801):
        old_id=f'ko_k1_{rank:04}';new_id=f'ko_k1_{n:04}'
        matching=[m for m in mappings if m['old_id']==old_id]
        if len(matching)!=1:errors.append(f'Missing migration for {old}');continue
        m=matching[0]
        if (m['old_lemma'],m['new_lemma'],m['new_id'],m['rank'])!=(old,new,new_id,rank):errors.append(f'Invalid migration: {old}')
        if old_id in active or any(e['lemma']==old for e in all_entries):errors.append(f'Retired word still active: {old}')
        e=active_exp.get(new_id)
        if not e or (e['lemma'],e['rank'],e['tier'],e['category'],e['pos'],e['sense'])!=(new,rank,m['tier'],m['category'],m['new_pos'],m['new_sense']):
            errors.append(f'New replacement not adopted: {new}')
    for e in all_entries:
        if e['id'] not in new_ids and e['id']!=f"ko_k1_{e['rank']:04}":errors.append(f"{e['id']}: existing ID/rank identity changed")
        if e['lemma']!=unicodedata.normalize('NFC',e['lemma']) or any(f!=unicodedata.normalize('NFC',f) for f in e['forms']):errors.append(f"{e['id']}: require NFC")
        if e['allow_inflection']!=(e['pos'] in ('verb','adjective')):errors.append(f"{e['id']}: allow_inflection/POS mismatch")
        if e['tier']!='core':
            start,end=e['introduced_from'],e['introduced_to'];lower,upper=profile['introduction']['ranges'][e['tier']]
            if start>end:errors.append(f"{e['id']}: introduction start exceeds end")
            if not lower<=start<=end<=upper:errors.append(f"{e['id']}: window outside tier range")
            if e['target_exposures']>301-end:errors.append(f"{e['id']}: too few remaining exposure texts")
            if e['target_exposures']>6 and not e['notes']:errors.append(f"{e['id']}: increased exposures require notes")
    tiers_by_lemma={e['lemma']:e['tier'] for e in exp}
    for lemma,tier in {'잠깐':'E1','어떻다':'E1','기억하다':'E2','부모':'E2','딸기':'E2','사촌':'E3','고추':'E3'}.items():
        if tiers_by_lemma.get(lemma)!=tier:errors.append(f'Accepted tier movement missing: {lemma}')
    uncle=next((e for e in exp if e['lemma']=='아저씨'),None)
    if uncle and '未知の成人男性への直接呼びかけを無条件に生成しない' not in (uncle['notes'] or ''):
        errors.append('아저씨 requires social-pragmatic restriction')
    candidates=files['k2_candidates.json']['entries']
    if len(candidates)!=7 or {e['former_id'] for e in candidates}!=retired_ids:errors.append('K2 candidate ledger must contain seven retired IDs')
    if files['k2_candidates.json']['counted_in_K1_budget']:errors.append('K2 candidate ledger must be outside K1')
    by_retired={m['old_id']:m for m in mappings}
    for candidate in candidates:
        m=by_retired.get(candidate['former_id'])
        if m and (candidate['lemma'],candidate['pos'],candidate['sense'],candidate['replacement_id'])!=(m['old_lemma'],m['old_pos'],m['old_sense'],m['new_id']):
            errors.append('K2 candidate ledger identity mismatch')
    proposals=files['expansion_replacement_proposals.json']
    if not proposals['applied'] or proposals['status']!='accepted':errors.append('Seven replacement decisions must be formally adopted')
    if {p['adopted_id'] for p in proposals['entries']}!=new_ids:errors.append('Adoption ledger ID mismatch')
    if len(proposals['entries'])!=7:errors.append('Adoption ledger must contain seven decisions')
    for proposal in proposals['entries']:
        m=by_retired.get(proposal['source_id'])
        if not m or proposal['status']!='accepted' or proposal['source_lemma']!=m['old_lemma'] or proposal['candidate']['lemma']!=m['new_lemma']:
            errors.append('Adoption ledger decision mismatch')
    proper={e['lemma'] for e in files['proper_names.json']['entries']}
    if proper&{e['lemma'] for e in all_entries}:errors.append('Active vocabulary contains a proper name')
    if profile['previous_vocab_coverage_hard_min']>profile['previous_vocab_coverage_target']:errors.append('Previous coverage hard exceeds target')
    if profile['controlled_vocab_coverage_hard_min']!=1:errors.append('Controlled vocabulary must be 100%')
    slots=275*2
    if profile['feasibility']['introduction_slots']!=slots:errors.append('Introduction slot metadata mismatch')
    if profile['feasibility']['required_new_entries']!=500:errors.append('Required entry metadata mismatch')
    if profile['feasibility']['slack_slots']!=slots-500:errors.append('Slack slot metadata mismatch')
    grammar=files['grammar.json']
    if len(grammar)!=32 or profile['grammar_count']!=32:errors.append('Grammar count must be 32')
    if [e['id'] for e in grammar]!=[f'ko_k1_g{i:02}' for i in range(1,33)]:errors.append('Grammar IDs must be ordered g01..g32')
    if [e['form'] for e in grammar[29:]]!=['-(으)로','부터 / 까지','만']:errors.append('Added grammar mismatch')
    exceptions=files['lexical_exceptions.json']['entries']
    if duplicate_values(e['id'] for e in exceptions) or duplicate_values(e['form'] for e in exceptions):errors.append('Duplicate lexical exception')
    if sum(e['kind']=='frozen_exception' for e in exceptions)>5:errors.append('Too many frozen exceptions')
    for e in exceptions:
        if e['kind']=='regular_vocab_form' and not e['requires_vocab']:errors.append('Regular form requires vocabulary dependency')
        if not set(e['requires_vocab'])<={v['lemma'] for v in all_entries}:errors.append('Unknown exception dependency')
    if errors:return result()
    _,failure=introduction_assignment(exp)
    if failure:errors.append('Introduction windows infeasible: '+failure)
    intro_rows=files['introduction_schedule.json']['rows']
    if [r['text'] for r in intro_rows]!=list(range(1,301)):errors.append('Schedule texts must be ordered 1..300')
    introduced=[vid for r in intro_rows for vid in r['entry_ids']]
    if duplicate_values(introduced):errors.append('Duplicate scheduled introduction')
    if set(introduced)!=set(active_exp):errors.append('Schedule must introduce every Expansion exactly once')
    for row in intro_rows:
        if row['text']>=276 and row['entry_ids']:errors.append('New vocabulary in consolidation zone')
        for vid in row['entry_ids']:
            e=active_exp.get(vid)
            if e and not e['introduced_from']<=row['text']<=e['introduced_to']:errors.append(f'{vid}: scheduled introduction outside window')
    exposures=files['vocab_exposure_schedule.json'];plans=exposures['entries']
    if duplicate_values(p['vocab_id'] for p in plans):errors.append('Duplicate exposure entry')
    if {p['vocab_id'] for p in plans}!=set(active_exp):errors.append('Exposure schedule must cover all Expansion entries')
    first_by_id={vid:r['text'] for r in intro_rows for vid in r['entry_ids']}
    for plan in plans:
        vid=plan['vocab_id'];first=plan['first_introduction_text'];reviews=plan['review_texts']
        e=active_exp.get(vid)
        if not e:continue
        if first_by_id.get(vid)!=first:errors.append(f'{vid}: first introduction disagrees with introduction plan')
        if first>=276:errors.append(f'{vid}: first introduction in consolidation zone')
        if len(set([first]+reviews))<e['target_exposures']:errors.append(f'{vid}: fewer than six distinct exposure texts')
        if reviews!=sorted(reviews) or len(reviews)!=len(set(reviews)):errors.append(f'{vid}: duplicate or unordered reviews')
        if any(t<=first for t in reviews):errors.append(f'{vid}: review before or at first introduction')
        ages=[t-first for t in reviews]
        if not any(1<=age<=5 for age in ages):errors.append(f'{vid}: missing near review')
        if not any(6<=age<=30 for age in ages):errors.append(f'{vid}: missing medium review')
        long_min=min(60,math.floor(.75*(300-first)))
        if not any(age>=long_min for age in ages):errors.append(f'{vid}: missing long-distance review')
    if errors:return result()
    recalculated=text_load_rows(exp,plans,profile['exposure_policy']['recent_window_texts'])
    if exposures['texts']!=recalculated:errors.append('Exposure per-text load/index mismatch')
    statistics=load_statistics(recalculated)
    if exposures['statistics']!=statistics:errors.append('Exposure statistics mismatch')
    policy=profile['exposure_policy'];concentration=[]
    for row in recalculated:
        total=row['total_scheduled_expansion_count'];text=row['text']
        if row['new_vocab_count']>2:errors.append(f'{text}: more than two new entries')
        if total>policy['all_text_load_warn_above']:concentration.append(f'{text}: scheduled Expansion {total} exceeds 16')
        if text>=276:
            if total>policy['fast_zone_load_warn_above']:concentration.append(f'{text}: fast-zone Expansion {total} exceeds 12')
            if row['tier_counts']['E3']>policy['fast_zone_E3_warn_above']:concentration.append(f'{text}: fast-zone E3 concentration')
            if row['recently_introduced_E3_count']>policy['fast_zone_recent_E3_warn_above']:concentration.append(f'{text}: recently introduced E3 in fast zone')
    warnings.extend('LOAD: '+message for message in concentration)
    counts=Counter(len(r['entry_ids']) for r in intro_rows[:275])
    summary.update(id_migration={'retired':7,'new':7,'next_sequence':808,'rank_independent':True},
        replacements={'adopted':7,'pending':0},
        coverage_policy={'controlled_hard_min':1.0,'previous_hard_min':.98,'previous_target':.99,'new_token_soft_max':3},
        introduction_capacity={'assigned':len(introduced),'slots':550,'slack':50,
            'period_counts':dict(sorted((str(k),v) for k,v in counts.items())),
            'last_introduction':max(p['first_introduction_text'] for p in plans),'consolidation_new_entries':0},
        exposure_plan={'entries':len(plans),'planned_entry_text_pairs':sum(1+len(p['review_texts']) for p in plans),
            'min_distinct_texts':min(1+len(set(p['review_texts'])) for p in plans),'load_statistics':statistics,
            'concentration_warning_count':len(concentration),'status':'planned_not_observed'})
    homographs=defaultdict(list)
    for e in all_entries:homographs[e['lemma']].append(e)
    summary['distinct_lemmas']=len(homographs)
    summary['core_expansion_same_lemma']={lemma:[dict(pos=e['pos'],sense=e['sense'],tier=e['tier']) for e in group]
        for lemma,group in sorted(homographs.items()) if any(e['tier']=='core' for e in group) and any(e['tier']!='core' for e in group)}
    warnings.extend(['Exposure schedule is a plan; actual text occurrences, naturalness and learner retention are unverified.',
                     'Coverage evaluator requires correctly resolved lemma/POS/sense and grammar spans; no Korean parser or text generation in this phase.'])
    return result()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=DEFAULT_DIR);parser.add_argument('--json',action='store_true')
    args=parser.parse_args();output=validate(args.data_dir)
    if args.json:print(json.dumps(output,ensure_ascii=False,indent=2))
    else:
        print('PASS (data and exposure-plan validation)' if output['ok'] else 'FAIL')
        for label in ('core','expansion','total','tiers','grammar','introduction_capacity'):
            if label in output['summary']:print(f"{label}: {output['summary'][label]}")
        if 'exposure_plan' in output['summary']:
            p=output['summary']['exposure_plan'];print(f"exposures: {p['planned_entry_text_pairs']}; min distinct texts: {p['min_distinct_texts']}; concentration warnings: {p['concentration_warning_count']}")
        for message in output['errors']:print('ERROR: '+message)
        for message in output['warnings']:print('WARNING: '+message)
    return 0 if output['ok'] else 1

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');raise SystemExit(main())
