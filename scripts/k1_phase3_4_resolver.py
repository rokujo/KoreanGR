"""Explicit uri modifier recovery, preserving approved 3.3 raw and quote layer."""
from copy import deepcopy
import re
from k1_phase3_3_resolver import analyze as previous_analyze, quotation_context, HINTS
from k1_phase3 import DATA, read

OVERLAY = DATA / 'phase3_4/uri_pronoun_modifier_contexts.json'


def recover_uri(text, result, files, scope='unspecified'):
    result = deepcopy(result)
    raw = result['raw_morphology']
    original_raw = deepcopy(raw)
    policy = read(OVERLAY)
    target = policy['registered_identity']
    entries = files['core_vocab.json'] + files['expansion_vocab.json']
    matches = [e for e in entries if all(e.get(k) == target[k] for k in ('id','lemma','pos','sense'))]
    audit = []
    for hit in re.finditer('우리', text):
        start, end = hit.span()
        indices = [i for i,r in enumerate(raw) if r['start'] < end and r['start'] + r['length'] > start]
        parts = [raw[i] for i in indices]
        old = [a for a in result['annotations'] if set(a['morph_indices']) & set(indices)]
        # False positives are costlier than refusing a valid but unknown parse.
        exact = (len(parts) == 1 and parts[0]['form'] == '우리' and
                 parts[0]['start'] == start and parts[0]['length'] == end-start)
        raw_pos = parts[0]['tag'] if len(parts) == 1 else '+'.join(p['tag'] for p in parts)
        next_token = raw[indices[-1]+1] if indices and indices[-1]+1 < len(raw) else None
        gap = text[end:next_token['start']] if next_token else ''
        head = next((h for h in policy['modifier_heads'] if next_token and
                     next_token['form'] == h['lemma'] and next_token['tag'] == 'NNG'), None)
        head_registered = bool(head and any(all(e.get(k)==head[k] for k in ('id','lemma','pos','sense')) for e in entries))
        following_span_exact = bool(head and text[next_token['start']:next_token['start']+next_token['length']] == head['lemma'])
        left_boundary = start == 0 or not re.match(r'[가-힣A-Za-z0-9_]',text[start-1])
        separated = bool(gap) and gap.isspace()
        attached_particle = bool(next_token and next_token['start']==end and next_token['tag'].startswith('J'))
        represented = [i for a in old for i in a['morph_indices']]
        exclusive = bool(old) and all(set(a['morph_indices']) <= set(indices) for a in old)
        accounted = set(represented)==set(indices) and len(represented)==len(set(represented))
        # Discourse evidence comes from raw NP with a subject/topic particle,
        # not from generated intents or a previous resolver's identity claim.
        anchors = []
        for n,r in enumerate(raw[:indices[0] if indices else 0]):
            if r['start'] < max(0,start-policy['discourse_lookback_chars']):
                continue
            if r['tag'] != 'NP' or r['form'] not in policy['speaker_anchor_forms']:
                continue
            following = raw[n+1] if n+1 < len(raw) else None
            if following and following['start'] == r['start']+r['length'] and following['tag'] in ('JKS','JX'):
                if following['form'] in ('가','는','도'):
                    anchors.append(dict(form=r['form'],raw_pos=r['tag'],start=r['start'],particle=following['form']))
        spatial = bool(next_token and separated and next_token['form'] in policy['ambiguous_spatial_heads'])
        noun_particle = bool(attached_particle and next_token['form'] in policy['noun_location_particles'])
        q = quotation_context(text,start,end)
        evidence = dict(exact_original_surface=text[start:end]=='우리',unique_registered_identity=len(matches)==1,
            single_exact_raw_span=exact,raw_np_or_nng=raw_pos in ('NP','NNG'),left_word_boundary=bool(left_boundary),
            no_particle_on_uri=not attached_particle,whitespace_before_head=separated,
            limited_registered_nominal_head=head_registered,following_head_exact=following_span_exact,
            speaker_group_raw_anchor=bool(anchors),no_spatial_noun_contrast=not spatial and not noun_particle,
            balanced_or_independent=not q['inside_unmatched'],annotation_group_exclusive=exclusive,
            raw_span_accounted_once=accounted)
        present = any(a['vocab_id']==target['id'] and a['start']==start and a['end']==end for a in old)
        if (raw_pos == 'NP' and present and exact and exclusive and accounted and
                len(matches)==1 and left_boundary and not spatial and not noun_particle):
            decision = 'ALREADY_REGISTERED'
        elif raw_pos == 'NNG' and all(evidence.values()):
            decision = 'RECOVERED'
        else:
            decision = 'REVIEW'
        row = dict(type='uri_pronoun_context',surface=text[start:end],raw_pos=raw_pos,
            raw_parts=deepcopy(parts),raw_indices=indices,start=start,end=end,scope=scope,
            preceding_tokens=deepcopy(raw[max(0,(indices[0] if indices else 0)-4):indices[0] if indices else 0]),
            following_tokens=deepcopy(raw[indices[-1]+1:indices[-1]+5]) if indices else [],
            following_noun=deepcopy(head),registered_id=target['id'],registered_pos=target['pos'],
            registered_sense=target['sense'],context_evidence=evidence,speaker_anchors=anchors,
            quotation_context=q,decision=decision,original_annotation=deepcopy(old),permission_granted=False)
        # Do not replace an overlapping compound or malformed raw group.
        if decision == 'RECOVERED':
            replacement = dict(surface='우리',lemma='우리',pos='pronoun',sense='we',vocab_id=target['id'],
                role='core',start=start,end=end,morph_indices=indices,grammar_id=None)
            result['annotations'] = [a for a in result['annotations'] if a not in old] + [replacement]
            result['unresolved_tokens'] = [a for a in result['unresolved_tokens'] if a not in old]
            result['annotation_review_required'] = [a for a in result['annotation_review_required'] if not (
                a.get('start')==start and a.get('type')=='identity_evidence_insufficient')]
            for d in result['resolver_decisions']:
                if d.get('start')==start and d.get('type')=='identity_boundary' and d.get('requires_candidate_review'):
                    d['requires_candidate_review']=False
                    d['discharged_by']='uri_pronoun_context'
            row['restored_annotation']=deepcopy(replacement)
        elif decision == 'REVIEW' and exact and exclusive and accounted:
            # A raw NP cage/locative contrast must not retain a usable Core ID.
            replacement = dict(surface='우리',lemma='우리',pos=None,sense=None,vocab_id=None,
                role='unresolved',start=start,end=end,morph_indices=indices,grammar_id=None)
            result['annotations'] = [a for a in result['annotations'] if a not in old] + [replacement]
            result['unresolved_tokens'] = [a for a in result['unresolved_tokens'] if a not in old] + [replacement]
        audit.append(row)
        result['resolver_decisions'].append(dict(row,status=decision,requires_candidate_review=decision=='REVIEW'))
    result['uri_recovery_audit']=audit
    result['annotations'].sort(key=lambda a:(a['start'],a['morph_indices'][0]))
    assert raw == original_raw, 'Uri recovery mutated raw morphology'
    return result


def analyze(text,files,text_number,selected_reviews=(),intents=(),scene_actions=(),kiwi=None,scope='unspecified'):
    base = previous_analyze(text,files,text_number,selected_reviews,intents,scene_actions,kiwi)
    return recover_uri(text,base,files,scope)
