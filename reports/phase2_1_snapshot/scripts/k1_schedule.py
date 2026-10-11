"""Deterministic introduction/review planning and independently reusable load metrics."""
from collections import Counter
import math
import heapq
from statistics import mean, median


def introduction_assignment(entries,texts=275,capacity=2,capacities=None,include_empty=False):
    """Earliest-deadline matching for interval jobs; optional reserved slots."""
    pending=sorted(entries,key=lambda e:(e['introduced_from'],e['rank']))
    heap=[];index=0;schedule=[]
    for text in range(1,texts+1):
        while index<len(pending) and pending[index]['introduced_from']<=text:
            e=pending[index];heapq.heappush(heap,(e['introduced_to'],e['rank'],e['id']));index+=1
        if heap and heap[0][0]<text:return None,f'{heap[0][2]} misses deadline {heap[0][0]}'
        slots=capacities.get(text,capacity) if capacities is not None else capacity
        if not isinstance(slots,int) or isinstance(slots,bool) or not 0<=slots<=capacity:
            return None,f'Invalid capacity at text {text}: {slots}'
        assigned=[]
        for _ in range(slots):
            if heap:assigned.append(heapq.heappop(heap)[2])
        if assigned or include_empty:schedule.append({'text':text,'entry_ids':assigned})
    if heap or index!=len(pending):return None,'Not enough slots inside introduction windows'
    return schedule,None


def distribution(values):
    ordered=sorted(values)
    if not ordered:
        return {'min':0,'max':0,'mean':0,'median':0,'p90':0}
    return {'min':ordered[0],'max':ordered[-1],'mean':round(mean(ordered),3),
            'median':median(ordered),'p90':ordered[math.ceil(.9*len(ordered))-1]}


def review_windows(first, total_texts=300):
    remaining=total_texts-first
    if remaining>=150:
        offsets=[(2,4),(8,15),(25,45),(70,110),(150,remaining)]
    elif remaining>=90:
        offsets=[(2,4),(8,15),(20,30),(40,60),(70,remaining)]
    elif remaining>=45:
        long_min=max(35,min(60,math.floor(.75*remaining)))
        offsets=[(2,4),(8,12),(16,20),(24,30),(long_min,remaining)]
    else:
        raise ValueError('Introduction after 255 leaves too little room for this dispersed plan')
    return [(first+low,first+high) for low,high in offsets]


def text_load_rows(entries, exposure_entries, recent_window=20):
    by_id={e['id']:e for e in entries}
    introductions={e['vocab_id']:e['first_introduction_text'] for e in exposure_entries}
    new_by_text={t:[] for t in range(1,301)}
    reviews_by_text={t:[] for t in range(1,301)}
    for entry in exposure_entries:
        new_by_text[entry['first_introduction_text']].append(entry['vocab_id'])
        for text in entry['review_texts']:reviews_by_text[text].append(entry['vocab_id'])
    rows=[]
    for text in range(1,301):
        new_ids=sorted(new_by_text[text],key=lambda vid:by_id[vid]['rank'])
        review_ids=sorted(reviews_by_text[text],key=lambda vid:by_id[vid]['rank'])
        scheduled=set(new_ids+review_ids)
        recent={vid for vid in scheduled if 0<=text-introductions[vid]<=recent_window}
        tiers={tier:sum(by_id[vid]['tier']==tier for vid in scheduled) for tier in ('E1','E2','E3')}
        rows.append(dict(text=text,new_vocab_ids=new_ids,review_vocab_ids=review_ids,
                         new_vocab_count=len(new_ids),review_vocab_count=len(review_ids),
                         recently_introduced_vocab_count=len(recent),
                         recently_introduced_E3_count=sum(by_id[vid]['tier']=='E3' for vid in recent),
                         total_scheduled_expansion_count=len(scheduled),tier_counts=tiers))
    return rows


def load_statistics(rows):
    fast=[r for r in rows if r['text']>=276]
    return {'all_texts':distribution([r['total_scheduled_expansion_count'] for r in rows]),
            'tiers':{tier:distribution([r['tier_counts'][tier] for r in rows]) for tier in ('E1','E2','E3')},
            'fast_zone':distribution([r['total_scheduled_expansion_count'] for r in fast]),
            'fast_zone_tiers':{tier:distribution([r['tier_counts'][tier] for r in fast]) for tier in ('E1','E2','E3')},
            'recently_introduced':distribution([r['recently_introduced_vocab_count'] for r in rows]),
            'fast_zone_recently_introduced':distribution([r['recently_introduced_vocab_count'] for r in fast]),
            'fast_zone_recently_introduced_E3':distribution([r['recently_introduced_E3_count'] for r in fast]),
            'periods':{f'{start:03}-{start+24:03}':{
                'new_entries':sum(r['new_vocab_count'] for r in rows[start-1:start+24]),
                'load':distribution([r['total_scheduled_expansion_count'] for r in rows[start-1:start+24]])}
                       for start in range(1,301,25)}}


def build_exposure_plan(entries, intro_rows, recent_window=20):
    by_id={e['id']:e for e in entries}
    first={vid:row['text'] for row in intro_rows for vid in row['entry_ids']}
    assert set(first)==set(by_id)
    load=Counter({row['text']:len(row['entry_ids']) for row in intro_rows})
    tier_load={tier:Counter() for tier in ('E1','E2','E3')}
    for vid,text in first.items():tier_load[by_id[vid]['tier']][text]+=1
    reviews={vid:[] for vid in first}
    jobs=[]
    for vid in sorted(first,key=lambda v:by_id[v]['rank']):
        for stage,(low,high) in enumerate(review_windows(first[vid])):
            jobs.append((high-low,high,low,by_id[vid]['rank'],stage,vid))
    # Narrow interval jobs first. Load includes initial introductions and all tiers.
    for width,high,low,rank,stage,vid in sorted(jobs):
        tier=by_id[vid]['tier']
        candidates=[t for t in range(low,high+1) if t not in reviews[vid]]
        center=(low+high)/2
        chosen=min(candidates,key=lambda t:(load[t],tier_load[tier][t],abs(t-center),t))
        reviews[vid].append(chosen)
        load[chosen]+=1;tier_load[tier][chosen]+=1
    exposure_entries=[dict(vocab_id=e['id'],first_introduction_text=first[e['id']],
                           review_texts=sorted(reviews[e['id']])) for e in entries]
    rows=text_load_rows(entries,exposure_entries,recent_window)
    return {'language':'ko','level':'K1','phase':'1.2','status':'planned_not_observed',
            'notes':'各語初出1＋再遭遇5＝異なる6教材の目標。本文未生成。実際の出現・習得を示さない。',
            'recent_window_texts':recent_window,'entries':exposure_entries,
            'texts':rows,'statistics':load_statistics(rows)}
