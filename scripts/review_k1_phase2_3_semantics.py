"""Separate post-hard-QA semantic screening stage; no text writes or approval."""
from k1_phase2_3 import *
from collections import defaultdict

def review():
    validation=read(REPORTS/'k1_phase2_3_validation_result.json')
    if not validation['ok'] or frozen_errors():raise ValueError('Complete hard validation and frozen-input integrity first')
    scenes={s['text_number']:s for s in read(PILOT/'authored_scenes.json')};records=[];groups=defaultdict(list)
    for path in sorted((PILOT/'texts').glob('*.json')):
        r=read(path);evidence=second_pass(scenes[r['text_number']],r)
        if evidence!=r['naturalness_semantic_review']:raise ValueError('Stale semantic evidence: '+r['id'])
        if r['translation_fidelity']['korean_sha256']!=sha256_text(r['text_ko']):raise ValueError('Stale translation')
        records.append(dict(id=r['id'],body_sha256=sha(path),semantic_review=evidence))
        for w in r['naturalness_lint']:
            # Templates group recurring risks, but examples retain their own context.
            groups[w['rule_id']].append(dict(id=r['id'],surface=w['surface'],context=r['text_ko'][max(0,w['start']-60):w['end']+60],reason=w['reason']))
    result=dict(phase='2.3',stage='separate_post_hard_QA_semantic_screen',human_approved=False,
                records=records,review_queue=dict(groups),warning_policy='Grouped candidates, not proven errors; contextual sense/intent reviews cannot receive blanket approval.')
    write(PILOT/'naturalness_semantic_review.json',result)
    print('Semantic screening:',len(records),'texts;',len(groups),'warning groups; no human approval claimed.')
    return result

if __name__=='__main__':review()
