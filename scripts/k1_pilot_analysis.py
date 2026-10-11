"""Kiwi morphology evidence + deliberately limited rules; no automatic sense truth.

The morpheme stream is reproducible evidence. Compound grouping and sense choices
remain generated hypotheses and are flagged independently for human review.
"""
from collections import defaultdict
import re
from kiwipiepy import Kiwi

PARTICLES={'은':'19','는':'19','이':'20','가':'20','을':'21','를':'21','에':'22','에서':'23',
           '도':'24','하고':'25','에게':'28','한테':'28','의':'29','로':'30','으로':'30','부터':'31','까지':'31','만':'32'}
DEFAULT_SENSE={'저':'i_humble','일':'work','눈':'eye','개':'dog','쓰다':'write','찍다':'take_photo',
               '이':'this','팔':'arm','봉지':'bag_packet','달':'month_duration','다리':'leg','배':'belly','풀':'grass','새':'new_attributive'}
TAG_POS={'NP':{'pronoun'},'MM':{'determiner','numeral'},'SN':{'numeral'},'NR':{'numeral'},
         'VV':{'verb'},'VA':{'adjective'},'MAG':{'adverb','conjunction'},'MAJ':{'conjunction','adverb'},'IC':{'interjection'}}
ALIASES={'이거':'이것','그거':'그것','저거':'저것','내':'나','네':'너','제':'저','한':'하나','두':'둘','세':'셋','네_numeral':'넷','스무':'스물','다른':'다르다'}

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
    annotations=[];issues=[];grammar=set();consumed=set();unresolved=[]
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
        for match in re.finditer(r'(?<!\S)'+re.escape(exception['form'])+r'(?=$|[\s.!?])',text):
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
        if len(content)==1 and nominal_suffixes:
            group=content+nominal_suffixes;lemma=''.join(raw[i]['form'] for i in group)
            entries=by_lemma.get(lemma,[])
            if len(entries)==1:annotate(group,entries[0],lemma,reason='compound_grouping');content=[]
        signature=[raw[i]['form'] for i in indices if raw[i]['tag'] not in ('EF','SF','EP')]
        exchange={'돕':'도와주다','빌리':'빌려주다','돌리':'돌려주다'}
        if len(signature)==3 and signature[0] in exchange and signature[1:]==['어','주']:
            group=[i for i in indices if raw[i]['tag'] not in ('EF','SF','EP')]
            lemma=exchange[signature[0]]
            annotate(group,by_lemma[lemma][0],lemma,reason='compound_grouping');content=[]
        if signature in (['좋','어','하'],['싫','어','하']):
            group=[i for i in indices if raw[i]['tag'] not in ('EF','SF','EP')]
            lemma='좋아하다' if signature[0]=='좋' else '싫어하다'
            annotate(group,by_lemma[lemma][0],lemma,reason='compound_grouping');content=[]
        if word.group().startswith('누군가'):
            group=[i for i in indices if raw[i]['form'] in ('누구','ᆫ가')]
            if len(group)==2:
                annotate(group,by_lemma['누군가'][0],'누군가',reason='compound_grouping');content=[i for i in content if i not in group]
        if len(content)>1:
            lemma=''.join(raw[i]['form'] for i in content)+'다'
            entries=by_lemma.get(lemma,[])
            if len(entries)==1 and raw[content[-1]]['tag'].split('-')[0] in ('VV','VA'):
                annotate(content,entries[0],lemma,reason='compound_grouping');content=[]
        # Kiwi analyses 공부하-/NNG+XSV as a dictionary compound, not two tokens.
        suffixes=[i for i in indices if raw[i]['tag'] in ('XSV','XSA')]
        if len(content)==1 and suffixes and raw[content[0]]['tag'] in ('NNG','XR'):
            group=content+suffixes
            lemma=''.join(raw[i]['form'] for i in group)+'다'
            content=[]
            entries=by_lemma.get(lemma,[])
            annotate(group,entries[0] if len(entries)==1 else None,lemma,reason='compound_grouping')
        for i in content:
            token=raw[i];tag=token['tag'].split('-')[0];form=token['form']
            lemma=ALIASES.get(form,form)
            if tag in ('VV','VA'):lemma=form+'다'
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
            compatible=[e for e in entries if e['pos'] in TAG_POS.get(tag,{'noun','counter','pronoun','numeral'})]
            if context_sense:
                entries=[e for e in entries if e['sense']==context_sense]
            elif compatible:entries=compatible
            # Exceptions: dictionary POS differs from Sejong verb/adjective analysis for 있다/없다/필요하다.
            if len(entries)>1:
                intended=overrides.get(lemma,DEFAULT_SENSE.get(lemma))
                selected=[e for e in entries if e['sense']==intended]
                entry=selected[0] if len(selected)==1 else None
            else:entry=entries[0] if entries else None
            reason='sense_disambiguation' if len(by_lemma.get(lemma,[]))>1 else 'bound_noun_or_counter' if tag=='NNB' else None
            if context_sense and entry and entry not in compatible:reason='Kiwi_POS_sense_disagreement'
            if lemma=='흘리다' and '눈물' in text[max(0,word.start()-15):word.start()]:reason='sense_extension_review'
            if form in ('내','제'):reason='contracted_possessive'
            if form=='제' and i+1<len(raw) and raw[i+1]['tag']=='JKS':reason='contracted_pronoun'
            if form=='다른':reason='attributive_pos_boundary';grammar.add('ko_k1_g26')
            annotate([i],entry,lemma,reason=reason)
        for i in indices:
            if i in consumed:continue
            t=raw[i];tag=t['tag'];f=t['form'];gid=None
            if tag.startswith('S') and tag!='SN':consumed.add(i);continue
            if tag.startswith('J'):gid=PARTICLES.get(f)
            elif tag=='VCP':gid='01'
            elif tag=='VCN':
                entries=by_lemma['아니다'];annotate([i],entries[0],'아니다');continue
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
                raw_morphology=raw,grammar_used=sorted(grammar),annotation_review_required=issues,unresolved_tokens=unresolved)
