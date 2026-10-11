"""Production-lite 001..100 controller; timings include live local author wall time.

No external model API is used: the current LLM authors files after each snapshot.
This is an operator-assisted callback protocol, not a prerecorded corpus replay.
"""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import time
from k1_phase3_9_gate import CandidateGate, StructuralStop, ROOT, read, write, atomic_write, digest
from k1_phase3_retry import stagnant_errors

PILOT=ROOT/'pilot/ko/k1/phase3_9'
LEDGER=ROOT/'state/phase3_9_production_exposure_ledger.json'
FREEZE=ROOT/'reports/k1_phase3_9_input_freeze.json'
TIMING=ROOT/'reports/k1_phase3_9_timing.json'
ENGINEERING_START_UTC='2026-10-11T07:17:57.949769+00:00'


def freeze_errors():
    return [p for p,h in read(FREEZE)['files'].items()
            if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]


from k1_phase3_6a import ProductionGate as FrozenProductionGate

class ProductionGate(FrozenProductionGate,CandidateGate):
    # Ordinary candidate errors are local retries through all five attempts.
    def _submit_locked(self,source):
        return CandidateGate._submit_locked(self,source)

    def __init__(self,run_dir=PILOT,ledger_path=LEDGER,**kwargs):
        CandidateGate.__init__(self,run_dir,ledger_path,max_text=100,**kwargs)


def now():return time.perf_counter()
def utc():
    from datetime import datetime,timezone
    return datetime.now(timezone.utc).isoformat()
def save_timing(d):atomic_write(TIMING,d)
def locked_code():
    lock=read(PILOT/'code_freeze.json')
    return [p for p,h in lock['files'].items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
def guard():
    if freeze_errors() or locked_code():raise StructuralStop('Frozen history or benchmark engine changed')


def begin(t):
    if t==1:
        if TIMING.exists():raise StructuralStop('Cannot restart benchmark or reuse credit')
        if freeze_errors():raise StructuralStop('History changed')
        watched=[ROOT/'docs/ko_k1_phase3_9_author_prompt.md']+list((ROOT/'scripts').glob('*.py'))+list((ROOT/'tests').glob('*.py'))+list((ROOT/'config/languages/ko/k1').rglob('*.json'))
        write(PILOT/'code_freeze.json',dict(files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in watched}))
        gate=ProductionGate();gate.initialize()
        # Initialization and full pre-run tests are engineering/setup, not production.
        data=dict(engineering_start_utc=ENGINEERING_START_UTC,production_start_utc=utc(),
                  production_start_counter=now(),texts=[],completed=False,
                  methodology='Live local LLM author, sequential snapshot/file callback; elapsed author stage includes model reasoning and file transport. Not external API throughput.')
    else:
        guard();data=read(TIMING);gate=ProductionGate()
    if data['texts'] and data['texts'][-1].get('committed') is not True:
        raise StructuralStop('Previous text is not committed')
    started=now();snap=gate.snapshot(t)
    state=gate.load()
    from k1_phase3_9_planner import proposals,contract
    presentation=proposals(gate.f,state,snap)
    write(PILOT/'scene_proposals'/f'K1-{t:03d}.json',presentation)
    write(PILOT/'author_contracts'/f'K1-{t:03d}.json',contract(gate.f,snap))
    data['texts'].append(dict(text_number=t,start_counter=started,start_utc=utc(),phase='scene_planning',
                             phase_start_counter=started,attempts=[],stages={},committed=False))
    save_timing(data)
    print(json.dumps(dict(author_prompt=str(ROOT/'docs/ko_k1_phase3_9_author_prompt.md'),snapshot=str(PILOT/'allowed_vocab_snapshots'/f'K1-{t:03d}-epoch-{t-1}.json'),
        planned=[e for e in snap['entries'] if e['role']=='current_new_expansion'],
        allowed_previous=[e['lemma'] for e in snap['entries'] if e['role']=='previous_expansion'],
        core_lemmas=[e['lemma'] for e in snap['entries'] if e['role']=='core'] if t==1 else 'Same frozen Core300; complete permitted entries in this snapshot file.',
        scene_proposals=presentation['scene_candidates'],health_before=presentation['health_before'],
        contract_path=str(PILOT/'author_contracts'/f'K1-{t:03d}.json'),
        genre_scene_constraints=read(ROOT/'config/languages/ko/k1/phase3_4/source.schema.json')['properties']['scene'],
        forbidden_future_vocabulary='Exact ID/lemma negative list in author contract. Never treat as generation candidates.',
        review_pool=__import__('k1_phase3_6a_gate').scheduler(gate.f,gate.load()).scene_candidates(t)),ensure_ascii=False))


def plan(path):
    guard();data=read(TIMING);r=data['texts'][-1];p=read(path)
    if r['phase']!='scene_planning' or p['text_number']!=r['text_number']:raise StructuralStop('Wrong planning state')
    r['stages']['scene_planning']=now()-r['phase_start_counter']
    r['plan']=p;r['phase']='author_draft';r['phase_start_counter']=now();save_timing(data)


def preflight(pairs_path):
    """One author-side lexical scan before submitting a complete candidate.

    No candidate journal, attempts, introductions or exposure credit is created.
    Diagnostics may drive prose repair; the eventual gate remains unchanged.
    """
    guard();data=read(TIMING);r=data['texts'][-1];gate=ProductionGate()
    if r.get('lexical_preflight'):raise StructuralStop('Initial draft preflight already recorded')
    if r['phase']!='author_draft':raise StructuralStop('Preflight only before initial candidate submission')
    from k1_phase3_8_analysis import analyze
    from k1_phase3_9_gate import permission_issues
    from k1_phase3 import vocab
    snapshot=gate.snapshot(r['text_number']);f=deepcopy(gate.f);v=vocab(f)
    f['_allowed_vocab']=[v[e['vocab_id']] for e in snapshot['entries']]
    ledger_before=hashlib.sha256(gate.ledger.read_bytes()).hexdigest();start=now();findings=[]
    pairs=read(pairs_path)
    selfcheck=read(pairs_path.with_name(pairs_path.stem+'-selfcheck.json'))
    required=('allowed_contract_read','content_membership_checked','title_checked','planned_new_checked','known_gaps_checked','references_checked')
    if not all(selfcheck.get(k) is True for k in required):raise StructuralStop('Author self-check missing')
    write(PILOT/'selfchecks'/f"K1-{r['text_number']:03d}.json",selfcheck)
    used=set()
    for index,pair in enumerate(pairs,1):
        a=analyze(pair[0],f,r['text_number'],intents=r['plan'].get('generated_intents',[]),scene_actions=r['plan']['scene_fingerprint']['main_actions'],kiwi=gate.kiwi,scope='author_lexical_preflight')
        from k1_phase3_8_sense import sense_checks
        used.update(x['vocab_id'] for x in a['annotations'] if x['vocab_id'])
        findings += [dict(sentence=index,reason='explicit_restricted_sense_violation',**x) for x in sense_checks(pair[0],a) if x['decision']=='FAIL']
        findings+= [dict(sentence=index,**x) for x in permission_issues(a,snapshot,f)]
    title=analyze(r['plan']['title_ko'],f,r['text_number'],kiwi=gate.kiwi,scope='title')
    findings += [dict(scope='title',**x) for x in permission_issues(title,snapshot,f)]
    findings += [dict(reason='planned_new_not_present',vocab_id=i) for i in snapshot['planned_new_vocab_ids'] if i not in used]
    from k1_phase3_9_planner import author_findings
    findings += author_findings(' '.join(p[0] for p in pairs),r['plan'].get('pack_intended',False))
    elapsed=now()-start
    if ledger_before!=hashlib.sha256(gate.ledger.read_bytes()).hexdigest():raise StructuralStop('Preflight changed actual state')
    r['preflight_seconds']=elapsed;r['stages']['lexical_preflight']=elapsed
    r['lexical_preflight']=dict(findings=findings,future_count=sum(x['reason']=='future_expansion' for x in findings),ledger_unchanged=True)
    if findings:
        r['stages']['author_draft']=max(0,now()-r['phase_start_counter']-elapsed)
        r['phase']='preflight_repair';r['phase_start_counter']=now()
    write(PILOT/'preflights'/f"K1-{r['text_number']:03d}.json",r['lexical_preflight']);save_timing(data)
    print(json.dumps(r['lexical_preflight'],ensure_ascii=False))


def validate(pairs_path):
    guard();data=read(TIMING);r=data['texts'][-1];gate=ProductionGate()
    if read(gate.control)['status']!='running':raise StructuralStop('Stopped run')
    if r['phase'] not in ('author_draft','preflight_repair','retry_repair'):raise StructuralStop('Wrong draft state')
    if not r.get('lexical_preflight'):raise StructuralStop('Author lexical preflight required before candidate submission')
    draft_sec=now()-r['phase_start_counter'];stage=r['phase']
    if stage=='author_draft':draft_sec=max(0,draft_sec-r.get('preflight_seconds',0))
    r['stages'][stage]=r['stages'].get(stage,0)+draft_sec
    pairs=read(pairs_path);plan=deepcopy(r['plan'])
    plan.update(sentences=[p[0] for p in pairs],translations_ja=[p[1] for p in pairs],
        semantic_evidence={k:dict(verdict='YES',reason='Provisional author checks during draft; explicit post-mechanical review is still required.') for k in __import__('k1_naturalness_lint').CHECKS},
        notes='Fresh Phase 3.9 sequential author draft, produced after an actual allowed snapshot. Semantic grammar roles are warnings only.')
    number=len(r['attempts'])+1
    write(PILOT/'sources'/f"K1-{r['text_number']:03d}-attempt-{number:02d}.json",plan)
    start=now();candidate,result=gate.submit(plan);elapsed=now()-start
    cpu=Counter()
    for m in gate.measurements:cpu[m['stage']]+=m['seconds']
    r['stages']['morphology_vocab_analysis']=r['stages'].get('morphology_vocab_analysis',0)+cpu['morphology_vocab_analysis']
    r['stages']['mechanical_validation']=r['stages'].get('mechanical_validation',0)+elapsed-cpu['morphology_vocab_analysis']
    a=dict(attempt=number,candidate=str(candidate.relative_to(ROOT)),hard_pass=result['hard_pass'],hard_errors=result['hard_errors'],
           author_seconds=draft_sec,validation_seconds=elapsed,stage_cpu_seconds=dict(cpu),
           future_usage_count=sum(x['reason']=='future_expansion' for x in result.get('invalid_usage_ids',[])))
    r['attempts'].append(a);r['candidate']=a['candidate'];r['phase']='naturalness_review' if result['hard_pass'] else 'retry_repair';r['phase_start_counter']=now()
    if read(gate.control)['status']=='stopped':
        data['stop']=read(gate.control)['stop'];data['production_end_counter']=now();data['production_end_utc']=utc();r.update(end_counter=data['production_end_counter'],total_seconds=data['production_end_counter']-r['start_counter'],phase='stopped')
    save_timing(data)
    print(json.dumps(dict(hard_pass=result['hard_pass'],hard_errors=result['hard_errors'],coverage=result.get('coverage'),eojeol=result.get('eojeol_count'),
        semantic_warnings=len(result.get('semantic_grammar_warnings',[])),naturalness=result.get('naturalness'),
        review=result.get('actual_review_vocab_ids'),incidental=result.get('incidental_previous_vocab_ids'),control=read(gate.control)),ensure_ascii=False))


def commit(review_path):
    guard();data=read(TIMING);r=data['texts'][-1]
    if r['phase']!='naturalness_review':raise StructuralStop('No candidate pending author review')
    r['stages']['naturalness_review']=r['stages'].get('naturalness_review',0)+now()-r['phase_start_counter']
    gate=ProductionGate();path=ROOT/r['candidate'];evidence=read(review_path)
    r.setdefault('author_review_history',[]).append(dict(attempt=len(r['attempts']),evidence=evidence))
    if not gate.approve(path,evidence):
        r['phase']='retry_repair';r['phase_start_counter']=now();save_timing(data);return
    start=now();record=gate.commit(path);elapsed=now()-start
    # Final evaluate consumes analysis/check timings; publication/recovery is the remaining transaction time.
    final=sum(m['seconds'] for m in gate.measurements)
    # Include measured pure evaluate overhead in final reanalysis; commit timer is explicitly taken around it below.
    r['stages']['final_reanalysis']=gate.final_reanalysis_seconds
    r['stages']['commit']=max(0,elapsed-gate.final_reanalysis_seconds)
    r['end_counter']=now();r['total_seconds']=r['end_counter']-r['start_counter'];r['committed']=True;r['phase']='committed'
    r['coverage']=record['coverage'];r['eojeol_count']=record['eojeol_count'];r['review_evidence']=evidence
    r['stages']['controller_overhead']=max(0,r['total_seconds']-sum(r['stages'].values()))
    if r['text_number']==100:
        data['completed']=True;data['production_end_counter']=now();data['production_end_utc']=utc()
    save_timing(data)
    after=gate.load()
    from k1_phase3_9_planner import health
    ids=set(record['actual_new_vocab_ids']+record['actual_review_vocab_ids']+record['incidental_previous_vocab_ids'])
    r['effective_review_credit']=len(ids)
    r['actual_previous_review_credit']=len(ids-set(record['actual_new_vocab_ids']))
    r['health_after']=health(after,r['text_number']);save_timing(data)
    gaps=record['naturalness']['natural_expression_gaps']
    if gaps:
        gap_path=ROOT/'reports/natural_expression_gaps.json'
        old=read(gap_path) if gap_path.exists() else dict(entries=[])
        if not isinstance(old,dict) or not isinstance(old.get('entries'),list):raise StructuralStop('Unknown gap history format')
        for x in gaps:
            event=dict(phase='3.9',text=r['text_number'],**x)
            if event not in old['entries']:old['entries'].append(event)
        atomic_write(gap_path,old)
    print(json.dumps(dict(text=r['text_number'],committed=True,total_seconds=r['total_seconds'],epoch=after['epoch'],effective_review_credit=len(ids),health=r['health_after']),ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['begin','plan','preflight','validate','commit']);parser.add_argument('argument')
    args=parser.parse_args()
    try:
        globals()[args.action](int(args.argument) if args.action=='begin' else Path(args.argument))
    except Exception as exc:
        if TIMING.exists():
            d=read(TIMING)
            if not d.get('production_end_counter'):
                end=now()
                if d['texts']:
                    r=d['texts'][-1]
                    if not r.get('end_counter'):
                        r['stages'][r['phase']]=r['stages'].get(r['phase'],0)+end-r['phase_start_counter']
                        r.update(end_counter=end,total_seconds=end-r['start_counter'],phase='stopped')
                d.update(production_end_counter=end,production_end_utc=utc(),stop=dict(type='structural_exception',reason=str(exc)))
                save_timing(d)
        raise
