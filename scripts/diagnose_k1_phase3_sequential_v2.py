"""Read-only diagnostic probes; no candidate or exposure credit."""
from copy import deepcopy
import json
from k1_phase3_sequential_v2 import SequentialGate, PILOT, REPORTS
from k1_phase3_sequential_v2_gate import read, write, build_snapshot
from k1_phase3_2_resolver import analyze

def main():
    g=SequentialGate();state=g.load();before=g.ledger.read_bytes()
    snapshot=build_snapshot(g.f,state,2)
    ids={e['vocab_id'] for e in snapshot['entries']}
    f=deepcopy(g.f);f['_allowed_vocab']=[e for e in f['core_vocab.json']+f['expansion_vocab.json'] if e['id'] in ids]
    probes=[
        ('standalone_no','아니요.'),
        ('comma_no','아니요, 책이 너무 비싸요.'),
        ('quoted_comma_no','"아니요, 책이 너무 비싸요."'),
        ('standalone_yes','네.'),
        ('quoted_comma_yes','"네, 여기 있어요."'),
        ('korean_object','저는 한국어를 배워요.'),
        ('korean_book','한국어 책이 있어요?'),
        ('quoted_korean_book','"한국어 책이 있어요?"'),
    ]
    rows=[]
    for name,text in probes:
        a=analyze(text,f,2,(),(),['ask','look','buy','give','read'],g.kiwi)
        rows.append(dict(name=name,text=text,raw_morphology=a['raw_morphology'],
                         annotations=a['annotations'],unresolved=a['unresolved_tokens'],
                         resolver_decisions=a['resolver_decisions'],grammar_used=a['grammar_used']))
    candidate=read(PILOT/'candidates/K1-002-attempt-01.json')
    assert before==g.ledger.read_bytes(), 'Diagnostic changed ledger'
    result=dict(probes=rows,state_unchanged=True,epoch=state['epoch'],last_committed_text=state['last_committed_text'],
                planned_new_ids=candidate['planned_new_vocab_ids'],actual_new_ids=candidate['actual_new_vocab_ids'],
                notes='Raw analysis and permitted identities only. These short probes are diagnostics, not K1-003+ materials or learner exposures.')
    write(REPORTS/'k1_phase3_sequential_v2_analyzer_diagnostics.json',result)
    print(json.dumps([dict(name=r['name'],resolved=[dict(lemma=a['lemma'],pos=a['pos'],sense=a['sense'],id=a['vocab_id']) for a in r['annotations'] if a['vocab_id']],unresolved=r['unresolved']) for r in rows],ensure_ascii=False))

if __name__=='__main__':main()
