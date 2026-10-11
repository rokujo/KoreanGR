"""Select 20 stress-test states from frozen data, never fixed replacement text numbers."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from k1_history import historical_root
ROOT=historical_root(ROOT)
DATA=ROOT/'config/languages/ko/k1'

def load_inputs():
    return {p.name:json.loads(p.read_text(encoding='utf-8')) for p in DATA.glob('*.json')}

def select(files):
    if files.get('id_migration.json',{}).get('phase')=='2.1A':
        raise ValueError('Phase 2.2 must reuse the frozen 20-number selection, not recompute it from new migration IDs.')
    vocab={e['id']:e for e in files['expansion_vocab.json']}
    schedule=files['vocab_exposure_schedule.json']
    first={e['vocab_id']:e['first_introduction_text'] for e in schedule['entries']}
    reasons={}
    def add(key,text):reasons[key]=text
    for m in files['id_migration.json']['mappings']:
        add('replacement:'+m['new_lemma'],first[m['new_id']])
    for vid,e in vocab.items():
        if e['confidence']=='medium':add('medium:'+e['lemma'],first[vid])
    add('first_e1',min(first[vid] for vid,e in vocab.items() if e['tier']=='E1'))
    add('first_e2',min(first[vid] for vid,e in vocab.items() if e['tier']=='E2'))
    rows=schedule['texts']
    add('first_single',min(r['text'] for r in rows if r['new_vocab_count']==1))
    add('first_zero',min(r['text'] for r in rows if r['new_vocab_count']==0))
    middle=files['profile.json']['target_texts']//2
    add('midpoint',min(rows,key=lambda r:(abs(r['text']-middle),r['text']))['text'])
    add('mid_zero',min((r for r in rows if r['new_vocab_count']==0),key=lambda r:(abs(r['text']-middle),r['text']))['text'])
    fast=[r for r in rows if r['text']>=files['profile.json']['introduction']['consolidation_from']]
    replacements={m['new_id'] for m in files['id_migration.json']['mappings']}
    add('fast_first',fast[0]['text'])
    add('fast_replacements',max(fast,key=lambda r:(len(set(r['review_vocab_ids'])&replacements),-r['text']))['text'])
    add('fast_late',max(r['text'] for r in fast if set(r['review_vocab_ids'])&replacements))
    numbers=sorted(set(reasons.values()))
    assert 18<=len(numbers)<=24
    return {'status':'pilot_selected_from_frozen_data','text_numbers':numbers,'selection_keys':reasons,
            'rows':[{'text_number':n,'reasons':[k for k,t in reasons.items() if t==n],
                     'scheduled_new_vocab_ids':rows[n-1]['new_vocab_ids'],
                     'scheduled_review_vocab_ids':rows[n-1]['review_vocab_ids']} for n in numbers]}

if __name__=='__main__':
    from k1_history import protect_historical_build
    protect_historical_build(Path(__file__).resolve().parents[1])
    path=ROOT/'pilot/ko/k1/selection.json';path.parent.mkdir(parents=True,exist_ok=True)
    selection=select(load_inputs())
    path.write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Selected:',selection['text_numbers'])
