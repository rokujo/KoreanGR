"""Production overlay for one evidenced Kiwi contraction defect. Raw is immutable."""
from copy import deepcopy
import re
from k1_phase3_4_resolver import analyze as previous_analyze, HINTS, OVERLAY


def analyze(text, files, text_number, selected_reviews=(), intents=(),
            scene_actions=(), kiwi=None, scope='unspecified'):
    a = previous_analyze(text, files, text_number, selected_reviews, intents,
                         scene_actions, kiwi, scope)
    raw_before = deepcopy(a['raw_morphology'])
    entries = files['core_vocab.json'] + files['expansion_vocab.json']
    drink = next(e for e in entries if (e['lemma'], e['pos'], e['sense']) ==
                 ('마시다', 'verb', 'drink'))
    a['drink_recovery_audit'] = []
    # Deliberately not a general surface alias or generic concatenation engine.
    for match in re.finditer(r'(?<!\S)(물|우유|커피|차)(을|를) 받고 (마셔요)(?=$|[.!?"”\s])', text):
        start, end = match.span(3)
        parts = [(i, r) for i, r in enumerate(raw_before)
                 if start <= r['start'] < end]
        signature = [(r['form'], r['tag']) for _, r in parts]
        if signature != [('말', 'VX'), ('시', 'EP'), ('어요', 'EF')]:
            continue  # Already normal VV, or different evidence: leave it alone.
        object_a = next((x for x in a['annotations'] if x['start'] == match.start(1)
                         and x['lemma'] == match.group(1) and x['pos'] == 'noun'
                         and x['vocab_id']), None)
        receive = next((x for x in a['annotations'] if match.start() < x['start'] < start
                        and x['lemma'] == '받다' and x['pos'] == 'verb'), None)
        liquid = object_a and object_a['sense'] in {'water', 'milk', 'coffee', 'tea'}
        indices = [i for i, _ in parts]
        offsets_ok = (indices == list(range(indices[0], indices[0] + 3))
                      and parts[0][1]['start'] == start
                      and parts[1][1]['start'] == start + 1
                      and parts[2][1]['start'] + parts[2][1]['length'] == end)
        evidence = dict(exact_surface=text[start:end], valid_inflection='마시+어요→마셔요',
                        registered_identity=drink['id'], explicit_liquid_object=bool(liquid),
                        registered_receive_coordination=bool(receive), contiguous_raw_indices=offsets_ok,
                        author_annotation_is_not_authority=True)
        decision = 'PASS' if liquid and receive and offsets_ok else 'REVIEW'
        a['drink_recovery_audit'].append(dict(type='limited_drink_contraction', surface=text[start:end],
            raw_parts=[r['form'] for _, r in parts], raw_tags=[r['tag'] for _, r in parts],
            start=start, end=end, scope=scope, registered_vocab_id=drink['id'],
            registered_pos=drink['pos'], registered_sense=drink['sense'], evidence=evidence, decision=decision))
        if decision != 'PASS':
            continue
        # Contracted stem and ending overlap in the raw analyzer. Retain this
        # evidence but create nonoverlapping original-character annotations.
        a['annotations'] = [x for x in a['annotations']
                            if not set(x.get('morph_indices', [])) & set(indices)]
        a['annotations'] += [dict(surface=text[start:start+2], lemma=drink['lemma'], pos='verb',
            sense=drink['sense'], vocab_id=drink['id'], role='core', start=start, end=start+2,
            morph_indices=indices[:2], grammar_id=None),
            dict(surface=text[start+2:end], lemma=None, pos=None, sense=None, vocab_id=None,
                 role='grammar_function', start=start+2, end=end, morph_indices=indices[2:],
                 grammar_id='ko_k1_g02')]
        a['annotations'].sort(key=lambda x: (x['start'], x['end']))
        a['annotation_review_required'] = [x for x in a['annotation_review_required']
            if not (x.get('start') in {start, start+1} and
                    x.get('type') == 'unapproved_or_unresolved_grammar')]
    a['unresolved_tokens'] = [x for x in a['annotations'] if x['role'] == 'unresolved']
    assert a['raw_morphology'] == raw_before
    return a
