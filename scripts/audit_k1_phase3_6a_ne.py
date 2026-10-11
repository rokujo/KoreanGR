"""Pre-run raw reproduction audit; never changes frozen failed annotations."""
from k1_phase3 import ROOT,files,read,write
from k1_phase2_3 import make_kiwi
from k1_phase3_6a_resolver import analyze,focused_scope_parity
from k1_phase3_6_resolver import analyze as previous

if __name__=='__main__':
    f=files();k=make_kiwi();old=read(ROOT/'pilot/ko/k1/phase3_6/candidates/K1-002-attempt-01.json');text=old['text_ko']
    a=analyze(text,f,2,kiwi=k,scope='frozen_failed_fulltext_reproduction')
    short=[analyze(s,f,2,kiwi=k,scope='sentence_probe') for s in old['source']['sentences']]
    parity=focused_scope_parity(text,a,old['source']['sentences'],short,f,2,old['planned_new_vocab_ids'],kiwi=k)
    contrast=[]
    for s in ('네.','"네."','네, 여기 있어요.','"네, 여기 있어요."','네, 저녁에 만나요.','"네, 저녁에 만나요."','네 책','네 가방','네 사람이 와요.'):
        b=analyze(s,f,2,kiwi=k);contrast.append(dict(text=s,raw=b['raw_morphology'],annotations=b['annotations'],audit=b['ne_response_recovery_audit']))
    assert a['raw_morphology']==previous(text,f,2,kiwi=k)['raw_morphology']
    assert not any(r['structural_defect'] for r in parity)
    write(ROOT/'reports/k1_phase3_6a_ne_identity_audit.json',dict(author_annotation_used=False,raw_preserved=True,
        frozen_source='pilot/ko/k1/phase3_6/candidates/K1-002-attempt-01.json',fulltext_raw=a['raw_morphology'],fulltext_annotations=a['annotations'],
        recoveries=a['ne_response_recovery_audit'],scope_parity=parity,contrasts=contrast))
    print('Exact response recovery audit PASS; no frozen annotation reused.')
