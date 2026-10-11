"""Sentence-local canonical identity; broad-scope output is immutable diagnostics.

Existing resolvers and morphology evidence are reused, not replaced by matching.
Offsets and raw indices in canonical annotations refer to the concatenated
sentence raw stream. Original paragraph/full streams are stored separately.
"""
from copy import deepcopy
import re
from k1_phase3_6c_resolver import analyze as local_analyze,HINTS,OVERLAY


def segments(text):
    """Keep quoted sentence punctuation and closing quotes in each exact span.

    A narration and its quoted turn are separate. No newline/whitespace or quote
    rewriting is performed; phrase titles with no terminal punctuation work too.
    """
    result=[];start=0
    for m in re.finditer(r'[.!?]+["”’」』]*',text):
        end=m.end()
        lo=start
        while lo<end and text[lo].isspace():lo+=1
        if lo<end:result.append((lo,end,text[lo:end]))
        start=end
    while start<len(text) and text[start].isspace():start+=1
    if start<len(text):result.append((start,len(text),text[start:]))
    return result


def diagnostics(text,canonical,files,t,selected=(),intents=(),actions=(),kiwi=None):
    full=local_analyze(text,files,t,selected,intents,actions,kiwi,scope='full_diagnostic')
    paragraphs=[];cursor=0
    for paragraph in text.split('\n\n'):
        lo=text.find(paragraph,cursor);cursor=lo+len(paragraph)
        paragraphs.append(dict(start=lo,end=cursor,analysis=local_analyze(paragraph,files,t,selected,intents,actions,kiwi,scope='paragraph_diagnostic')))
    rows=[]
    for x in canonical['canonical_lexical_map']:
        if not x['canonical_vocab_id']:continue
        for scope,lo,hi,a in [('full_text',0,len(text),full)]+[('paragraph',p['start'],p['end'],p['analysis']) for p in paragraphs]:
            if not lo<=x['start']<x['end']<=hi:continue
            hits=[z for z in a['annotations'] if z['start']<x['end']-lo and z['end']>x['start']-lo]
            ids=sorted({z['vocab_id'] for z in hits if z['vocab_id']})
            tags=sorted({a['raw_morphology'][i]['tag'] for z in hits if z['vocab_id'] for i in z.get('morph_indices',[])})
            stags=sorted({r['tag'] for r in x['sentence_raw']})
            different=ids!=[x['canonical_vocab_id']]
            posonly=not different and tags!=stags
            rows.append(dict(type='scope_identity_disagreement_warning' if different or posonly else 'scope_identity_parity',scope=scope,
                start=x['start'],end=x['end'],surface=x['surface'],sentence_identity=x['canonical_vocab_id'],diagnostic_identities=ids,
                sentence_raw_pos=stags,diagnostic_raw_pos=tags,id_disagreement=different,pos_only_disagreement=posonly,
                disagreement=different or posonly,structural_defect=False,decision='WARNING_ONLY' if different or posonly else 'CONSISTENT'))
    return rows,full,paragraphs


def analyze(text,files,text_number,selected_reviews=(),intents=(),scene_actions=(),kiwi=None,scope='unspecified'):
    pieces=segments(text);results=[]
    for lo,hi,sentence in pieces:
        a=local_analyze(sentence,files,text_number,selected_reviews,intents,scene_actions,kiwi,scope='canonical_sentence')
        results.append((lo,hi,a))
    keys=('annotations','raw_morphology','annotation_review_required','unresolved_tokens','resolver_decisions',
          'quote_recovery_audit','uri_recovery_audit','drink_recovery_audit','ne_response_recovery_audit','controlled_surface_recovery_audit')
    out={k:[] for k in keys};out['grammar_used']=[];out['canonical_lexical_map']=[];out['sentence_analyses']=[]
    for index,(lo,hi,a) in enumerate(results,1):
        raw_offset=len(out['raw_morphology'])
        out['sentence_analyses'].append(dict(sentence_index=index,start=lo,end=hi,text=text[lo:hi],analysis=deepcopy(a)))
        for x in a['annotations']:
            evidence=[deepcopy(a['raw_morphology'][i]) for i in x.get('morph_indices',[])]
            out['canonical_lexical_map'].append(dict(sentence_index=index,start=x['start']+lo,end=x['end']+lo,surface=x['surface'],
                canonical_vocab_id=x['vocab_id'],lemma=x['lemma'],pos=x['pos'],sense=x['sense'],sentence_raw=evidence,
                canonical_reason='Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override.'))
        for key in keys:
            for original in a.get(key,[]):
                row=deepcopy(original)
                for field in ('start','end'):
                    if isinstance(row.get(field),int):row[field]+=lo
                if key=='annotations':row['morph_indices']=[i+raw_offset for i in row.get('morph_indices',[])]
                row['sentence_index']=index
                out[key].append(row)
        out['grammar_used']+=a['grammar_used']
    out['grammar_used']=sorted(set(out['grammar_used']))
    out['lexical_authority']='sentence_local'
    # Preflight/title and sentence prechecks need no broad-scope diagnostics.
    if scope=='full_candidate':
        rows,full,paragraphs=diagnostics(text,out,files,text_number,selected_reviews,intents,scene_actions,kiwi)
        out.update(scope_diagnostics=rows,full_text_diagnostic=full,paragraph_diagnostics=paragraphs)
    else:out['scope_diagnostics']=[]
    return out
