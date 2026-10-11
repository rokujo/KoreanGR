"""Validate Phase 1.1 data. Exit 0: structural checks pass; 1: invalid; 2: dependency missing.

Run from any directory: python /path/to/scripts/validate_k1_vocab.py [--json]
This validates data and introduction capacity, not learner text quality or real learning.
"""
import argparse
from collections import Counter, defaultdict
import heapq
import json
from pathlib import Path
import sys
import unicodedata

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print('Missing jsonschema. Run: python -m pip install -r requirements-dev.txt', file=sys.stderr)
    raise SystemExit(2)

DEFAULT_DIR = Path(__file__).resolve().parents[1] / 'config/languages/ko/k1'
CATEGORY_COUNTS = {
    'people_social':40,'places_objects':90,'food_nature':50,'verbs':100,
    'adjectives':65,'adverbs_connectors':50,'time_counters_units':35,
    'abstract_body_emotion':40,'school_work_transport_info':30,
}

def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON object key: {key}')
        result[key]=value
    return result

def load_json(path):
    def reject_constant(value):
        raise ValueError(f'Non-JSON numeric constant: {value}')
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)

def duplicate_values(values):
    return [value for value,count in Counter(values).items() if count>1]

def key(entry):
    return (entry['lemma'],entry['pos'],entry['sense'])

def introduction_assignment(entries, texts=275, capacity=2, capacities=None, include_empty=False):
    """Earliest-deadline scheduling of unit jobs with release times and deadlines.

    For integer interval windows and identical slots this gives a feasibility witness.
    The witness is not a curriculum, does not assert semantic exposure or known ratio.
    """
    pending=sorted(entries,key=lambda e:(e['introduced_from'],e['rank']))
    heap=[];index=0;schedule=[]
    for text in range(1,texts+1):
        while index<len(pending) and pending[index]['introduced_from']<=text:
            e=pending[index]
            heapq.heappush(heap,(e['introduced_to'],e['rank'],e['id']))
            index+=1
        if heap and heap[0][0]<text:
            return None,f'{heap[0][2]} misses deadline {heap[0][0]}'
        assigned=[]
        slots=capacities.get(text,capacity) if capacities is not None else capacity
        if not isinstance(slots,int) or isinstance(slots,bool) or not 0<=slots<=capacity:
            return None,f'Invalid capacity at text {text}: {slots}'
        for _ in range(slots):
            if heap:
                deadline,rank,entry_id=heapq.heappop(heap)
                assigned.append(entry_id)
        if assigned or include_empty:schedule.append({'text':text,'entry_ids':assigned})
    if heap or index!=len(pending):
        return None,'Not enough slots inside introduction windows'
    return schedule,None

def validate(data_dir):
    errors=[];warnings=[];summary={}
    def error(message):errors.append(message)
    files={}
    names=['core_vocab.json','expansion_vocab.json','core_vocab.source.json','grammar.json',
           'lexical_exceptions.json','profile.json','proper_names.json',
           'expansion_replacement_proposals.json','introduction_schedule.json',
           'vocab.schema.json','grammar.schema.json','support.schema.json']
    for name in names:
        try:files[name]=load_json(data_dir/name)
        except (OSError,ValueError) as exc:error(f'{name}: {exc}')
    if errors:return {'ok':False,'errors':errors,'warnings':warnings,'summary':summary}
    for name,schema_name in [('core_vocab.json','vocab.schema.json'),
                            ('expansion_vocab.json','vocab.schema.json'),
                            ('core_vocab.source.json','vocab.schema.json'),
                            ('grammar.json','grammar.schema.json')]:
        schema=files[schema_name]
        try:Draft202012Validator.check_schema(schema)
        except Exception as exc:
            error(f'{schema_name}: invalid JSON Schema: {exc}');continue
        for problem in Draft202012Validator(schema).iter_errors(files[name]):
            location='/'.join(str(p) for p in problem.absolute_path) or '<root>'
            error(f'{name}:{location}: {problem.message}')
    support=files['support.schema.json']
    try:
        Draft202012Validator.check_schema(support)
        for name,definition in [('profile.json','profile'),('lexical_exceptions.json','exceptions'),
                                ('proper_names.json','proper_names'),
                                ('expansion_replacement_proposals.json','replacement_proposals'),
                                ('introduction_schedule.json','introduction_schedule')]:
            schema={**support,'$ref':f'#/$defs/{definition}'}
            for problem in Draft202012Validator(schema).iter_errors(files[name]):
                location='/'.join(str(p) for p in problem.absolute_path) or '<root>'
                error(f'{name}:{location}: {problem.message}')
    except Exception as exc:error(f'support.schema.json: {exc}')
    # Avoid interpreting invalid shapes as trusted semantic data.
    if errors:return {'ok':False,'errors':errors,'warnings':warnings,'summary':summary}
    core=files['core_vocab.json'];exp=files['expansion_vocab.json'];all_entries=core+exp
    source=files['core_vocab.source.json'];profile=files['profile.json']
    summary.update(core=len(core),expansion=len(exp),total=len(all_entries),source_core=len(source),
                   tiers=dict(Counter(e['tier'] for e in exp)),
                   expansion_pos=dict(sorted(Counter(e['pos'] for e in exp).items())),
                   expansion_categories=dict(Counter(e.get('category') for e in exp)),
                   grammar=len(files['grammar.json']),
                   confidence=dict(Counter(e.get('confidence','unspecified') for e in exp)))
    for label,actual,expected in [('Core',len(core),300),('Expansion',len(exp),500),('Total',len(all_entries),800),('Source Core',len(source),300)]:
        if actual!=expected:error(f'{label} count: {actual}, expected {expected}')
    for label,values in [('ID',[e['id'] for e in all_entries]),
                         ('rank',[e['rank'] for e in all_entries]),
                         ('lemma+POS+sense',[key(e) for e in all_entries])]:
        duplicates=duplicate_values(values)
        if duplicates:error(f'Duplicate {label}: {duplicates}')
    overlap=set(map(key,core)) & set(map(key,exp))
    if overlap:error(f'Core/Expansion overlap: {sorted(overlap)}')
    source_overlap=set(map(key,source)) & set(map(key,exp))
    if source_overlap:error(f'Original Core/Expansion overlap: {sorted(source_overlap)}')
    if any(e['tier']!='core' for e in core):error('Core contains non-core tier')
    if Counter(e['tier'] for e in exp)!=Counter({'E1':200,'E2':200,'E3':100}):error('Tier counts must be E1=200 E2=200 E3=100')
    if Counter(e.get('category') for e in exp)!=Counter(CATEGORY_COUNTS):error('Expansion category counts differ from target')
    if set(e['rank'] for e in all_entries)!=set(range(1,801)):error('Ranks must cover 1..800')
    if [e['rank'] for e in core]!=list(range(1,301)):error('Core ranks must be ordered 1..300')
    if [e['rank'] for e in exp]!=list(range(301,801)):error('Expansion ranks must be ordered 301..800')
    for e in all_entries:
        if e['id']!=f"ko_k1_{e['rank']:04}":error(f"{e['id']}: ID/rank mismatch")
        if e['lemma']!=unicodedata.normalize('NFC',e['lemma']):error(f"{e['id']}: lemma must be NFC")
        if any(form!=unicodedata.normalize('NFC',form) for form in e['forms']):error(f"{e['id']}: forms must be NFC")
        if e['allow_inflection']!=(e['pos'] in ('verb','adjective')):
            error(f"{e['id']}: allow_inflection must match predicate POS (numeral allomorphs go in forms)")
        if e['tier']!='core':
            start,end=e['introduced_from'],e['introduced_to']
            if start>end:error(f"{e['id']}: introduction start exceeds end")
            lower,upper=profile['introduction']['ranges'][e['tier']]
            if not lower<=start<=end<=upper:error(f"{e['id']}: window outside tier range")
            if e['target_exposures']>profile['target_texts']-end+1:
                error(f"{e['id']}: too few distinct texts after latest introduction")
            if e['target_exposures']>6 and not e['notes']:
                error(f"{e['id']}: increased exposures require notes")
    proper_lemmas={e['lemma'] for e in files['proper_names.json']['entries']}
    if proper_lemmas & {e['lemma'] for e in all_entries}:error('Counted vocabulary contains a registered proper name')
    if not profile['hard_min_known_vocab_ratio']<=profile['target_known_vocab_ratio']:
        error('hard_min_known_vocab_ratio must not exceed target_known_vocab_ratio')
    expected_slots=profile['introduction']['last_text']*profile['new_vocab']['max_entries_per_text']
    if profile['feasibility']['introduction_slots']!=expected_slots:error('Introduction slot metadata mismatch')
    if profile['feasibility']['required_new_entries']!=len(exp):error('Required new entry metadata mismatch')
    if profile['feasibility']['slack_slots']!=expected_slots-len(exp):error('Slack slot metadata mismatch')
    grammar=files['grammar.json']
    if len(grammar)!=32 or len(grammar)!=profile['grammar_count']:error('Grammar count must be 32 and match profile')
    if [e['id'] for e in grammar]!=[f'ko_k1_g{i:02}' for i in range(1,33)]:error('Grammar IDs must be ordered g01..g32')
    if [e['form'] for e in grammar[29:]]!=['-(으)로','부터 / 까지','만']:error('Added grammar must be means/direction, start/end, limitation')
    exceptions=files['lexical_exceptions.json']['entries']
    if duplicate_values(e['id'] for e in exceptions):error('Duplicate exception ID')
    if duplicate_values(e['form'] for e in exceptions):error('Duplicate exception form')
    frozen=[e for e in exceptions if e['kind']=='frozen_exception']
    if len(frozen)>5:error('Frozen exception count exceeds five; review required')
    for e in exceptions:
        if e['kind']=='regular_vocab_form' and not e['requires_vocab']:error(f"{e['id']}: regular form requires a vocabulary link")
        for lemma in e['requires_vocab']:
            if lemma not in {e['lemma'] for e in all_entries}:error(f"{e['id']}: unknown vocabulary dependency {lemma}")
    witness=None
    if not errors:
        witness,failure=introduction_assignment(exp,profile['introduction']['last_text'],profile['new_vocab']['max_entries_per_text'])
        if failure:error(f'Introduction windows infeasible: {failure}')
    proposals=files['expansion_replacement_proposals.json']['entries']
    proposed_sources=[e['source_id'] for e in proposals]
    if duplicate_values(proposed_sources):error('Duplicate replacement proposal source')
    candidates=[(e['candidate']['lemma'],e['candidate']['pos'],e['candidate']['sense']) for e in proposals]
    if duplicate_values(candidates):error('Duplicate replacement candidate')
    if set(candidates) & set(map(key,all_entries)):error('Replacement candidate already in active vocabulary')
    active_by_id={e['id']:e for e in exp}
    valid_pos={'noun','verb','adjective','adverb','pronoun','determiner','numeral','counter','conjunction','interjection'}
    for proposal in proposals:
        active=active_by_id.get(proposal['source_id'])
        if not active:
            error(f"Unknown proposal source: {proposal['source_id']}");continue
        if key(active)!=(proposal['source_lemma'],proposal['source_pos'],proposal['source_sense']):error('Replacement proposal source identity mismatch')
        candidate=proposal['candidate']
        if candidate['pos'] not in valid_pos:error('Invalid replacement candidate POS')
        if candidate['tier']!=active['tier']:error('One-for-one replacement candidate must preserve tier counts')
        if candidate['category']!=active['category']:error('One-for-one replacement candidate must preserve category counts')
        if proposal['status']!='pending_human_review':error('Replacement proposal must remain pending human review')
    # Dry-run counts and lexical identities, never write projected terms into the DB.
    replacements={p['source_id']:p['candidate'] for p in proposals}
    projected=[{**e,**replacements[e['id']]} if e['id'] in replacements else e for e in exp]
    if len(projected)!=500 or len(core)+len(projected)!=800:error('Replacement projection changes vocabulary counts')
    if Counter(e['tier'] for e in projected)!=Counter({'E1':200,'E2':200,'E3':100}):error('Replacement projection changes tier counts')
    if Counter(e['category'] for e in projected)!=Counter(CATEGORY_COUNTS):error('Replacement projection changes category counts')
    if duplicate_values(key(e) for e in core+projected):error('Replacement projection causes lemma+POS+sense collision')
    if proper_lemmas & {e['lemma'] for e in projected}:error('Replacement projection includes a proper name')
    rows=files['introduction_schedule.json']['rows']
    if [row['text'] for row in rows]!=list(range(1,301)):error('Schedule texts must be ordered 1..300')
    scheduled_ids=[entry_id for row in rows for entry_id in row['entry_ids']]
    if duplicate_values(scheduled_ids):error('Duplicate scheduled introduction')
    if set(scheduled_ids)!=set(active_by_id):error('Schedule must introduce every Expansion entry exactly once')
    for row in rows:
        text=row['text']
        if text>=profile['introduction']['consolidation_from'] and row['entry_ids']:
            error(f'New vocabulary in consolidation zone at text {text}')
        lemmas=[]
        for entry_id in row['entry_ids']:
            e=active_by_id.get(entry_id)
            if e is None:continue
            lemmas.append(e['lemma'])
            if not e['introduced_from']<=text<=e['introduced_to']:error(f'{entry_id}: scheduled introduction outside window')
        if len(set(lemmas))>profile['new_vocab']['max']:error(f'Too many new lemmas at text {text}')
    intro_rows=[row for row in rows if row['text']<=profile['introduction']['last_text']]
    counts=Counter(len(row['entry_ids']) for row in intro_rows)
    if not counts[0] or not counts[1]:error('Schedule witness must include zero- and one-introduction texts inside 1..275')
    if errors:return {'ok':False,'errors':errors,'warnings':warnings,'summary':summary}
    if witness is not None:
        summary['introduction_capacity']={
            'assigned':sum(len(t['entry_ids']) for t in witness),
            'texts_used':sum(bool(row['entry_ids']) for row in intro_rows),'period_texts':275,
            'slots':expected_slots,'slack':expected_slots-len(exp),
            'witness_period_counts':dict(sorted((str(k),v) for k,v in counts.items())),
            'witness_assigned':len(scheduled_ids),
            'witness_last_introduction':max(row['text'] for row in intro_rows if row['entry_ids']),
            'consolidation_texts':25,'consolidation_new_entries':sum(len(row['entry_ids']) for row in rows if row['text']>=276)}
        summary['known_ratio_policy']={'hard_min':profile['hard_min_known_vocab_ratio'],
                                       'target':profile['target_known_vocab_ratio'],
                                       'first_text_new_lemma_token_soft_max':profile['new_vocab']['first_text_new_lemma_token_soft_max']}
        summary['replacement_proposals']={'pending':len(proposals),'applied':False,
            'projection':{'core':len(core),'expansion':len(projected),'total':len(core)+len(projected),
                          'tiers':dict(Counter(e['tier'] for e in projected)),
                          'categories':dict(Counter(e['category'] for e in projected)),
                          'collisions':0,
                          'notes':'Dry-run counts and lexical identity checks only; not adopted DB or certified language quality.'}}
    homographs=defaultdict(list)
    for e in all_entries:homographs[e['lemma']].append(e)
    summary['core_expansion_same_lemma']={
        lemma:[{'pos':e['pos'],'sense':e['sense'],'tier':e['tier']} for e in group]
        for lemma,group in sorted(homographs.items())
        if any(e['tier']=='core' for e in group) and any(e['tier']!='core' for e in group)}
    summary['distinct_lemmas']=len(homographs)
    warnings.extend([
        'Replacement proposals are pending; the active 500 contains seven provisional K2 deferral candidates.',
        'At most three new-lemma tokens does not guarantee hard 98% or target 99%; actual lexical denominator and knowledge must be measured.',
        'Counts/schema pass does not certify dictionary senses, naturalness, learner familiarity, or six real exposure texts.',
    ])
    return {'ok':not errors,'errors':errors,'warnings':warnings,'summary':summary}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=DEFAULT_DIR)
    parser.add_argument('--json',action='store_true',help='Machine-readable results')
    args=parser.parse_args()
    result=validate(args.data_dir)
    if args.json:
        print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print('PASS (structural validation; review warnings below)' if result['ok'] else 'FAIL')
        for label in ('core','expansion','total','tiers','grammar','introduction_capacity'):
            if label in result['summary']:print(f"{label}: {result['summary'][label]}")
        for message in result['errors']:print(f'ERROR: {message}')
        for message in result['warnings']:print(f'WARNING: {message}')
    return 0 if result['ok'] else 1

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
