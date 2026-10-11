"""Conservative grammar32 semantic overlay; raw analysis is never modified.

PASS is confined to explicit local frames. Unrecognized relationships REVIEW.
Neither generated grammar labels nor scene labels confer permission.
"""
import hashlib
import re
from k1_phase3 import ROOT, read

REGISTRY=ROOT/'config/languages/ko/k1/grammar_semantics.json'
LOCATION=set('여기 거기 저기 어디 집 학교 회사 가게 식당 카페 병원 은행 시장 공원 도서관 화장실 방 교실 길 거리 역 밖 안 앞 뒤 옆 위 아래 곳 도시 운동장 동네 바다 산 부엌 버스 지하철 택시 자동차 기차 의자 책상 침대 문 창문 공책 종이 가방 책'.split())
HUMAN=set('나 저 너 우리 누구 사람 친구 가족 아버지 어머니 아들 딸 형 오빠 누나 언니 동생 남자 여자 아이 학생 선생님 손님 할머니 할아버지 아저씨 사촌 직원 의사'.split())
TIME=set('오늘 어제 내일 지금 아침 점심 저녁 밤 시간 시 분 주 월 년 날 하루 주말 월요일 화요일 수요일 목요일 금요일 토요일 일요일 봄 여름 가을 겨울 때 처음 마지막 생일'.split())
MOVE=set('가다 오다 들어가다 들어오다 나가다 돌아가다 돌아오다 걷다 뛰다 도착하다 출발하다 올라가다 내려가다 건너다 지나가다 내리다 타다 이사하다'.split())
ACTION_AT=set('읽다 쓰다 먹다 마시다 공부하다 일하다 운동하다 만나다 기다리다 사다 팔다 자다 앉다 서다 쉬다 웃다 배우다 가르치다 이야기하다 하다 말하다 듣다 보다 찾다 놀다 요리하다 씻다 닦다 붙이다 그리다 찍다 전화하다 사용하다 준비하다 넣다 꺼내다 잃다 받다 주다'.split())
RECIPIENT=set('주다 도와주다 말하다 전화하다 가르치다 물어보다 보내다 빌려주다 돌려주다'.split())
TRANSITIVE=set('가져가다 가져오다 먹다 마시다 보다 듣다 말하다 읽다 쓰다 하다 만나다 기다리다 사다 팔다 주다 받다 열다 닫다 입다 벗다 타다 공부하다 좋아하다 싫어하다 알다 모르다 배우다 가르치다 찾다 잃다 빌리다 만들다 씻다 요리하다 전화하다 사용하다 도와주다 생각하다 넣다 찍다 닦다 붙이다 들다 던지다 잡다 꺼내다 놓다 준비하다 확인하다 기억하다 고르다 그리다 물어보다 초대하다'.split())
TRANSPORT=set('버스 지하철 택시 자동차 자전거 기차 비행기 배'.split())
TOOLS={'연필':{'쓰다','그리다'},'펜':{'쓰다','그리다'},'물':{'씻다','닦다'},'손':{'들다','닦다','씻다','잡다'},'풀':{'붙이다'},'테이프':{'붙이다'},'전화':{'말하다','전화하다'},'휴대폰':{'말하다','전화하다','찍다'},'컴퓨터':{'공부하다','일하다','쓰다'},'숟가락':{'먹다'},'젓가락':{'먹다'}}
POSSESSIONS=set('집 학교 교실 방 책 공책 종이 사진 휴대폰 컴퓨터 전화 의자 책상 침대 가방 옷 신발 우산 돈 자동차 자전거 선물 이름 가족 친구'.split())

def registry():
    r=read(REGISTRY); path=ROOT/r['authoritative_source']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=r['authoritative_sha256']:raise RuntimeError('Frozen grammar definition digest mismatch')
    original=read(path)
    if len(r['entries'])!=32 or {e['grammar_id'] for e in r['entries']}!={g['id'] for g in original}:raise RuntimeError('Semantic registry is not grammar32')
    if any(e['frozen_definition']!=next(g for g in original if g['id']==e['grammar_id']) for e in r['entries']):raise RuntimeError('Semantic definition was expanded or altered')
    return {e['grammar_id']:e for e in r['entries']}

def sentence_span(text,start):
    left=max(text.rfind(c,0,start) for c in '.!?\n')+1
    end=min([p+1 for c in '.!?\n' if (p:=text.find(c,start))>=0] or [len(text)])
    return left,end

def checks(text,analysis,scope='body'):
    reg=registry(); annotations=analysis['annotations']; raw=analysis['raw_morphology']; result=[]
    occurrences=[dict(a) for a in annotations if a.get('grammar_id')]
    for a in occurrences:
        if a['grammar_id']=='ko_k1_g27':
            left=[x for x in annotations if x.get('vocab_id') and x['start']<=a['start'] and x['pos'] in ('verb','adjective')]
            if left and left[-1]['lemma'] in ('있다','없다'):
                a['morphological_grammar_id']='ko_k1_g27';a['grammar_id']='ko_k1_g26'
    # A frozen g14 surface may be returned as one EF token rather than EP 시.
    # Detect its semantic candidate without changing raw tokens or discharging
    # an unresolved token in the preceding morphology/permission gate.
    for i,t in enumerate(raw):
        if t['tag']=='EF' and t['form'] in ('세요','으세요') and not any(i in a.get('morph_indices',[]) for a in occurrences):
            occurrences.append(dict(grammar_id='ko_k1_g14',surface=text[t['start']:t['start']+t['length']],
                start=t['start'],end=t['start']+t['length'],morph_indices=[i],morphology_candidate_only=True))
    # Contracted possessives retain lexical identity in the analyzer; they are
    # semantic uses of the already frozen g29, not new lexical identities.
    for a in annotations:
        if a.get('lemma') in ('나','저') and a['surface'] in ('내','제'):
            occurrences.append(dict(a,grammar_id='ko_k1_g29',contracted_genitive=True))
    seen=set()
    for a in sorted(occurrences,key=lambda x:(x['start'],x['grammar_id'])):
        gid=a['grammar_id']; n=int(gid[-2:]); lo,hi=sentence_span(text,a['start']); sentence=text[lo:hi].strip()
        # Construction components (e.g. 고 + 싶 / 수 + 있다) count once.
        key=(gid,lo,hi) if n in (4,5,6,16,17,18) else (gid,a['start'],a['end'])
        if key in seen:continue
        seen.add(key)
        local=[x for x in annotations if x['start']>=lo and x['start']<hi and x.get('vocab_id')]
        before=[x for x in local if x['start']<a['start']]
        after=[x for x in local if x['start']>=a['end']]
        dep=before[-1] if before else None
        if n==29:
            overlap=[x for x in local if x['start']==a['start'] and x['lemma'] in ('나','저') and x['surface'] in ('내','제')]
            if overlap:dep=overlap[0]
        predicates=[x for x in local if x.get('pos') in ('verb','adjective')]
        following_pred=[x for x in predicates if x['start']>=a['end']]
        # Korean contracted endings can share the stem's original character.
        # Their raw indices differ; overlap is evidence, not an alias.
        preceding_pred=[x for x in predicates if x['start']<=a['start']]
        if n in (26,27) and preceding_pred:dep=preceding_pred[-1]
        head=(following_pred[0] if following_pred else preceding_pred[-1] if preceding_pred else None)
        d=dep['lemma'] if dep else None; p=head['lemma'] if head else None
        lemmas={x['lemma'] for x in local}; past=any(t['tag']=='EP' and t['form'] in ('었','았','였') and lo<=t['start']<hi for t in raw)
        ev=dict(frozen_allowed=reg[gid]['allowed_functions'],raw_parts=[raw[i] for i in a.get('morph_indices',[])],
                registered_dependent=dep,registered_head=head,local_registered_lemmas=sorted(lemmas),
                source='raw morphology + registered identities + local syntax; no author meaning labels')
        decision='REVIEW'; function='unresolved'; reason='No sufficient local frame evidence'
        def choose(func,why,status='PASS'):
            return status,func,why
        if n==1:
            if re.search(r'거예요',sentence):decision,function,reason=choose('future_bound_copula','Internal copula of g04; g04 independently checked')
            elif dep and dep['pos'] in ('noun','pronoun','numeral','counter'):decision,function,reason=choose('identity','Registered nominal predicate + VCP/polite copula')
        elif n==2:
            if predicates or re.search(r'(?:이에요|예요|거예요)',sentence):decision,function,reason=choose('polite_present','Polite predicate terminal; past/aspect/construction meanings separately checked')
        elif n==3:
            if re.search(r'(?:았었|었었|였었)',sentence):decision,function,reason=choose('double_past','Double past explicitly unapproved','FAIL')
            elif re.search(r'(?:어|아)\s*봤',sentence):reason='needs_human_policy: g03/g18 experience/trial-past wording'
            elif predicates or '아니다' in lemmas or any(t['tag']=='VCP' and lo<=t['start']<hi for t in raw):decision,function,reason=choose('simple_past','Single past marker on registered predicate')
        elif n==4:
            if lemmas & {'비','눈'} and p=='오다':reason='Weather prediction is not a controllable future plan'
            elif any(x in lemmas for x in ('내일','나','저','우리')) and p in MOVE|ACTION_AT|TRANSITIVE and not ('지금' in lemmas and '내일' not in lemmas):decision,function,reason=choose('future_plan','Prospective time or first-person controllable action with 거예요')
            else:reason='Plan versus conjecture is not independently established'
        elif n==5:
            if lemmas & {'자주','매일','보통','항상'}:reason='Habit marker conflicts with current-progressive evidence; REVIEW, not warning-only commit'
            elif re.search(r'(?:입|신|쓰|열|닫|앉|서)고 있',sentence):decision,function,reason=choose('result_state','Possible maintained result/positional state; not frozen progressive','REVIEW')
            elif '지금' in lemmas and preceding_pred and preceding_pred[-1]['pos']=='verb':decision,function,reason=choose('ongoing_action','Explicit 지금 + registered action + 고 있다')
        elif n==6:
            subject=next((x['lemma'] for x in local if re.match(r'(?:는|은|이|가|도)',text[x['end']:hi])),None)
            if subject in ('나','저','우리') or (sentence.rstrip('"” ').endswith('?') and not (lemmas & (HUMAN-{'너','누구'}))):decision,function,reason=choose('own_wish' if subject in ('나','저','우리') else 'question_to_addressee','Explicit speaker subject or addressee question + action')
            else:reason='needs_human_policy: unexpressed speaker or third-person wish'
        elif n in (7,8):
            if head and (head['pos']=='verb' or n==7 and head['pos']=='adjective'):decision,function,reason=choose('short_negation' if n==7 else 'capacity_or_circumstance_inability','Negator + registered predicate of permitted POS')
            elif n==8 and head and head['pos']=='adjective':decision,function,reason=choose('adjective_inability','못 + adjective is not frozen ability','FAIL')
        elif n==9:
            if preceding_pred and following_pred:decision,function,reason=choose('sequence','Two independently registered predicate clauses, not grouped auxiliary')
        elif n==10:
            pairs=[{'작다','좋다'},{'어렵다','재미있다'},{'비싸다','좋다'},{'춥다','좋다'},{'많다','작다'},{'바쁘다','하다'}]
            if any(pair<=lemmas for pair in pairs) or re.search(r'지만[^.!?]*(?:안 |못 |없)',sentence):decision,function,reason=choose('contrast','Overt opposed evaluative pair or negative second proposition')
        elif n in (11,12):
            causal=bool((lemmas & {'비','눈'} and lemmas & {'우산','집','춥다','못','안'}) or
                (lemmas & {'아프다','피곤하다','늦다','배고프다','덥다','어렵다','모르다'} and lemmas & {'쉬다','자다','병원','먹다','마시다','기다리다','배우다','말하다','설명하다','하다'}))
            chains={('씻다','먹다'),('받다','읽다'),('읽다','쓰다'),('사다','주다'),('열다','들어가다'),('가다','만나다')}
            related=bool(preceding_pred and following_pred and (preceding_pred[-1]['lemma'],following_pred[0]['lemma']) in chains)
            if n==11 and causal and re.search(r'(?:세요|까요)',sentence):decision,function,reason=choose('reason_followed_by_instruction','Frozen g11 note excludes reason + command/proposal','FAIL')
            elif n==12 and past and preceding_pred and preceding_pred[-1]['lemma'] in MOVE:reason='Discovery after arrival is possible; reason not established'
            elif causal or n==11 and related:decision,function,reason=choose('reason' if causal else 'related_sequence','Visible causal lexical frame or licensed tightly related chain')
        elif n==13:
            if past:reason='Past/counterfactual antecedent requires policy/context review'
            elif preceding_pred and following_pred:decision,function,reason=choose('concrete_condition','Concrete registered antecedent and consequent; no counterfactual/past marker')
        elif n==14:
            if predicates and predicates[-1]['pos']=='verb' and not re.search(r'(?:선생님|아버지|어머니)(?:이|가|은|는)',sentence):decision,function,reason=choose('request','Action directive; no overt third-person respectful subject')
            else:reason='Directive versus generic honorific not established'
        elif n==15:
            if (lemmas & {'우리','나','저'} or '같이' in lemmas) and p in MOVE|TRANSITIVE|ACTION_AT:decision,function,reason=choose('invitation','Overt joint/speaker action proposal')
            else:reason='Intention check versus prediction needs context/policy'
        elif n==16:
            if lemmas & {'비','눈'} and preceding_pred and preceding_pred[-1]['lemma']=='오다':decision,function,reason=choose('epistemic_possibility','Weather possibility is not action ability','FAIL')
            elif preceding_pred and preceding_pred[-1]['pos']=='verb' and preceding_pred[-1]['lemma'] in TRANSITIVE|MOVE|ACTION_AT:decision,function,reason=choose('ability','Controllable action + explicit 수 있다/없다')
        elif n==17:
            if preceding_pred and preceding_pred[-1]['pos']=='verb' and re.search(r'(?:아|어|해)야\s*해',sentence):decision,function,reason=choose('obligation','Registered action + mandatory 해야 하다, no inference frame')
        elif n==18:
            if preceding_pred and preceding_pred[-1]['pos']=='verb':
                if past:reason='needs_human_policy: experiential/trial past wording'
                else:decision,function,reason=choose('trial','Action + raw VX 보다; not lexical VV perception')
        elif n==19:
            if dep and dep['pos'] in ('noun','pronoun','numeral','counter'):decision,function,reason=choose('topic','Nominal JX topic; verbal ETM is separate g27')
        elif n==20:
            if p=='아니다':decision,function,reason=choose('negative_copula_complement','Explicit 아니다 exception in frozen notes')
            elif p=='되다' and any(x['lemma'] in ('나','저','우리') for x in before[:-1]):reason='needs_human_policy: 되다 complement is not explicitly settled'
            elif dep and dep['pos'] in ('noun','pronoun','numeral','counter'):decision,function,reason=choose('subject','Registered nominal subject + predicate')
        elif n==21:
            if p in TRANSITIVE:decision,function,reason=choose('direct_object','Registered transitive predicate local object frame')
            elif p in {'가다','오다'} and d in {'여행','운동','공부'}:decision,function,reason=choose('direct_object','Registered event-object + action frame; not path or duration extent')
            elif p in {'걷다','가다','오다','자다','쉬다'}:decision,function,reason=choose('path_extent' if p in MOVE else 'time_extent','Extent versus basic object boundary requires policy/context','REVIEW')
        elif n==22:
            if d in {'하루','주','월','년'} and any(x['pos'] in ('numeral','counter') for x in after):decision,function,reason=choose('quantity_per_unit','Duration + measured quantity is not a point time','REVIEW')
            elif d in TIME:decision,function,reason=choose('point_time','Registered temporal dependent')
            elif d in LOCATION and p in MOVE|{'앉다','서다','놓다','넣다','붙이다'}:decision,function,reason=choose('destination','Locative dependent + movement/placement predicate')
            elif d in LOCATION and p in {'있다','없다','살다'}:decision,function,reason=choose('existence_location','Locative dependent + existential/residential predicate')
        elif n==23:
            if text[a['end']:hi].startswith('부터') and d in LOCATION:decision,function,reason=choose('spatial_start_end','Explicit g31 place-start compound 에서부터; not standalone source')
            elif d in LOCATION and p in MOVE and (p in {'돌아오다','돌아가다','출발하다'} or d in TRANSPORT and p=='내리다' or any(x['grammar_id'] in ('ko_k1_g22','ko_k1_g30','ko_k1_g31') and a['end']<x['start']<hi for x in occurrences)):
                decision,function,reason=choose('source','Origin + explicit destination/return/departure/vehicle-exit frame; g23 source explicitly reserved','FAIL')
            elif d in LOCATION and p in {'걷다','뛰다','내리다'}:decision,function,reason=choose('action_location','Locomotion activity/disembark action at a place; no separate destination/source cue')
            elif d in LOCATION and p in ACTION_AT:decision,function,reason=choose('action_location','Registered action occurs at locative dependent')
        elif n==24:
            if d in ('나','저','우리','친구','동생','어머니','아버지','내일','오늘') and not re.search(r'아무|조차|심지어',sentence):decision,function,reason=choose('simple_addition','Ordinary human/time additive focus; frozen 저도 example supports speaker addition')
            else:reason='Simple addition versus scalar/indefinite focus not established'
        elif n==25:
            if dep and dep['pos'] in ('noun','pronoun'):
                if d in HUMAN and p in MOVE|ACTION_AT|TRANSITIVE:decision,function,reason=choose('companionship','Human companion + shared-action predicate')
                elif after and after[0]['pos'] in ('noun','pronoun'):decision,function,reason=choose('nominal_coordination','Two registered nominal conjuncts; not verbal 하다 grouping')
        elif n in (26,27):
            if n==26 and dep and (dep['pos']=='adjective' or d in ('있다','없다')):decision,function,reason=choose('existential_attributive' if d in ('있다','없다') else 'adjective_attributive','Registered adjective/existential head')
            elif n==27 and dep and dep['pos']=='verb':decision,function,reason=choose('verb_present_attributive','Present ETM 는 on registered verb')
        elif n==28:
            if d in HUMAN and p in RECIPIENT:decision,function,reason=choose('recipient' if p in {'주다','보내다','빌려주다','돌려주다'} else 'counterparty','Human recipient/counterparty + giving/communication frame')
            elif p in {'받다','빌리다','듣다','배우다'}:reason='needs_human_policy: human source versus counterparty not defined'
        elif n==29:
            owner=dep if not a.get('contracted_genitive') else a
            thing=after[0]['lemma'] if after else None
            if owner and owner['lemma'] in HUMAN and thing in POSSESSIONS:decision,function,reason=choose('ownership','Human possessor + concrete registered possession')
            else:reason='needs_human_policy: abstract belonging/relation not delimited'
        elif n==30:
            if d in {'선물','학생','선생님','친구','의사','아저씨'} and p in {'주다','일하다','되다','하다'}:decision,function,reason=choose('role','Role/status/as-a-gift not in frozen transport/tool/direction','FAIL')
            elif d in TRANSPORT and p in MOVE:decision,function,reason=choose('transport','Transport noun + registered movement frame')
            elif d in TOOLS and p in TOOLS[d] and not (d=='풀' and dep.get('sense')!='glue'):decision,function,reason=choose('instrument','Exact tool/predicate frame and registered sense')
            elif d in LOCATION and p in MOVE:decision,function,reason=choose('direction','Locative dependent + directional movement frame')
            elif d in {'나무','종이','물'} and p=='만들다':decision,function,reason=choose('material','Material is explicitly unapproved','FAIL')
        elif n==31:
            if d in TIME:decision,function,reason=choose('temporal_start_end','Registered temporal endpoint')
            elif d in LOCATION and p in MOVE|ACTION_AT:decision,function,reason=choose('spatial_start_end','Locative interval endpoint + event')
            else:reason='Interval versus scalar emphasis not established'
        elif n==32:
            if dep and dep['pos'] in ('noun','pronoun') and not re.search(r'기만|만에|만하',sentence):decision,function,reason=choose('simple_nominal_limit','Nominal limit attached to ordinary event')
        # Every PASS must name an allowed function, except transparent components
        # of explicitly authorized constructions (g01 inside g04; g23 in g31).
        delegated=(n==1 and function=='future_bound_copula') or (n==23 and function=='spatial_start_end')
        if decision=='PASS' and function not in reg[gid]['allowed_functions'] and not delegated:
            raise RuntimeError('Semantic classifier attempted unregistered permission')
        result.append(dict(grammar_id=gid,surface=a['surface'],start=a['start'],end=a['end'],scope=scope,
            morphological_grammar_id=a.get('morphological_grammar_id',gid),
            sentence=sentence,clause=sentence,head_predicate=p,governor=head,dependent=dep,
            semantic_role_candidate=function,local_context=text[max(0,lo-80):hi],
            allowed_function=function if decision=='PASS' else None,detected_function=function,
            allowed_function_candidate=function if function in reg[gid]['allowed_functions'] else None,
            confidence=1.0 if decision=='PASS' else .95 if decision=='FAIL' else 0.0,
            evidence=dict(ev,reason=reason),decision=decision))
    accounted={x['grammar_id'] for x in result}|{x.get('morphological_grammar_id') for x in result}
    for gid in set(analysis['grammar_used'])-accounted:
        result.append(dict(grammar_id=gid,surface=None,sentence=text,scope=scope,allowed_function=None,
            detected_function='unmapped_occurrence',evidence={'reason':'Grammar ID has no anchored occurrence'},decision='REVIEW',confidence=0.0))
    return result

def summarize(rows):
    return {d:sum(x['decision']==d for x in rows) for d in ('PASS','REVIEW','FAIL')}
