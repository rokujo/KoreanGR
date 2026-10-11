"""Coverage of annotated lexical tokens, not Korean parsing or learner knowledge.

Each item is {kind: vocab|proper_name|exception|grammar|punctuation|unknown, id: ...}.
The caller must resolve lemma/POS/sense, grammar roles and exact fixed spans first.
This module validates identities and temporal permission before counting them.
"""
from fractions import Fraction


def evaluate_lexical_tokens(tokens,text,files):
    if isinstance(text,bool) or not isinstance(text,int) or not 1<=text<=300:
        raise ValueError('text must be an integer in 1..300')
    profile=files['profile.json']
    core={e['id']:e for e in files['core_vocab.json']}
    expansion={e['id']:e for e in files['expansion_vocab.json']}
    if 'introduction_schedule.json' in files:
        first={vid:r['text'] for r in files['introduction_schedule.json']['rows'] for vid in r['entry_ids']}
    else: # compatibility for frozen token fixtures without an introduction table
        first={e['vocab_id']:e['first_introduction_text'] for e in files['vocab_exposure_schedule.json']['entries']}
    proper={e['lemma'] for e in files['proper_names.json']['entries']}
    exceptions={e['id'] for e in files['lexical_exceptions.json']['entries'] if e['kind']=='frozen_exception'}
    grammar={e['id'] for e in files['grammar.json']}
    N=controlled=previous=U=0;new_ids=set();errors=[];warnings=[];frozen_occurrences=0
    for position,token in enumerate(tokens):
        kind=token.get('kind');identity=token.get('id')
        if kind=='punctuation':continue
        if kind=='grammar':
            if identity not in grammar:errors.append(f'Token {position}: unapproved grammar identity')
            continue
        N+=1
        allowed=False;prior=False
        if kind=='vocab' and identity in core:allowed=prior=True
        elif kind=='vocab' and identity in expansion:
            introduced=first[identity]
            allowed=introduced<=text;prior=introduced<text
            if introduced==text:U+=1;new_ids.add(identity)
        elif kind=='proper_name' and identity in proper:allowed=prior=True
        elif kind=='exception' and identity in exceptions:
            allowed=prior=True;frozen_occurrences+=1
        if allowed:controlled+=1
        else:errors.append(f'Token {position}: uncontrolled vocabulary or future introduction')
        if prior:previous+=1
    new_lemmas={expansion[vid]['lemma'] for vid in new_ids}
    if frozen_occurrences>files['lexical_exceptions.json']['policy']['max_occurrences_per_text']:
        errors.append('Too many frozen-expression occurrences')
    if len(new_lemmas)>profile['new_vocab']['max'] or len(new_ids)>profile['new_vocab']['max_entries_per_text']:
        errors.append('Too many current new lemmas/entries')
    if N==0:
        errors.append('N=0 is invalid')
        return dict(ok=False,N=0,U=U,controlled_vocab_coverage=None,previous_vocab_coverage=None,
                    dynamic_hard_new_token_limit=0,errors=errors,warnings=warnings)
    controlled_ratio=Fraction(controlled,N);previous_ratio=Fraction(previous,N)
    hard=Fraction(str(profile['previous_vocab_coverage_hard_min']))
    target=Fraction(str(profile['previous_vocab_coverage_target']))
    hard_limit=int(N*(1-hard))
    if controlled_ratio<Fraction(str(profile['controlled_vocab_coverage_hard_min'])):
        errors.append('controlled_vocab_coverage below hard 100%')
    if previous_ratio<hard:errors.append('previous_vocab_coverage below hard 98%')
    elif previous_ratio<target:warnings.append('previous_vocab_coverage below target 99%')
    if U>profile['new_vocab']['first_text_new_lemma_token_soft_max']:
        warnings.append('Current new-token count exceeds soft maximum 3; review exception')
    if controlled==N and previous!=N-U:errors.append('Coverage accounting inconsistency')
    return dict(ok=not errors,N=N,U=U,controlled_tokens=controlled,previous_tokens=previous,
                new_lemma_count=len(new_lemmas),new_entry_count=len(new_ids),
                controlled_vocab_coverage=float(controlled_ratio),previous_vocab_coverage=float(previous_ratio),
                dynamic_hard_new_token_limit=hard_limit,target_new_token_limit=int(N*(1-target)),
                errors=errors,warnings=warnings)
