"""Exact response 네 recovery only; immutable morphology and short-scope evidence."""
from copy import deepcopy
import re
from k1_phase3_6_resolver import analyze as previous_analyze, HINTS, OVERLAY
from k1_phase3_3_resolver import quotation_context, role

YES=('ko_k1_0442','네','interjection','yes')


def analyze(text,files,text_number,selected_reviews=(),intents=(),scene_actions=(),kiwi=None,scope='unspecified'):
    a=previous_analyze(text,files,text_number,selected_reviews,intents,scene_actions,kiwi,scope)
    before=deepcopy(a['raw_morphology']);a['ne_response_recovery_audit']=[]
    matches=[e for e in files['core_vocab.json']+files['expansion_vocab.json']
             if (e['id'],e['lemma'],e['pos'],e['sense'])==YES]
    for hit in re.finditer(r'(?<![가-힣A-Za-z0-9_])네(?![가-힣A-Za-z0-9_])',text):
        start,end=hit.span();q=quotation_context(text,start,end)
        left=q['open_offset']+1 if q['inside_balanced'] else max(text.rfind(ch,0,start) for ch in '.!?\n')+1
        initial=not text[left:start].strip();right=text[end:end+1]
        boundary=not right or right in ',，.!?\n"”’」』'
        indices=[i for i,r in enumerate(before) if r['start']<end and r['start']+r['length']>start]
        parts=[before[i] for i in indices]
        signature=[(r['form'],r['tag']) for r in parts]
        split=(signature==[('너','NP'),('의','JKG')]
               and all(r['start']==start and r['length']==1 for r in parts)
               and indices==list(range(indices[0],indices[0]+2)))
        old=[x for x in a['annotations'] if set(x.get('morph_indices',[]))&set(indices)]
        exclusive=bool(old) and all(set(x['morph_indices'])<=set(indices) for x in old)
        # A punctuation boundary separates the response from the following
        # clause. A whitespace-adjacent possessed noun has no such boundary.
        response=initial and boundary and not q['inside_unmatched']
        probe=None;short_yes=False
        if split and response:
            if q['inside_balanced']:
                lo,hi=q['open_offset'],q['close_offset']+1
            else:
                lo=left;terminator=re.search(r'[.!?\n]',text[end:])
                hi=end+terminator.end() if terminator else len(text)
            probe_text=text[lo:hi]
            # Use the frozen previous resolver, not this layer recursively.
            p=previous_analyze(probe_text,files,text_number,selected_reviews,(),(),kiwi,scope='ne_short_scope_evidence')
            probe_start=start-lo
            short_yes=any(x['vocab_id']==YES[0] and x['pos']=='interjection' and x['sense']=='yes'
                          and x['start']==probe_start and x['end']==probe_start+1 for x in p['annotations'])
            raw_ic=any(r['form']=='네' and r['tag']=='IC' and r['start']==probe_start and r['length']==1
                       for r in p['raw_morphology'])
            short_yes=short_yes and raw_ic
            probe=dict(text=probe_text,original_start=lo,raw=p['raw_morphology'],annotations=p['annotations'],raw_ic=raw_ic,
                       registered_yes=short_yes)
        evidence=dict(exact_original_surface=text[start:end]=='네',unique_registered_yes=len(matches)==1,
            utterance_initial=initial,response_punctuation_boundary=boundary,
            balanced_or_independent=not q['inside_unmatched'],no_direct_possessive_nominal=boundary,
            exact_overlapping_ner_ui_signature=split,exclusive_annotations=exclusive,
            short_scope_raw_ic_and_registered_yes=short_yes,annotation_intent_not_used=True)
        already=any(x['vocab_id']==YES[0] and x['start']==start and x['end']==end for x in old)
        decision='ALREADY_REGISTERED' if already else 'RECOVERED' if all(evidence.values()) else 'DECLINED'
        row=dict(type='exact_ne_response_recovery',surface=text[start:end],start=start,end=end,scope=scope,
            raw_parts=[r['form'] for r in parts],raw_tags=[r['tag'] for r in parts],raw_indices=indices,
            registered_vocab_id=YES[0],registered_pos=YES[2],registered_sense=YES[3],
            quotation_context=q,evidence=evidence,short_scope_probe=probe,
            original_annotations=deepcopy(old),decision=decision,permission_granted=False)
        if decision=='RECOVERED':
            a['annotations']=[x for x in a['annotations'] if x not in old]
            e=matches[0]
            a['annotations'].append(dict(surface='네',lemma='네',pos='interjection',sense='yes',vocab_id=e['id'],
                role=role(e,files,text_number,selected_reviews),start=start,end=end,morph_indices=indices,grammar_id=None))
            a['annotation_review_required']=[x for x in a['annotation_review_required'] if x.get('start')!=start]
        if split and response and decision=='DECLINED':
            a['resolver_decisions'].append(dict(type='ne_response_evidence_insufficient',start=start,surface='네',
                status='REVIEW',requires_candidate_review=True,evidence=evidence))
        a['ne_response_recovery_audit'].append(row)
    a['annotations'].sort(key=lambda x:(x['start'],x['end']))
    a['unresolved_tokens']=[x for x in a['annotations'] if x['role']=='unresolved']
    a['grammar_used']=sorted({x['grammar_id'] for x in a['annotations'] if x.get('grammar_id')}|
        ({'ko_k1_g26'} if any(x['type']=='attributive_pos_boundary' for x in a['annotation_review_required']) else set()))
    assert a['raw_morphology']==before
    return a


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
    focus=set(new_ids)|{e['id'] for e in files['core_vocab.json']+files['expansion_vocab.json'] if e['lemma'] in risk}
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
            recoveries=[r for r in a.get('ne_response_recovery_audit',[]) if r['start']==lo and r['end']==hi]
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
