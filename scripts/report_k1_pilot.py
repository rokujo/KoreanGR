"""Revalidate the final pilot and render human review and aggregate evidence."""
from collections import Counter
import json
import re
import statistics
from pathlib import Path
from select_k1_pilot import ROOT,load_inputs,select
from validate_k1_pilot import PILOT,validate

def main():
    from k1_history import protect_historical_build
    protect_historical_build(Path(__file__).resolve().parents[1])
    files=load_inputs();selected=select(files);result=validate();records={}
    for path in sorted((PILOT/'texts').glob('K1-*.json')):
        record=json.loads(path.read_text(encoding='utf-8'));records[record['text_number']]=record
    vocab={e['id']:e for e in files['core_vocab.json']+files['expansion_vocab.json']}
    grammar={e['id']:e['form'] for e in files['grammar.json']}
    def words(ids):return '、'.join(f"{vocab[x]['lemma']}（{vocab[x]['gloss_ja']} / {x}）" for x in ids) or 'なし'
    review=['# K1 Phase 2 パイロット本文・人間レビュー用','',
        '20本のみ。自己評価と機械判定は母語話者レビューの代替ではありません。語義・複合語・文法機能のannotationは仮説です。',
        'PASSは構造・許可条件の暫定判定。予定語を省いた教材は、言語hard条件が通っても総合FAILにしています。',
        '過去語の導入状態はPhase 1.2の予定を仮定しています。20本だけで全語を実導入したという意味ではありません。',
        '日本語訳では作者設定により동생を「弟」としました。韓国語の語そのものは性別を明示しません。','']
    by_result={r['text_number']:r for r in result['results']}
    for t,record in records.items():
        r=by_result[t];c=record['coverage'];conflicts=record['semantic_schedule_conflicts']
        review.extend([f'## K1-{t:03}', '',f"**{record['title_ko']}** — {record['genre']}",'',
            '### 韓国語本文','',record['text_ko'],'','### 日本語訳','',record['translation_ja'],'',
            '### 語彙・検証','',f"- 新出予定／実使用: {words(record['scheduled_new_vocab_ids'])} / {words(record['actually_used_new_vocab_ids'])}",
            f"- review予定: {words(record['scheduled_review_vocab_ids'])}",f"- 実使用review: {words(record['actually_used_review_vocab_ids'])}",
            f"- 予定外の導入済みExpansion: {words(record['extra_previous_vocab_ids'])}",
            f"- N={c['denominator_N']}、U={c['new_tokens_U']}、controlled={c['controlled_vocab_coverage']:.2%}、previous={c['previous_vocab_coverage']:.3%}、target99達成={c['target_99_met']}",
            f"- {record['eojeol_count']} 어절 / {record['sentence_count']}文 / 一文最大{record['max_sentence_eojeol']} 어절。4〜7範囲外の文: {r['metrics']['preferred_sentence_outliers'] or 'なし'}",
            '- 使用文法: '+ '、'.join(grammar[g] for g in record['grammar_used']),
            f"- 総合判定: **{r['status']}** / 言語hard条件とtargetだけの判定: {r['language_status']}",
            f"- 検証フラグ: `{json.dumps(record['validation'],ensure_ascii=False)}`",
            f"- hardエラー: {r['errors'] or 'なし'} / 注意: {r['warnings'] or 'なし'}",'',
            '### 自己評価（要人間確認）','',
            '- 自然さ: '+record['notes'][0],
            f"- K1としての簡単さ: 一文最大{record['max_sentence_eojeol']}語。Coreの主語・動作を反復し、時系列を短い文で追う構成。語義の理解容易さは未測定。",
            f"- scheduled語の詰め込み感: 予定{r['scheduled_expansion_count']}語中{r['used_scheduled_expansion_count']}語を使用。"+('省略理由を下記に記録。' if conflicts else '全語を使用したが、場面の切替や副次的事件の必要性は人間が確認する。'),
            '- 不自然な言い換え: 未登録の基本語を別義で代用しない方針。紙・場所などの広い指示語、過剰な本当に／少しの挿入が読みを止めないか確認する。',
            '- 文法難度: 上記の許可文法だけを認識。長い連体修飾や理由節は初心者が順に処理できるか確認する。',
            f"- annotation ambiguity: {r['annotation_ambiguity_occurrences']}出現、{r['annotation_ambiguity_types']}組のtype+lemma。未解決token={r['unresolved_token_count']}。曖昧候補は下記で明示。",'',
            '### semantic_schedule_conflicts',''])
        if conflicts:
            review.extend(['|語・ID|問題|移動候補（未適用）|','|---|---|---|'])
            for conflict in conflicts:
                review.append(f"|{conflict['lemma']} / {conflict['vocab_id']}|{conflict['reason']}|"+', '.join(f'K1-{n:03}' for n in conflict['proposed_text_candidates'])+'|')
        else:review.append('なし。')
        issue_types=Counter((a['type'],a['lemma']) for a in record['annotation_review_required'])
        review.extend(['','### annotation_review_required','', '|type|lemma|出現数|','|---|---|---:|'])
        for (kind,lemma),count in sorted(issue_types.items(),key=lambda x:str(x[0])):review.append(f'|{kind}|{lemma}|{count}|')
        review.extend(['',f"完全なsurface・offset・lemma・POS・sense・ID・raw解析: [K1-{t:03}.json](../pilot/ko/k1/texts/K1-{t:03}.json)",''])
    (ROOT/'reports/k1_phase2_pilot_review.md').write_text('\n'.join(review)+'\n',encoding='utf-8')
    lengths=[r['eojeol_count'] for r in records.values()];ratios=[r['coverage']['previous_vocab_coverage'] for r in records.values()]
    load12=[r for r in result['results'] if 12<=r['scheduled_expansion_count']<=13]
    summary=dict(text_numbers=selected['text_numbers'],counts=result['counts'],language_counts=result['language_counts'],
        mean_eojeol=round(statistics.mean(lengths),3),min_eojeol=min(lengths),max_eojeol=max(lengths),
        previous_coverage=dict(min=min(ratios),max=max(ratios),mean=statistics.mean(ratios),median=statistics.median(ratios)),
        controlled_violation_texts=sum(r['coverage']['controlled_vocab_coverage']!=1 for r in result['results']),
        grammar_violation_texts=sum(not r['validation']['grammar_pass'] for r in result['results']),
        semantic_schedule_conflicts=result['semantic_schedule_conflict_count'],conflict_texts=result['schedule_conflict_texts'],
        annotation_ambiguity_occurrences=sum(r['annotation_ambiguity_occurrences'] for r in result['results']),
        annotation_ambiguity_type_lemma_text_groups=sum(r['annotation_ambiguity_types'] for r in result['results']),
        unresolved_tokens=sum(r['unresolved_token_count'] for r in result['results']),
        scheduled_12_13_texts=len(load12),scheduled_12_13_complete=sum(r['validation']['schedule_pass'] for r in load12),
        scheduled_entry_text_pairs=sum(r['scheduled_expansion_count'] for r in result['results']),
        realized_scheduled_entry_text_pairs=sum(r['used_scheduled_expansion_count'] for r in result['results']),
        mass_generation_ready=False,naturalness_human_approved=False)
    result['aggregate']=summary
    (ROOT/'reports/k1_phase2_pilot_validation_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=['# 韓国語 K1 Phase 2 少数本文生成・検証パイロット','', '作業日: 2026-10-10。生成は20本だけ。K1全300本文の生成・K2設計・UI・TTSは行っていない。','',
        '**大量生成へは現時点で進めない。** 語彙・文法・長さのhard条件は20本で成立したが、予定語の意味的な適合と人間による語義・自然さの確認が残る。','',
        '## 1. freezeと対象選定','',
        'Phase 1.2のconfig JSON16ファイル、既存実装6ファイル、既存テスト2ファイルをSHA-256で固定した。`k1_phase2_input_freeze.json` とvalidatorで一致を確認。Core300 / Expansion500 / Total800、Tier200/200/100、文法32、7組入替、ID migration、coverage policy、両scheduleを変更していない。','',
        '教材番号: '+', '.join(f'K1-{n:03}' for n in selected['text_numbers'])+'。',
        '新7語とmedium5語は全て初出教材を選んだ。番号はselect_k1_pilot.pyがmigration・confidence・scheduleから読み取る。初期E1、E2初出、中盤、新出0/1/2、高速期の最初・新7語reviewが多い回・後期を追加した。後期の番号を語ごとの定数にしていない。',
        '未生成の過去教材が導入済みであるという番号状態を仮定して、未導入語の混入を検査した。20本だけで学習者にその語彙を導入した実験ではない。','',
        '## 2. 判定・coverage・長さ','',
        f"総合: PASS={summary['counts']['PASS']} / FAIL={summary['counts']['FAIL']} / PASS_WITH_TARGET_MISS={summary['counts']['PASS_WITH_TARGET_MISS']}。",
        '総合FAILにはscheduled語の省略を含む。語彙・文法・長さ・一文hard上限・98%だけの判定では全20本が通り、target99達成6本 / 未達14本。PASSはannotation仮説が正しいという条件付きで、自然さの合格ではない。',
        f"平均{summary['mean_eojeol']:.2f} 어절、範囲{summary['min_eojeol']}〜{summary['max_eojeol']}。controlled違反{summary['controlled_violation_texts']}本、認識可能な文法違反{summary['grammar_violation_texts']}本、hardエラー教材{result['hard_error_texts']}本。",
        f"previous coverage: min {min(ratios):.3%} / max {max(ratios):.3%} / mean {statistics.mean(ratios):.3%} / median {statistics.median(ratios):.3%}。",
        '全教材の新出は0〜2 lemma。2語導入は各1回、1語導入は1回。soft3超過なし。Nは本文の内容語・意味単位token総数で、助詞・語尾・許可文法機能・句読点を除く。複合lemmaは登録単位、固定句は一致span単位。未許可・未解決内容語を分母から除かない。Uは現在初出エントリの出現総数。titleはN/Uの外で別に語彙・文法を照合した。',
        '2語導入では99%にN≥200が必要。今回のNは120〜135程度で、自然な120〜180어절本文は99%に届かなかった。3 tokenまでを一律に許すこともせず、floor(N/50)を優先した。target missを隠さず、hard98%合格と区別する。',
        'K1-184には自然な人物紹介の3어절文が1文ある。4〜7はpreferredなので警告、hard10以内ならFAILにしない。機械的な語数のための副詞追加を避けた。','',
        '|教材|新出|review予定|予定Expansion|使用予定語|어절|N/U|previous|総合|','|---|---:|---:|---:|---:|---:|---|---:|---|']
    for r in result['results']:
        record=records[r['text_number']];c=r['coverage']
        report.append(f"|{r['id']}|{len(record['scheduled_new_vocab_ids'])}|{len(record['scheduled_review_vocab_ids'])}|{r['scheduled_expansion_count']}|{r['used_scheduled_expansion_count']}|{record['eojeol_count']}|{c['denominator_N']}/{c['new_tokens_U']}|{c['previous_vocab_coverage']:.3%}|{r['status']}|")
    report.extend(['','## 3. 予定語の意味的な適合','',
        f"{summary['conflict_texts']}教材で{summary['semantic_schedule_conflicts']}件のsemantic_schedule_conflict。予定{summary['scheduled_entry_text_pairs']}組中、本文で実現した予定露出は{summary['realized_scheduled_entry_text_pairs']}組。予定外の導入済み語は別欄へ記録し、欠落を埋めたことにしていない。",
        f"予定12〜13語の教材は{len(load12)}本。その全予定語を入れたのは{summary['scheduled_12_13_complete']}本（"+', '.join(r['id'] for r in load12 if r['validation']['schedule_pass'])+'）。語数として入る場合はあるが、どの組合せでも自然に成立するとは確認できない。',
        'これは今回選んだ小場面に対する不適合であり、別の場面でも絶対に不可能という証明ではない。全語を入れたK1-246・252も人形の遊びや第二の小問題が増え、母語話者が詰め込み感を確認する必要がある。',
        '移動候補は本文ごとのJSONとレビューMarkdownに全件記録。タグの近さ・既存負荷から未選択教材を3つ挙げた候補で、初出より後・300以内・既存同語reviewと重ならないことだけを検証している。移動後の6教材・分散間隔・負荷・新しい本文の自然さは未承認。元scheduleへ適用していない。','',
        '|問題|原因|修正候補（未適用）|','|---|---|---|',
        '|물고기を食事に混ぜられない|許可義は生きた動物。食材の魚にすり替えられない|動物観察が主目的のreview回へ移す|',
        '|찍다の印義が宿泊準備に入らない|Coreの写真義と別エントリ|書類・店で印を押す回へ移す|',
        '|料理回に수영장・미술관が入らない|短期再遭遇が別ジャンルへ割り当てられた|相談・外出回のreviewへ移す|',
        '|高速期の이・테이프・던지다|朝の歯磨き、箱へ貼る、球遊びに必要な닦다・붙이다・공が未登録|関連する別の小場面へ移す。基本語不足は次の人間レビューで検討|',
        '|99%が2語導入で未達|U=2、N<200。어절とNは異なる|98%hard/99%targetを区別して運用。99%必達にするなら長さや導入計画の仕様レビューが必要|','',
        '## 4. 新7語の実用例','', '|語|教材|本文からの用例|','|---|---|---|'])
    for m in files['id_migration.json']['mappings']:
        t=selected['selection_keys']['replacement:'+m['new_lemma']];record=records[t]
        a=next(a for a in record['annotations'] if a['vocab_id']==m['new_id'])
        start=max(record['text_ko'].rfind(p,0,a['start']) for p in '.!?')+1
        ends=[record['text_ko'].find(p,a['start']) for p in '.!?'];end=min(e for e in ends if e>=0)+1
        report.append(f"|{m['new_lemma']}|K1-{t:03}|{record['text_ko'][start:end].strip()}|")
    report.extend(['',
        '아저씨は店員の叙述と友達の父親・施設の職員の叙述に限定し、未知の成人男性へ直接呼びかけていない。K1-180で店員が家へ牛乳を届ける前提は近所の顔見知りを想定しており、自然さの人間確認が必要。가만히は기다리다に付け、未許可の-아/어 있다で迂回していない。',
        'medium5語は全て初出を使用。미술관は写真を見る行き先、박물관は町の家の写真を見る場所、결국は早すぎる外出の結末、관심は写真への関心。意味自体を絞れるが、展示場面が写真に偏る理由は그림が未登録であることも影響している。', '',
        '## 5. annotation・raw解析・依存の限界','',
        'A: generated annotations（lemma/POS/sense/ID/roleとoffset）。B: raw本文をKiwiで再解析し、正規化規則・登録ID・導入時点・文法span・計数・保存メタデータを照合。C: 未解決tokenとannotation_review_requiredを別リストで保存した。BはAと同じ正規化規則を共有するため、独立した意味の正解を提供しない。',
        f"未解決tokenは最終版で{summary['unresolved_tokens']}。annotation ambiguityは{summary['annotation_ambiguity_occurrences']}出現、type+lemma+教材の組では{summary['annotation_ambiguity_type_lemma_text_groups']}組。これは誤り確定数ではない。複合lemma・助数詞・同形語・文法補助用法が繰り返し現れるため、出現数と組数を区別した。",
        'K1-180の차는 써요はKiwiがVVで解析し、単純なPOS一致だとCore 쓰다/writeを選ぶ。作者の意図したbitterをその文だけで指定し、Kiwi_POS_sense_disagreementとして残した。annotationだけで100%の実意味coverageを証明できない具体例である。흘리다の눈물用例は中心義「こぼす」の範囲を人間が確認するsense_extension_reviewとして記録した。',
        '外部依存はkiwipiepy==0.24.0 / kiwipiepy_model==0.24.0をrequirements-phase2.txtへ追加した。既存requirements-dev.txtは変更していない。形態素・POS・offsetによる表層照合のためで、sense disambiguationの完成とは扱わない。使用APIは[Kiwi公式README](https://github.com/bab2min/kiwipiepy)のtokenize。ユーザー辞書を登録語へ強制的に寄せる操作は行っていない。',
        '生本文だけから32項目のあらゆる用法を完全判定する解析器ではない。認識不能な形は未解決として落とす。比較보다、와/과、-지 않다、名詞化-기、-으면서を検出するfixtureと、許可した試行-아/어 보다のfixtureで境界を検査した。','',
        '## 6. 高速多読ゾーン','',
        'K1-276・284・299は新出0、previous100%。全予定語を使えたのは299。276は歯のreview、284はテープと投げるreviewを省略した。未知語がないことと読みやすいことは別で、複数の準備工程を詰め込んだ284は12語枠の圧力が残る。299は既出표を反復し、切符の指示対象を明確にした。実読速度や学習者の習熟は未測定。','',
        '## 7. 検証・再実行・次の判断','',
        '既存validatorは800語・32文法・全scheduleについてPASSを維持。既存16＋パイロット10の計26テストメソッドがPASS。最終の本文校正後にもパイロット10メソッドを再実行し、PASSを確認した。',
        'パイロットvalidatorは予定語を省いた教材をFAILにするので、現在CLI終了コード1は意図した評価結果。ツール故障やhard98%未達と混同しない。詳細はk1_phase2_pilot_validation_result.json。', '',
        '```powershell','python -m pip install -r requirements-phase2.txt','python -B scripts/validate_k1_vocab.py','python -B scripts/validate_k1_pilot.py --save',
        'python -B -m unittest discover -s tests -v','python -B scripts/report_k1_pilot.py','```','',
        '本文再現はbuild_k1_pilot.py。authored_scenes.jsonは20本分だけで、selection_keyから番号を取得する。生成済みテキストはpilot/ko/k1/texts/K1-xxx.json、本文・訳・自己評価の一覧はk1_phase2_pilot_review.md。',
        '仕様変更について、語彙800や文法32を今回直ちに変える必要があるとは断定しない。ただし大量生成前に、意味を考慮したreview配置の人間レビューと承認が必要。닦다・붙이다・공・그림・들다のような基本語の不足、-게・動詞過去連体の不在による表現圧力は別の修正候補として記録し、今回のDBや文法へ追加していない。',
        '母語話者は自然さ、呼称、各語の中心義、文法境界、訳の主語・時系列、12〜13語の副次的事件を確認する。その後、承認されたschedule修正または場面選定の改善を別フェーズで検証する。**全300本の大量生成にはまだ進めない。**'])
    (ROOT/'reports/k1_phase2_pilot_report.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    proposals=[dict(source_text=r['text_number'],**c) for r in result['results'] for c in r['semantic_schedule_conflicts']]
    (ROOT/'reports/k1_phase2_schedule_move_proposals.json').write_text(json.dumps(dict(status='proposed_not_applied',source_schedule_frozen=True,
        entries=proposals,limitations='Semantic alternatives only; revalidate distinct six exposures, distances and destination load before approval.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
