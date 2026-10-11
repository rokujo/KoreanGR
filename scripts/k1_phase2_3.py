"""Phase 2.3 revision pipeline, with a distinct semantic second pass and freeze."""
from copy import deepcopy
from collections import Counter
from jsonschema import Draft202012Validator
from k1_phase2_2 import (ROOT, DATA, REPORTS, read, write, sha, inputs, selection,
                         make_kiwi as base_kiwi, record, state_steps, text_schema, annotation_triage)
from k1_naturalness_lint import lint, semantic_review, CHECKS, translation_lint
from validate_k1_phase2_2 import inspect_record

PILOT=ROOT/'pilot/ko/k1/phase2_3'
FREEZE=REPORTS/'k1_phase2_3_input_freeze.json'

def make_kiwi():
    kiwi=base_kiwi()
    # This existing registered verb's future form was split into 가지+어+오.
    # A dictionary segmentation hint licenses no new lemma, sense or grammar.
    kiwi.add_user_word('가져오','VV',5.0)
    return kiwi

def frozen_errors():
    return ['Frozen changed/missing: '+p for p,h in read(FREEZE)['files'].items()
            if not (ROOT/p).exists() or sha(ROOT/p)!=h]

RULES=[
('genitive_overuse',['학교의 학생','수업의 시간','버스의 문','영화의 이야기'],'avoid literal Japanese-style genitive chaining; prefer conventional noun adjacency or a simple clause. Retain 의 for meaningful ownership/clarity.',True),
('verb_argument_frame',['책을 물어보다 as borrow request','친구의 이름을 말하다 as call','무거운 가방을 받다 as carry help','친구에게 의자를 주다'],'Preserve verb intent and argument roles. Ask a direct question or omit; hold with introduced 들다; sit rather than fabricate a chair transfer.',True),
('vague_positive_reaction',['약속을 아주 좋아해요','이야기를 듣고 아주 좋아해요','친구는 잘 잡고 아주 좋아해요'],'State a concrete licensed reaction such as 웃다, 괜찮다 or 재미있다 if that is the intended meaning. Otherwise omit. 좋아하다 remains valid for actual preferences.',True),
('filler_adverb',['먼저 같이 천천히','아주 정말','repeating 조금 to pad length'],'Do not pad to 4–7 eojeol. Short natural sentences are acceptable within hard max. Repetition within 2–3 sentences needs a semantic reason.',True),
('scene_plausibility',['employee waiting at entrance for this customer','handing phone to employee to buy charger','travel narration to shop employee'],'One goal or closely linked goals. Ask why the person is there, whether action is ordinary here, and whether the review word alone motivated it.',True),
('reference_clarity',['사진의 저하고 동생','이것은 작은 집하고 학교예요','그 집은 지금 없어요'],'Name antecedent/agent when switching. Distinguish depiction from object and absence in picture from nonexistence. Window eligibility is not referent evidence.',True),
('habit_vs_progressive',['자주 공부하고 있어요'],'Habit: simple present. -고 있다 only for an action in progress at the reference time; habitual words are candidate warnings, not a ban.',True),
('restricted_sense',['종이에 자리가 없다','칼을 쓰다 with write ID','마음에 들다 with hold ID'],'License lemma + POS + sense, not lemma alone. Check 들다 hold/lift, 풀 glue/grass, 이 tooth/determiner/numeral, 눈 eye/snow, 쓰다 write/bitter. Retired identities are hard lexical violations.',True),
('unnatural_substitution',['friend name used instead of calling','time used instead of a memory of the day'],'If natural permitted wording is unavailable, omit/defer and record natural_expression_gap. Never stretch a synonym, sense or character action.',False),
('translation_fidelity',['좋아해요 translated as 喜ぶ','translation fixing a wrong subject or causal relation'],'Finalize Korean first; freshly translate its meaning, omitted subject and timeline faithfully. A bilingual second pass records evidence; model review is not approval.',True),
]

FRAMES=[
dict(lemma='물어보다',intent='ask_about_information',object_examples=['시간','가격'],risk='책을 물어보다 cannot silently mean ask to borrow a book',strategy='Direct book-existence question in quotation marks, or omit; no indirect quotative grammar.'),
dict(lemma='말하다',intent='say_information',object_examples=['이름','시간','이야기'],risk='Saying a name is not calling a friend',strategy='Delete calling action if 부르다 not yet introduced.'),
dict(lemma='받다',intent='receive_transfer',object_examples=['선물','책','영수증'],risk='Heavy bag receipt is not automatically carry/hold assistance',strategy='Introduced 들다 for physical lifting; 받다 can remain when actual transfer is narrated.'),
dict(lemma='주다',intent='give_transfer',object_examples=['선물','책','물'],risk='Giving a chair may invent unnecessary furniture movement',strategy='Have guest sit in a chair if that is all the scene needs.'),
dict(lemma='좋아하다',intent='like_preference',object_examples=['음식','영화','친구'],risk='Not an untyped happy reaction',strategy='Explicit preference object or concrete smile; otherwise omit.'),
dict(lemma='들다',sense='hold_lift_by_hand',intent='physical_hold_lift',object_examples=['가방','책','상자'],risk='Cost/liking/aging/entry not licensed',strategy='Identify physical object and action; no need to append 손으로 solely to explain sense.'),
dict(lemma='쓰다',sense='write',intent='write_text',object_examples=['이름','답'],risk='Using a knife is not writing; bitter adjective is a separate ID',strategy='Use Core 사용하다 for a tool; contextual review of adjective bitter.'),
dict(lemma='자리',sense='seat',intent='seat',object_examples=['버스 자리'],risk='Paper room or broad outdoor space is not a seat',strategy='Describe small paper/large drawing or use 곳 when introduced/contextually natural.'),
]

def guidelines():
    data=dict(version='2.3',language='ko',level='K1',priority='very simple natural Korean before review quota',
        pipeline=['frozen introduction state','single scene/goal and agents','scene-specific positive review gate','draft Korean','hard lexical/grammar/coverage QA','warning lint','naturalness_semantic_review','omit/defer gaps; revalidate','freeze Korean body hash','fresh Japanese translation','translation fidelity second pass','human review'],
        hard_constraints_unchanged=True,model_or_regex_is_final_approval=False,
        rules=[dict(id='nat_'+cat,category=cat,severity='warning',bad_examples=bad,preferred_strategy=strategy,autolint_possible=possible,
                    notes='Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.') for cat,bad,strategy,possible in RULES],
        semantic_frames=FRAMES,semantic_review_checks=list(CHECKS),
        quotation_policy='Direct standalone speech with an explicit speaker is punctuation, not new indirect quotation morphology. Analyze the quoted sentence with the same 32 grammar rules; never license 라고/달라고/nominalization by quotation.',
        length_policy='4–7 preferred is soft. If meaningful natural scene remains under 120, redesign with relevant actions or report a gap; never fill with adverbs.',
        review_defer_policy='Freeze windows. Omitted actual reviews earn no credit. Keep unmet debt for later semantically compatible selection; six actual distinct texts still required at text 300.')
    write(DATA/'naturalness_guidelines.json',data)
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['version','rules','semantic_frames','pipeline'],
      'properties':{'rules':{'type':'array','minItems':10,'items':{'type':'object','required':['id','category','severity','bad_examples','preferred_strategy','autolint_possible','notes'],
          'properties':{'id':{'type':'string','pattern':'^nat_[a-z_]+$'},'severity':{'const':'warning'},'bad_examples':{'type':'array','minItems':1,'items':{'type':'string'}},'preferred_strategy':{'type':'string','minLength':1},'autolint_possible':{'type':'boolean'},'notes':{'type':'string'}}}}}}
    write(DATA/'naturalness_guidelines.schema.json',schema)
    doc=['# 韓国語K1 自然さ生成guideline','', '語彙800・文法32・導入予定・window・coverageは固定。自然さをreview語数より優先する。短い自然な文を、好ましい文長へ副詞で引き伸ばさない。','',
         '## 生成から承認まで','', ' → '.join(data['pipeline']),'', '直接会話は話者を明示する。引用内も同じ32文法で検証し、間接引用や名詞化を追加許可しない。','']
    for r in data['rules']:
        doc += ['## '+r['category'],'',r['preferred_strategy'],'','危険例: '+' / '.join(r['bad_examples']),'',r['notes'],'']
    doc+=['## 二次意味レビュー','', ' / '.join(CHECKS),'','各項目をYES/NO/REVIEW＋文脈の根拠で記録する。YESもモデルの仮判定であり、人間承認へ昇格させない。NOは書き直し・省略・defer、REVIEWは根拠付きで人間へ絞り込む。','',
          '## 語義と台帳','', '자리は席。紙の余白に広げない。Core 쓰다は書く、道具には사용하다。들다は手に持つ・持ち上げるだけ。아저씨のadult_man_addressは現行notesの叙述優先と名称がずれるため将来レビューへ送り、今回変更しない。','',
          'reviewの取りこぼしは選択予定を実出現として数えない。incidental exposureは本文の実使用だけから記録する。自然に書けない箇所はnatural_expression_gapにし、未許可語を使うより省略・延期する。','',
          '99%はtarget。U=2,N<200のtarget missは予想される。controlled100%とprevious98%をhard検査し、Nから未知語を隠さない。']
    (ROOT/'docs').mkdir(exist_ok=True);(ROOT/'docs/ko_k1_naturalness_guidelines.md').write_text('\n'.join(doc)+'\n',encoding='utf-8')

def second_pass(scene,rec):
    reasons=scene.get('semantic_evidence',{})
    evidence={k:dict(verdict='YES',reason=reasons.get(k,'Revised single-scene body checked against the stated intent; this is an author judgment, not independent Korean review.')) for k in CHECKS}
    if any(a['lemma'] in ('아저씨','풀','이','눈','들다','쓰다') and a['role']!='grammar_function' and (a['lemma']!='이' or a['sense']=='tooth') for a in rec['annotations']):
        evidence['natural_arguments']=dict(verdict='REVIEW',reason='Context-specific sense shortlist: check physical hold/lift, glue/grass, tooth/eye and writing; adult-man reference label remains frozen.')
    if any(a['lemma'] in ('이것','그것') for a in rec['annotations']):
        evidence['clear_references']=dict(verdict='REVIEW',reason='Concrete antecedent identified in preceding scene, but beginner readability requires contextual human review.')
    # Candidate findings must not be silently converted into blanket model YES.
    mapping={'nat_filler_adverb':'meaningful_adverbs','nat_reference_clarity':'clear_references',
             'nat_verb_argument_frame':'natural_arguments','nat_genitive_overuse':'necessary_genitives',
             'nat_scene_plausibility':'plausible_actions','nat_habit_vs_progressive':'simple_natural_construction'}
    for rule,check in mapping.items():
        candidates=[w for w in rec['naturalness_lint'] if w['rule_id']==rule]
        if candidates:
            reason=f"{len(candidates)} candidate warning(s): verify their specific context rather than approve the repeated template automatically. "
            if scene['text_number']==242 and rule=='nat_verb_argument_frame':
                reason+='The visitor hands over a bag before sitting to eat; receiving that bag is an actual transfer, not a substitute for carrying a heavy bag.'
            evidence[check]=dict(verdict='REVIEW',reason=reason)
    return semantic_review(evidence)

def build():
    if frozen_errors():raise ValueError(frozen_errors())
    guidelines();files=inputs();kiwi=make_kiwi();scenes=read(PILOT/'authored_scenes.json')
    def revised(scene,proposal):
        r=record(scene,files,proposal,kiwi);r['phase']='2.3'
        r['naturalness_lint']=lint(r['text_ko'],r['annotations'],files['id_migration.json']['retired_ids'])
        r['naturalness_semantic_review']=second_pass(scene,r)
        r['natural_expression_gaps']=scene.get('natural_expression_gaps',[])
        r['translation_fidelity']=dict(korean_sha256=sha256_text(r['text_ko']),
            process='Fresh Japanese translation authored after this Korean revision; no automatic copying from old JSON.',
            flags=translation_lint(scene.get('aligned_translation',[])),model_second_pass='meaning_subject_timeline_checked_not_independent_gold',human_approved=False)
        r['author_review']={'naturalness':scene['comment'],'ease':'Core repetition and short sentences; no padding to preferred length.',
            'packing':'Soft review target; veto/defer wins over count.','paraphrase':'Licensed sense only; omissions retained in gap/defer ledger.',
            'grammar':'Unchanged 32; standalone direct dialogue sentences reanalysed.','annotation':'Generated hypotheses; triage remains separate.'}
        return r
    records,ledger=state_steps(files,scenes,revised);ledger['phase']='2.3'
    for r in records:write(PILOT/'texts'/f"{r['id']}.json",r)
    selected=selection(files);selected['phase']='2.3';write(PILOT/'selection.json',selected)
    schema=text_schema();schema['properties']['phase']['const']='2.3'
    for k in ('naturalness_lint','naturalness_semantic_review','natural_expression_gaps','translation_fidelity'):
        schema['properties'][k]={'type':'array' if k in ('naturalness_lint','natural_expression_gaps') else 'object'};schema['required'].append(k)
    schema['title']='Phase 2.3 separate language revisions, hard QA plus nonauthoritative semantic pass'
    write(PILOT/'pilot_text.schema.json',schema);write(PILOT/'exposure_ledger.json',ledger)
    checks=[inspect_record(r,files,kiwi) for r in records]
    print([(r['id'],r['metrics']['eojeol_count'],r['coverage']['denominator_N'],r['errors']) for r in checks])
    return records

def sha256_text(text):
    import hashlib
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

if __name__=='__main__':build()
