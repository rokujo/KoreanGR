"""Approved 3.3 engine, new actual sequential run, never beyond K1-050."""
import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import statistics
from k1_phase3_sequential_v3_gate import CandidateGate, StructuralStop, read, write, ROOT, scheduler
from k1_phase3_retry import stagnant_errors
from k1_phase3 import sha

PILOT = ROOT/'pilot/ko/k1/phase3_sequential_v3'
LEDGER = ROOT/'state/phase3_sequential_v3_001_050_exposure_ledger.json'
REPORTS = ROOT/'reports'
FREEZE = REPORTS/'k1_phase3_sequential_v3_input_freeze.json'

def freeze():
    if FREEZE.exists(): return
    manifest = read(REPORTS/'k1_phase3_3_artifact_manifest.json')
    previous = read(REPORTS/'k1_phase3_3_input_freeze.json')
    expected = dict(previous['files'], **manifest['files'])
    invalid = [p for p,h in expected.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    if invalid: raise StructuralStop('Approved freeze mismatch: '+str(invalid))
    paths = set(expected) | {'reports/k1_phase3_3_artifact_manifest.json','reports/k1_phase3_3_input_freeze.json'}
    paths |= {p.relative_to(ROOT).as_posix() for p in (ROOT/'config/languages/ko/k1').rglob('*.json')}
    paths |= {'scripts/k1_phase3_sequential_v3_gate.py', 'scripts/k1_phase3_sequential_v3.py',
              'pilot/ko/k1/phase3_sequential_v3/source.schema.json',
              'pilot/ko/k1/phase3_sequential_v3/candidate.schema.json'}
    write(FREEZE,dict(run='phase3_sequential_v3',files={p:sha(ROOT/p) for p in sorted(paths)}))

def freeze_errors():
    return [p for p,h in read(FREEZE)['files'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]

def similarity(a,b):
    parts=[]
    for key in ('goal','setting','participants','problem_type','resolution_type','main_actions'):
        x,y=a[key],b[key]
        if isinstance(x,list):
            parts.append(len(set(x)&set(y))/len(set(x)|set(y)) if x or y else 1)
        else: parts.append(int(x==y))
    return sum(parts)/len(parts)

class SequentialGate(CandidateGate):
    def __init__(self,run_dir=PILOT,ledger_path=LEDGER,**kwargs):
        super().__init__(run_dir,ledger_path,max_attempts=kwargs.pop('max_attempts',5),max_text=50,**kwargs)

    def _submit_locked(self,source):
        path,result=super()._submit_locked(source)
        if not result['hard_pass'] and result['attempt_number']>=2:
            previous=read(path.with_name(f"K1-{result['text_number']:03d}-attempt-{result['attempt_number']-1:02d}.json"))
            stagnant=stagnant_errors(previous,result)
            if stagnant:
                self.reject_run(dict(type='same_hard_error_twice_without_improvement',text=result['text_number'],
                                     attempt=result['attempt_number'],errors=stagnant))
        return path,result

    def run_one(self,text,generator):
        paths=sorted((self.path/'candidates').glob(f'K1-{text:03d}-attempt-*.json'))
        feedback=read(paths[-1]) if paths else None
        for number in range(len(paths)+1,self.max_attempts+1):
            if read(self.control)['status']!='running': return None
            try:
                source=generator(self.snapshot(text),deepcopy(feedback),number)
                path,result=self.submit(source)
                if result['hard_pass']: return self.commit(path)
                feedback=result
            except StructuralStop: raise
            except Exception as exc:
                self.reject_run(dict(type='structural_failure',reason=str(exc)))
                raise StructuralStop(str(exc)) from exc
        return None

    def _recover_locked(self):
        super()._recover_locked()
        state=self.load();t=state['last_committed_text'];rows=state['committed_records']
        if not t: return
        # Retain the original sequential-run safety stops; regex warnings alone
        # are never confirmed semantic issues.
        confirmed=Counter(x['category'] for r in rows[-5:] for x in r['source'].get('confirmed_naturalness_issues',[]))
        cluster=[r['text_number'] for r in rows[-10:] if similarity(rows[-1]['scene_fingerprint'],r['scene_fingerprint'])>=.85]
        near=sum(0<=d['window']['to']-t<=3 for d in state['review_debt'])
        if state['expired_review_debt']:
            self.reject_run(dict(type='expired_review_debt',text=t,debt=state['expired_review_debt']))
        elif near>=30:
            self.reject_run(dict(type='near_deadline_mass',text=t,count=near))
        elif any(n>=3 for n in confirmed.values()):
            self.reject_run(dict(type='repeated_confirmed_naturalness_issue',text=t,categories=dict(confirmed)))
        elif len(cluster)>=4:
            self.reject_run(dict(type='scene_skeleton_repetition',text=t,cluster=cluster))
        if t%10==0:
            checkpoint=summarize(self)
            write(self.path/'checkpoints'/f'K1-{t:03d}.json',checkpoint)
            if self.path==PILOT:
                write(REPORTS/f'phase3_sequential_v3_checkpoint_{t:03d}.json',checkpoint)
                (REPORTS/f'phase3_sequential_v3_checkpoint_{t:03d}.md').write_text(
                    f'# Sequential v2 checkpoint K1-{t:03d}\n\n```json\n'+json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n```\n',encoding='utf-8')

def draft_from_pairs(path):
    source=read(path);pairs=source.pop('pairs')
    source['sentences']=[p[0] for p in pairs];source['translations_ja']=[p[1] for p in pairs]
    return source

def summarize(gate):
    state=gate.load();rows=state['committed_records']
    attempts=[read(p) for p in sorted((gate.path/'candidates').glob('*.json'))]
    failed=[a for a in attempts if not a['hard_pass']]
    ac=[r['attempt_number'] for r in rows]
    scene_pairs=[dict(text=r['text_number'],previous=p['text_number'],similarity=similarity(r['scene_fingerprint'],p['scene_fingerprint']))
                 for n,r in enumerate(rows) for p in rows[max(0,n-10):n]]
    hist=Counter(e['actual_exposure_count'] for e in state['entries'])
    sentence_sizes=[size for r in rows for size in r['sentence_eojeol_counts']]
    return dict(run='phase3_sequential_v3',generated_count=len(rows),control=read(gate.control),max_attempts=5,
        total_candidate_attempts=len(attempts),rejected_candidates=len(failed),
        first_attempt_pass_count=sum(n==1 for n in ac),first_attempt_pass_rate=sum(n==1 for n in ac)/len(rows) if rows else None,
        mean_attempts_per_committed_text=statistics.mean(ac) if ac else None,
        mean_attempts_per_started_text=len(attempts)/len({a['text_number'] for a in attempts}) if attempts else None,
        retry_reason_distribution=dict(Counter(e['code'] for a in failed for e in a['hard_errors'])),
        future_contaminated_candidates=sum(any(e['code']=='future_expansion' for e in a['hard_errors']) for a in attempts),
        future_candidate_contamination_rate=sum(any(e['code']=='future_expansion' for e in a['hard_errors']) for a in attempts)/len(attempts) if attempts else None,
        resolver_review_count=sum(d['status']=='REVIEW' for a in attempts for d in a.get('resolver_decisions',[])),
        hard_errors=sum(len(r['hard_errors']) for r in rows),controlled_violations=sum(r['coverage']['controlled_vocab_coverage']!=1 for r in rows),
        previous_below_98=sum(r['coverage']['previous_vocab_coverage']<.98 for r in rows),
        grammar_violations=sum(any(e['code']=='grammar32' for e in r['hard_errors']) for r in rows),
        unresolved_content_words=sum(len(r['unresolved_tokens']) for r in rows),
        introduced_count=sum(e['actual_first_text'] is not None for e in state['entries']),
        selected_review_exposures=sum(e['selected_review_exposure_count'] for e in state['entries']),
        incidental_exposures=sum(e['incidental_exposure_count'] for e in state['entries']),exposure_distribution=dict(sorted(hist.items())),
        outstanding_debt=len(state['review_debt']),expired_debt=len(state['expired_review_debt']),
        near_deadline_debt=sum(0<=d['window']['to']-state['last_committed_text']<=3 for d in state['review_debt']),
        naturalness_warning_categories=dict(Counter(w['rule_id'] for r in rows for w in r['naturalness']['lint_warnings'])),
        confirmed_naturalness_issues=[dict(text=r['text_number'],issue=x) for r in rows for x in r['source'].get('confirmed_naturalness_issues',[])],
        semantic_review_flags=sum(len(r['naturalness']['semantic_review']['flags']) for r in rows),
        translation_flags=sum(len(r['translation_fidelity_flags']) for r in rows),
        natural_expression_gaps=[dict(text=r['text_number'],gap=x) for r in rows for x in r['naturalness']['natural_expression_gaps']],
        genre_distribution=dict(Counter(r['genre'] for r in rows)),scene_similarity_pairs=scene_pairs,
        high_scene_similarity_pairs=[p for p in scene_pairs if p['similarity']>=.85],
        eojeol_mean=statistics.mean(r['eojeol_count'] for r in rows) if rows else None,
        eojeol_min=min((r['eojeol_count'] for r in rows),default=None),eojeol_max=max((r['eojeol_count'] for r in rows),default=None),
        sentence_length_distribution=dict(sorted(Counter(sentence_sizes).items())),
        sentence_preferred_compliance=sum(3<=n<=7 for n in sentence_sizes)/len(sentence_sizes) if sentence_sizes else None,
        frozen_input_violations=freeze_errors() if FREEZE.exists() else [])

def opportunity(gate):
    state=gate.load();t=state['last_committed_text']+1
    if t>50 or read(gate.control)['status']!='running': return dict(next_text=None,control=read(gate.control))
    snap=gate.snapshot(t);v={e['vocab_id']:e for e in snap['entries']};s=scheduler(gate.f,state);due=[]
    for i,e in s.entries.items():
        if i not in v or v[i]['role']!='previous_expansion' or len(s.actual[i])>=6: continue
        ws=[w for n,w in enumerate(e['review_windows']) if n not in s.credits[i] and w['from']<=t]
        if ws: due.append(dict(lemma=v[i]['lemma'],id=i,exposures=len(s.actual[i]),last=max(s.actual[i]),deadline=min(w['to'] for w in ws),affinity=e.get('scene_affinity',[])))
    return dict(next_text=t,new=[dict(id=i,lemma=v[i]['lemma'],pos=v[i]['pos'],sense=v[i]['sense']) for i in snap['planned_new_vocab_ids']],
                review_due=sorted(due,key=lambda x:x['deadline']),state_epoch=state['epoch'])

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['init','next','submit','summary']);p.add_argument('--source');a=p.parse_args()
    g=SequentialGate()
    if a.action=='init': freeze();g.initialize()
    if freeze_errors():
        g.reject_run(dict(type='frozen_input_changed',files=freeze_errors()));raise StructuralStop('Freeze mismatch')
    if a.action=='submit':
        source=draft_from_pairs(Path(a.source));path,result=g.submit(source)
        if result['hard_pass']: result=g.commit(path)
        print(json.dumps(dict(text=result['text_number'],attempt=result['attempt_number'],hard_pass=result['hard_pass'],
            eojeol=result.get('eojeol_count'),coverage=result.get('coverage'),errors=result['hard_errors'],
            invalid=result.get('invalid_usage_ids'),control=read(g.control)),ensure_ascii=False))
    write(REPORTS/'k1_phase3_sequential_v3_live_validation.json',summarize(g))
    print(json.dumps(opportunity(g) if a.action!='summary' else summarize(g),ensure_ascii=False))

if __name__=='__main__': main()
