"""Phase 3.2: POS/context-conditioned identities and explicit grouping evidence.

Frozen earlier parsers are not imported or patched. Raw Kiwi remains unchanged.
REVIEW is preferable to a unique but incompatible dictionary entry.
"""
from collections import defaultdict
import re
from kiwipiepy import Kiwi

PARTICLES={'은':'19','는':'19','이':'20','가':'20','을':'21','를':'21','에':'22','에서':'23',
           '도':'24','하고':'25','에게':'28','한테':'28','의':'29','로':'30','으로':'30','부터':'31','까지':'31','만':'32'}
LEGACY_DEFAULT_SENSE_AUDIT={'저':'i_humble','일':'work','눈':'eye','개':'dog','쓰다':'write','찍다':'take_photo',
               '이':'this','팔':'arm','봉지':'bag_packet','달':'month_duration','다리':'leg','배':'belly','풀':'grass','새':'new_attributive'}
TAG_POS={'NP':{'pronoun'},'MM':{'determiner','numeral'},'SN':{'numeral'},'NR':{'numeral'},
         'VV':{'verb'},'VA':{'adjective'},'MAG':{'adverb','conjunction'},'MAJ':{'conjunction','adverb'},'IC':{'interjection'}}
TAG_POS.update(NNG={'noun'},NNP={'noun'},NNB={'noun','counter'},XR=set())
ALIAS_AUDIT=[
    dict(surface=s,old_target=t,classification='pos_conditioned_alias',condition='raw NP; registered pronoun identity; no global text replacement')
    for s,t in [('이거','이것'),('그거','그것'),('저거','저것')]] + [
    dict(surface=s,old_target=t,classification='context_conditioned_alias',condition='raw NP plus possessive nominal context; raw IC/MM cannot use this pronoun alias')
    for s,t in [('내','나'),('네','너'),('제','저')]] + [
    dict(surface=s,old_target=t,classification='pos_conditioned_alias',condition='raw MM/NR plus following nominal; registered numeral; no sense extension')
    for s,t in [('한','하나'),('두','둘'),('세','셋'),('스무','스물')]] + [
    dict(surface='네_numeral',old_target='넷',classification='unsafe_alias_remove',condition='Synthetic key never a surface; replace with explicit 네 MM/NR contextual branch'),
    dict(surface='다른',old_target='다르다',classification='context_conditioned_alias',condition='exact attributive surface, raw MM, following nominal; explicit adjective bridge + g26')]

def following_nominal(raw,index,text):
    """Only the immediately following raw noun, without an intervening delimiter."""
    if index+1>=len(raw):return False
    token,next_token=raw[index],raw[index+1]
    return next_token['tag'].split('-')[0] in ('NNG','NNP','NNB') and not re.search(r'[.,!?"“”\n]',text[token['start']+token['length']:next_token['start']])

def identity_candidate(raw,index,text):
    t=raw[index];form=t['form'];tag=t['tag'].split('-')[0]
    nominal=following_nominal(raw,index,text)
    if form=='네':
        if tag=='IC':
            if nominal:return form,'ambiguous_yes_or_possessive',False
            return form,'registered_interjection_not_pronoun_alias',True
        if tag in ('MM','NR') and nominal:return '넷','native_numeral_context',True
        if tag=='NP' and nominal:return '너','contracted_possessive',True
        return form,'ambiguous_ne_context',False
    if form in ('이거','그거','저거'):
        return {'이거':'이것','그거':'그것','저거':'저것'}[form],'pronoun_surface_normalization',tag=='NP'
    if form in ('내','제'):
        return {'내':'나','제':'저'}[form],'contracted_possessive',tag=='NP' and nominal
    if form in ('한','두','세','스무'):
        return {'한':'하나','두':'둘','세':'셋','스무':'스물'}[form],'native_numeral_context',tag in ('MM','NR') and nominal
    if form=='다른':return '다르다','attributive_pos_boundary',tag=='MM' and nominal
    if tag in ('VV','VA'):return form+'다',None,True
    return form,None,True

def compatible_entry(entry,tag,lemma,reason,raw,index):
    if tag=='MM' and entry['pos']=='numeral' and lemma in ('일','이','삼','사','오','육','칠','팔','구','십','백','천','만'):return False
    if entry['pos'] in TAG_POS.get(tag,set()):return True
    # Explicit Korean predicate/DB bridge; cannot license any new lemma/sense.
    if tag=='VV' and entry['pos']=='adjective' and lemma in ('있다','없다','필요하다'):return True
    if tag=='MM' and entry['pos']=='adjective' and lemma=='다르다' and reason=='attributive_pos_boundary':return True
    if tag=='NNG' and entry['pos']=='counter' and index>0:
        return raw[index-1]['tag'].split('-')[0] in ('NR','SN','MM')
    return False

def choose_entry(entries,tag,lemma,reason,raw,index,sense=None):
    compatible=[e for e in entries if compatible_entry(e,tag,lemma,reason,raw,index)]
    if tag in ('NNB','NNG') and index>0 and raw[index-1]['tag'].split('-')[0] in ('NR','SN','MM'):
        counters=[e for e in compatible if e['pos']=='counter']
        if counters:compatible=counters
    if sense is not None:compatible=[e for e in compatible if e['sense']==sense]
    return compatible[0] if len(compatible)==1 else None

def contextual_sense(text,token,lemma):
    """Small positive evidence rules, not a global dictionary sense default."""
    left=max(text.rfind(c,0,token['start']) for c in '.!?\n')+1
    ends=[p for c in '.!?\n' if (p:=text.find(c,token['start']))>=0]
    clause=text[left:min(ends) if ends else len(text)]
    rules={
        '눈':{'eye':r'눈물|눈[^.!?]*(?:아파|아프|감아|감고)|(?:울|얼굴)', 'snow':r'눈[^.!?]*(?:와요|왔어요|올 거)|겨울|춥'},
        '풀':{'glue':r'붙이|붙여|종이|테이프', 'grass':r'나무|공원|꽃'},
        '다리':{'leg':r'아파|아프|다치|몸|다리[^.!?]*움직', 'bridge':r'건너|강|다리[^.!?]*(?:지나|위)'},
        '배':{'belly':r'아파|아프|배고|몸', 'pear':r'먹|과일|사과'}
    }
    matches=[s for s,p in rules.get(lemma,{}).items() if re.search(p,clause)]
    return matches[0] if len(matches)==1 else None

def predicate_context_conflict(text,token,lemma,tag):
    if lemma!='쓰다' or tag!='VV':return False
    left=max(text.rfind(c,0,token['start']) for c in '.!?\n')+1
    prefix=text[left:token['start']]
    return bool(re.search(r'(?:약|커피|차|음식)(?:이|가)\s+(?:(?:너무|아주|정말)\s+)?$',prefix))

def make_kiwi():return Kiwi(num_workers=1)

def morphology(text,kiwi):
    return [dict(form=t.form,tag=t.tag,start=t.start,length=t.len) for t in kiwi.tokenize(text)]

def analyze(text,files,text_number,scheduled_review,overrides=None,kiwi=None):
    kiwi=kiwi or make_kiwi();raw=morphology(text,kiwi);overrides=overrides or {}
    vocab=files['core_vocab.json']+files['expansion_vocab.json']
    proper={e['lemma']:e for e in files['proper_names.json']['entries']}
    by_lemma=defaultdict(list)
    for e in vocab:by_lemma[e['lemma']].append(e)
    first={vid:r['text'] for r in files['introduction_schedule.json']['rows'] for vid in r['entry_ids']}
    annotations=[];issues=[];grammar=set();consumed=set();unresolved=[];decisions=[]
    words=list(re.finditer(r'\S+',text))
    def annotate(indices,entry=None,lemma=None,grammar_id=None,reason=None):
        ts=[raw[i] for i in indices];start=min(t['start'] for t in ts);end=max(t['start']+t['length'] for t in ts)
        end=max(start+1,end);end=min(len(text),end)
        if grammar_id:
            grammar.add(grammar_id);role='grammar_function';pos=None;sense=None;vid=None
        elif entry:
            role='core' if entry['tier']=='core' else 'current_new_expansion' if first[entry['id']]==text_number else 'scheduled_review' if entry['id'] in scheduled_review else 'previous_expansion'
            pos=entry['pos'];sense=entry['sense'];vid=entry['id'];lemma=entry['lemma']
        elif lemma in proper:role='proper_name';pos='noun';sense=proper[lemma]['kind'];vid=None
        else:role='unresolved';pos=None;sense=None;vid=None
        item=dict(surface=text[start:end],lemma=lemma,pos=pos,sense=sense,vocab_id=vid,role=role,
                  start=start,end=end,morph_indices=indices,grammar_id=grammar_id)
        annotations.append(item);consumed.update(indices)
        if reason:issues.append(dict(type=reason,surface=item['surface'],lemma=lemma,start=start,candidate_id=vid))
        if vid in files['profile.json'].get('lexical_sense_policy',{}).get('context_review_required_ids',[]):
            issues.append(dict(type='restricted_sense_context_review',surface=item['surface'],lemma=lemma,
                               start=start,candidate_id=vid))
        if not entry and not grammar_id and role=='unresolved':unresolved.append(item)
    for exception in files['lexical_exceptions.json']['entries']:
        if exception['kind']!='frozen_exception':continue
        for match in re.finditer(r'(?:(?<!\S)|(?<=["“‘]))'+re.escape(exception['form'])+r'(?=$|[\s.!?"”’])',text):
            indices=[i for i,t in enumerate(raw) if match.start()<=t['start']<match.end()]
            annotations.append(dict(surface=match.group(),lemma=exception['form'],pos='interjection',sense='fixed_expression',
                vocab_id=None,role='frozen_exception',start=match.start(),end=match.end(),morph_indices=indices,grammar_id=None,
                exception_id=exception['id']))
            consumed.update(indices)
            issues.append(dict(type='frozen_span_resolution',surface=match.group(),lemma=exception['form'],start=match.start(),candidate_id=exception['id']))
    for word in words:
        indices=[i for i,t in enumerate(raw) if word.start()<=t['start']<word.end() and i not in consumed]
        content=[i for i in indices if raw[i]['tag'].split('-')[0] in ('NNG','NNP','NNB','NP','NR','MM','MAG','MAJ','IC','VV','VA','SN','XR')]
        nominal_suffixes=[i for i in indices if raw[i]['tag']=='XSN']
        if len(content)==1 and nominal_suffixes and raw[content[0]]['tag'].split('-')[0] in ('NNG','NNP'):
            group=content+nominal_suffixes;lemma=''.join(raw[i]['form'] for i in group)
            entries=by_lemma.get(lemma,[])
            entries=[e for e in entries if e['pos']=='noun']
            if len(entries)==1 and group==list(range(min(group),max(group)+1)):
                annotate(group,entries[0],lemma,reason='registered_nominal_suffix_group');content=[]
        signature=[raw[i]['form'] for i in indices if raw[i]['tag'] not in ('EF','SF','EP')]
        exchange={'돕':'도와주다','빌리':'빌려주다','돌리':'돌려주다'}
        valid_exchange_surface=bool(signature and signature[0] in exchange and word.group().lstrip('"“‘').startswith({'돕':'도와','빌리':'빌려','돌리':'돌려'}[signature[0]]))
        if len(signature)==3 and signature[0] in exchange and signature[1:]==['어','주'] and valid_exchange_surface and [raw[i]['tag'].split('-')[0] for i in indices if raw[i]['tag'] not in ('EF','SF','EP')]==['VV','EC','VX']:
            group=[i for i in indices if raw[i]['tag'] not in ('EF','SF','EP')]
            lemma=exchange[signature[0]]
            entries=[e for e in by_lemma.get(lemma,[]) if e['pos']=='verb']
            if len(entries)==1:annotate(group,entries[0],lemma,reason='registered_exchange_group');content=[]
        if signature in (['좋','어','하'],['싫','어','하']) and [raw[i]['tag'].split('-')[0] for i in indices if raw[i]['tag'] not in ('EF','SF','EP')]==['VA','EC','XSV']:
            group=[i for i in indices if raw[i]['tag'] not in ('EF','SF','EP')]
            lemma='좋아하다' if signature[0]=='좋' else '싫어하다'
            entries=[e for e in by_lemma.get(lemma,[]) if e['pos']=='verb']
            if len(entries)==1:annotate(group,entries[0],lemma,reason='registered_liking_group');content=[]
        if word.group().startswith('누군가'):
            group=[i for i in indices if raw[i]['form'] in ('누구','ᆫ가')]
            entries=[e for e in by_lemma.get('누군가',[]) if e['pos']=='pronoun']
            if len(group)==2 and len(entries)==1 and raw[group[0]]['tag']=='NP' and raw[group[1]]['tag']=='EF':
                annotate(group,entries[0],'누군가',reason='registered_pronoun_group');content=[i for i in content if i not in group]
        if len(content)>1:
            lemma=''.join(raw[i]['form'] for i in content)+'다'
            entries=by_lemma.get(lemma,[])
            last_tag=raw[content[-1]]['tag'].split('-')[0]
            entries=[e for e in entries if e['pos'] in TAG_POS.get(last_tag,set())]
            adjacent=content==list(range(min(content),max(content)+1))
            valid_prefix=all(raw[i]['tag'].split('-')[0] in ('NNG','XR','VV','VA') for i in content[:-1])
            if len(entries)==1 and adjacent and valid_prefix and last_tag in ('VV','VA'):
                annotate(content,entries[0],lemma,reason='compound_grouping');content=[]
        # Kiwi analyses 공부하-/NNG+XSV as a dictionary compound, not two tokens.
        suffixes=[i for i in indices if raw[i]['tag'] in ('XSV','XSA')]
        if len(content)==1 and suffixes and raw[content[0]]['tag'] in ('NNG','XR'):
            group=content+suffixes
            lemma=''.join(raw[i]['form'] for i in group)+'다'
            entries=by_lemma.get(lemma,[])
            expected='verb' if raw[suffixes[0]]['tag']=='XSV' else 'adjective'
            entries=[e for e in entries if e['pos']==expected]
            contiguous=group==list(range(min(group),max(group)+1)) and len(suffixes)==1
            # N + 하고 may be missegmented as N + 하/XSV + 고/EC.
            # A registered food enumeration with an overt second object and
            # a licensed eating/liking predicate is independent local evidence.
            after=text[word.end():].split('.')[0].split('?')[0].split('!')[0]
            next_tokens=[j for j,t in enumerate(raw) if word.end()<=t['start']<word.end()+len(after)]
            second=next_tokens[:2]
            object_pair=len(second)==2 and raw[second[0]]['tag'].split('-')[0]=='NNG' and raw[second[1]]['tag']=='JKO'
            first_food=any(e['pos']=='noun' and 'food' in e['tags'] for e in by_lemma.get(raw[content[0]]['form'],[]))
            second_food=object_pair and any(e['pos']=='noun' and 'food' in e['tags'] for e in by_lemma.get(raw[second[0]]['form'],[]))
            predicate=any((t['form'] in ('먹','마시','좋아하','싫어하') and t['tag'].split('-')[0]=='VV') for t in raw if word.end()<=t['start']<word.end()+len(after))
            ending=[i for i in indices if raw[i]['form']=='고' and raw[i]['tag']=='EC']
            nominal_resegment=not entries and contiguous and raw[suffixes[0]]['form']=='하' and ending==[max(group)+1] and first_food and second_food and predicate and word.group().strip('“”".,!?').endswith('하고')
            if nominal_resegment:
                i=content[0];noun_entries=[e for e in by_lemma[raw[i]['form']] if e['pos']=='noun']
                entry=choose_entry(noun_entries,'NNG',raw[i]['form'],None,raw,i)
                annotate([i],entry,raw[i]['form'],reason='nominal_particle_resegmentation')
                annotate(suffixes+ending,grammar_id='ko_k1_g25',reason='nominal_particle_resegmentation')
                decisions.append(dict(type='noun_hago_boundary',surface=word.group(),lemma=raw[i]['form'],status='RESOLVED',
                    evidence=dict(raw_noun=True,registered_compound=False,second_food_object=True,registered_food_predicate=True),raw_indices=group+ending))
                content=[]
            elif len(entries)==1 and contiguous:
                annotate(group,entries[0],lemma,reason='registered_hada_group');content=[]
            else:
                annotate(group,None,lemma,reason='unsupported_compound_boundary');content=[]
                decisions.append(dict(type='compound_boundary',surface=word.group(),lemma=lemma,start=word.start(),status='REVIEW',requires_candidate_review=True))
        for i in content:
            token=raw[i];tag=token['tag'].split('-')[0];form=token['form']
            lemma,alias_reason,identity_supported=identity_candidate(raw,i,text)
            if predicate_context_conflict(text,token,lemma,tag):
                identity_supported=False;alias_reason='predicate_pos_context_conflict'
            if tag in ('VV','VA') and form in ('있','없') and i>0 and raw[i-1]['form']=='수':
                annotate([i],grammar_id='ko_k1_g16',reason='grammar_content_boundary');continue
            if tag in ('VV','VA') and form=='하' and i>0 and raw[i-1]['form'] in ('어야','아야'):
                annotate([i],grammar_id='ko_k1_g17',reason='grammar_content_boundary');continue
            # Listed ability/future bound nouns are excluded only in their exact construction.
            if tag=='NNB' and form in ('수','거','것'):
                left=text[max(0,word.start()-16):word.start()];right=text[word.end():word.end()+14]
                if form=='수' and re.search(r'(을|ㄹ|갈|할|볼|올|줄|읽을|먹을|탈)\s*$',left) and re.match(r'\s+(있|없)',right):
                    annotate([i],grammar_id='ko_k1_g16',reason='grammar_content_boundary');continue
                if form=='거' and word.group().startswith('거예요'):
                    annotate([i],grammar_id='ko_k1_g04',reason='grammar_content_boundary');continue
            # 안/못 are grammar negation, not free adverbs.
            if form in ('안','못') and tag=='MAG':
                annotate([i],grammar_id='ko_k1_g07' if form=='안' else 'ko_k1_g08',reason='grammar_content_boundary');continue
            entries=by_lemma.get(lemma,[])
            context_sense=None
            for override_key,intended in overrides.items():
                if not override_key.endswith('::'+lemma):continue
                clause=override_key[:-(len(lemma)+2)];start=text.find(clause)
                if start>=0 and start<=token['start']<start+len(clause):context_sense=intended
            # Generated sense suggestions cannot bypass POS/morphology evidence.
            compatible=[e for e in entries if compatible_entry(e,tag,lemma,alias_reason,raw,i)]
            intended=contextual_sense(text,token,lemma) if len(compatible)>1 else None
            # Suggestions must agree with independently visible local evidence;
            # an author cannot resolve a homograph merely by naming a sense.
            suggestion=context_sense or overrides.get(lemma)
            if suggestion is not None and suggestion!=intended and len(compatible)>1:identity_supported=False
            entry=choose_entry(entries,tag,lemma,alias_reason,raw,i,intended) if identity_supported else None
            reason=alias_reason or ('sense_disambiguation' if len(by_lemma.get(lemma,[]))>1 else 'bound_noun_or_counter' if tag=='NNB' else None)
            if not identity_supported or (entries and not entry):
                reason='identity_evidence_insufficient'
                decisions.append(dict(type='identity_boundary',surface=text[token['start']:token['start']+token['length']],
                    lemma=lemma,start=token['start'],raw_pos=tag,registered_candidates=[dict(id=e['id'],pos=e['pos'],sense=e['sense']) for e in entries],
                    alias_reason=alias_reason,status='REVIEW',requires_candidate_review=True))
            if lemma=='흘리다' and '눈물' in text[max(0,word.start()-15):word.start()]:reason='sense_extension_review'
            if form=='제' and i+1<len(raw) and raw[i+1]['tag']=='JKS':reason='contracted_pronoun'
            if form=='다른' and entry:grammar.add('ko_k1_g26')
            annotate([i],entry,lemma,reason=reason)
        for i in indices:
            if i in consumed:continue
            t=raw[i];tag=t['tag'];f=t['form'];gid=None
            if tag.startswith('S') and tag!='SN':consumed.add(i);continue
            if tag.startswith('J'):gid=PARTICLES.get(f)
            elif tag=='VCP':gid='01'
            elif tag=='VCN':
                entries=[e for e in by_lemma['아니다'] if e['pos']=='adjective']
                annotate([i],entries[0] if len(entries)==1 else None,'아니다');continue
            elif tag=='EP' and f in ('었','았','였'):gid='03'
            elif tag=='EP' and f=='시' and word.group().rstrip('.!?').endswith('세요'):gid='14'
            elif tag=='EF' and f in ('ㄹ까요','을까요','ᆯ까요'):gid='15'
            elif tag=='EF' and f in ('예요','에요'):gid='01'
            elif tag=='EF' and f in ('어요','아요','여요','어','아'):gid='02'
            elif tag=='EC':
                gid={'고':'09','지만':'10','어서':'11','아서':'11','여서':'11','라서':'11','니까':'12','으니까':'12','면':'13','으면':'13','어야':'17','아야':'17'}.get(f)
                if f=='고' and i+1<len(raw) and raw[i+1]['tag']=='VX':gid={'싶':'06','있':'05'}.get(raw[i+1]['form'],gid)
                if f in ('어','아') and i+1<len(raw) and raw[i+1]['tag']=='VX' and raw[i+1]['form']=='보':gid='18'
            elif tag=='VX' and f=='싶' and i>0 and raw[i-1]['form']=='고':gid='06'
            elif tag=='VX' and f=='있' and i>0 and raw[i-1]['form']=='고':gid='05'
            elif tag=='VX' and f=='보' and i>0 and raw[i-1]['form'] in ('어','아'):gid='18'
            elif tag=='ETM':
                gid='27' if f=='는' else '26' if f in ('ㄴ','은','ᆫ') and i>0 and raw[i-1]['tag'].split('-')[0] in ('VA','XSA') else None
                if f in ('ㄹ','을','ᆯ') and i+1<len(raw):gid='16' if raw[i+1]['form']=='수' else '04' if raw[i+1]['form']=='거' else None
            if gid:annotate([i],grammar_id='ko_k1_g'+gid)
            else:annotate([i],lemma=f,reason='unapproved_or_unresolved_grammar')
    for i,t in enumerate(raw):
        if i not in consumed:annotate([i],lemma=t['form'],reason='unaccounted_morpheme')
    return dict(annotations=sorted(annotations,key=lambda a:(a['start'],a['morph_indices'][0])),
                raw_morphology=raw,grammar_used=sorted(grammar),annotation_review_required=issues,unresolved_tokens=unresolved,
                boundary_decisions=decisions)
