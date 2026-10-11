"""Candidate gate: pure draft evaluation, bounded retries, atomic actual commit.

The authoritative ledger embeds committed records. One atomic file replacement
publishes record/history/exposures together. texts/ is a recoverable projection.
Candidate journals/snapshots never count as learner exposure or genre history.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import os
import re
import uuid
import time
from contextlib import contextmanager
from k1_phase3 import files as official_files,read,write,metrics,actual_coverage_files,vocab
from k1_phase3 import ROOT
from jsonschema import Draft202012Validator
from k1_phase2_3 import make_kiwi
from k1_review_scheduler import ReviewScheduler
from k1_naturalness_lint import lint,semantic_review,translation_lint,CHECKS
from k1_phase3_6a_resolver import analyze,HINTS,OVERLAY,focused_scope_parity
from k1_grammar_semantic_gate import checks as semantic_checks, REGISTRY
from lexical_coverage import evaluate_lexical_tokens
from validate_k1_pilot import token_stream

class StructuralStop(RuntimeError):pass

def construction_errors(text,scope):
    # Explicit forms only. Semantic roles of allowed particles never enter here.
    patterns = (r'지\s*않', r'고\s*싶어(?:하|해|했|할)', r'(?:로서|으로써)')
    return [dict(code='unapproved_construction',detail=dict(scope=scope,surface=m.group(),start=m.start()))
            for pattern in patterns for m in re.finditer(pattern,text)]


def digest(obj):return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
def seal(state):
    result=deepcopy(state);result.pop('state_checksum',None);result['state_checksum']=digest(result);return result

def atomic_write(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        with tmp.open('w',encoding='utf-8',newline='\n') as stream:
            stream.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');stream.flush();os.fsync(stream.fileno())
        os.replace(tmp,path)
    finally:
        if tmp.exists():tmp.unlink()

@contextmanager
def writer_lock(ledger):
    """OS advisory lock released automatically on process death, same volume."""
    lockpath=Path(str(ledger)+'.lock');lockpath.parent.mkdir(parents=True,exist_ok=True)
    with lockpath.open('a+b') as stream:
        if stream.seek(0,2)==0:stream.write(b'0');stream.flush()
        stream.seek(0)
        try:
            if os.name=='nt':
                import msvcrt
                msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as exc:raise StructuralStop('Concurrent run writer refused') from exc
        try:yield
        finally:
            stream.seek(0)
            if os.name=='nt':msvcrt.locking(stream.fileno(),msvcrt.LK_UNLCK,1)
            else:fcntl.flock(stream.fileno(),fcntl.LOCK_UN)

def input_digest(f):
    engine={name:hashlib.sha256((ROOT/'scripts'/name).read_bytes()).hexdigest() for name in
        ('k1_phase3_2_analysis.py','k1_phase3_2_resolver.py','k1_phase3_2_gate.py','k1_phase3_3_resolver.py','k1_phase3_3_gate.py','k1_phase3_3.py','k1_phase3_sequential_v3_gate.py','k1_phase3_sequential_v3.py','k1_phase3_4_resolver.py','k1_phase3_4_gate.py','k1_phase3_4.py','build_k1_phase3_4_schemas.py','k1_phase3_6a_gate.py','k1_phase3_6a_resolver.py','k1_phase3_6a.py','report_k1_phase3_6a.py','k1_grammar_semantic_gate.py')}
    return digest(dict(production_policy=read(ROOT/'config/languages/ko/k1/production_lite_policy.json'),grammar_semantics=read(REGISTRY),inputs={n:f[n] for n in f if not n.startswith('_')},morphology_hints=read(HINTS),uri_context_overlay=read(OVERLAY),schemas={n:read(ROOT/'config/languages/ko/k1/phase3_4'/n) for n in ('source.schema.json','candidate.schema.json')},engine=engine))

def scheduler(f,state):
    s=ReviewScheduler(f['vocab_review_windows.json'])
    for r in state['committed_records']:
        s.record(r['text_number'],r['actual_new_vocab_ids']+r['actual_review_vocab_ids']+r['incidental_previous_vocab_ids'])
    return s

def build_snapshot(f,state,text):
    v=vocab(f);rows=f['introduction_schedule.json']['rows'];windows=f['vocab_review_windows.json']['entries']
    if (len(f['core_vocab.json']),len(f['expansion_vocab.json']),len(v),len(f['grammar.json']))!=(300,500,800,32):raise StructuralStop('Invalid frozen input cardinality')
    if Counter(e['tier'] for e in f['expansion_vocab.json'])!=Counter(E1=200,E2=200,E3=100):raise StructuralStop('Invalid tier cardinality')
    if len({(e['lemma'],e['pos'],e['sense']) for e in v.values()})!=800:raise StructuralStop('Frozen identity collision')
    first={i:r['text'] for r in rows for i in r['entry_ids']}
    if len(first)!=500 or set(first)!={e['id'] for e in f['expansion_vocab.json']}:raise StructuralStop('Incomplete introduction plan')
    if any(w['first_introduction_text']!=first[w['vocab_id']] for w in windows):raise StructuralStop('Introduction/window contradiction')
    new=next(r['entry_ids'] for r in rows if r['text']==text)
    if len(new)>2 or len({v[i]['lemma'] for i in new})>2:raise StructuralStop('Planned new lemma count exceeds 2')
    actual={e['vocab_id'] for e in state['entries'] if e['actual_first_text'] is not None and e['actual_first_text']<text}
    hints={e['vocab_id']:e for e in read(HINTS)['entries']}
    permitted=[]
    for e in f['core_vocab.json']+f['expansion_vocab.json']:
        role='core' if e['tier']=='core' else 'current_new_expansion' if e['id'] in new else 'previous_expansion' if e['id'] in actual else None
        if not role:continue
        hint=hints.get(e['id'])
        if hint and (hint['lemma'],hint['pos'],hint['sense'])!=(e['lemma'],e['pos'],e['sense']):raise StructuralStop('Morphology hint identity mismatch')
        permitted.append(dict(vocab_id=e['id'],lemma=e['lemma'],pos=e['pos'],sense=e['sense'],tier=e['tier'],role=role,
            allowed_inflections=e['allow_inflection'],forms=e['forms'],morphology_hints=hint or dict(
                morphology_class='registered_hada_compound' if e['lemma'].endswith('하다') else 'registered_lemma',
                policy='No productive synonym/directional alias. Only registered meaning and grammar32; forms are not an exhaustive conjugation dictionary.')))
    return dict(text_number=text,state_checksum=state['state_checksum'],input_digest=input_digest(f),
        planned_new_vocab_ids=sorted(new),entries=permitted,
        allowed_proper_names=[dict(vocab_id='proper:'+e['lemma'],lemma=e['lemma'],pos='noun',sense=e['kind'],tier=None,role='proper_name',allowed_inflections=False) for e in f['proper_names.json']['entries']],
        lexical_exceptions=[dict(vocab_id=e['id'],lemma=e['form'],pos='interjection',sense='fixed_expression',tier=None,role='frozen_exception',allowed_inflections=False,kind=e['kind']) for e in f['lexical_exceptions.json']['entries'] if e['kind']=='frozen_exception'],
        policy=dict(only_actual_previous=True,grammar_count=32,new_lemma_max=2,controlled_hard=1.0,previous_hard=.98,
                    draft_target_eojeol=[130,150],hard_length=[120,180],hard_sentence_max=10,no_filler_padding=True))

def permission_issues(a,snapshot,f,intents=()):
    allowed={e['vocab_id'] for e in snapshot['entries']};v=vocab(f)
    first={i:r['text'] for r in f['introduction_schedule.json']['rows'] for i in r['entry_ids']}
    retired=set(f['id_migration.json']['retired_ids']);invalid=[]
    for x in a['annotations']:
        i=x['vocab_id']
        if i and i not in allowed:
            reason='retired_id_or_sense' if i in retired else 'future_expansion' if first.get(i,999)>snapshot['text_number'] else 'unconfirmed_previous_expansion'
            invalid.append(dict(vocab_id=i,lemma=x['lemma'],surface=x['surface'],start=x['start'],reason=reason))
        elif x['role']=='unresolved':invalid.append(dict(vocab_id=None,lemma=x['lemma'],surface=x['surface'],start=x['start'],reason='unknown_or_unresolved'))
        elif i and (x['lemma'],x['pos'],x['sense'])!=(v[i]['lemma'],v[i]['pos'],v[i]['sense']):invalid.append(dict(vocab_id=i,lemma=x['lemma'],reason='identity_mismatch'))
    for x in intents:
        i=x.get('vocab_id');e=v.get(i)
        if i in retired:invalid.append(dict(vocab_id=i,lemma=x.get('lemma'),reason='retired_id_or_sense'))
        elif not e or any(x.get(k)!=e[k] for k in ('lemma','pos','sense')):invalid.append(dict(vocab_id=i,lemma=x.get('lemma'),reason='unregistered_intended_identity'))
        elif i not in allowed:invalid.append(dict(vocab_id=i,lemma=x.get('lemma'),reason='future_expansion' if first.get(i,999)>snapshot['text_number'] else 'unconfirmed_previous_expansion'))
    return invalid

class CandidateGate:
    def __init__(self,run_dir,ledger_path,f=None,kiwi=None,max_attempts=5,max_text=50):
        self.path=Path(run_dir);self.ledger=Path(ledger_path);self.f=deepcopy(f or official_files())
        self.kiwi=kiwi or make_kiwi();self.max_attempts=max_attempts;self.max_text=max_text
        self.control=self.path/'run_control.json'
        self.measurements=[]
        if not 1<=max_attempts<=5 or not 1<=max_text<=50:raise ValueError('Retry/run bounds invalid')

    def initialize(self):
        if self.ledger.exists() or self.control.exists():raise StructuralStop('Cannot reset an existing run')
        entries=[dict(vocab_id=e['id'],lemma=e['lemma'],first_planned_text=next(r['text'] for r in self.f['introduction_schedule.json']['rows'] if e['id'] in r['entry_ids']),
            actual_first_text=None,actual_texts=[],actual_exposure_count=0,incidental_exposure_count=0,selected_review_exposure_count=0,
            last_exposure_text=None,paid_review_windows={},active_window=[],outstanding_debt=[],deadline_status='not_introduced') for e in self.f['expansion_vocab.json']]
        state=seal(dict(phase='3.6a',epoch=0,last_committed_text=0,input_digest=input_digest(self.f),committed_records=[],entries=entries,
            genre_history=[],scene_history=[],review_debt=[],expired_review_debt=[]))
        build_snapshot(self.f,state,1)
        with writer_lock(self.ledger):
            if self.ledger.exists():raise StructuralStop('Concurrent initialization refused')
            atomic_write(self.ledger,state)
            write(self.path/'initial_state.json',state)
            atomic_write(self.control,dict(status='running',max_attempts=self.max_attempts,max_text=self.max_text,stop=None))

    def load(self):
        state=read(self.ledger);copy=deepcopy(state);checksum=copy.pop('state_checksum',None)
        if checksum!=digest(copy) or state['input_digest']!=input_digest(self.f):raise StructuralStop('State checksum/input corruption')
        if state['last_committed_text']!=len(state['committed_records']) or state['epoch']!=len(state['committed_records']) or [r['text_number'] for r in state['committed_records']]!=list(range(1,state['last_committed_text']+1)):raise StructuralStop('Noncontiguous committed history')
        if state['genre_history']!=[dict(text=r['text_number'],genre=r['genre']) for r in state['committed_records']]:raise StructuralStop('Genre history corruption')
        if state['scene_history']!=[dict(text=r['text_number'],scene_fingerprint=r['scene_fingerprint']) for r in state['committed_records']]:raise StructuralStop('Scene history corruption')
        s=scheduler(self.f,state)
        if len(state['entries'])!=500 or {e['vocab_id'] for e in state['entries']}!=set(s.entries):raise StructuralStop('State vocabulary corruption')
        for e in state['entries']:
            i=e['vocab_id'];xs=sorted(s.actual[i])
            if xs!=e['actual_texts'] or len(xs)!=e['actual_exposure_count'] or e['actual_first_text']!=(min(xs) if xs else None):raise StructuralStop('Exposure state corruption')
            if e['paid_review_windows']!={str(k):value for k,value in s.credits[i].items()}:raise StructuralStop('Debt payment corruption')
        return state

    def snapshot(self,text):
        state=self.load()
        if text!=state['last_committed_text']+1 or text>self.max_text:raise StructuralStop('Wrong next text or smoke boundary')
        snap=build_snapshot(self.f,state,text)
        write(self.path/'allowed_vocab_snapshots'/f'K1-{text:03d}-epoch-{state["epoch"]}.json',snap)
        return snap

    def measured(self,stage,fn,*args,**kwargs):
        start=time.perf_counter()
        try:return fn(*args,**kwargs)
        finally:self.measurements.append(dict(stage=stage,seconds=time.perf_counter()-start))

    def evaluate(self,source,state,snapshot):
        """Pure: no files/state writes. Sentence prechecks omit global N/U/length."""
        t=source['text_number'];s=scheduler(self.f,state);v=vocab(self.f)
        allowed={e['vocab_id'] for e in snapshot['entries']}
        f=deepcopy(self.f);f['_allowed_vocab']=[v[i] for i in allowed]
        actions=source['scene_fingerprint']['main_actions'];intents=source.get('generated_intents',[])
        approved=[]
        for lemma in source.get('review_candidates',[]):
            approved += [e['id'] for e in self.f['expansion_vocab.json'] if e['lemma']==lemma and e['id'] in allowed]
        selection=s.select(t,source['scene'],approved_ids=approved,desired=8)
        selected=[r['vocab_id'] for r in selection['selected_reviews']]
        text='\n\n'.join(' '.join(source['sentences'][i:i+6]) for i in range(0,len(source['sentences']),6))
        prechecks=[];sentence_results=[]
        for n,sentence in enumerate(source['sentences'],1):
            a=self.measured('morphology_vocab_analysis',analyze,sentence,f,t,selected,intents,actions,self.kiwi,scope='sentence_precheck')
            sentence_results.append(a)
            issues=permission_issues(a,snapshot,f)
            prechecks.append(dict(sentence=n,passed=not issues and not any(d.get('requires_candidate_review') for d in a['resolver_decisions']),invalid_usage_ids=issues,resolver_decisions=a['resolver_decisions']))
        a=self.measured('morphology_vocab_analysis',analyze,text,f,t,selected,intents,actions,self.kiwi,scope='full_candidate')
        invalid=permission_issues(a,snapshot,f,intents)
        for annotation in a['annotations']:
            if annotation['vocab_id'] and annotation['vocab_id'] not in allowed:annotation['role']='invalid_usage'
        errors=[dict(code=x['reason'],detail=x) for x in invalid]
        scope_checks=self.measured('morphology_vocab_analysis',focused_scope_parity,text,a,source['sentences'],sentence_results,f,t,snapshot['planned_new_vocab_ids'],selected,intents,actions,self.kiwi)
        errors += [dict(code='scope_identity_mismatch',detail=x) for x in scope_checks if x['structural_defect']]
        # Same original clause, valid in isolation but unresolved in full scope:
        # record a structural defect, not permission to silently replace identity.
        for x in invalid:
            if x['reason']!='unknown_or_unresolved':continue
            cursor=0
            for n,sentence in enumerate(source['sentences']):
                begin=text.find(sentence,cursor);cursor=begin+len(sentence)
                if begin<=x.get('start',-1)<cursor and prechecks[n]['passed']:
                    errors.append(dict(code='structural_analyzer_defect',detail=dict(usage=x,sentence=sentence,isolated_pass=True)))

        for d in a['resolver_decisions']:
            if d.get('requires_candidate_review'):errors.append(dict(code='unresolved_context_ambiguity',detail=d))
        used={x['vocab_id'] for x in a['annotations'] if x['vocab_id']};new=set(snapshot['planned_new_vocab_ids'])
        previous={e['vocab_id'] for e in snapshot['entries'] if e['role']=='previous_expansion'}
        actual_new=sorted(used&new);actual_review=sorted(used&set(selected)&previous)
        incidental=sorted((used&previous)-set(selected))
        if actual_new!=sorted(new):errors.append(dict(code='planned_new_not_present',detail=sorted(new-used)))
        m=metrics(text)
        if not 120<=m['eojeol_count']<=180:errors.append(dict(code='length',detail=m['eojeol_count']))
        if m['max_sentence_eojeol']>10:errors.append(dict(code='sentence_hard_max',detail=m['max_sentence_eojeol']))
        cov=evaluate_lexical_tokens(token_stream(a['annotations']),t,actual_coverage_files(f,s,t,new))
        errors += [dict(code='coverage_or_token_policy',detail=e) for e in cov['errors']]
        if len({v[i]['lemma'] for i in actual_new})>2:errors.append(dict(code='new_lemma_limit',detail=actual_new))
        grammar_allowed={g['id'] for g in self.f['grammar.json']}
        if set(a['grammar_used'])-grammar_allowed:errors.append(dict(code='grammar32',detail=sorted(set(a['grammar_used'])-grammar_allowed)))
        title=self.measured('morphology_vocab_analysis',analyze,source['title_ko'],f,t,selected,intents,actions,self.kiwi,scope='title')
        if permission_issues(title,snapshot,f):errors.append(dict(code='title_permission',detail=permission_issues(title,snapshot,f)))
        grammar_checks=self.measured('semantic_diagnostics',semantic_checks,text,a,'body')+self.measured('semantic_diagnostics',semantic_checks,source['title_ko'],title,'title')
        # Semantic role classifications are diagnostics only under Phase 3.6.
        for scope, content in [('body',text),('title',source['title_ko'])]:
            errors += construction_errors(content,scope)
        pairs=list(zip(source['sentences'],source['translations_ja']))
        if len(source['sentences'])!=len(source['translations_ja']):errors.append(dict(code='translation_alignment',detail='sentence count'))
        # Human semantic approval is not claimed. Explicit NO prevents commit.
        review=semantic_review(source['semantic_evidence'])
        if any(x['verdict']=='NO' for x in review['checks'].values()):errors.append(dict(code='semantic_repair_required',detail=review['flags']))
        lintwarnings=lint(text,a['annotations'],set(f['id_migration.json']['retired_ids']))
        return dict(id=f'K1-{t:03d}',text_number=t,title_ko=source['title_ko'],genre=source['genre'],scene=source['scene'],
            text_ko=text,translation_ja='\n\n'.join(' '.join(source['translations_ja'][i:i+6]) for i in range(0,len(source['translations_ja']),6)),
            planned_new_vocab_ids=sorted(new),actual_new_vocab_ids=actual_new,selected_review_vocab_ids=selected,
            actual_review_vocab_ids=actual_review,incidental_previous_vocab_ids=incidental,invalid_usage_ids=invalid,
            **m,
            coverage=dict(denominator_N=cov['N'],new_tokens_U=cov['U'],controlled_vocab_coverage=cov['controlled_vocab_coverage'],previous_vocab_coverage=cov['previous_vocab_coverage'],target_99_met=cov['previous_vocab_coverage'] is not None and cov['previous_vocab_coverage']>=.99),
            scope_identity_checks=scope_checks,semantic_grammar_checks=grammar_checks,semantic_grammar_warnings=[c for c in grammar_checks if c['decision']!='PASS'],hard_errors=errors,hard_pass=not errors,token_soft_warnings=cov['warnings'],
            naturalness=dict(lint_warnings=lintwarnings,semantic_review=review,natural_expression_gaps=source.get('natural_expression_gaps',[])),
            scene_fingerprint=source['scene_fingerprint'],sentence_prechecks=prechecks,
            translation_pairs=[dict(ko=k,ja=j) for k,j in pairs],translation_fidelity_flags=translation_lint(pairs),
            source=deepcopy(source),snapshot_digest=digest(snapshot),state_checksum_before=state['state_checksum'],**a)

    def reject_run(self,reason):atomic_write(self.control,dict(read(self.control),status='stopped',stop=reason))

    def submit(self,source):
        with writer_lock(self.ledger):return self._submit_locked(source)

    def _submit_locked(self,source):
        control=read(self.control)
        if control['status']!='running':raise StructuralStop('Run no longer accepts candidates')
        try:
            state=self.load();before_hash=hashlib.sha256(self.ledger.read_bytes()).hexdigest();t=source.get('text_number',state['last_committed_text']+1);snapshot=self.snapshot(t)
            attempts=sorted((self.path/'candidates').glob(f'K1-{t:03d}-attempt-*.json'))
            number=len(attempts)+1
            if number>self.max_attempts:raise StructuralStop('Attempt budget exhausted')
            format_errors=list(Draft202012Validator(read(ROOT/'config/languages/ko/k1/phase3_4/source.schema.json')).iter_errors(source))
            result=self.evaluate(source,state,snapshot) if not format_errors else dict(id=f'K1-{t:03d}',text_number=t,
                hard_pass=False,hard_errors=[dict(code='candidate_format',detail=e.message) for e in format_errors],
                source=deepcopy(source),state_checksum_before=state['state_checksum'],snapshot_digest=digest(snapshot))
            after_hash=hashlib.sha256(self.ledger.read_bytes()).hexdigest()
            if before_hash!=after_hash:raise StructuralStop('Candidate evaluation changed authoritative state')
        except Exception as exc:
            self.reject_run(dict(type='structural_failure',reason=str(exc)))
            raise StructuralStop(str(exc)) from exc
        result['attempt_number']=number;result['candidate_status']='PASS_PENDING_COMMIT' if result['hard_pass'] else 'REJECTED'
        result['ledger_sha_before_evaluation']=before_hash;result['ledger_sha_after_evaluation']=after_hash
        result['candidate_digest']=digest(result)
        schema_errors=list(Draft202012Validator(read(ROOT/'config/languages/ko/k1/phase3_4/candidate.schema.json')).iter_errors(result))
        if schema_errors:
            self.reject_run(dict(type='candidate_schema_contract_failure',text=t,errors=[e.message for e in schema_errors]))
            raise StructuralStop('Candidate output violates run schema')
        target=self.path/'candidates'/f'K1-{t:03d}-attempt-{number:02d}.json'
        if target.exists():raise StructuralStop('Candidate journal collision')
        write(target,result)
        if not result['hard_pass']:
            write(self.path/'failed_attempts'/target.name,result)
            if number==self.max_attempts:self.reject_run(dict(type='candidate_retries_exhausted',text=t,attempts=number,errors=result['hard_errors']))
        return target,result

    def commit(self,candidate_path,fault_at=None):
        try:
            with writer_lock(self.ledger):return self._commit_locked(candidate_path,fault_at)
        except StructuralStop as exc:
            self.reject_run(dict(type='structural_commit_failure',reason=str(exc)))
            raise

    def _commit_locked(self,candidate_path,fault_at=None):
        candidate=read(candidate_path);check=deepcopy(candidate);expected=check.pop('candidate_digest')
        if digest(check)!=expected:raise StructuralStop('Candidate artifact tampered')
        if not candidate['hard_pass']:raise StructuralStop('Rejected candidate cannot commit')
        state=self.load();t=candidate['text_number'];commit_id=expected
        existing=next((r for r in state['committed_records'] if r['text_number']==t),None)
        if existing:
            if existing['commit_id']!=commit_id:raise StructuralStop('Different committed body at this text')
            self._recover_locked();return existing
        if read(self.control)['status']!='running':raise StructuralStop('Stopped run cannot commit')
        if state['state_checksum']!=candidate['state_checksum_before']:raise StructuralStop('Stale candidate state')
        snapshot=build_snapshot(self.f,state,t)
        if digest(snapshot)!=candidate['snapshot_digest']:raise StructuralStop('Stale allowed snapshot')
        # Final raw reanalysis, permission and coverage before atomic commit.
        final_start=time.perf_counter()
        final=self.evaluate(candidate['source'],state,snapshot)
        self.final_reanalysis_seconds=time.perf_counter()-final_start
        if not final['hard_pass'] or any(final[k]!=candidate[k] for k in ('text_ko','annotations','raw_morphology','coverage','grammar_used','invalid_usage_ids','semantic_grammar_checks','scope_identity_checks')):
            self.reject_run(dict(type='final_reanalysis_failed',text=t));raise StructuralStop('Final reanalysis failed')
        final.update(commit_id=commit_id,committed=True,attempt_number=candidate['attempt_number'],final_reanalysis_pass=True)
        next_state=deepcopy(state);next_state['committed_records'].append(final);next_state['last_committed_text']=t;next_state['epoch']+=1
        next_state['genre_history'].append(dict(text=t,genre=final['genre']))
        next_state['scene_history'].append(dict(text=t,scene_fingerprint=final['scene_fingerprint']))
        s=scheduler(self.f,next_state);debt=[]
        for e in next_state['entries']:
            i=e['vocab_id'];xs=sorted(s.actual[i]);windows=s.entries[i]['review_windows']
            ds=[dict(vocab_id=i,window_index=n,window=w) for n,w in enumerate(windows) if n not in s.credits[i] and w['from']<=t and xs]
            e.update(actual_first_text=min(xs) if xs else None,actual_texts=xs,actual_exposure_count=len(xs),last_exposure_text=max(xs) if xs else None,
                incidental_exposure_count=sum(i in r['incidental_previous_vocab_ids'] for r in next_state['committed_records']),
                selected_review_exposure_count=sum(i in r['actual_review_vocab_ids'] for r in next_state['committed_records']),
                paid_review_windows={str(k):value for k,value in s.credits[i].items()},active_window=[d['window'] for d in ds],outstanding_debt=ds,
                deadline_status='expired' if any(d['window']['to']<t for d in ds) else 'open' if ds else 'not_open_or_paid' if xs else 'not_introduced')
            debt+=ds
            if xs and max(0,6-len(xs))>300-t:raise StructuralStop('Review distinct-text quota mathematically infeasible')
        next_state['review_debt']=debt;next_state['expired_review_debt']=[d for d in debt if d['window']['to']<t]
        next_state=seal(next_state)
        if fault_at=='before_publish':raise OSError('Injected crash before authoritative atomic publish')
        atomic_write(self.ledger,next_state)
        if fault_at=='after_publish':raise OSError('Injected crash after publish, before materialized text projection')
        self._recover_locked()
        return final

    def recover(self):
        """Idempotent projection; never repeats introduction/exposure/debt credit."""
        with writer_lock(self.ledger):return self._recover_locked()

    def _recover_locked(self):
        state=self.load()
        for r in state['committed_records']:atomic_write(self.path/'texts'/f"K1-{r['text_number']:03d}.json",r)
        if state['last_committed_text']==self.max_text:atomic_write(self.control,dict(read(self.control),status='completed',stop=None))

    def run_one(self,text,generator):
        """Callback gets allowed snapshot + prior attempt diagnostics, not seeds."""
        feedback=None
        for attempt in range(1,self.max_attempts+1):
            try:
                snap=self.snapshot(text)
                source=generator(snap,feedback,attempt)
                path,result=self.submit(source)
                if result['hard_pass']:return self.commit(path)
            except Exception as exc:
                self.reject_run(dict(type='structural_failure',reason=str(exc)))
                raise StructuralStop(str(exc)) from exc
            feedback=deepcopy(result)
        return None
