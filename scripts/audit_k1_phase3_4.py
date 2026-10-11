"""Pure new-layer contrast audit; never grants exposure or edits old results."""
from copy import deepcopy
from jsonschema import Draft202012Validator
from k1_phase3 import files, read, write, ROOT
from k1_phase2_3 import make_kiwi
from k1_phase3_2_analysis import morphology
from k1_phase3_4_resolver import analyze
from build_k1_phase3_4_schemas import contracts


def audit():
    f=files();f['_allowed_vocab']=f['core_vocab.json']+f['expansion_vocab.json'];kiwi=make_kiwi()
    cases=read(ROOT/'tests/fixtures/k1_phase3_4_uri_scope.json')['scope_cases']
    cases += [dict(scope='positive_contrast',text=s) for s in (
        '우리 집에 가요.','우리 학교에 가요.','우리 가족이 와요.','"우리 집에 올 거예요?"')]
    cases += [dict(scope='noun_contrast',text=s) for s in (
        '우리 안에 개가 있어요.','우리에서 사람이 나와요.','우리 밖에 사람이 있어요.')]
    rows=[]
    for case in cases:
        a=analyze(case['text'],f,2,(),(),(),kiwi,scope=case['scope'])
        preserved=a['raw_morphology']==morphology(case['text'],kiwi)
        assert preserved
        rows.append(dict(**case,raw_morphology=a['raw_morphology'],annotations=a['annotations'],
            unresolved=a['unresolved_tokens'],uri_audit=a['uri_recovery_audit'],quote_audit=a['quote_recovery_audit'],
            raw_preserved=preserved,expected_review=case['scope']=='noun_contrast',
            passed=(any(d['decision']=='REVIEW' for d in a['uri_recovery_audit']) if case['scope']=='noun_contrast'
                    else not a['unresolved_tokens'] and all(d['decision']!='REVIEW' for d in a['uri_recovery_audit']))))
    uri=dict(phase='3.4',cases=rows,all_pass=all(r['passed'] for r in rows),credit=False)
    write(ROOT/'reports/k1_phase3_4_uri_context_audit.json',uri)
    template=read(ROOT/'pilot/ko/k1/phase3_sequential_v3/candidates/K1-001-attempt-02.json')
    candidate,source=contracts();validator=Draft202012Validator(candidate)
    positive=[];negative=[]
    for n in range(1,51):
        obj=deepcopy(template);obj.update(id=f'K1-{n:03d}',text_number=n)
        positive.append(dict(id=obj['id'],text_number=n,errors=[e.message for e in validator.iter_errors(obj)]))
    for ident in ('K1-000','K1-051','K1-099','K1-300','K1-01','K1-1','KO-K1-001','K2-001'):
        obj=deepcopy(template);obj['id']=ident
        negative.append(dict(id=ident,rejected=not validator.is_valid(obj)))
    schema=dict(positive=positive,negative=negative,all_pass=all(not p['errors'] for p in positive) and all(p['rejected'] for p in negative),
        scene_catalog=source['properties']['scene']['items']['enum'],genres=source['properties']['genre']['enum'],
        scene_catalog_changed=False,genre_provenance='Phase 3 user genre list plus approved Phase 2.3/3 pilot labels; no quotas or new scene categories',
        old_genre_schema_unrestricted=True,new_genre_schema_finite=True,generic_id_and_range_separated=True,
        candidate_contract_max=50,smoke_control_max=3,credit=False)
    write(ROOT/'reports/k1_phase3_4_forward_schema_audit.json',schema)
    print({'uri_audit_cases':len(rows),'uri_pass':uri['all_pass'],'schema_positive':len(positive),'schema_negative':len(negative),'schema_pass':schema['all_pass']})
    return uri,schema

if __name__=='__main__':audit()
