"""One-time run-envelope scaffolding; never run after production_start."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
def put(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def build():
    if (ROOT/'reports/k1_phase3_9_timing.json').exists():raise RuntimeError('Production already started')
    watched=[]
    for folder in ('pilot','reports','state','config','docs','scripts','tests'):
        watched += [p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix not in ('.pyc','.lock') and '__pycache__' not in p.parts and '3_9' not in p.name and 'phase3_9' not in p.parts and p.name!='natural_expression_gaps.json']
    put(ROOT/'reports/k1_phase3_9_input_freeze.json',{'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in watched}})
    for name in ('source.schema.json','candidate.schema.json'):
        x=json.loads((ROOT/'config/languages/ko/k1/phase3_4'/name).read_text(encoding='utf8'))
        x['properties']['text_number']['maximum']=100
        if name.startswith('candidate'):x['properties']['id']['allOf'][1]['enum']=[f'K1-{n:03d}' for n in range(1,101)]
        put(ROOT/'config/languages/ko/k1/phase3_9'/name,x)
    # Only paths, provenance and run bound differ. evaluate() is byte-identical.
    s=(ROOT/'scripts/k1_phase3_8_gate.py').read_text(encoding='utf8')
    s=s.replace("phase3_4'/n)","phase3_9'/n)").replace('phase3_4/source.schema','phase3_9/source.schema').replace('phase3_4/candidate.schema','phase3_9/candidate.schema')
    s=s.replace('max_text=50','max_text=100').replace('max_text<=50','max_text<=100').replace("phase='3.8'","phase='3.9'")
    (ROOT/'scripts/k1_phase3_9_gate.py').write_text(s,encoding='utf8')
    s=(ROOT/'scripts/k1_phase3_8.py').read_text(encoding='utf8').replace('3_8_gate','3_9_gate').replace('phase3_8','phase3_9').replace('k1_phase3_8_input','k1_phase3_9_input').replace('k1_phase3_8_timing','k1_phase3_9_timing').replace('ko_k1_phase3_8_author','ko_k1_phase3_9_author').replace('Phase 3.8 sequential','Phase 3.9 sequential').replace('max_text=50','max_text=100').replace("==50:","==100:")
    start=s.index("ENGINEERING_START_UTC=");end=s.index('\n',start)
    s=s[:start]+"ENGINEERING_START_UTC="+repr(datetime.now(timezone.utc).isoformat())+s[end:]
    (ROOT/'scripts/k1_phase3_9.py').write_text(s,encoding='utf8')
    s=(ROOT/'scripts/run_k1_phase3_8_tests.py').read_text(encoding='utf8').replace('3_8','3_9').replace('050','100')
    (ROOT/'scripts/run_k1_phase3_9_tests.py').write_text(s,encoding='utf8')
if __name__=='__main__':build()
