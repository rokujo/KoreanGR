"""Build only the 20 authored pilot scenes and generated annotation hypotheses."""
import json
from pathlib import Path
from select_k1_pilot import ROOT,load_inputs,select
from k1_pilot_analysis import analyze,make_kiwi
from validate_k1_pilot import PILOT,text_metrics,token_stream,check_freeze
from lexical_coverage import evaluate_lexical_tokens

def build():
    from k1_history import protect_historical_build
    protect_historical_build(Path(__file__).resolve().parents[1])
    assert not check_freeze(),check_freeze()
    files=load_inputs();selection=select(files);kiwi=make_kiwi()
    vocab={e['id']:e for e in files['core_vocab.json']+files['expansion_vocab.json']}
    first={e['vocab_id']:e['first_introduction_text'] for e in files['vocab_exposure_schedule.json']['entries']}
    scenes=json.loads((PILOT/'authored_scenes.json').read_text(encoding='utf-8'))
    (PILOT/'texts').mkdir(exist_ok=True)
    records=[]
    for scene in scenes:
        t=selection['selection_keys'][scene['selection_key']];row=files['vocab_exposure_schedule.json']['texts'][t-1]
        def paragraphs(lines):return '\n\n'.join(' '.join(lines[i:i+7]) for i in range(0,len(lines),7))
        text=paragraphs(scene['sentences']);analysis=analyze(text,files,t,row['review_vocab_ids'],scene.get('sense_overrides'),kiwi)
        used={a['vocab_id'] for a in analysis['annotations'] if a['vocab_id']}
        actual_new=sorted(used&set(row['new_vocab_ids']));actual_review=sorted(used&set(row['review_vocab_ids']))
        conflicts=[]
        for vid in set(row['new_vocab_ids']+row['review_vocab_ids'])-used:
            e=vocab[vid];declared=[o for o in scene['omit_reviews'] if (o['lemma'],o['sense'])==(e['lemma'],e['sense'])]
            reason=declared[0]['reason'] if declared else '予定語と本文の使用義が一致しない。意味を偽って予定に合わせない。'
            candidates=[]
            for other in files['vocab_exposure_schedule.json']['texts']:
                n=other['text']
                if n in selection['text_numbers'] or n<=first[vid] or n==t or vid in other['review_vocab_ids'] or vid in other['new_vocab_ids']:continue
                score=sum(len(set(e['tags'])&set(vocab[x]['tags'])) for x in other['new_vocab_ids']+other['review_vocab_ids'])
                candidates.append((-score,other['total_scheduled_expansion_count'],abs(n-t),n))
            proposed=[x[3] for x in sorted(candidates)[:3]]
            conflicts.append(dict(type='semantic_schedule_conflict',vocab_id=vid,lemma=e['lemma'],sense=e['sense'],reason=reason,
                proposed_text_candidates=proposed,proposal_status='candidate_only_schedule_unchanged',
                proposal_notes='タグの場面適合候補。移動後の距離・6教材・他語負荷・本文の意味を人間が再検証する。'))
        coverage=evaluate_lexical_tokens(token_stream(analysis['annotations']),t,files);metrics=text_metrics(text)
        flags=dict(vocab_pass=coverage['ok'],grammar_pass=not any(x['type']=='unapproved_or_unresolved_grammar' for x in analysis['annotation_review_required']),length_pass=120<=metrics['eojeol_count']<=180,
            sentence_length_pass=metrics['max_sentence_eojeol']<=10,schedule_pass=not conflicts,naturalness_review_required=True)
        record=dict(id=f'K1-{t:03}',text_number=t,title_ko=scene['title_ko'],genre=scene['genre'],text_ko=text,
            translation_ja=paragraphs(scene['translations']),scheduled_new_vocab_ids=row['new_vocab_ids'],scheduled_review_vocab_ids=row['review_vocab_ids'],
            actually_used_new_vocab_ids=actual_new,actually_used_review_vocab_ids=actual_review,
            extra_previous_vocab_ids=sorted(vid for vid in used if vid in first and first[vid]<t and vid not in row['review_vocab_ids']),
            grammar_used=analysis['grammar_used'],eojeol_count=metrics['eojeol_count'],sentence_count=metrics['sentence_count'],max_sentence_eojeol=metrics['max_sentence_eojeol'],
            coverage=dict(denominator_N=coverage['N'],new_tokens_U=coverage['U'],controlled_vocab_coverage=coverage['controlled_vocab_coverage'],
                previous_vocab_coverage=coverage['previous_vocab_coverage'],target_99_met=coverage['previous_vocab_coverage']>=.99),
            validation=flags,semantic_schedule_conflicts=sorted(conflicts,key=lambda c:c['vocab_id']),
            notes=[scene['comment'],'過去Expansionの導入状態はfreezeした全300本予定の仮定。パイロット20本だけの実導入履歴ではない。',
                   '本文だけをN/Uの対象にする。titleは別に許可語・文法を照合。日本語訳は制限外。',
                   '동생は性別を明示しない語。作者設定と自然な日本語訳では弟を想定した。韓国語から性別が確定したという意味ではない。'],
            annotation_origin='Kiwi morphology + generated rule-normalization hypotheses; not gold',
            sense_overrides=scene.get('sense_overrides',{}),**{k:analysis[k] for k in ('annotations','raw_morphology','annotation_review_required','unresolved_tokens')})
        (PILOT/'texts'/f'K1-{t:03}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');records.append(record)
    (PILOT/'selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert sorted(r['text_number'] for r in records)==selection['text_numbers']
    print('Built',len(records),'pilot texts; frozen inputs unchanged.')

if __name__=='__main__':build()
