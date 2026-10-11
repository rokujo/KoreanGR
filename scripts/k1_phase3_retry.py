"""Separate actual sequential run; the approved Phase 3.1 remains immutable."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import statistics
from k1_candidate_gate import CandidateGate, StructuralStop, atomic_write, read, write, ROOT
from k1_phase3 import files, sha

PILOT = ROOT / 'pilot/ko/k1/phase3_retry'
LEDGER = ROOT / 'state/phase3_retry_001_050_exposure_ledger.json'
REPORTS = ROOT / 'reports'
FREEZE = REPORTS / 'k1_phase3_retry_input_freeze.json'

def error_measures(candidate):
    """Per error identity, lower is better. Length uses remaining distance."""
    result = Counter()
    for error in candidate['hard_errors']:
        code, detail = error['code'], error.get('detail')
        if code == 'length':
            result[(code, '')] = max(120-detail, detail-180, 0)
        elif code == 'coverage_or_token_policy' and isinstance(detail, str) and detail.startswith('controlled_vocab_coverage below'):
            result[(code, 'controlled_floor')] = 1-candidate['coverage']['controlled_vocab_coverage']
        elif code == 'coverage_or_token_policy' and isinstance(detail, str) and detail.startswith('previous_vocab_coverage below'):
            result[(code, 'previous_floor')] = .98-candidate['coverage']['previous_vocab_coverage']
        elif isinstance(detail, dict):
            result[(code, detail.get('vocab_id') or detail.get('lemma') or detail.get('rule_id') or '')] += 1
        else:
            result[(code, str(detail))] += 1
    return result

def stagnant_errors(previous, current):
    before, after = error_measures(previous), error_measures(current)
    return [dict(code=k[0], identity=k[1], before=before[k], after=after[k])
            for k in before.keys() & after.keys() if after[k] >= before[k]]

class SequentialGate(CandidateGate):
    def __init__(self, run_dir=PILOT, ledger_path=LEDGER, **kwargs):
        budget = kwargs.pop('max_attempts', 5)
        if not 1 <= budget <= 5:
            raise ValueError('Maximum five attempts')
        super().__init__(run_dir, ledger_path, max_attempts=min(budget, 3), max_text=50, **kwargs)
        self.max_attempts = budget

    def _submit_locked(self, source):
        path, result = super()._submit_locked(source)
        if not result['hard_pass'] and result['attempt_number'] >= 2:
            previous = read(path.with_name(f"K1-{result['text_number']:03d}-attempt-{result['attempt_number']-1:02d}.json"))
            stagnant = stagnant_errors(previous, result)
            if stagnant:
                self.reject_run(dict(type='same_hard_error_twice_without_improvement',
                    text=result['text_number'], attempt=result['attempt_number'], errors=stagnant))
        return path, result

    def run_one(self, text, generator):
        """Resume journals without resetting the budget or masking a stop reason."""
        paths=sorted((self.path/'candidates').glob(f'K1-{text:03d}-attempt-*.json'))
        feedback=read(paths[-1]) if paths else None
        for number in range(len(paths)+1,self.max_attempts+1):
            if read(self.control)['status']!='running':return None
            try:
                source=generator(self.snapshot(text),deepcopy(feedback),number)
                path,result=self.submit(source)
                if result['hard_pass']:return self.commit(path)
                feedback=result
            except StructuralStop:
                raise
            except Exception as exc:
                self.reject_run(dict(type='structural_failure',reason=str(exc)))
                raise StructuralStop(str(exc)) from exc
        return None

    def _recover_locked(self):
        super()._recover_locked()
        state=self.load();number=state['last_committed_text']
        if number and number%10==0:
            checkpoint=summarize(self)
            write(self.path/'checkpoints'/f'K1-{number:03d}.json',checkpoint)
            if self.path==PILOT:
                write(REPORTS/f'phase3_retry_checkpoint_{number:03d}.json',checkpoint)
                (REPORTS/f'phase3_retry_checkpoint_{number:03d}.md').write_text(
                    f'# Phase 3 retry checkpoint K1-{number:03d}\n\n'+
                    '```json\n'+__import__('json').dumps(checkpoint,ensure_ascii=False,indent=2)+'\n```\n',encoding='utf-8')

def freeze():
    if FREEZE.exists():
        return
    manifest = read(REPORTS/'k1_phase3_1_artifact_manifest.json')
    old = read(REPORTS/'k1_phase3_1_input_freeze.json')
    paths = set(manifest['files']) | set(old['files'])
    paths |= {'reports/k1_phase3_1_artifact_manifest.json', 'reports/k1_phase3_1_input_freeze.json'}
    paths |= {p.relative_to(ROOT).as_posix() for p in (ROOT/'config/languages/ko/k1').rglob('*.json')}
    missing = [p for p in paths if not (ROOT/p).is_file()]
    if missing:
        raise StructuralStop(str(missing))
    write(FREEZE, dict(run='phase3_retry', files={p:sha(ROOT/p) for p in sorted(paths)}))

def freeze_errors():
    return [p for p,h in read(FREEZE)['files'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]

def draft_from_pairs(path):
    """Authored bilingual sentences, produced only for the current actual state."""
    draft = read(path)
    pairs = draft.pop('pairs')
    draft['sentences'] = [p[0] for p in pairs]
    draft['translations_ja'] = [p[1] for p in pairs]
    return draft

def summarize(gate):
    state = gate.load()
    rows = state['committed_records']
    attempts = [read(p) for p in sorted((gate.path/'candidates').glob('*.json'))]
    rejected = [a for a in attempts if not a['hard_pass']]
    committed_attempts = [r['attempt_number'] for r in rows]
    exposures = Counter(e['actual_exposure_count'] for e in state['entries'])
    lint = Counter(w['rule_id'] for r in rows for w in r['naturalness']['lint_warnings'])
    return dict(run='phase3_retry', generated_count=len(rows), control=read(gate.control),
        total_candidate_attempts=len(attempts), rejected_candidates=len(rejected),
        first_attempt_pass_count=sum(n==1 for n in committed_attempts),
        first_attempt_pass_rate=sum(n==1 for n in committed_attempts)/len(rows) if rows else None,
        mean_attempts_per_committed_text=statistics.mean(committed_attempts) if rows else None,
        retry_reason_distribution=dict(Counter(e['code'] for a in rejected for e in a['hard_errors'])),
        future_contaminated_candidates=sum(any(e['code']=='future_expansion' for e in a['hard_errors']) for a in attempts),
        future_candidate_contamination_rate=sum(any(e['code']=='future_expansion' for e in a['hard_errors']) for a in attempts)/len(attempts) if attempts else None,
        resolver_review_count=sum(d['status']=='REVIEW' for a in attempts for d in a.get('resolver_decisions',[])),
        hard_errors=sum(len(r['hard_errors']) for r in rows),
        controlled_violations=sum(r['coverage']['controlled_vocab_coverage']!=1 for r in rows),
        previous_below_98=sum(r['coverage']['previous_vocab_coverage']<.98 for r in rows),
        unresolved_content_words=sum(len(r['unresolved_tokens']) for r in rows),
        grammar_violations=sum(any(e['code']=='grammar32' for e in r['hard_errors']) for r in rows),
        introduced_count=sum(e['actual_first_text'] is not None for e in state['entries']),
        selected_review_exposures=sum(e['selected_review_exposure_count'] for e in state['entries']),
        incidental_exposures=sum(e['incidental_exposure_count'] for e in state['entries']),
        exposure_distribution=dict(sorted(exposures.items())),
        outstanding_debt=len(state['review_debt']), expired_debt=len(state['expired_review_debt']),
        near_deadline_debt=sum(0<=d['window']['to']-state['last_committed_text']<=3 for d in state['review_debt']),
        naturalness_warning_categories=dict(lint),
        semantic_review_flags=sum(len(r['naturalness']['semantic_review']['flags']) for r in rows),
        translation_flags=sum(len(r['translation_fidelity_flags']) for r in rows),
        natural_expression_gaps=[dict(text=r['text_number'],gap=x) for r in rows for x in r['naturalness']['natural_expression_gaps']],
        genre_distribution=dict(Counter(r['genre'] for r in rows)),
        eojeol_mean=statistics.mean(r['eojeol_count'] for r in rows) if rows else None,
        eojeol_min=min((r['eojeol_count'] for r in rows),default=None),
        eojeol_max=max((r['eojeol_count'] for r in rows),default=None),
        frozen_input_violations=freeze_errors())

def opportunity(gate):
    from k1_candidate_gate import scheduler
    state=gate.load();t=state['last_committed_text']+1
    if t>50 or read(gate.control)['status']!='running':
        return dict(next_text=None,control=read(gate.control))
    snap=gate.snapshot(t)
    v={e['vocab_id']:e for e in snap['entries']}
    s=scheduler(gate.f,state)
    due=[]
    for i,entry in s.entries.items():
        if i not in v or v[i]['role']!='previous_expansion' or len(s.actual[i])>=6:
            continue
        windows=[w for n,w in enumerate(entry['review_windows']) if n not in s.credits[i] and w['from']<=t]
        if windows:
            due.append(dict(lemma=v[i]['lemma'],id=i,exposures=len(s.actual[i]),
                last=max(s.actual[i]),deadline=min(w['to'] for w in windows),affinity=entry.get('scene_affinity',[])))
    return dict(next_text=t,new=[v[i] for i in snap['planned_new_vocab_ids']],
                review_due=sorted(due,key=lambda x:x['deadline']),state_epoch=state['epoch'])

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['init','next','submit','summary']);p.add_argument('--source');a=p.parse_args()
    g=SequentialGate()
    if a.action=='init':
        freeze();g.initialize()
    if freeze_errors():
        g.reject_run(dict(type='frozen_input_changed',files=freeze_errors()));raise StructuralStop('Freeze mismatch')
    if a.action=='submit':
        source=draft_from_pairs(Path(a.source));path,result=g.submit(source)
        if result['hard_pass']:
            result=g.commit(path)
        print(__import__('json').dumps(dict(text=result['text_number'],attempt=result['attempt_number'],
            hard_pass=result['hard_pass'],eojeol=result.get('eojeol_count'),coverage=result.get('coverage'),
            errors=result['hard_errors'],invalid=result.get('invalid_usage_ids'),control=read(g.control)),ensure_ascii=True))
    write(REPORTS/'k1_phase3_retry_live_validation.json',summarize(g))
    print(__import__('json').dumps(opportunity(g) if a.action!='summary' else summarize(g),ensure_ascii=True))

if __name__=='__main__':main()
