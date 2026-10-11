"""Author only the explicitly approved A20+B5, with frozen input verification."""
import sys,json
from k1_phase2_2 import *

def build():
    freeze();files=inputs();selected=selection(files)
    scenes=read(PILOT/'authored_scenes.json')
    numbers=[s['text_number'] for s in scenes]
    if len(numbers)!=len(set(numbers)) or not set(numbers)<=set(selected['all_text_numbers']):raise ValueError('Unapproved or duplicate pilot number')
    kiwi=make_kiwi()
    records,ledger=state_steps(files,scenes,lambda scene,proposal:record(scene,files,proposal,kiwi))
    for rec in records:write(PILOT/'texts'/f"{rec['id']}.json",rec)
    write(PILOT/'selection.json',selected);write(PILOT/'pilot_text.schema.json',text_schema())
    write(PILOT/'exposure_ledger.json',ledger)
    from validate_k1_phase2_2 import inspect_record
    checks=[inspect_record(r,files,kiwi) for r in records]
    print(json.dumps([{'id':r['id'],'eojeol':r['metrics']['eojeol_count'],'N':r['coverage']['denominator_N'],'U':r['coverage']['new_tokens_U'],
                      'review':r['review_count'],'status':r['status'],'errors':r['errors']} for r in checks],ensure_ascii=False,indent=2))
    print('Draft count:',len(records),'approved maximum:25')
    if check_freeze():raise ValueError(check_freeze())
    return records

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');build()
