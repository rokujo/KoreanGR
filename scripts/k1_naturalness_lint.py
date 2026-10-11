"""Conservative candidate warnings, never a Korean naturalness oracle.

Offsets refer to the original body. No warning changes lexical licensing or N/U.
Scene/intent, references and translation require a separate contextual pass.
"""
import re
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
GUIDELINES = ROOT / 'config/languages/ko/k1/naturalness_guidelines.json'
FILLERS = ('먼저','같이','천천히','조금','아주','정말')

def sentences(text):
    return [(m.start()+len(m.group())-len(m.group().lstrip()), m.group().strip()) for m in re.finditer(r'[^.!?]+[.!?][”"]?|[^.!?]+$', text) if m.group().strip()]

def lint(text, annotations=(), retired_ids=()):
    warnings = []
    def emit(rule, start, end, reason):
        warnings.append(dict(rule_id=rule, severity='warning', start=start, end=end,
                             surface=text[start:end], reason=reason, requires_context_review=True))
    patterns = {
      'nat_genitive_overuse': r'(?:학교의 (?:학생|길|이야기|문)|수업의 시간|버스의 (?:번호|시간|문|창문)|영화의 이야기|그림의 이야기|시계의 시간|오늘의 시간|(?:고양이|꽃)의 사진|(?:옆|안|앞)의 (?:의자|운동장|큰 건물))',
      'nat_verb_argument_frame': r'(?:책을[^.!?]*물어[봐보]|이름을[^.!?]*말해|(?:친구의 |무거운 )가방을[^.!?]*받|(?:친구|동생)에게[^.!?]*의자를[^.!?]*줘)',
      'nat_vague_positive_reaction': r'(?:약속을[^.!?]*좋아|이야기를 듣고[^.!?]*좋아|잘 잡고[^.!?]*좋아)',
      'nat_habit_vs_progressive': r'(?:자주|매일|항상|보통)[^.!?]*고 있어',
      'nat_restricted_sense': r'(?:종이(?:에|에는)[^.!?]*자리|자리가 많이|(?:돈|비용|마음|나이)[^.!?]*들어요|도장[^.!?]*찍)',
      'nat_scene_plausibility': r'(?:직원은 문 앞에서[^.!?]*기다|직원에게 휴대폰을[^.!?]*줘)',
    }
    for rule, pattern in patterns.items():
        for m in re.finditer(pattern, text): emit(rule, m.start(), m.end(), 'Registered risk pattern; intent/context may justify it.')
    rows = sentences(text)
    for n,(offset,s) in enumerate(rows):
        gens=list(re.finditer(r'\S+의(?=\s)',s))
        if len(gens)>=2: emit('nat_genitive_overuse',offset,offset+len(s),'Two explicit genitives in one sentence; review necessity, not a ban.')
        filler=list(re.finditer(r'(?<!\S)(?:'+ '|'.join(FILLERS)+r')(?=\s)',s))
        if len(filler)>=2:emit('nat_filler_adverb',offset,offset+len(s),'Several filler candidates in one sentence; require a semantic reason.')
        for word in FILLERS:
            if re.search(r'(?<!\S)'+word+r'(?=\s)',s) and any(re.search(r'(?<!\S)'+word+r'(?=\s)',ss) for _,ss in rows[max(0,n-2):n]):
                emit('nat_filler_adverb',offset,offset+len(s),f'{word} repeats within three sentences; meaningful repetition can be retained.')
        if re.search(r'(?:이것|그것|그 사람|여기|거기)',s):
            emit('nat_reference_clarity',offset,offset+len(s),'Demonstrative candidate: verify a concrete antecedent, speaker and location in context.')
    for a in annotations:
        if a.get('vocab_id') in retired_ids:
            emit('nat_restricted_sense',a['start'],a['end'],'Retired identity detected; the lexical validator separately enforces this as a hard error.')
        if a.get('lemma') in ('들다','풀','이','눈','쓰다','아저씨') and a.get('role')!='grammar_function' and (a.get('lemma')!='이' or a.get('sense')=='tooth'):
            emit('nat_restricted_sense',a['start'],a['end'],f"Context review: {a.get('lemma')} / {a.get('sense')}; lemma membership alone is insufficient.")
    return warnings

CHECKS = ('coherent_goal','plausible_actions','no_review_only_actions','natural_arguments',
          'clear_references','necessary_genitives','meaningful_adverbs','simple_natural_construction')

def semantic_review(evidence):
    """Require explicit contextual judgments; never turn model YES into approval."""
    missing=set(CHECKS)-set(evidence)
    if missing:raise ValueError('Missing semantic checks: '+str(sorted(missing)))
    for check in CHECKS:
        row=evidence[check]
        if row.get('verdict') not in ('YES','NO','REVIEW') or not row.get('reason'):
            raise ValueError('Semantic judgment needs verdict and reason: '+check)
    return dict(stage='naturalness_semantic_review',origin='author_second_pass_not_independent_gold',
                checks=evidence,flags=[k for k in CHECKS if evidence[k]['verdict']!='YES'],
                human_approved=False,approval_policy='Human/context review required; regex and model judgments are screening only.')

def translation_lint(pairs):
    """Only a few observable mismatches. Absence of flags is not proof of fidelity."""
    flags=[]
    for n,pair in enumerate(pairs):
        ko,ja=pair
        if '좋아' in ko and '喜' in ja and '好き' not in ja:
            flags.append(dict(sentence=n+1,type='positive_reaction_translation',ko=ko,ja=ja))
        if '웃' in ko and '笑' not in ja:
            flags.append(dict(sentence=n+1,type='smile_translation_review',ko=ko,ja=ja))
    return flags
