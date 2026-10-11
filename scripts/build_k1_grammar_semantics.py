"""Meaning registry derived ONLY from frozen grammar.json and local K1 notes.

Alternate meanings are adversarial labels, never permission additions.
The original grammar database is not rewritten.
"""
import hashlib
from k1_phase3 import ROOT, read, write

# ID order is checked against the authoritative form, not assumed by a caller.
ROWS = [
('copula', ['identity'], ['change','existential'], 'registered nominal predicate; bound future 거 handled by g04', '그 사람이 의사가 됐어요.', None),
('present', ['polite_present'], ['unapproved_speech_level'], 'polite terminal of a licensed predicate; tense/aspect is checked separately', None, None),
('past', ['simple_past'], ['double_past','independent_experience'], 'single past marker; ordinary completed event', '책을 읽었었어요.', '이 책을 읽어 봤어요.'),
('plan', ['future_plan'], ['epistemic_conjecture'], 'explicit prospective time or first-person action plan', '지금 집에 있을 거예요.', '친구는 학교에 갈 거예요.'),
('progressive', ['ongoing_action'], ['result_state','habitual_only'], 'action verb + current-action evidence; no habit marker without explicit now', '매일 공부하고 있어요.', '친구는 책을 읽고 있어요.'),
('wish', ['own_wish','question_to_addressee'], ['third_person_desiderative_derivation'], 'first-person subject or direct question to addressee', '친구는 책을 읽고 싶어해요.', '친구는 책을 읽고 싶어요.'),
('negation', ['short_negation'], ['long_negation'], '안 attached to a licensed negatable predicate', '학교에 가지 않아요.', None),
('inability', ['capacity_or_circumstance_inability'], ['adjective_inability'], 'action verb; capacity or circumstances', '방이 못 커요.', None),
('coordination', ['parallel','sequence'], ['resultative_state'], 'two independent licensed predicates; auxiliary compounds excluded', '문을 열고 있어요.', None),
('contrast', ['contrast'], ['mere_sequence'], 'visible opposed propositions or concrete concession', None, '책을 읽지만 집에 가요.'),
('reason_sequence', ['reason','related_sequence'], ['unrelated_sequence','reason_followed_by_instruction'], 'causal lexical pair or tightly related action chain', '비가 와서 우산을 가져가세요.', '책을 읽어서 학교에 가요.'),
('reason', ['reason'], ['discovery'], 'causal relation; commands/proposals permitted; discovery not permitted', '집에 가니까 친구가 있었어요.', '책을 읽으니까 학교에 가요.'),
('condition', ['concrete_condition'], ['counterfactual','complex_hypothetical'], 'concrete state/action antecedent and contingent consequence', None, '돈이 많았으면 좋겠어요.'),
('request', ['request','instruction'], ['generic_honorific_statement'], 'action directed to addressee; not third-person respectful narration', '선생님이 학교에 가세요.', None),
('proposal', ['invitation','intention_check'], ['complex_conjecture'], 'joint/first-person controllable action question', '내일 비가 올까요?', '친구가 올까요?'),
('ability', ['ability'], ['epistemic_possibility'], '수 construction + controllable action capacity', '친구는 지금 집에 있을 수 있어요.', None),
('obligation', ['obligation'], ['necessary_condition_inference'], 'licensed action + 해야 하다 construction', '비가 와야 추워요.', None),
('trial', ['trial'], ['visual_perception','generic_auxiliary'], 'action verb + auxiliary 보다, not lexical seeing', None, None),
('topic', ['topic','contrast_topic'], ['adnominal_ending'], 'nominal phrase topic, ending 는 is handled by g27', None, None),
('subject', ['subject','negative_copula_complement'], ['unapproved_complement'], 'nominal subject or explicit 아니다 complement; 되다 complement needs policy', None, '저는 선생님이 돼요.'),
('object', ['direct_object'], ['path_extent','time_extent'], 'nominal argument of a transitive lexical frame', '길을 걸어요.', None),
('at_to', ['existence_location','destination','point_time'], ['quantity_per_unit','cause','recipient'], 'time/location noun and matching predicate', '감기에 아파요.', '이것에 좋아요.'),
('at', ['action_location'], ['source','agent'], 'action occurs at location; movement source is not authorized', '학교에서 집으로 와요.', None),
('addition', ['simple_addition'], ['scalar_even','unapproved_indefinite_negation'], 'explicit additive referent/parallel proposition in context', '아이도 이것을 알아요.', '저도 책을 읽어요.'),
('with_and', ['nominal_coordination','companionship'], ['quotative','verbal_hada_group'], 'noun + 하고 plus nominal peer or joint-action predicate', '가라고 하고 가요.', None),
('adjective_modifier', ['adjective_attributive','existential_attributive'], ['verb_past_attributive'], 'registered adjective or explicitly listed 있는/없는', '어제 읽은 책이에요.', None),
('verb_modifier', ['verb_present_attributive'], ['verb_past_attributive','verb_future_attributive'], 'registered action verb and present modifier', '내일 읽을 책이에요.', None),
('to_person', ['recipient','counterparty'], ['source','nonhuman_destination'], 'human noun/pronoun + giving/communication predicate', '친구에게서 책을 받아요.', '친구에게 책을 받아요.'),
('genitive', ['ownership','belonging'], ['subjective_genitive','material','generic_relation'], 'explicit human possessor and concrete possessed object', '나무의 의자예요.', '영화의 이야기예요.'),
('by_toward', ['transport','instrument','direction'], ['role','material','cause','change_result'], 'dependent noun class AND governing predicate frame agree', '사진을 선물로 줘요.', '이것으로 괜찮아요.'),
('range', ['temporal_start_end','spatial_start_end'], ['scalar_even'], 'time/place endpoint and relevant event; emphasis not permitted', '아이까지 이것을 알아요.', None),
('only', ['simple_nominal_limit'], ['ten_thousand','nominalization_only','elapsed_time','worth_doing'], 'nominal attachment and ordinary event restriction', '책을 읽기만 해요.', None),
]

POLICY = {
3: 'g03 excludes experience in notes, while g18 explicitly licenses experiential tried-past with g03. Trial past is not auto-approved until the interpretation is confirmed.',
4: 'Plan centered and avoid frequent conjecture do not precisely define the permitted amount of conjecture. No automatic conjecture permission.',
6: 'Own wishes / questions to others are centered, but bare third-person -고 싶다 is not expressly banned. Treat it as needs_human_policy.',
15: 'meaning_ja includes 〜でしょうか but notes center on invitation/intention and avoid complex conjecture. Predictive questions are not auto-approved.',
20: 'Notes explicitly admit 아니다 complements but do not explicitly settle 되다 complements. Core 되다 remains active; no lexical change.',
24: 'Simple addition is allowed; the reference to the permitted scope of 아무N도 does not define that scope. Scalar/indefinite readings need policy.',
28: '受け手・相手 does not explicitly authorize a source with 받다. Bare recipient/source ambiguity is REVIEW, not automatic source permission.',
29: '所有・所属 does not delimit abstract content relationships. Concrete ownership is auto-checkable; broader relation needs policy.',
}

def build():
    path=ROOT/'config/languages/ko/k1/grammar.json'; grammar=read(path)
    assert len(grammar)==len(ROWS)==32
    entries=[]
    for index,(g,row) in enumerate(zip(grammar,ROWS),1):
        assert g['id']==f'ko_k1_g{index:02d}'
        code,allowed,other,context,negative,ambiguous=row
        entries.append(dict(grammar_id=g['id'],surface=g['form'],frozen_definition=g,
            allowed_functions=allowed,disallowed_or_unapproved_functions=other,
            required_context=[context,'Registered lexical identity and untouched raw morphology are required; author labels alone are insufficient.'],
            positive_examples=[g['example']],negative_examples=[negative] if negative else [],
            ambiguous_examples=[ambiguous] if ambiguous else [],
            autocheck='hard' if index in (1,2,3,7,8,17,18,19,26,27,32) else 'heuristic',
            auto_pass_possible=True,context_review_possible=True,
            needs_human_policy=POLICY.get(index),notes=g['notes'],
            alternate_fixture_note=None if negative or ambiguous else 'No forced artificial same-surface negative; invalid morphology remains the preceding gate responsibility.'))
    result=dict(version='3.5',authoritative_source='config/languages/ko/k1/grammar.json',
        authoritative_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        policy='Only evidence-backed allowed meanings PASS. FAIL and REVIEW both prevent commit. This is a limited role/frame checker, not a complete Korean semantic parser.',entries=entries)
    write(ROOT/'config/languages/ko/k1/grammar_semantics.json',result)
    return result

if __name__=='__main__':build()
