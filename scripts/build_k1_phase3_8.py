"""One-time version scaffolding. Never execute after production_start."""
from pathlib import Path
import json,hashlib,datetime

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def build():
    watched=[]
    for folder in ('pilot','reports','state','config','docs','scripts','tests'):
        watched += [p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix not in ('.pyc','.lock') and '__pycache__' not in p.parts and '3_8' not in p.name and 'phase3_8' not in p.parts]
    write(ROOT/'reports/k1_phase3_8_input_freeze.json',dict(files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in watched}))
    for name in ('k1_phase3_7_analysis.py','k1_phase3_7_gate.py','k1_phase3_7.py','report_k1_phase3_7.py','run_k1_phase3_7_tests.py','audit_k1_phase3_7.py'):
        src=(ROOT/'scripts'/name).read_text(encoding='utf8').replace('3_7','3_8').replace('3.7','3.8')
        (ROOT/'scripts'/name.replace('3_7','3_8')).write_text(src,encoding='utf8')
    cfg=ROOT/'config/languages/ko/k1'
    write(cfg/'basic_sense_families.json',dict(version='phase3_8',authority='Explicit Phase 3.8 human approval; overlay supersedes only the old meal exclusions of these two IDs.',entries=[
        dict(vocab_id='ko_k1_0072',lemma='아침',registered_sense='morning',allowed_functions=['morning_time','breakfast_meal'],gloss_ja='朝・朝食',new_id=False),
        dict(vocab_id='ko_k1_0074',lemma='저녁',registered_sense='evening',allowed_functions=['evening_time','dinner_meal'],gloss_ja='夕方・晩・夕食',new_id=False)]))
    # Only explicitly contrasting existing notes, not a dictionary sense inventory.
    specs=[
      ('ko_k1_0073','점심을 먹어요.','점심은 정확히 열두 시라는 뜻이에요.',r'정확히\s*열두\s*시|정오','strict_noon'),
      ('ko_k1_0078','오 분 동안 기다려요.','좋은 분이 와요.',r'좋은\s*분|그\s*분|이\s*분','honorific_person'),
      ('ko_k1_0080','일 월이에요.','세 월 동안 기다려요.',r'(?:한|두|세|네)\s*월\s*동안','duration_month'),
      ('ko_k1_0127','차를 마셔요.','차를 운전해요.',r'차(?:를|로|가).*?(?:운전|주차)|차를\s*타','automobile'),
      ('ko_k1_0133','친구의 말을 들어요.','말을 타요.',r'말(?:을|에)\s*타|말이\s*달려','horse'),
      ('ko_k1_0135','일을 해요.','일이 일어났어요.',r'일이\s*(?:일어났|생겼)','incident'),
      ('ko_k1_0153','눈이 와요.','눈을 감아요.',r'눈(?:을|이)\s*(?:감|아파)|눈으로\s*봐','eye'),
      ('ko_k1_0178','이름을 써요.','모자를 써요.',r'(?:모자|안경|기계)(?:를|을)\s*쓰|컴퓨터를\s*써','wear_or_use'),
      ('ko_k1_0229','사진을 찍어요.','도장을 찍어요.',r'(?:도장|점|인장)(?:을|를)\s*찍','stamp_or_mark'),
      ('ko_k1_0808','이를 닦아요.','실력을 닦아요.',r'(?:실력|솜씨|학문)(?:을|를)\s*닦','abstract_skill'),
      ('ko_k1_0810','공을 던져요.','공을 세워요.',r'공을\s*세워|공이\s*크다는\s*업적','merit'),
      ('ko_k1_0389','집이 보여요.','사진을 보여요.',r'사진을\s*보여','causative_show'),
      ('ko_k1_0495','표를 사요.','표에 숫자를 정리해요.',r'표에\s*숫자.*정리|표를\s*작성','table'),
      ('ko_k1_0511','기사가 버스를 운전해요.','기사를 읽어요.',r'기사(?:를|가).*?(?:읽|신문)|기사에서\s*뉴스','news_article'),
      ('ko_k1_0812','가방을 들어요.','마음에 들어요.',r'마음에\s*들|(?:돈|비용|나이)(?:이|가)\s*들','cost_liking_age'),
      ('ko_k1_0809','종이를 붙여요.','불을 붙여요.',r'불을\s*붙','ignite'),
      ('ko_k1_0804','휴대폰을 충전해요.','마음을 충전해요.',r'(?:마음|기분|의욕)(?:을|를)\s*충전','figurative_recharge'),
      ('ko_k1_0786','밤에 꿈을 꿨어요.','제 꿈은 의사예요.',r'(?:제|나의)\s*꿈은\s*(?:의사|선생님)|장래의\s*꿈','future_aspiration')]
    vs={e['id']:e for name in ('core_vocab.json','expansion_vocab.json') for e in read(cfg/name)}
    entries=[]
    for i,pos,neg,pattern,function in specs:
        e=vs[i];assert e['notes']
        entries.append(dict(vocab_id=i,lemma=e['lemma'],pos=e['pos'],allowed_sense=e['sense'],source=dict(file='config/languages/ko/k1/'+('core_vocab.json' if e['tier']=='core' else 'expansion_vocab.json'),notes=e['notes']),positive_example=pos,negative_example=neg,negative_pattern=pattern,disallowed_function=function,mechanical_policy='Reject only canonical occurrence of this ID plus clear local negative context. Missing pattern evidence is not a new inferred sense restriction; author checks remain required.'))
    write(cfg/'explicit_restricted_senses.json',dict(version='phase3_8',scope='Existing explicit lexical sense restrictions only. POS boundaries and grammar restrictions retain their existing gates; no new restriction is invented.',entries=entries,excluded_notes=['Social address/register guidance is naturalness review, not a new lexical sense hard rule.','POS-only/compound/grammar boundary notes are already governed by the frozen analyzer/form gate.','Old breakfast/dinner exclusions are superseded only by basic_sense_families.json.','普通の中心義のglossや多義性だけを根拠に新しいhard restrictionを作らない。']))
    p=ROOT/'scripts/k1_phase3_8_analysis.py';s=p.read_text(encoding='utf8')
    s=s.replace("tags=sorted({r['tag'] for r in a['raw_morphology'] if r['start']<x['end']-lo and r['start']+r['length']>x['start']-lo})","tags=sorted({a['raw_morphology'][i]['tag'] for z in hits if z['vocab_id'] for i in z.get('morph_indices',[])})")
    p.write_text(s,encoding='utf8')
    p=ROOT/'scripts/k1_phase3_8.py';s=p.read_text(encoding='utf8')
    s=s.replace("ENGINEERING_START_UTC='2026-10-10T22:45:11.381976+00:00'",'ENGINEERING_START_UTC='+repr(datetime.datetime.now(datetime.timezone.utc).isoformat()))
    s=s.replace("    # Administrative range/path adapter only; inherited rules remain unchanged.","    # Ordinary candidate errors are local retries through all five attempts.\n    def _submit_locked(self,source):\n        return CandidateGate._submit_locked(self,source)\n")
    s=s.replace("docs/ko_k1_phase3_6b_author_prompt.md","docs/ko_k1_phase3_8_author_prompt.md")
    s=s.replace("a=analyze(pair[0],f,r['text_number'],kiwi=gate.kiwi,scope='author_lexical_preflight')","a=analyze(pair[0],f,r['text_number'],intents=r['plan'].get('generated_intents',[]),scene_actions=r['plan']['scene_fingerprint']['main_actions'],kiwi=gate.kiwi,scope='author_lexical_preflight')\n        from k1_phase3_8_sense import sense_checks\n        findings += [dict(sentence=index,reason='explicit_restricted_sense_violation',**x) for x in sense_checks(pair[0],a) if x['decision']=='FAIL']")
    p.write_text(s,encoding='utf8')
    prompt=(ROOT/'docs/ko_k1_phase3_6b_author_prompt.md').read_text(encoding='utf8')
    (ROOT/'docs/ko_k1_phase3_8_author_prompt.md').write_text(prompt+'\n\n## Phase 3.8 sense policy\n\nUse only the Expansion IDs in the current allowed snapshot. Do not substitute a future synonym. 아침 may mean morning or breakfast; 저녁 may mean evening or dinner, under the existing IDs. All other entries receive no inferred sense expansion. Explicit restricted entries are attached to the snapshot with their original notes: use the allowed sense, especially 찍다/photo, 쓰다/write, 들다/hold or lift by hand. Ordinary semantic grammar REVIEW is diagnostic only. Do not repair prose merely to reduce diagnostic counts.\n',encoding='utf8')
if __name__=='__main__':build()
