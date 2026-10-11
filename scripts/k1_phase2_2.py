"""Separate 25-text pilot. Frozen input assumptions never count as delivered texts."""
from pathlib import Path
import hashlib
import json
from collections import Counter
from copy import deepcopy
import re

from k1_pilot_analysis import analyze as base_analyze, make_kiwi as base_kiwi
from k1_review_scheduler import ReviewScheduler
from lexical_coverage import evaluate_lexical_tokens
from validate_k1_pilot import text_metrics, token_stream

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'config/languages/ko/k1'
PILOT = ROOT / 'pilot/ko/k1/phase2_2'
REPORTS = ROOT / 'reports'
FREEZE = REPORTS / 'k1_phase2_2_input_freeze.json'
B_IDS = ['ko_k1_0808', 'ko_k1_0810', 'ko_k1_0812', 'ko_k1_0811', 'ko_k1_0809']

def make_kiwi():
    """Registered lexical segmentation hints; neither new entries nor sense gold."""
    kiwi=base_kiwi()
    for form,tag in [('수건','NNG'),('제일','MAG'),('물어보','VV'),('오래되','VA')]:
        kiwi.add_user_word(form,tag,5.0)
    return kiwi

def analyze(text,files,text_number,scheduled_review,overrides=None,kiwi=None):
    """A single audited compound fallback; raw evidence retained, never sense gold."""
    result=base_analyze(text,files,text_number,scheduled_review,overrides,kiwi)
    raw=result['raw_morphology']
    for word in re.finditer(r'\S+',text):
        ids=[i for i,t in enumerate(raw) if word.start()<=t['start']<word.end()]
        content=[i for i in ids if raw[i]['tag'] not in ('EF','SF','EP')]
        if [raw[i]['form'] for i in content]!=['묻','어','보']:continue
        if [raw[i]['tag'].split('-')[0] for i in content]!=['VV','EC','VX']:continue
        matches=[e for e in files['expansion_vocab.json'] if (e['lemma'],e['pos'],e['sense'])==('물어보다','verb','ask')]
        if len(matches)!=1:continue
        e=matches[0];first=next(r['text'] for r in files['introduction_schedule.json']['rows'] if e['id'] in r['entry_ids'])
        start=raw[content[0]]['start'];end=raw[content[-1]]['start']+raw[content[-1]]['length']
        removed=[a for a in result['annotations'] if set(a['morph_indices'])&set(content)]
        result['annotations']=[a for a in result['annotations'] if a not in removed]
        result['unresolved_tokens']=[a for a in result['unresolved_tokens'] if a not in removed]
        starts={a['start'] for a in removed}
        result['annotation_review_required']=[i for i in result['annotation_review_required'] if i['start'] not in starts]
        result['annotations'].append(dict(surface=text[start:end],lemma=e['lemma'],pos=e['pos'],sense=e['sense'],vocab_id=e['id'],
            role='current_new_expansion' if first==text_number else 'scheduled_review' if e['id'] in scheduled_review else 'previous_expansion',
            start=start,end=end,morph_indices=content,grammar_id=None))
        result['annotation_review_required'].append(dict(type='compound_grouping',surface=text[start:end],lemma=e['lemma'],start=start,candidate_id=e['id']))
    result['annotations'].sort(key=lambda a:(a['start'],a['morph_indices'][0]))
    present={a['grammar_id'] for a in result['annotations'] if a['grammar_id']}
    # Retain the original attributive normalization, which stores g26 separately.
    if any(i['type']=='attributive_pos_boundary' for i in result['annotation_review_required']):present.add('ko_k1_g26')
    result['grammar_used']=sorted(present)
    return result

def annotation_triage(records,files):
    from k1_annotation_triage import classify,CATEGORIES
    vocab=vocab_map(files);grammar_ids={g['id'] for g in files['grammar.json']}
    groups={};counts=Counter({c:0 for c in CATEGORIES})
    for rec in records:
        for issue in rec['annotation_review_required']:
            category,pattern=classify(issue,rec,vocab,grammar_ids)
            if issue['type'] in ('contracted_possessive','contracted_pronoun'):
                a=next((a for a in rec['annotations'] if a['start']==issue['start'] and a['vocab_id']==issue['candidate_id']),None)
                if a and a['pos']=='pronoun' and a['lemma'] in ('나','저') and all(rec['raw_morphology'][i]['tag']=='NP' for i in a['morph_indices']):
                    category,pattern='benign_expected','registered_pronoun_contraction'
            key=(category,issue['type'],issue['candidate_id'],pattern)
            g=groups.setdefault(key,dict(category=category,type=issue['type'],vocab_id=issue['candidate_id'],lemma=issue['lemma'],pattern=pattern,
                representative_context=rec['text_ko'][max(0,issue['start']-25):issue['start']+45],occurrences=[],review_status='not_human_approved'))
            g['occurrences'].append(dict(text=rec['text_number'],start=issue['start'],surface=issue['surface']));counts[category]+=1
    return dict(status='triaged_not_human_approved',occurrence_counts=dict(counts),group_counts=dict(Counter(g['category'] for g in groups.values())),
                total_occurrences=sum(counts.values()),total_groups=len(groups),groups=list(groups.values()),
                policy='Review repeated templates once with matching context preconditions; sense contexts still require contextual review, not blanket approval.')

def read(path):
    def pairs(items):
        d = {}
        for k,v in items:
            if k in d: raise ValueError('Duplicate JSON key: '+k)
            d[k]=v
        return d
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def write(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inputs():
    names = ['core_vocab.json','expansion_vocab.json','grammar.json','profile.json','id_migration.json',
             'introduction_schedule.json','vocab_review_windows.json','proper_names.json','lexical_exceptions.json']
    return {n:read(DATA/n) for n in names}

def selection(files):
    old=read(ROOT/'pilot/ko/k1/selection.json')['text_numbers']
    first={i:r['text'] for r in files['introduction_schedule.json']['rows'] for i in r['entry_ids']}
    extra=sorted(first[i] for i in B_IDS)
    if len(set(old))!=20 or len(set(extra))!=5 or set(old)&set(extra):
        raise ValueError('A20/B5 must be disjoint and derived from frozen data')
    return {'phase':'2.2','comparison_A':old,'first_introduction_B':extra,
            'all_text_numbers':sorted(old+extra),'B_target_vocab_ids':B_IDS,
            'selection_origin':'A from saved Phase 2 selection; B from active introductions, not hardcoded numbers'}

def freeze():
    if FREEZE.exists():
        errors=check_freeze()
        if errors:raise ValueError(errors)
        return
    paths=list(DATA.glob('*.json'))
    paths += [p for d in ('scripts','tests') for p in (ROOT/d).glob('*.py') if 'phase2_2' not in p.name]
    paths += [p for p in (ROOT/'pilot/ko/k1').rglob('*') if p.is_file() and 'phase2_2' not in p.parts]
    paths += [p for p in REPORTS.rglob('*') if p.is_file() and 'phase2_2' not in p.name and '__pycache__' not in p.parts]
    write(FREEZE,{'phase':'2.2','scope':'All active K1 inputs, prior implementations and original pilot/history artifacts.',
                  'files':{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(paths))}})

def check_freeze():
    if not FREEZE.exists():return ['Missing Phase 2.2 freeze manifest']
    return ['Frozen input changed/missing: '+p for p,h in read(FREEZE)['files'].items()
            if not (ROOT/p).exists() or sha(ROOT/p)!=h]

def vocab_map(files):return {e['id']:e for e in files['core_vocab.json']+files['expansion_vocab.json']}

def candidate_ids(scene, files):
    entries=files['expansion_vocab.json'];result=[]
    for word in scene['review_candidates']:
        lemma,sep,sense=word.partition('::')
        matches=[e['id'] for e in entries if e['lemma']==lemma and (not sep or e['sense']==sense)]
        # A core helper and a future candidate are never silently promoted to a review.
        if len(matches)==1:result+=matches
        elif len(matches)>1:raise ValueError('Specify candidate sense: '+word)
    return sorted(set(result))

def plan(scene, files, state):
    return state.select(scene['text_number'], scene['scene'], approved_ids=candidate_ids(scene,files),desired=8)

def paragraphs(sentences):
    return '\n\n'.join(' '.join(sentences[i:i+7]) for i in range(0,len(sentences),7))

def source_text(scene):
    if 'sentences' in scene:
        return paragraphs([p[0] for p in scene['sentences']]),paragraphs([p[1] for p in scene['sentences']])
    return scene['text_ko'],scene['translation_ja']

def record(scene, files, proposal, kiwi):
    t=scene['text_number'];text,translation=source_text(scene)
    reviews=[r['vocab_id'] for r in proposal['selected_reviews']]
    new=proposal['new_vocab_ids'];vocab=vocab_map(files)
    first={i:r['text'] for r in files['introduction_schedule.json']['rows'] for i in r['entry_ids']}
    analysis=analyze(text,files,t,reviews,scene.get('sense_overrides'),kiwi)
    used={a['vocab_id'] for a in analysis['annotations'] if a['vocab_id']}
    actual_new=sorted(used&set(new));actual_review=sorted(used&set(reviews))
    coverage=evaluate_lexical_tokens(token_stream(analysis['annotations']),t,files)
    metrics=text_metrics(text)
    conflicts=[{'type':'semantic_schedule_conflict','vocab_id':i,'lemma':vocab[i]['lemma'],'sense':vocab[i]['sense'],
        'reason':'Selected review could not be integrated into the authored scene; retain window/debt, never alter frozen plan.',
        'resolution':'defer_within_window_or_carry_to_next','window_source_unchanged':True} for i in sorted(set(reviews)-used)]
    grammar_pass=not any(x['type'] in ('unapproved_or_unresolved_grammar','unaccounted_morpheme') for x in analysis['annotation_review_required'])
    flags=dict(vocab_pass=coverage['ok'],grammar_pass=grammar_pass,length_pass=120<=metrics['eojeol_count']<=180,
        sentence_length_pass=metrics['max_sentence_eojeol']<=10,schedule_pass=not conflicts and set(actual_new)==set(new),naturalness_review_required=True)
    return dict(id=f'K1-{t:03}',phase='2.2',group='B' if t in selection(files)['first_introduction_B'] else 'A',text_number=t,
        title_ko=scene['title_ko'],genre=scene['genre'],text_ko=text,translation_ja=translation,
        scheduled_new_vocab_ids=new,scheduled_review_vocab_ids=reviews,actually_used_new_vocab_ids=actual_new,
        actually_used_review_vocab_ids=actual_review,extra_previous_vocab_ids=sorted(i for i in used if i in first and first[i]<t and i not in reviews),
        grammar_used=analysis['grammar_used'],eojeol_count=metrics['eojeol_count'],sentence_count=metrics['sentence_count'],max_sentence_eojeol=metrics['max_sentence_eojeol'],
        coverage=dict(denominator_N=coverage['N'],new_tokens_U=coverage['U'],controlled_vocab_coverage=coverage['controlled_vocab_coverage'],
                      previous_vocab_coverage=coverage['previous_vocab_coverage'],target_99_met=coverage['previous_vocab_coverage'] is not None and coverage['previous_vocab_coverage']>=.99),
        validation=flags,semantic_schedule_conflicts=conflicts,notes=[scene['comment'],
            'Sparse pilot: earlier ungenerated introductions are hypothetical prerequisites, not delivered/observed exposures.',
            'Only the body contributes N/U; title validated separately; translation is unrestricted.',
            'Selection scores use introduction-only hypothetical seeds plus earlier accepted pilot occurrences; no invented background reviews.'],
        annotation_origin='Unchanged Kiwi/rule hypotheses, not independent sense gold',sense_overrides=scene.get('sense_overrides',{}),
        scene_affinity=scene['scene'],scheduler_selection=proposal,
        author_review={'naturalness':scene['comment']+' 要母語話者確認。', 'ease':f"平均{metrics['eojeol_count']/metrics['sentence_count']:.2f}어절/文。既知基本語を反復。",
          'packing':f"選択review{len(reviews)}語、実使用{len(actual_review)}語。数に合わせた副次事件を加えない。",
          'paraphrase':'歯・絵・貼付・保持・球遊びは許可された中心義で直接表現。その他は既知基本語を反復。',
          'grammar':'32項目内を機械検査し、境界用法は別途レビュー。', 'annotation':'生成annotationは正解ではない。型別triageを参照。'},
        **{k:analysis[k] for k in ('annotations','raw_morphology','annotation_review_required','unresolved_tokens')})

def state_steps(files,scenes,callback):
    state=ReviewScheduler(files['vocab_review_windows.json'])
    by_text={s['text_number']:s for s in scenes}
    observed=[];assumed=[];result=[]
    for t in range(1,max(by_text,default=0)+1):
        if t not in by_text:
            new=state.new_ids(t)
            if new:state.record(t,new);assumed += [{'text_number':t,'vocab_id':i,'kind':'hypothetical_introduction_only'} for i in new]
            continue
        scene=by_text[t];proposal=plan(scene,files,state)
        rec=callback(scene,proposal)
        actual=set(rec['actually_used_new_vocab_ids']+rec['actually_used_review_vocab_ids']+rec['extra_previous_vocab_ids'])
        # Do not silently record future or absent introductions in an invalid draft.
        admissible={i for i in actual if i in state.entries and t>=state.entries[i]['first_introduction_text'] and
                    (t==state.entries[i]['first_introduction_text'] or state.entries[i]['first_introduction_text'] in state.actual[i])}
        state.record(t,admissible)
        observed += [{'text_number':t,'vocab_id':i,'kind':'pilot_annotated_occurrence_not_independent_gold'} for i in sorted(admissible)]
        result.append(rec)
    return result,{'phase':'2.2','hypothetical_introduction_seeds':assumed,'pilot_occurrences':observed,
                   'final_500_by_six_actual_complete':False,'full_300_review_history_available':False,
                   'warnings':'Window deadline debts cannot be judged as mass-run failures in this sparse pilot.'}

def text_schema():
    s=deepcopy(read(ROOT/'pilot/ko/k1/pilot_text.schema.json'))
    s['title']='Phase 2.2 comparison A20 + auxiliary first-introduction B5'
    additions={'phase':{'const':'2.2'},'group':{'enum':['A','B']},'scene_affinity':{'type':'array','minItems':1,'uniqueItems':True,'items':{'type':'string'}},
        'scheduler_selection':{'type':'object'},'author_review':{'type':'object'}}
    s['properties'].update(additions);s['required']+=list(additions)
    s['properties']['semantic_schedule_conflicts']={'type':'array','items':{'type':'object','required':['type','vocab_id','reason','resolution','window_source_unchanged'],
        'properties':{'type':{'const':'semantic_schedule_conflict'},'vocab_id':{'type':'string'},'reason':{'type':'string','minLength':1},
                      'resolution':{'const':'defer_within_window_or_carry_to_next'},'window_source_unchanged':{'const':True}}}}
    return s
