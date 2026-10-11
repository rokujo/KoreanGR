"""One-time scaffolding. Extract existing contract names without editing history."""
import ast, json, hashlib
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
def build():
    if (ROOT/'reports/k1_phase3_9a_timing.json').exists():raise RuntimeError('Production already started')
    old=(ROOT/'scripts/k1_phase3_9.py').read_text(encoding='utf8')
    keys=next(ast.literal_eval(n.value) for n in ast.walk(ast.parse(old)) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='required' for t in n.targets))
    p=ROOT/'config/languages/ko/k1/author_selfcheck.schema.json'
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Author self-check: existing Phase 3.9 contract','type':'object','required':list(keys),'properties':{**{k:{'type':'boolean','const':True} for k in keys},'notes':{'type':'string'}},'additionalProperties':False}
    if p.exists():raise RuntimeError('Do not overwrite single schema source')
    p.write_text(json.dumps(schema,indent=2)+'\n',encoding='utf8')
    gate=(ROOT/'scripts/k1_phase3_9_gate.py').read_text(encoding='utf8').replace("phase='3.9'","phase='3.9a'")
    (ROOT/'scripts/k1_phase3_9a_gate.py').write_text(gate,encoding='utf8')
    c=old.replace('3_9','3_9a').replace('Phase 3.9 sequential','Phase 3.9a sequential').replace("phase='3.9'","phase='3.9a'")
    a=c.index('ENGINEERING_START_UTC=');b=c.index('\n',a)
    c=c[:a]+'ENGINEERING_START_UTC='+repr(datetime.now(timezone.utc).isoformat())+c[b:]
    (ROOT/'scripts/k1_phase3_9a.py').write_text(c,encoding='utf8')
    for src,dst in [('run_k1_phase3_9_tests.py','run_k1_phase3_9a_tests.py'),('report_k1_phase3_9.py','report_k1_phase3_9a.py')]:
        s=(ROOT/'scripts'/src).read_text(encoding='utf8').replace('3_9','3_9a').replace("phase='3.9'","phase='3.9a'").replace('Phase 3.9','Phase 3.9a')
        (ROOT/'scripts'/dst).write_text(s,encoding='utf8')
    (ROOT/'docs/ko_k1_phase3_9a_author_prompt.md').write_text((ROOT/'docs/ko_k1_phase3_9_author_prompt.md').read_text(encoding='utf8').replace('Phase 3.9','Phase 3.9a'),encoding='utf8')
    watched=[p for folder in ('pilot','reports','state','config','docs','scripts','tests') for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix not in ('.pyc','.lock') and '__pycache__' not in p.parts and '3_9a' not in p.name and 'phase3_9a' not in p.parts and p.name not in ('natural_expression_gaps.json','author_selfcheck.schema.json')]
    (ROOT/'reports/k1_phase3_9a_input_freeze.json').write_text(json.dumps({'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in watched}},indent=2)+'\n',encoding='utf8')
    print(json.dumps({'existing_schema_keys':keys,'history_files_frozen':len(watched)}))
if __name__=='__main__':build()
