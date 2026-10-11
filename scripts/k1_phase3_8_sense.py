"""Small ID-scoped lexical policy overlay, not general word-sense disambiguation.

The occurrence must already have a canonical ID. A negative regex alone never
changes that identity. Unmatched contexts remain for author naturalness review;
no inferred dictionary meaning is added or prohibited.
"""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/'config/languages/ko/k1'
def policies():
    return {n:json.loads((CFG/n).read_text(encoding='utf8')) for n in ('basic_sense_families.json','explicit_restricted_senses.json')}

def validate_policy(files):
    """Policy integrity, not an audit of ordinary meanings of all 800 entries."""
    p=policies();v={e['id']:e for name in ('core_vocab.json','expansion_vocab.json') for e in files[name]}
    expected={'ko_k1_0072':('아침','morning',['morning_time','breakfast_meal']),
              'ko_k1_0074':('저녁','evening',['evening_time','dinner_meal'])}
    assert len(p['basic_sense_families.json']['entries'])==2
    for e in p['basic_sense_families.json']['entries']:
        assert (e['lemma'],e['registered_sense'],e['allowed_functions'])==expected[e['vocab_id']]
        assert (v[e['vocab_id']]['lemma'],v[e['vocab_id']]['sense'])==(e['lemma'],e['registered_sense'])
    ids=[]
    for e in p['explicit_restricted_senses.json']['entries']:
        ids.append(e['vocab_id']);original=v[e['vocab_id']]
        assert (original['lemma'],original['pos'],original['sense'])==(e['lemma'],e['pos'],e['allowed_sense'])
        assert original['notes']==e['source']['notes'] and original['notes']
        assert not re.search(e['negative_pattern'],e['positive_example'])
        assert re.search(e['negative_pattern'],e['negative_example'])
    assert len(ids)==len(set(ids)) and not set(ids)&set(expected)
    return True

def sense_checks(text,analysis):
    rows=[];registry={e['vocab_id']:e for e in policies()['explicit_restricted_senses.json']['entries']}
    for x in analysis['annotations']:
        e=registry.get(x.get('vocab_id'))
        if not e:continue
        # Exact local clause around the occurrence; never let a negative phrase
        # in a different sentence taint a legitimate use elsewhere in the text.
        start=max(text.rfind(c,0,x['start']) for c in '.!?')+1
        ends=[p for c in '.!?' if (p:=text.find(c,x['end']))>=0]
        end=min(ends)+1 if ends else len(text)
        clause=text[start:end];match=re.search(e['negative_pattern'],clause)
        rows.append(dict(vocab_id=e['vocab_id'],lemma=e['lemma'],surface=x['surface'],start=x['start'],end=x['end'],sentence=clause,
            allowed_sense=e['allowed_sense'],decision='FAIL' if match else 'NO_CLEAR_VIOLATION',
            detected_function=e['disallowed_function'] if match else None,
            evidence=dict(canonical_identity=x['vocab_id'],explicit_source=e['source'],negative_context=match.group() if match else None),
            category='lexical_policy_violation' if match else 'restricted_sense_usage',
            exhaustive_semantic_proof=False))
    return rows

def basic_family_usages(text,analysis):
    families={e['vocab_id']:e for e in policies()['basic_sense_families.json']['entries']};out=[]
    for x in analysis['annotations']:
        e=families.get(x.get('vocab_id'))
        if not e:continue
        tail=text[x['end']:];clause=re.split(r'[.!?]',tail,maxsplit=1)[0]
        meal=bool(re.match(r'(?:을|은|도|만)\s*.*먹',clause)) and not bool(re.match(r'에',clause))
        function=e['allowed_functions'][1 if meal else 0]
        out.append(dict(vocab_id=x['vocab_id'],surface=x['surface'],start=x['start'],end=x['end'],function=function,registered_sense_unchanged=x['sense'],decision='ALLOWED_BASIC_FAMILY',new_vocabulary_count=0,classification_scope='narrow meal/time diagnostic; not an exhaustive sense classifier'))
    return out
