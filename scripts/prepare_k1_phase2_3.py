"""Initialize a separate revision; never edit Phase 2.2 or frozen language inputs."""
from k1_phase2_2 import ROOT, DATA, REPORTS, read, write, sha, check_freeze

PILOT=ROOT/'pilot/ko/k1/phase2_3'
FREEZE=REPORTS/'k1_phase2_3_input_freeze.json'

def prepare():
    if check_freeze():raise ValueError(check_freeze())
    if not FREEZE.exists():
        paths=list(DATA.glob('*.json'))
        paths += [p for p in (ROOT/'pilot/ko/k1/phase2_2').rglob('*') if p.is_file()]
        paths += [p for p in REPORTS.glob('k1_phase2_2*') if p.is_file()]
        paths += [p for d in ('scripts','tests') for p in (ROOT/d).glob('*.py') if 'phase2_3' not in p.name and 'naturalness' not in p.name]
        write(FREEZE,dict(scope='All existing K1 JSON inputs and complete Phase 2.2 artifacts/codes; additive guideline is not lexical expansion.',files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(paths))}))
    source=ROOT/'pilot/ko/k1/phase2_2/authored_scenes.json'
    if not (PILOT/'authored_scenes.json').exists():
        write(PILOT/'authored_scenes.json',read(source))

if __name__=='__main__':prepare()
