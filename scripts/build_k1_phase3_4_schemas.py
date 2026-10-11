"""Build a reusable K1 candidate ID contract, independent of smoke control."""
from copy import deepcopy
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
SCHEMAS=ROOT/'config/languages/ko/k1/phase3_4'
GENRES=['daily_life','school','family','friends','friendship','food','shopping','transport',
        'weather','home','small_problem','short_dialogue','simple_outing','objects','simple_hobby',
        'health','outdoor','travel','work']

def contracts(maximum=50):
    if not 1 <= maximum <= 999:
        raise ValueError('Three-digit K1 contract range is invalid')
    old=ROOT/'pilot/ko/k1/phase3_sequential_v3'
    candidate=json.loads((old/'candidate.schema.json').read_text(encoding='utf-8'))
    candidate['$defs']={'generic_k1_id':{'type':'string','pattern':'^K1-[0-9]{3}$'}}
    candidate['properties']['id']={'allOf':[{'$ref':'#/$defs/generic_k1_id'},
         {'enum':[f'K1-{t:03d}' for t in range(1,maximum+1)]}]}
    candidate['properties']['text_number']['maximum']=maximum
    candidate['allOf']=[{'if':{'properties':{'text_number':{'const':t}}},
                         'then':{'properties':{'id':{'const':f'K1-{t:03d}'}}}}
                        for t in range(1,maximum+1)]
    source=json.loads((old/'source.schema.json').read_text(encoding='utf-8'))
    source['properties']['text_number']['maximum']=maximum
    source['properties']['genre']={'enum':GENRES}
    windows=json.loads((ROOT/'config/languages/ko/k1/vocab_review_windows.json').read_text(encoding='utf-8'))
    source['properties']['scene']['items']['enum']=deepcopy(windows['scene_catalog'])
    return candidate,source

def main():
    SCHEMAS.mkdir(parents=True,exist_ok=True)
    candidate,source=contracts(50)
    for name,obj in [('candidate.schema.json',candidate),('source.schema.json',source)]:
        (SCHEMAS/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
