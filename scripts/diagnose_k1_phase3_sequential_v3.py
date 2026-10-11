"""Pure contrast diagnostics over the frozen 3.3 engine, not exposures."""
from copy import deepcopy
import json
from k1_phase3_sequential_v3 import SequentialGate, REPORTS, PILOT
from k1_phase3_sequential_v3_gate import read, write, build_snapshot
from k1_phase3_3_resolver import analyze

def main():
    g=SequentialGate();state=g.load();before=g.ledger.read_bytes();snap=build_snapshot(g.f,state,2)
    ids={e['vocab_id'] for e in snap['entries']};f=deepcopy(g.f)
    f['_allowed_vocab']=[e for e in f['core_vocab.json']+f['expansion_vocab.json'] if e['id'] in ids]
    cases=[
        ('plain_question','우리 집에 올 거예요?'),
        ('quoted_question','"우리 집에 올 거예요?"'),
        ('speaker_and_quote','저는 친구에게 말해요. "우리 집에 올 거예요?"'),
        ('unquoted_narration','친구는 우리 집에 올 거예요.'),
        ('topic_pronoun','우리는 방에 들어가요.'),
        ('noun_pen_contrast','우리 안에 개가 있어요.'),
        ('quoted_yes_regression','"네, 시간이 있어요."'),
        ('quoted_no_regression','"아니요, 비가 많이 와요."'),
    ]
    candidate=read(PILOT/'candidates/K1-002-attempt-02.json')
    full=candidate['text_ko']
    cases.extend([
        ('candidate_full_text',full),
        ('candidate_paragraph',next(p for p in full.split('\n\n') if '"우리 집에 올 거예요?"' in p)),
        ('diagnostic_full_without_quotes',full.replace('"','')),
    ])
    rows=[]
    for name,text in cases:
        a=analyze(text,f,2,(),(),['phone','choose_meeting_place','welcome','watch_movie','say_goodbye'],g.kiwi)
        rows.append(dict(name=name,text=text,raw_morphology=a['raw_morphology'],annotations=a['annotations'],
                         unresolved=a['unresolved_tokens'],resolver_decisions=a['resolver_decisions']))
    assert before==g.ledger.read_bytes()
    result=dict(probes=rows,state_unchanged=True,epoch=state['epoch'],last_committed_text=state['last_committed_text'],
                policy='Diagnostic evidence only. No candidate generation, grammar expansion or learner exposure credit.')
    write(REPORTS/'k1_phase3_sequential_v3_analyzer_diagnostics.json',result)
    print(json.dumps([dict(name=r['name'],raw_uri=[x for x in r['raw_morphology'] if x['form']=='우리'],
        identities=[dict(lemma=a['lemma'],pos=a['pos'],id=a['vocab_id']) for a in r['annotations'] if a['vocab_id']],
        unresolved=r['unresolved']) for r in rows],ensure_ascii=False))

if __name__=='__main__':main()
