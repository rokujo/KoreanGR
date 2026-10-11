"""Report-only replay of frozen texts; never imports or pays their exposure."""
from collections import Counter
from k1_phase3 import ROOT, read, write, files
from k1_phase3_4_resolver import analyze
from k1_phase3_2_analysis import make_kiwi
from k1_grammar_semantic_gate import checks, summarize, registry

ADVERSARIAL=[
('g30_transport','버스로 학교에 가요.',30,'PASS'),
('g30_tool','연필로 이름을 써요.',30,'PASS'),
('g30_direction','집으로 가요.',30,'PASS'),
('g30_role','사진을 선물로 줘요.',30,'FAIL'),
('bad_003','사진을 선물로 주고 싶어요.',30,'FAIL'),
('g30_status','학생으로 일해요.',30,'FAIL'),
('g30_unknown','이것으로 괜찮아요.',30,'REVIEW'),
('g30_material','나무로 의자를 만들어요.',30,'FAIL'),
('corrected_003','저는 어머니에게 사진을 주고 싶어요.',28,'PASS'),
('progressive_habit','자주 공부하고 있어요.',5,'REVIEW'),
('progressive_now','저는 지금 책을 읽고 있어요.',5,'PASS'),
('progressive_result','저는 지금 옷을 입고 있어요.',5,'REVIEW'),
('condition','시간이 있으면 책을 읽어요.',13,'PASS'),
('reason','비가 와서 집에 있어요.',11,'PASS'),
('reason_instruction','비가 와서 우산을 가져가세요.',11,'FAIL'),
('source','학교에서 집으로 와요.',23,'FAIL'),
('location','집에서 책을 읽어요.',23,'PASS'),
('destination','학교에 가요.',22,'PASS'),
('existence','집에 있어요.',22,'PASS'),
('ownership','친구의 책이에요.',29,'PASS'),
('abstract_genitive','영화의 이야기예요.',29,'REVIEW'),
('recipient','친구에게 책을 줘요.',28,'PASS'),
('human_source','친구에게 책을 받아요.',28,'REVIEW'),
('addition','저도 학교에 가요.',24,'PASS'),
('scalar_addition','아이도 이것을 알아요.',24,'REVIEW'),
('range','아침부터 저녁까지 일해요.',31,'PASS'),
('scalar_until','아이까지 이것을 알아요.',31,'REVIEW'),
('limit','물만 마셔요.',32,'PASS'),
('elapsed_time_not_simple_limit','하루만에 집에 와요.',32,'PRECEDING_REJECT'),
('nominalization_not_simple_limit','책을 읽기만 해요.',32,'REVIEW'),
('path_not_established_object','길을 걸어요.',21,'REVIEW'),
('quantity_per_time','하루에 책을 두 권 읽어요.',22,'REVIEW'),
('companionship','친구하고 가요.',25,'PASS'),
('noun_coordinate','밥하고 국을 먹어요.',25,'PASS'),
('prediction','내일 비가 올 거예요.',4,'REVIEW'),
('possibility','내일 비가 올 수 있어요.',16,'FAIL'),
('third_person_wish','친구는 책을 읽고 싶어요.',6,'REVIEW'),
('become_complement','저는 선생님이 돼요.',20,'REVIEW'),
]

def fixtures():
    entries=registry(); rows=[]
    for g in entries.values():
        rows.append(dict(id=g['grammar_id']+'_frozen_positive',text=g['positive_examples'][0],grammar_id=g['grammar_id'],expected='PASS',provenance='frozen grammar.json example',target_semantic_only=True))
    for key,text,n,expected in ADVERSARIAL:
        rows.append(dict(id=key,text=text,grammar_id=f'ko_k1_g{n:02d}',expected=expected,provenance='local adversarial meaning contrast',target_semantic_only=expected!='PRECEDING_REJECT'))
    write(ROOT/'tests/fixtures/k1_phase3_5_grammar_semantics.json',rows)
    return rows

def audit():
    f=files();f['_allowed_vocab']=f['core_vocab.json']+f['expansion_vocab.json'];k=make_kiwi()
    cases=[]
    for row in fixtures():
        a=analyze(row['text'],f,255,[],kiwi=k,scope='grammar_fixture')
        cs=checks(row['text'],a);target=[x for x in cs if x['grammar_id']==row['grammar_id']]
        passed=(not target and bool(a['unresolved_tokens'])) if row['expected']=='PRECEDING_REJECT' else bool(target) and all(x['decision']==row['expected'] for x in target)
        cases.append(dict(row,checks=cs,target_found=bool(target),passed=passed,
            preceding_morphology_unresolved=a['unresolved_tokens'],raw_morphology=a['raw_morphology']))
    write(ROOT/'reports/k1_phase3_5_fixture_audit.json',cases)
    corpus=[]
    paths=list((ROOT/'pilot/ko/k1/phase2_3/texts').glob('*.json'))+list((ROOT/'pilot/ko/k1/phase3_4_corrected_smoke/texts').glob('*.json'))
    for path in sorted(paths):
        old=read(path);text=old['text_ko']
        # All800 registered identities available for report-only analysis,
        # not permission for generating texts or importing prior-run credits.
        a=analyze(text,f,old['text_number'],[],kiwi=k,scope='frozen_report_only')
        cs=checks(text,a)+checks(old['title_ko'],analyze(old['title_ko'],f,old['text_number'],[],kiwi=k,scope='title'),'title')
        corpus.append(dict(path=path.relative_to(ROOT).as_posix(),id=old['id'],
            checks=cs,counts=summarize(cs),raw_analysis_unresolved=a['unresolved_tokens'],
            automatic_failures=[x for x in cs if x['decision']=='FAIL'],
            review_candidates=[x for x in cs if x['decision']=='REVIEW']))
    write(ROOT/'reports/k1_phase3_5_existing_text_audit.json',corpus)
    print(dict(fixtures=len(cases),fixture_failures=sum(not c['passed'] for c in cases),texts=len(corpus),decisions=dict(Counter(x['decision'] for c in corpus for x in c['checks']))))
    return cases,corpus

if __name__=='__main__':audit()
