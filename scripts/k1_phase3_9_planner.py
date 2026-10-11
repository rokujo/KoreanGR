"""Scene presentation only: frozen window payment and validators are untouched.

Affinities are hints; author realization can veto every suggestion. Plans give
neither exposure credit nor permission to use an unintroduced word.
"""
from collections import Counter
import re
from k1_phase3 import vocab

GAPS = {
    '펴다': {'avoid':'책을 열어요', 'strategy':'omit opening the paper book; 책을 읽어요'},
    '입히다': {'avoid':'입다 as dress somebody else', 'strategy':'omit dressing another person'},
    '지우다': {'avoid':'닦다 as erase', 'strategy':'omit erasing; 다시 써요 if natural'},
}
BAD_PATTERNS = [
    ('recipient_smile',r'\S+(?:에게|한테)\s+웃', 'use natural seeing/smiling or omit'),
    ('paper_book_open',r'책을\s*열', 'omit opening; read the book'),
    ('close_bicycle',r'자전거를\s*닫', 'omit unavailable action'),
]
def author_findings(text,intended_pack=False):
    result=[dict(category='naturalness',key=k,strategy=s) for k,p,s in BAD_PATTERNS if re.search(p,text)]
    if intended_pack and re.search(r'가방을\s*만들',text):result.append(dict(category='naturalness',key='pack_bag_substitution',strategy='omit packing; describe necessary objects'))
    return result

def health(state, n):
    capped=sum(min(6,e['actual_exposure_count']) for e in state['entries'])
    remaining=3000-capped
    rate=remaining/(300-n) if n<300 else (0 if not remaining else None)
    return dict(capped_exposure_progress=capped,required_total=3000,remaining_required_capped_credits=remaining,
        remaining_texts_to_300=300-n,required_future_credit_rate=rate,
        planning_color='GREEN' if rate is not None and rate<=11 else 'YELLOW' if rate is not None and rate<=13 else 'RED',
        outstanding_windows=len(state['review_debt']),expired_windows=len(state['expired_review_debt']))

def debt_candidates(f,state,t):
    v=vocab(f);actual={e['vocab_id']:e for e in state['entries']};result=[]
    for w in f['vocab_review_windows.json']['entries']:
        e=actual[w['vocab_id']]
        if e['actual_first_text'] is None or e['actual_first_text']>=t:continue
        opened=[(i,x) for i,x in enumerate(w['review_windows']) if x['from']<=t and str(i) not in e['paid_review_windows']]
        if not opened:continue
        i,x=opened[0];width=x['to']-x['from']+1;remaining=x['to']-t+1
        gap=t-e['last_exposure_text'];shortage=max(0,6-e['actual_exposure_count'])
        urgency=20/max(1,remaining);old=max(0,t-x['to'])
        # Presentation priority, never a change to frozen scheduler.select().
        priority=urgency+4*shortage+min(old,40)+min(gap,30)/3-(20 if gap<3 else 0)
        result.append(dict(vocab_id=e['vocab_id'],lemma=e['lemma'],sense=v[e['vocab_id']]['sense'],
            scene_affinity=w['scene_affinity'],window_index=i,window=x,remaining_fraction=max(0,remaining)/width,
            exposure_count=e['actual_exposure_count'],last_exposure_text=e['last_exposure_text'],
            expired=old>0,priority=round(priority,3),consider_early=remaining/width>.25,
            required_capped_credit=shortage>0))
    return sorted(result,key=lambda x:(-x['priority'],x['window']['to'],x['vocab_id']))

def proposals(f,state,snapshot):
    t=snapshot['text_number'];v=vocab(f);new=snapshot['planned_new_vocab_ids'];pool=debt_candidates(f,state,t)
    ws={e['vocab_id']:e for e in f['vocab_review_windows.json']['entries']}
    genres=Counter(x['genre'] for x in state['genre_history'])
    scene_genre={'food':'food','kitchen':'food','school':'school','shopping':'shopping','transport':'transport',
        'travel':'travel','home':'home','health':'health','body':'health','outdoor':'outdoor','nature':'weather',
        'work':'work','communication':'short_dialogue','friendship':'friends','family':'family',
        'object_problem':'small_problem','lost_and_found':'small_problem'}
    hints=[set(ws[i]['scene_affinity']) for i in new]
    scenes=sorted(set.union(*hints)) if hints else f['vocab_review_windows.json']['scene_catalog']
    candidates=[]
    for scene in scenes:
        fit=[x for x in pool if scene in x['scene_affinity']]
        # Unique under-exposed words first; repeat already-capped words only if
        # needed for a still-unpaid spaced window or a natural incidental use.
        fit.sort(key=lambda x:(not x['required_capped_credit'],-x['priority'],x['vocab_id']))
        bundle=fit[:14];new_fit=sum(scene in h for h in hints)
        genre=scene_genre[scene]
        score=100*new_fit+sum(max(0,x['priority']) for x in bundle)/max(1,len(bundle))+4*len(bundle)-4*genres[genre]
        candidates.append(dict(scene=[scene],suggested_genre=genre,new_lemmas=[v[i]['lemma'] for i in new],
            planned_hint_fit=new_fit,score=round(score,3),bundle=bundle,
            strategy='One small shared goal. Hints are provisional: veto unrelated words; do not add side events.',
            semantic_veto_overrides_deadline=True))
    return dict(text_number=t,health_before=health(state,t-1),scene_candidates=sorted(candidates,key=lambda x:-x['score'])[:3],
        considerations=[dict(vocab_id=x['vocab_id'],window_index=x['window_index'],text=t,
            before_last_quarter=x['consider_early'],matched_scene_candidates=[c['scene'][0] for c in candidates if x in c['bundle']],
            disposition='considered_not_observed') for x in pool],
        debt_pool=pool,selection_is_exposure=False)

def contract(f,snapshot):
    allowed={e['vocab_id'] for e in snapshot['entries']}
    def compact(e):return {k:e[k] for k in ('vocab_id','lemma','pos','sense','forms','role')}
    return dict(ALLOWED_CORE=[compact(e) for e in snapshot['entries'] if e['role']=='core'],
        ALLOWED_NEW=[compact(e) for e in snapshot['entries'] if e['role']=='current_new_expansion'],
        ACTIVE_EXPANSION=[compact(e) for e in snapshot['entries'] if e['role']=='previous_expansion'],
        FORBIDDEN_FUTURE=[dict(id=e['id'],lemma=e['lemma'],pos=e['pos'],sense=e['sense']) for e in f['expansion_vocab.json'] if e['id'] not in allowed],
        RESTRICTED_SENSE=snapshot['explicit_restricted_senses'],BASIC_SENSE_FAMILY=snapshot['basic_sense_families'],
        PROPER_NAMES=snapshot['allowed_proper_names'],FROZEN_EXCEPTIONS=snapshot['lexical_exceptions'],KNOWN_GAPS=GAPS,
        instructions='Use no content identity outside ALLOWED_CORE + ACTIVE_EXPANSION + ALLOWED_NEW. FORBIDDEN_FUTURE is a negative list, not generation suggestions.')
