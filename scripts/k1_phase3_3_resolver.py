"""Two explicitly licensed surface recoveries over immutable 3.2 raw output.

This is not a generic token concatenator, alias table or sense dictionary.
Temporal permission is checked by the candidate gate after identity recovery.
"""
from copy import deepcopy
import re
from k1_phase3_2_resolver import analyze as previous_analyze, HINTS

TARGETS = {
    '아니요': ('ko_k1_0443', 'interjection', 'no_polite'),
    '한국어': ('ko_k1_0169', 'noun', 'korean_language'),
}
RAW_SIGNATURES = {
    '아니요': [(('아니', 'VCN'), ('요', 'EC')), (('아니', 'VCN'), ('요', 'EF'))],
    '한국어': [(('한', 'MM'), ('국어', 'NNG'))],
}
NOMINAL_TAGS = {'NNG','NNP','NNB','NP','NR'}
PARTICLE_TAGS = {'JKS','JKO','JX','JKG','JKB','JC'}

def quote_ranges(text):
    """Balanced literal quotes, retaining original offsets and unmatched opens."""
    stack=[];pairs=[]
    opening={'“':'”','‘':'’','「':'」','『':'』'}
    for n,ch in enumerate(text):
        if ch in ('"', "'"):
            if stack and stack[-1][2]==ch:
                start,op,close=stack.pop();pairs.append((start,n,op,close))
            else: stack.append((n,ch,ch))
        elif ch in opening: stack.append((n,ch,opening[ch]))
        elif stack and ch==stack[-1][2]:
            start,op,close=stack.pop();pairs.append((start,n,op,close))
    return pairs,stack

def quotation_context(text,start,end):
    pairs,unclosed=quote_ranges(text)
    containing=[p for p in pairs if p[0]<start and end<=p[1]]
    p=max(containing,key=lambda p:p[0]) if containing else None
    return dict(inside_balanced=bool(p),open_offset=p[0] if p else None,
                close_offset=p[1] if p else None,opening=p[2] if p else None,
                closing=p[3] if p else None,
                inside_unmatched=any(o<start for o,_,_ in unclosed))

def role(entry,files,t,selected):
    first={i:r['text'] for r in files['introduction_schedule.json']['rows'] for i in r['entry_ids']}
    return ('core' if entry['tier']=='core' else 'current_new_expansion' if first[entry['id']]==t
            else 'scheduled_review' if entry['id'] in selected else 'previous_expansion')

def local_position(text,start,end,raw,indices,surface,q):
    left_boundary=start==0 or not bool(re.match(r'[가-힣A-Za-z0-9_]',text[start-1]))
    if surface=='아니요':
        left=q['open_offset']+1 if q['inside_balanced'] else max(text.rfind(ch,0,start) for ch in '.!?\n')+1
        initial=not text[left:start].strip()
        right=text[end:end+1]
        response_end=(not right or right in ',.!?\n"”’」』')
        # Spaces alone are not a clause boundary. No automatic assembly of
        # 아니요가..., 답은 아니요..., or an unbalanced quotation.
        return dict(left_word_boundary=left_boundary,utterance_initial=initial,
                    response_clause_boundary=response_end,
                    negative_response_position=initial and response_end,
                    balanced_or_independent=not q['inside_unmatched'])
    next_index=indices[-1]+1 if indices else None
    next_token=raw[next_index] if next_index is not None and next_index<len(raw) else None
    right=text[end:end+1]
    attached=bool(next_token and next_token['start']==end and next_token['tag'] in PARTICLE_TAGS)
    delimiter=not right or right.isspace() or right in ',.!?"”’」』'
    # A head noun after whitespace, a licensed attached nominal particle, or
    # a complete bare nominal utterance is positive nominal-position evidence.
    head=bool(next_token and text[end:next_token['start']].isspace()
              and next_token['tag'].split('-')[0] in NOMINAL_TAGS)
    bare=delimiter and (not next_token or next_token['tag'].startswith('S'))
    return dict(left_word_boundary=left_boundary,nominal_position=attached or head or bare,
                right_word_or_particle_boundary=delimiter or attached,
                balanced_or_independent=not q['inside_unmatched'])

def recover_registered_surfaces(text,result,files,t,selected=()):
    """Return a separate annotation layer; never edit raw forms/tags/offsets."""
    result=deepcopy(result);raw=result['raw_morphology'];raw_before=deepcopy(raw)
    entries=files['core_vocab.json']+files['expansion_vocab.json'];audit=[]
    for surface,(vid,pos,sense) in TARGETS.items():
        matches=[e for e in entries if (e['id'],e['lemma'],e['pos'],e['sense'])==(vid,surface,pos,sense)]
        for hit in re.finditer(re.escape(surface),text):
            start,end=hit.span();q=quotation_context(text,start,end)
            indices=[i for i,r in enumerate(raw) if r['start']<end and r['start']+r['length']>start]
            parts=[raw[i] for i in indices]
            contiguous=bool(indices) and indices==list(range(indices[0],indices[-1]+1))
            partition=bool(parts) and parts[0]['start']==start and parts[-1]['start']+parts[-1]['length']==end and all(
                a['start']+a['length']==b['start'] for a,b in zip(parts,parts[1:]))
            signature=tuple((r['form'],r['tag']) for r in parts)
            position=local_position(text,start,end,raw,indices,surface,q)
            old=[a for a in result['annotations'] if set(a['morph_indices'])&set(indices)]
            exclusive=bool(old) and all(set(a['morph_indices'])<=set(indices) for a in old)
            represented=[i for a in old for i in a['morph_indices']]
            covered=set(represented)==set(indices) and len(represented)==len(set(represented))
            evidence=dict(exact_original_substring=text[start:end]==surface,
                unique_registered_identity=len(matches)==1,
                raw_indices_consecutive=contiguous,exact_raw_character_partition=partition,
                no_internal_whitespace=not any(ch.isspace() for ch in text[start:end]),
                no_internal_punctuation=all(not r['tag'].startswith('S') or r['tag']=='SN' for r in parts),
                explicit_raw_pos_signature=signature in RAW_SIGNATURES[surface],
                original_parts_concatenate=''.join(r['form'] for r in parts)==surface,
                annotation_group_exclusive=exclusive,raw_indices_accounted_once=covered,**position)
            existing=any(a['vocab_id']==vid and a['start']==start and a['end']==end for a in old)
            decision='ALREADY_REGISTERED' if existing else 'RECOVERED' if all(evidence.values()) else 'DECLINED'
            row=dict(type='exact_registered_surface_recovery',surface=surface,
                original_substring=text[start:end],raw_parts=[r['form'] for r in parts],
                raw_tags=[r['tag'] for r in parts],raw_indices=indices,start=start,end=end,
                registered_vocab_id=vid,registered_pos=pos,registered_sense=sense,
                quotation_context=q,evidence=evidence,decision=decision,
                permission_granted=False,scope='Two explicit identities only; candidate gate checks actual permission')
            if decision=='RECOVERED':
                result['annotations']=[a for a in result['annotations'] if a not in old]
                result['unresolved_tokens']=[a for a in result['unresolved_tokens'] if a not in old]
                old_starts={a['start'] for a in old}
                result['annotation_review_required']=[a for a in result['annotation_review_required'] if a['start'] not in old_starts]
                for d in result['resolver_decisions']:
                    if d.get('start') in old_starts and d.get('requires_candidate_review'):
                        d['requires_candidate_review']=False;d['discharged_by']='exact_registered_surface_recovery'
                entry=matches[0]
                annotation=dict(surface=surface,lemma=entry['lemma'],pos=pos,sense=sense,vocab_id=vid,
                    role=role(entry,files,t,selected),start=start,end=end,morph_indices=indices,grammar_id=None)
                result['annotations'].append(annotation)
                row['replaced_annotations']=old
                row['restored_annotation']=deepcopy(annotation)
            audit.append(row)
    result['annotations'].sort(key=lambda a:(a['start'],a['morph_indices'][0]))
    result['quote_recovery_audit']=sorted(audit,key=lambda d:d['start'])
    result['resolver_decisions'] += [dict(d,status=d['decision'],requires_candidate_review=False) for d in result['quote_recovery_audit']]
    result['grammar_used']=sorted({a['grammar_id'] for a in result['annotations'] if a['grammar_id']}|
        ({'ko_k1_g26'} if any(x['type']=='attributive_pos_boundary' for x in result['annotation_review_required']) else set()))
    assert raw==raw_before, 'Surface recovery changed raw morphology'
    return result

def analyze(text,files,text_number,selected_reviews=(),intents=(),scene_actions=(),kiwi=None):
    result=previous_analyze(text,files,text_number,selected_reviews,intents,scene_actions,kiwi)
    return recover_registered_surfaces(text,result,files,text_number,selected_reviews)
