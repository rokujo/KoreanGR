"""Closed-vocabulary evidence overlay; never mutate raw morphology or invent senses."""
from copy import deepcopy
import re
from k1_phase3_6a_resolver import analyze as previous_analyze,HINTS,OVERLAY
from k1_phase3_3_resolver import quotation_context,role,PARTICLE_TAGS,NOMINAL_TAGS
from k1_phase3 import DATA,read

REGISTRY=DATA/'controlled_surface_recovery.json'

def allowed_entries(f):
    # Production provides the actual snapshot. Diagnostic calls must explicitly
    # provide a closed allowed list too; absence does not authorize all Expansion.
    return f.get('_allowed_vocab',f['core_vocab.json'])

def recover(text,result,f,t,selected=(),kiwi=None,scope='unspecified'):
    a=deepcopy(result);raw=a['raw_morphology'];before=deepcopy(raw)
    policy=read(REGISTRY);classes={e['vocab_id']:e for e in policy['entries']}
    allowed=allowed_entries(f);by_surface={}
    for e in allowed:
        c=classes[e['id']]
        if (e['lemma'],e['pos'],e['sense'])!=(c['lemma'],c['pos'],c['sense']):raise ValueError('Surface registry identity mismatch')
        for form in c['registered_surfaces']:by_surface.setdefault(form,[]).append(e)
    audit=[]
    for surface,entries in sorted(by_surface.items(),key=lambda item:-len(item[0])):
        c=classes[entries[0]['id']]
        # Existing specific resolvers own other high-risk words and conjugations.
        if c['classification']=='morphology_required' or (c['classification']=='context_required' and surface!='우리'):continue
        for hit in re.finditer(re.escape(surface),text):
            start,end=hit.span()
            if start and re.match(r'[가-힣A-Za-z0-9_]',text[start-1]):continue
            indices=[i for i,r in enumerate(raw) if r['start']<end and r['start']+r['length']>start]
            parts=[raw[i] for i in indices]
            old=[x for x in a['annotations'] if set(x.get('morph_indices',[]))&set(indices)]
            represented=[i for x in old for i in x.get('morph_indices',[])]
            following=raw[indices[-1]+1] if indices and indices[-1]+1<len(raw) else None
            q=quotation_context(text,start,end)
            evidence=dict(exact_registered_surface=text[start:end]==surface,
                allowed_unique_identity=len(entries)==1,
                indices_contiguous=bool(indices) and indices==list(range(indices[0],indices[-1]+1)),
                exact_character_partition=bool(parts) and parts[0]['start']==start and parts[-1]['start']+parts[-1]['length']==end and all(x['start']+x['length']==y['start'] for x,y in zip(parts,parts[1:])),
                no_internal_whitespace_or_punctuation=bool(parts) and not any(ch.isspace() for ch in text[start:end]) and all(not p['tag'].startswith('S') for p in parts),
                annotation_exclusive=bool(old) and all(set(x.get('morph_indices',[]))<=set(indices) and x['start']>=start and x['end']<=end for x in old),
                raw_accounted_once=set(represented)==set(indices) and len(represented)==len(set(represented)),
                no_conflicting_registered_identity=all(x.get('vocab_id') in (None,entries[0]['id']) for x in old),
                balanced_boundary=not q['inside_unmatched'])
            probe=None;anchors=[]
            if c['classification']=='unique_safe':
                attached=bool(following and following['start']==end and (following['tag'] in PARTICLE_TAGS or following['tag']=='VCP'))
                head=bool(following and text[end:following['start']].isspace() and following['tag'] in NOMINAL_TAGS)
                bare=not text[end:end+1] or text[end:end+1] in '.!?"”’」』'
                evidence.update(nominal_position=attached or head or bare,
                    nominal_raw_parts=bool(parts) and all(x['tag'] in NOMINAL_TAGS|{'MM','MAG'} for x in parts),
                    exact_raw_parts=''.join(p['form'] for p in parts)==surface)
            else:
                sentence_left=max(text.rfind(ch,0,start) for ch in '.!?\n')+1
                tail=re.search(r'[.!?\n]',text[end:]);sentence_right=end+tail.end() if tail else len(text)
                if q['inside_balanced']:sentence_left=q['open_offset'];sentence_right=q['close_offset']+1
                clause=text[sentence_left:sentence_right]
                # Independent old analyzer: no generated intents, no recursion.
                p=previous_analyze(clause,f,t,selected,(),(),kiwi,scope='controlled_surface_short_evidence')
                local=start-sentence_left
                short_np=any(r['form']=='우리' and r['tag']=='NP' and r['start']==local for r in p['raw_morphology'])
                short_id=any(x['vocab_id']=='ko_k1_0004' and x['start']==local and x['end']==local+2 for x in p['annotations'])
                probe=dict(text=clause,original_start=sentence_left,raw_morphology=p['raw_morphology'],annotations=p['annotations'])
                for i,r in enumerate(raw):
                    if not max(0,start-350)<=r['start']<start:continue
                    next_r=raw[i+1] if i+1<len(raw) else None
                    if r['tag']=='NP' and r['form'] in ('저','나','우리') and next_r and next_r['start']==r['start']+r['length'] and next_r['tag'] in ('JKS','JX'):
                        anchors.append(deepcopy(r))
                # Short NP group-reference is syntactic evidence for a standalone
                # sentence; NNG recovery additionally requires actual discourse.
                human_heads=policy['uri_topic_context']['human_group_predicates']
                group_predicate=any(r['tag']=='VV' and r['form'] in human_heads for r in p['raw_morphology'])
                spatial=bool(re.search(r'우리\s*(?:안|밖|위|아래|앞|뒤|옆)(?:에|에서|으로|로|은|는|이|가|\s)',clause) or text[end:].startswith(('에서','에','의')))
                evidence.update(exact_uri_single_raw=len(parts)==1 and parts[0]['form']=='우리' and parts[0]['tag'] in ('NP','NNG'),
                    following_topic_particle=bool(following and following['start']==end and following['form']=='는' and following['tag']=='JX'),
                    independent_short_np_identity=short_np and short_id,
                    speaker_group_evidence=bool(anchors) or bool(parts and parts[0]['tag']=='NP' and short_np),
                    human_group_predicate=group_predicate,no_spatial_enclosure_frame=not spatial)
            existing=any(x['vocab_id']==entries[0]['id'] and x['start']==start and x['end']==end for x in old)
            decision='ALREADY_REGISTERED' if existing else 'RECOVERED' if all(evidence.values()) else 'REVIEW'
            # Existing verified modifier resolution is authoritative for its own
            # limited construction; this layer does not broaden or revoke it.
            row=dict(type='controlled_lexical_surface_recovery',classification=c['classification'],surface=surface,start=start,end=end,
                registered_vocab_id=entries[0]['id'],registered_pos=entries[0]['pos'],registered_sense=entries[0]['sense'],scope=scope,
                raw_parts=deepcopy(parts),raw_indices=indices,quotation_context=q,evidence=evidence,
                short_scope_probe=probe,speaker_anchors=anchors,original_annotations=deepcopy(old),decision=decision,
                current_snapshot_permission=True,annotation_intent_not_authority=True)
            if decision=='RECOVERED':
                e=entries[0];a['annotations']=[x for x in a['annotations'] if x not in old]
                a['annotations'].append(dict(surface=surface,lemma=e['lemma'],pos=e['pos'],sense=e['sense'],vocab_id=e['id'],role=role(e,f,t,selected),start=start,end=end,morph_indices=indices,grammar_id=None))
                a['annotation_review_required']=[x for x in a['annotation_review_required'] if not (x.get('start')==start and x.get('type') in ('identity_evidence_insufficient','identity_boundary'))]
                for d in a['resolver_decisions']:
                    if d.get('start')==start and d.get('type') in ('identity_boundary','uri_pronoun_context') and d.get('requires_candidate_review'):
                        d.update(requires_candidate_review=False,discharged_by='controlled_surface_evidence')
            audit.append(row)
    a['controlled_surface_recovery_audit']=audit
    a['annotations'].sort(key=lambda x:(x['start'],x['end']))
    a['unresolved_tokens']=[x for x in a['annotations'] if x['role']=='unresolved']
    assert raw==before
    return a

def analyze(text,files,text_number,selected_reviews=(),intents=(),scene_actions=(),kiwi=None,scope='unspecified'):
    base=previous_analyze(text,files,text_number,selected_reviews,intents,scene_actions,kiwi,scope)
    return recover(text,base,files,text_number,selected_reviews,kiwi,scope)


def focused_scope_parity(text,full,sentences,sentence_results,files,t,new_ids,selected=(),intents=(),actions=(),kiwi=None):
    """Identity comparison, not another sense resolver or semantic-role gate.

    Sentence prechecks are reused. Paragraphs are analyzed once. Only current
    new / risky identities are compared at original character coordinates.
    """
    scopes=[];cursor=0
    for sentence,a in zip(sentences,sentence_results):
        lo=text.find(sentence,cursor)
        if lo<0:raise ValueError('Sentence span cannot align to original text')
        scopes.append(dict(scope='sentence',lo=lo,hi=lo+len(sentence),analysis=a));cursor=lo+len(sentence)
    cursor=0
    for paragraph in text.split('\n\n'):
        lo=text.find(paragraph,cursor)
        a=analyze(paragraph,files,t,selected,intents,actions,kiwi,scope='paragraph_parity')
        scopes.append(dict(scope='paragraph',lo=lo,hi=lo+len(paragraph),analysis=a));cursor=lo+len(paragraph)
    scopes.append(dict(scope='full_text',lo=0,hi=len(text),analysis=full))
    risk={'네','너','아니요','한국어','우리','저','이','그','눈','풀','쓰다','걷다','개'}
    focus={r['registered_vocab_id'] for sc in scopes for r in sc['analysis'].get('controlled_surface_recovery_audit',[])}|set(new_ids)|{e['id'] for e in files['core_vocab.json']+files['expansion_vocab.json'] if e['lemma'] in risk}
    spans=set()
    for sc in scopes:
        for x in sc['analysis']['annotations']:
            if x['vocab_id'] in focus:spans.add((x['start']+sc['lo'],x['end']+sc['lo']))
    rows=[]
    for start,end in sorted(spans):
        views=[]
        for sc in scopes:
            if not sc['lo']<=start<end<=sc['hi']:continue
            lo,hi=start-sc['lo'],end-sc['lo'];a=sc['analysis']
            ids=sorted({x['vocab_id'] for x in a['annotations'] if x['vocab_id'] and x['start']<hi and x['end']>lo})
            pre=ids
            recoveries=[r for r in a.get('ne_response_recovery_audit',[])+a.get('controlled_surface_recovery_audit',[]) if r['start']==lo and r['end']==hi]
            if recoveries:
                pre=sorted({x['vocab_id'] for r in recoveries for x in r['original_annotations'] if x['vocab_id']})
            views.append(dict(scope=sc['scope'],original_offset=sc['lo'],before_recovery_ids=pre,resolved_ids=ids,
                ne_recovery_decisions=[r['decision'] for r in recoveries]))
        after={tuple(v['resolved_ids']) for v in views};before={tuple(v['before_recovery_ids']) for v in views}
        mismatch=len(after)>1;observed=len(before)>1 or mismatch
        rows.append(dict(type='SCOPE_IDENTITY_MISMATCH' if observed else 'SCOPE_IDENTITY_PARITY',start=start,end=end,
            surface=text[start:end],views=views,decision='UNRESOLVED' if mismatch else 'RECOVERED_SAFE' if observed else 'CONSISTENT',
            structural_defect=mismatch,author_intent_not_authority=True))
    return rows
