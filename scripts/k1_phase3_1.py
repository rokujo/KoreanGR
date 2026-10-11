"""One-text controlled regression smoke, never K1-002+ generation."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from k1_phase3 import ROOT,REPORTS,STATE,DATA,PILOT as PHASE3,read,write,sha,files
from k1_candidate_gate import CandidateGate,digest,build_snapshot,permission_issues
from k1_phase3_1_resolver import analyze
from k1_phase2_3 import make_kiwi

RUN_DIR=ROOT/'pilot/ko/k1/phase3_1'
LEDGER=STATE/'phase3_1_smoke_exposure_ledger.json'
FREEZE=REPORTS/'k1_phase3_1_input_freeze.json'

def freeze():
    if FREEZE.exists():
        errors=freeze_errors()
        if errors:raise ValueError(errors)
        return
    old=read(REPORTS/'k1_phase3_input_freeze.json')['files']
    phase3=read(REPORTS/'k1_phase3_artifact_manifest.json')['files']
    if any(sha(ROOT/p)!=h for p,h in {**old,**phase3}.items()):raise ValueError('Phase 3 history already changed')
    paths={ROOT/p for p in {**old,**phase3}}
    paths.add(REPORTS/'k1_phase3_artifact_manifest.json')
    paths.update(DATA.glob('*.json'))
    write(FREEZE,dict(phase='3.1',scope='All frozen K1 inputs, prior implementations, and full Phase 3 failure/history. No reinterpretation as success.',
        files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths)}))

def freeze_errors():
    return ['Changed prior history/input: '+p for p,h in read(FREEZE)['files'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]

def smoke_source(snapshot,feedback,attempt):
    """Deterministic authored repair callback exercises actual gate feedback.

    The historical failure is intentionally replayed once. This is not evidence
    that a language model will always repair arbitrary errors within three tries.
    """
    if snapshot['text_number']!=1:raise ValueError('Smoke generator only supports 001')
    src=deepcopy(read(PHASE3/'sources/K1-001.json'))
    if attempt>1:
        codes={e['code'] for e in feedback['hard_errors']}
        if attempt==2 and 'future_expansion' not in codes:raise ValueError('Expected first feedback future vocabulary')
        if attempt==3 and codes!={'length'}:raise ValueError('Third repair must address only coherent length expansion')
        i=src['sentences'].index('친구도 집에 들어오고 싶어요.')
        src['sentences'][i]='친구도 집에서 쉬고 싶어요.'
        src['translations_ja'][i]='友達も家で休みたいです。'
        src['notes'].append('Future directional verb omitted in favor of the same indoor rain-waiting goal, not synonym aliasing.')
    if attempt==3:
        ss=[];jj=[]
        for ko,ja in zip(src['sentences'],src['translations_ja']):
            if ko=='세 시가 되면 밖에 나가요.':
                ss.append('친구는 창문 앞에 서서 밖을 봐요.');jj.append('友達は窓の前に立って外を見ます。')
            ss.append(ko);jj.append(ja)
            if ko=='저는 친구 사진을 찍어요.':
                ss += ['친구는 제 휴대폰으로 친구 사진을 봐요.','사진에 꽃도 많이 있어요.']
                jj += ['友達は私の携帯で友達の写真を見ます。','写真には花もたくさん写っています。']
        src['sentences']=ss;src['translations_ja']=jj
        src['semantic_evidence']['no_review_only_actions']['reason']='reviewなし。窓から天気を確認し、公園で撮った写真を確認するという同じ外出の準備と結果だけを補った。'
        src['notes'].append('16 eojeol added: checking weather at window, viewing the actual photo and its flowers. No filler adverbs added.')
    src['generated_intents']=[dict(sentence='공원까지 친구하고 걸어요.',surface='걸어요',lemma='걷다',pos='verb',sense='walk',vocab_id='ko_k1_0186')]
    src['translation_fidelity_review']='最終candidateの韓国語各文と対照。休みたい意図・窓での確認・携帯上の写真確認を訳に反映。訳で未許可語や方向動詞を補正しない。'
    return src

PROBES=[
    ('걷다','공원까지 친구하고 걸어요.','d_irregular'),
    ('걷다','공원까지 친구하고 걸었어요.','d_irregular_past'),
    ('듣다','저는 음악을 들어요.','d_irregular'),
    ('듣다','저는 음악을 들었어요.','d_irregular_past'),
    ('도와주다','저는 친구를 도와줘요.','b_irregular_compound'),
    ('도와주다','친구를 도와주고 싶어요.','b_irregular_compound_auxiliary'),
    ('덥다','오늘 날씨가 더워요.','b_irregular'),
    ('춥다','오늘 날씨가 추워요.','b_irregular'),
    ('쉽다','이 문제는 쉬워요.','b_irregular'),
    ('어렵다','이 숙제는 어려워요.','b_irregular'),
    ('가깝다','집이 학교에서 가까워요.','b_irregular'),
    ('무겁다','이 가방은 무거워요.','b_irregular'),
    ('가볍다','이 책은 가벼워요.','b_irregular'),
    ('뜨겁다','이 물은 뜨거워요.','b_irregular'),
    ('차갑다','이 물은 차가워요.','b_irregular'),
    ('빠르다','버스가 빨라요.','reu_irregular'),
    ('모르다','저는 친구 이름을 몰라요.','reu_irregular'),
    ('다르다','저하고 친구는 달라요.','reu_irregular'),
    ('고르다','저는 사과를 골라요.','reu_irregular'),
    ('부르다','저는 친구를 불러요.','reu_irregular'),
    ('닫다','문을 닫아요.','d_regular_negative_control'),
    ('받다','저는 책을 받아요.','d_regular_negative_control'),
    ('입다','저는 옷을 입어요.','b_regular_negative_control'),
    ('공부하다','저는 한국어를 공부해요.','hada_compound'),
    ('운동하다','친구는 공원에서 운동해요.','hada_compound'),
    ('전화하다','저는 친구에게 전화해요.','hada_compound'),
    ('준비하다','저는 여행을 준비해요.','hada_compound'),
    ('사용하다','저는 컴퓨터를 사용해요.','hada_compound')
]

def audit_morphology(kiwi):
    f=files();v=f['core_vocab.json']+f['expansion_vocab.json'];f['_allowed_vocab']=v
    from k1_phase2_2 import analyze as before
    rows=[]
    for lemma,sentence,kind in PROBES:
        entries=[e for e in v if e['lemma']==lemma and e['pos'] in ('verb','adjective')]
        if len(entries)!=1:
            rows.append(dict(lemma=lemma,kind=kind,status='not_unambiguous_active_entry'));continue
        e=entries[0];word=sentence.split()[-1].rstrip('.')
        intents=[dict(sentence=sentence,surface=word,lemma=lemma,pos=e['pos'],sense=e['sense'],vocab_id=e['id'])] if lemma=='걷다' else []
        raw=before(sentence,f,255,[],{},kiwi);a=analyze(sentence,f,255,[],intents,['walk'] if lemma=='걷다' else [],kiwi)
        passed=not a['unresolved_tokens'] and e['id'] in {x['vocab_id'] for x in a['annotations']}
        rows.append(dict(lemma=lemma,vocab_id=e['id'],sense=e['sense'],kind=kind,sentence=sentence,
            before_unresolved=raw['unresolved_tokens'],after_unresolved=a['unresolved_tokens'],target_recognized=passed,
            raw_morphology=a['raw_morphology'],resolver_decisions=a['resolver_decisions']))
    stem_candidates=[]
    for e in v:
        if e['pos'] not in ('verb','adjective'):continue
        stem=e['lemma'][:-1];last=ord(stem[-1]) if stem else 0
        jong=(last-0xAC00)%28 if 0xAC00<=last<=0xD7A3 else None
        categories=[]
        if jong==7:categories.append('d_stem_candidate_not_automatically_irregular')
        if jong==17:categories.append('b_stem_candidate_not_automatically_irregular')
        if stem.endswith('르'):categories.append('reu_stem_candidate')
        if e['lemma'].endswith('하다'):categories.append('registered_hada_compound')
        if categories:stem_candidates.append(dict(vocab_id=e['id'],lemma=e['lemma'],sense=e['sense'],candidate_classes=categories))
    result=dict(scope='Inventory of active 800 + selected valid-inflection regression probes, not exhaustive conjugation or sense gold; audit all-permitted scenario is never credited to smoke.',
        inactive_standalone_help=dict(lemma='돕다',active=any(e['lemma']=='돕다' for e in v),alternative_registered_lemma='도와주다'),
        stem_candidates=stem_candidates,probes=rows,probe_count=len(rows),failed_probes=[r for r in rows if not r.get('target_recognized',False)])
    write(REPORTS/'k1_phase3_1_morphology_audit.json',result)
    return result

def smoke():
    freeze();kiwi=make_kiwi()
    g=CandidateGate(RUN_DIR,LEDGER,kiwi=kiwi,max_attempts=3,max_text=1)
    g.initialize();result=g.run_one(1,smoke_source)
    audit=audit_morphology(kiwi)
    print(dict(smoke_hard_pass=bool(result),attempts=result['attempt_number'] if result else 3,
        eojeol=result['eojeol_count'] if result else None,coverage=result['coverage'] if result else None,
        morphology_failed=len(audit['failed_probes']),freeze_errors=freeze_errors()))

if __name__=='__main__':smoke()
