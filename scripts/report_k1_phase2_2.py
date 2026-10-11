"""Human review pack with strictly separate comparison A and first-introduction B."""
from k1_phase2_2 import *
from statistics import mean,median
import math

def table(headers,rows):
    return '\n'.join(['|'+'|'.join(headers)+'|','|'+'|'.join(['---']*len(headers))+'|']+
                     ['|'+'|'.join(str(x).replace('|','/') for x in row)+'|' for row in rows])

def stats(values):
    s=sorted(values)
    return dict(min=min(s),max=max(s),mean=round(mean(s),3),median=median(s),p90=s[max(0,math.ceil(.9*len(s))-1)])

def sentences_with(rec, ids):
    out=[]
    for match in re.finditer(r'[^.!?]*[.!?][”"]?',rec['text_ko']):
        if any(a['vocab_id'] in ids and match.start()<=a['start']<match.end() for a in rec['annotations']):out.append(match.group().strip())
    return out

def render():
    files=inputs();vocab=vocab_map(files);selected=selection(files)
    result=read(REPORTS/'k1_phase2_2_validation_result.json')
    records={r['text_number']:r for r in [read(p) for p in sorted((PILOT/'texts').glob('K1-*.json'))]}
    checks={r['text_number']:r for r in result['results']}
    old=read(ROOT/'reports/k1_phase2_pilot_validation_result.json');old_rows={r['text_number']:r for r in old['results']}
    def labels(ids):return ', '.join(vocab[i]['lemma']+'/'+vocab[i]['sense'] for i in ids) or 'なし'
    for group,key in [('A','comparison_A'),('B','first_introduction_B')]:
        lines=[f'# K1 Phase 2.2 人間レビュー用 {group}', '',
               'A=Phase 2と同じ20番号の直接比較。B=新5語の初出補助パイロット。集計を混ぜない。', '',
               '自動PASSは生成annotationと規則の整合条件。自然さ・訳・語義は未承認。先行未生成教材の導入状態は仮定。', '']
        for t in selected[key]:
            r=records[t];c=checks[t]
            lines += [f'## K1-{t:03} — {r["title_ko"]}', '',r['text_ko'],'','**日本語訳**','',r['translation_ja'],'',
                      '**新出語**：'+labels(r['scheduled_new_vocab_ids']), '',
                      '**動的選択review**：'+labels(r['scheduled_review_vocab_ids']), '',
                      '**追加の既出Expansion**：'+labels(r['extra_previous_vocab_ids']), '',
                      f"N={c['coverage']['denominator_N']}、U={c['coverage']['new_tokens_U']}、controlled={c['coverage']['controlled_vocab_coverage']:.2%}、previous={c['coverage']['previous_vocab_coverage']:.3%}。", '',
                      '**使用文法**：'+', '.join(next(g['form'] for g in files['grammar.json'] if g['id']==i) for i in r['grammar_used']), '',
                      f"validator：{c['status']}。{c['metrics']['eojeol_count']}어절、{c['metrics']['sentence_count']}文、最大{c['metrics']['max_sentence_eojeol']}어절/文。新出token内訳："+labels(list(c['new_token_counts']))+f" {list(c['new_token_counts'].values())}。", '',
                      f"semantic_schedule_conflict={len(r['semantic_schedule_conflicts'])}。raw未解決token={c['unresolved_token_count']}。annotationレビュー候補{c['annotation_ambiguity_occurrences']}件（型別台帳へまとめる）。", '',
                      '**自己評価（人間レビューの代替ではない）**', '']
            names={'naturalness':'自然さ','ease':'K1の簡単さ','packing':'詰め込み感','paraphrase':'言い換え','grammar':'文法難度','annotation':'annotation ambiguity'}
            lines += ['- '+names[k]+'：'+v for k,v in r['author_review'].items()]
            if c['warnings']:lines+=['','soft warning：'+' / '.join(c['warnings'])]
            lines+=['']
        (REPORTS/f'k1_phase2_2_pilot_review_{group}.md').write_text('\n'.join(lines),encoding='utf-8')
    (REPORTS/'k1_phase2_2_pilot_review.md').write_text(
        '# K1 Phase 2.2 レビュー入口\n\n[A：比較用20本](k1_phase2_2_pilot_review_A.md)\n\n[B：新5語初出5本](k1_phase2_2_pilot_review_B.md)\n\n[全体報告](k1_phase2_2_pilot_report.md)\n',encoding='utf-8')
    comparisons=[]
    for t in selected['comparison_A']:
        before=old_rows[t];after=checks[t]
        comparisons.append(dict(text_number=t,old_language_status=before['language_status'],new_language_status=after['status'],
            old_exact_schedule_status=before['status'],old_conflict_count=len(before['semantic_schedule_conflicts']),
            new_selected_review_conflict_count=len(after['semantic_schedule_conflicts']),old_eojeol=before['metrics']['eojeol_count'],new_eojeol=after['metrics']['eojeol_count'],
            old_previous=before['coverage']['previous_vocab_coverage'],new_previous=after['coverage']['previous_vocab_coverage'],
            old_fixed_review_count=before['scheduled_expansion_count']-len(records[t]['scheduled_new_vocab_ids']),
            new_selected_review_count=after['review_count'],old_total_scheduled=before['scheduled_expansion_count'],
            new_total_scheduled=after['scheduled_expansion_count'],new_actual_expansion_count=after['actual_expansion_count'],
            body_changed=read(ROOT/'pilot/ko/k1/texts'/f'K1-{t:03}.json')['text_ko']!=records[t]['text_ko'],
            scene_changed=t in (1,40,85,150,170,299)))
    old_conflicts=[]
    for row in old['results']:
        for conflict in row['semantic_schedule_conflicts']:
            i=conflict['vocab_id'];t=row['text_number'];actual_here=i in records[t]['actually_used_review_vocab_ids']+records[t]['extra_previous_vocab_ids']
            actual_elsewhere=[n for n,r in records.items() if n!=t and i in r['actually_used_review_vocab_ids']+r['extra_previous_vocab_ids']]
            status='same_text_actual' if actual_here else 'other_pilot_actual' if actual_elsewhere else 'not_selected_debt_retained'
            if i not in vocab:status='retired_from_active_K1'
            old_conflicts.append(dict(original_text=t,vocab_id=i,lemma=conflict['lemma'],sense=conflict['sense'],resolution=status,
                actual_other_texts=sorted(actual_elsewhere),meaning_naturalness_human_approved=False,
                explanation='Absent selections are not failed exact assignments; unfinished windows remain debts, not fulfilled exposures.'))
    write(REPORTS/'k1_phase2_2_comparison.json',{'phase':'2.2','group':'A_only','rows':comparisons,'old_23_conflict_disposition':old_conflicts,
        'causal_limit':'Changed scenes, vocabulary, word order and analyzer hints; uncontrolled pilot, not isolation of scheduler effect.'})
    write(REPORTS/'k1_phase2_2_annotation_triage.json',result['annotation_triage'])
    deferments=[]
    windows={e['vocab_id']:e for e in files['vocab_review_windows.json']['entries']}
    for t,rec in records.items():
        for conflict in rec['semantic_schedule_conflicts']:
            e=windows[conflict['vocab_id']]
            options=[{'from':max(t+1,w['from']),'to':w['to'],'window_index':index}
                     for index,w in enumerate(e['review_windows']) if w['to']>t]
            selected_row=next(r for r in rec['scheduler_selection']['selected_reviews'] if r['vocab_id']==e['vocab_id'])
            deferments.append(dict(vocab_id=e['vocab_id'],source_text=t,selected_window_index=selected_row['window_index'],
                missed_deadline=selected_row['deadline'],candidate_opportunities=options,
                scene_candidates=e['scene_affinity'],proposal_only=True,actual_future_exposure_confirmed=False,
                reason='Photo conversation does not naturally require the book counter. Use a book borrowing/reading scene; keep unpaid debt.'))
    write(PILOT/'review_deferments.json',{'phase':'2.2','window_source_unchanged':True,'proposals':deferments})
    lines=['# K1 Phase 2.2 — 比較20本＋新5語初出5本', '',
        '承認された25本だけを生成。A20とB5を分離して集計した。正式な800語・32文法・ID migration・coverage・introduction/windowを変更していない。既存Phase 2の20本文・レポート・validationも変更なし。', '',
        f"機械条件：{'PASS' if result['ok'] else 'FAIL'}。全体errors={len(result['errors'])}。自然さ・語義・日本語訳は人間未承認。", '',
        '## A / B 別の結果', '',
        table(['群','本数','PASS','TARGET_MISS','FAIL','平均어절','previous最小','review5〜8達成'],[
            [g,s['text_count'],s['counts']['PASS'],s['counts']['PASS_WITH_TARGET_MISS'],s['counts']['FAIL'],f"{s['mean_eojeol']:.2f}",f"{s['previous_coverage_min']:.3%}",f"{s['review_soft_target_met']}/{s['text_count']}"] for g,s in result['groups'].items()]), '',
        table(['群','previous分布 (%)','controlled違反','文法hard違反','scheduled review conflict'],[
            [g,stats([100*r['coverage']['previous_vocab_coverage'] for r in checks.values() if r['group']==g]),
             sum(r['coverage']['controlled_vocab_coverage']!=1 for r in checks.values() if r['group']==g),
             sum(not r['validation']['grammar_pass'] for r in checks.values() if r['group']==g),
             result['groups'][g]['semantic_schedule_conflict_count']] for g in ('A','B')]), '',
        'A番号：'+', '.join(f'{n:03}' for n in selected['comparison_A'])+'。', '',
        'B番号：'+', '.join(f'{n:03}' for n in selected['first_introduction_B'])+'。双方の番号はデータから取得し、BをA比較成績へ混ぜていない。', '',
        '2 new tokensでN<200ならprevious99%を達成できない。hard98%を満たすTARGET_MISSは設計上の期待結果で、大量生成blockerではない。全25本でcontrolled100%、previous98%以上、120〜180어절、文最大10、32文法内、新出最大2lemma・soft3tokenを検査。', '',
        '本報告のPASS/TARGET_MISSは言語hard条件の成績。K1-103だけschedule_pass=falseで권（冊）が未消化。写真会話に冊数の一文を足さず、借りる・読書する場面への繰越候補をreview_deferments.jsonへ保存。元windowは変更せず、次の出現は未確認のまま残す。', '',
        '## A：Phase 2との直接比較', '',
        '旧20本も言語hard failureは0だった。旧overall FAIL12本は固定reviewの23 conflictによる。新方式の選択済みreviewとの衝突を別に比較する。', '',
        table(['番号','旧→新어절','旧→新previous','旧固定review→新review','旧conflict→新conflict','実使用Expansion'],[
            [f"{r['text_number']:03}",f"{r['old_eojeol']}→{r['new_eojeol']}",f"{r['old_previous']:.2%}→{r['new_previous']:.2%}",
             f"{r['old_fixed_review_count']}→{r['new_selected_review_count']}",f"{r['old_conflict_count']}→{r['new_selected_review_conflict_count']}",r['new_actual_expansion_count']] for r in comparisons]), '',
        '全20本文を変更した。特に040はオレンジ退役後の비누初出、150はバスの開閉、170は絵の描き直し、299は球遊びへsceneを選び直した。したがって自然さの変化をschedulerだけの因果効果とみなさない。', '',
        '旧23 conflictの扱い（同番号で用いた／別pilotで用いた／未選択・債務保持／退役）。「未選択」は6露出達成を意味せず、次の自然な教材とwindowで回収する。', '',
        table(['旧番号','lemma / sense','新方式の扱い','別pilotでの実使用番号'],[
            [f"{r['original_text']:03}",r['lemma']+'/'+r['sense'],r['resolution'],', '.join(str(n) for n in r['actual_other_texts']) or '—'] for r in old_conflicts]), '',
        '## B：新5語の初出自然さ', '',
        table(['番号','対象語','新出token合計U','対象token','N','previous','review','conflict'],[
            [f'{t:03}',vocab[i]['lemma'],checks[t]['coverage']['new_tokens_U'],checks[t]['new_token_counts'].get(i,0),checks[t]['coverage']['denominator_N'],
             f"{checks[t]['coverage']['previous_vocab_coverage']:.3%}",checks[t]['review_count'],len(checks[t]['semantic_schedule_conflicts'])]
            for i in B_IDS for t in selected['first_introduction_B'] if i in records[t]['scheduled_new_vocab_ids']]), '',
        '020は机の水を拭く。033は誕生日のボールの受け渡し。110は階段で友達の荷物を持つ。111は絵で家と学校を話す。127は糊で写真を貼る。対象語は各1token、同回のもう一つの新出語も各1token。場面の目的・対象・解決に関与させ、初出内反復を増やしていない。', '',
        '早期Bの制約にも注意：020では이/toothや칫솔は未導入なので歯磨きはしない。033では던지다が未導入なので球の投擲はしない。111では그리다が未導入なので描画はしない。127では테이프が未導入なので풀/glueを用いる。既出後のAで標準場面を検証した。', '',
        '## lexical gapが解消された用例', '']
    for label,t,lemmas in [('이＋닦다',276,{'이','닦다'}),('테이프＋붙이다',284,{'테이프','붙이다'}),('던지다＋공',299,{'던지다','공'}),('미술관/그리다＋그림',189,{'미술관','그리다','그림'}),('가방/책＋들다',110,{'들다'})]:
        ids={i for i,e in vocab.items() if e['lemma'] in lemmas}
        lines += [f'**{label}（K1-{t:03}）**','',*sentences_with(records[t],ids),'']
    lines += ['들다は手で荷物を持つ中心義だけ。Core찍다/take_photoを使用し、stamp義・도장・배터리等の未採用語は使わない。生解析のsenseラベルだけで別義を承認しない。', '',
        '## 語彙負荷・高速多読ゾーン', '']
    for group in ('A','B'):
        rows=[r for r in checks.values() if r['group']==group]
        lines += [f'{group}選択review分布：`{stats([r["review_count"] for r in rows])}`。', '',
                  f'{group}実使用Expansion（extra既出込み）分布：`{stats([r["actual_expansion_count"] for r in rows])}`。','']
    lines += ['5〜8はsoft目標。001は先行語がなく0、150/234/255は自然に承認できる候補が3/4/4であり、数のための副次事件を足さなかった。選択reviewの減少と本文全体のExpansion密度は別指標として監視する。', '',
        table(['高速番号','어절','review','全実使用Expansion','最近20本のE3','previous','自己評価'],[
            [f'{t:03}',checks[t]['metrics']['eojeol_count'],checks[t]['review_count'],checks[t]['actual_expansion_count'],checks[t]['recently_introduced_E3_count'],
             f"{checks[t]['coverage']['previous_vocab_coverage']:.2%}",'単一の問題・目的。人間による速度評価は未実施。'] for t in selected['comparison_A'] if t>=276]), '',
        '高速3本は新出0。最近20本に初出したE3の集中なし。ただし既出語でも読者が自動化できている保証はなく、実読速度・疲労は人間で確認する。', '',
        '## annotation・解析の限界', '',
        f"25本：{result['annotation_triage']['total_occurrences']}候補を{result['annotation_triage']['total_groups']}型へ整理。`{result['annotation_triage']['occurrence_counts']}`。", '',
        table(['群','annotation候補数','まとめた型数','カテゴリ別件数'],[
            [g,(tri:=annotation_triage([r for r in records.values() if r['group']==g],files))['total_occurrences'],tri['total_groups'],tri['occurrence_counts']] for g in ('A','B')]), '',
        '旧269件との比較対象はAのみ。Bの5本文を足した25本合計を旧20本の件数と直接比較しない。表現量と解析ヒントも変わっているため単純な改善率とはしない。', '',
        'benign_expected／lexical sense／grammar boundary／true unresolvedを分離。저・제の構造上明確な代名詞は型でまとめ、일・풀・이の文脈義、들다の物理義、compoundと助数詞は条件を限定してレビューする。型の承認を全用法へ拡張しない。raw未解決内容語は全本文0。', '',
        '既存Kiwiと規則は変更せず、Phase 2.2専用に수건/제일/물어보/오래되の登録語ヒントと、묻+어+보→登録lemma 물어보다の一어절内groupingを追加。raw形態素と境界レビューを保存した。묻다単独は依然未許可。新たな外部依存は追加していない。', '',
        '草稿では禁止-기/-지 않다/-게、未来連体、未導入語が検出され本文を修正した。さらに人間的な語義監査で일/workを一般活動の名詞化に流用する文、들다を「気に入る」にする文も除いた。自動ラベル一致だけでは語義の正しさを保証できない実例である。', '',
        '## schedulerの運用証拠と残る条件', '',
        '新出アンカー→scene→作者承認したreview候補→schedulerの意味適合・期限・過去回数・距離・意味領域分散の順位付け→本文→再解析の順で記録。候補判定はauthor judgementで、全候補プールを無理に本文へ入れない。selectionスコアと除外理由を各JSONに保存し、validatorが履歴から再計算する。', '',
        '先行未生成回はintroduction-onlyの仮種まき。架空の背景reviewは作っていない。exposure_ledgerは仮定と25本の生成annotationに基づく出現を分離した。期限債務は現実の300本連続運用の測定ではない。500語×6つの異なる本文での最終実出現は、25本では証明しない。', '',
        'medium confidence：아저씨の呼称語用、미술관/박물관の区別、결국の結末での自然さ、관심の関心対象の文脈を人間で確認。今回はいずれも文脈に役割があるが、自動PASSを母語話者承認に置換しない。', '',
        '## 最終判断・成果物', '',
        '**機械hard条件を通過し、少数パイロットの人間レビューへ進める。全300本の大量生成には進めない。** B5で初出の中心性を実本文として検査できた。次はA/Bの自然さと訳、語義境界、5〜8reviewの成立、本文全体のExpansion密度を確認する。連続生成時のwindow債務と最終6露出は別途必要。', '',
        '凍結manifest：k1_phase2_2_input_freeze.json。本文：pilot/ko/k1/phase2_2/texts/ の25 JSON。', '',
        '検証：k1_phase2_2_validation_result.json。比較：k1_phase2_2_comparison.json。型別annotation：k1_phase2_2_annotation_triage.json。人間レビュー：k1_phase2_2_pilot_review_A.md / _B.md。', '',
        '再現：`python -B scripts/build_k1_phase2_2.py`、検証：`python -B scripts/validate_k1_phase2_2.py --save`。再現は承認済み25本だけを上書きし、旧pilotと正式DBを更新しない。', '']
    evidence=REPORTS/'k1_phase2_2_test_result.json'
    if evidence.exists():lines += ['テスト：'+json.dumps(read(evidence)['runs'],ensure_ascii=False),'']
    (REPORTS/'k1_phase2_2_pilot_report.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':render()
