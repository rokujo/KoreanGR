"""Small, auditable morphology repairs, not a complete sense disambiguator."""
from copy import deepcopy
import re
from k1_phase3_2_analysis import analyze as base_analyze
from k1_phase3 import DATA,read

HINTS=DATA/'phase3_1/morphology_hints.json'

def find_intent(text,sentence,word,intents):
    matching=[i for i in intents if i.get('sentence')==sentence and i.get('surface')==word]
    return matching[0] if len(matching)==1 else None

def walk_evidence(sentence,word,intent,scene_actions,files,allowed_ids):
    """No object and both licensed place-marker and companion evidence required.

    This deliberately rejects some real walking uses, e.g. 길을 걸어요, rather
    than auto-resolving every homographic 걸- as walk. No hang->walk alias.
    """
    entries=files['core_vocab.json']+files['expansion_vocab.json']
    walk=next(e for e in entries if (e['lemma'],e['pos'],e['sense'])==('걷다','verb','walk'))
    places={e['lemma'] for e in entries if e['id'] in allowed_ids and e['pos']=='noun' and 'place' in e['tags']}
    humans={'친구','가족','아버지','어머니','동생','형','오빠','누나','언니','사람','아이'}
    humans &= {e['lemma'] for e in entries if e['id'] in allowed_ids}
    forms=next(e['forms'] for e in read(HINTS)['entries'] if e['vocab_id']==walk['id'])
    evidence=dict(registered_identity=walk['id'] in allowed_ids,
        valid_inflection=word in forms,
        generated_intent_matches=bool(intent and all(intent.get(k)==walk[k] for k in ('lemma','pos','sense')) and intent.get('vocab_id')==walk['id']),
        locomotion_scene=bool(set(scene_actions)&{'walk','locomotion'}),
        licensed_location_marker=any(re.search(r'(?<![가-힣])'+re.escape(p)+r'(?:까지|에서|으로|로|에)(?=\s)',sentence) for p in places),
        human_companion=any(re.search(r'(?<![가-힣])'+re.escape(h)+r'하고(?=\s)',sentence) for h in humans),
        no_direct_object=not bool(re.search(r'[가-힣]+(?:을|를)(?=\s)',sentence)))
    return dict(status='RESOLVED' if all(evidence.values()) else 'REVIEW',evidence=evidence,
        vocab_id=walk['id'],lemma='걷다',pos='verb',sense='walk',
        scope='Conservative local-context inference; not native speaker approval')

def analyze(text,files,text_number,selected_reviews=(),intents=(),scene_actions=(),kiwi=None):
    result=base_analyze(text,files,text_number,selected_reviews,{},kiwi)
    result['resolver_decisions']=result.pop('boundary_decisions',[])
    allowed={e['id'] for e in files.get('_allowed_vocab',files['core_vocab.json'])}
    # Exact registered exchange compound prefix. Keep all raw tokens unchanged.
    exchange={'돕':'도와주다','빌리':'빌려주다','돌리':'돌려주다','묻':'물어보다'}
    for word in re.finditer(r'\S+',text):
        ids=[i for i,t in enumerate(result['raw_morphology']) if word.start()<=t['start']<word.end()]
        if len(ids)<3:continue
        ts=[result['raw_morphology'][i] for i in ids[:3]]
        lemma=exchange.get(ts[0]['form'])
        tail='보' if lemma=='물어보다' else '주'
        if not lemma or [t['form'] for t in ts[1:]]!=['어',tail] or ts[0]['tag'].split('-')[0]!='VV' or ts[1]['tag']!='EC' or ts[2]['tag'].split('-')[0] not in ('VV','VX'):continue
        expected_surface={'도와주다':'도와','빌려주다':'빌려','돌려주다':'돌려','물어보다':'물어'}[lemma]
        if not text[ts[0]['start']:].startswith(expected_surface):continue
        matches=[e for e in files['core_vocab.json']+files['expansion_vocab.json'] if e['lemma']==lemma and e['pos']=='verb']
        if len(matches)!=1:continue
        e=matches[0];group=ids[:3]
        old=[a for a in result['annotations'] if set(a['morph_indices'])&set(group)]
        result['annotations']=[a for a in result['annotations'] if a not in old]
        result['unresolved_tokens']=[a for a in result['unresolved_tokens'] if a not in old]
        starts={a['start'] for a in old}
        result['annotation_review_required']=[a for a in result['annotation_review_required'] if a['start'] not in starts]
        start=ts[0]['start'];end=ts[2]['start']+ts[2]['length']
        # Known compound segmentation is independent of temporal permission.
        role='core' if e['tier']=='core' else 'scheduled_review' if e['id'] in selected_reviews else 'previous_expansion'
        result['annotations'].append(dict(surface=text[start:end],lemma=e['lemma'],pos=e['pos'],sense=e['sense'],vocab_id=e['id'],role=role,start=start,end=end,morph_indices=group,grammar_id=None))
        result['resolver_decisions'].append(dict(type='registered_compound_prefix',lemma=lemma,surface=word.group(),start=start,
            raw_signature=[t['form'] for t in ts],status='GROUPED_NOT_PERMISSION_GRANTED'))
    # Walking resolution operates on full eojeol but replaces only its lexical
    # stem annotation. Endings and raw morphology remain separate evidence.
    for match in re.finditer(r'[^.!?]+[.!?][”"]?|[^.!?]+$',text):
        sentence=match.group().strip();offset=match.start()+len(match.group())-len(match.group().lstrip())
        for wordmatch in re.finditer(r'\S+',sentence):
            word=wordmatch.group().strip('"“”.,!?')
            intent=find_intent(text,sentence,word,intents)
            if word not in ('걸어요','걸었어요','걸어서','걸으면','걸을까요') and not (intent and intent.get('lemma')=='걷다'):continue
            decision=walk_evidence(sentence,word,intent,scene_actions,files,allowed)
            start=offset+wordmatch.start();end=offset+wordmatch.end()
            decision.update(type='walk_hang_context',surface=word,sentence=sentence,start=start,end=end)
            candidates=[a for a in result['annotations'] if start<=a['start']<end and a['role']!='grammar_function']
            can_replace=len(candidates)==1 and candidates[0]['lemma'] in ('걷다','걸다') and all(result['raw_morphology'][i]['tag'].split('-')[0]=='VV' for i in candidates[0]['morph_indices'])
            if decision['status']=='RESOLVED' and can_replace:
                a=candidates[0];original=deepcopy(a)
                a.update(lemma='걷다',pos='verb',sense='walk',vocab_id=decision['vocab_id'],role='core')
                result['unresolved_tokens']=[x for x in result['unresolved_tokens'] if x is not a]
                result['annotation_review_required']=[x for x in result['annotation_review_required'] if x['start']!=a['start']]
                result['annotation_review_required'].append(dict(type='limited_context_resolution',surface=a['surface'],lemma='걷다',start=a['start'],candidate_id=a['vocab_id']))
                decision['original_annotation']=original
            elif decision['status']=='RESOLVED':
                decision['status']='REVIEW';decision['reason']='Raw predicate/eojeol grouping not uniquely supported'
            # If author asserts WALK but evidence is insufficient, no valid
            # dictionary annotation may bypass the conservative ambiguity gate.
            uncertain_walk=any(a['lemma']=='걷다' or (a['lemma']=='걸다' and not a['vocab_id']) for a in candidates)
            decision['requires_candidate_review']=bool(decision['status']=='REVIEW' and (uncertain_walk or (intent and intent.get('lemma')=='걷다')))
            result['resolver_decisions'].append(decision)
    result['annotations'].sort(key=lambda a:(a['start'],a['morph_indices'][0]))
    # Only a successful independently constrained prefix/context resolver can
    # discharge a boundary REVIEW attached to the exact replaced raw span.
    resolved_starts={d['start'] for d in result['resolver_decisions'] if d.get('status')=='RESOLVED' and 'original_annotation' in d}
    for d in result['resolver_decisions']:
        if d.get('type')=='identity_boundary' and d.get('start') in resolved_starts:d['requires_candidate_review']=False
    result['grammar_used']=sorted({a['grammar_id'] for a in result['annotations'] if a['grammar_id']})
    if any(x['type']=='attributive_pos_boundary' for x in result['annotation_review_required']):
        result['grammar_used']=sorted(set(result['grammar_used'])|{'ko_k1_g26'})
    return result
