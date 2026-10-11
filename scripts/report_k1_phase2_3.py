"""Trace language-review decisions to original Korean, translations and hard metrics."""
from collections import Counter
from k1_phase2_3 import *
from k1_naturalness_lint import sentences

OLD_TRANSLATION_ISSUES=[
(33,'저는 계단에서 친구의 이름을 말해요.','私は階段から友達の名前を呼びます。','말하다を呼ぶ意味に補正。呼ぶ行為を削除。'),
(33,'어머니도 친구를 보고 아주 좋아해요.','母も友達を見てとても喜びます。','好きという韓国語を喜ぶに補正。本文を웃다へ。'),
(33,'친구도 저를 보고 아주 좋아해요.','友達も私を見てとても喜びます。','好きと喜ぶの混同。本文側を笑うに確定。'),
(85,'친구는 제 책을 아주 좋아해요.','友達は私の本をとても喜びます。','借りた本への反応を訳だけ喜ぶへ補正。本文を受け取って笑うへ。'),
(111,'이것은 작은 집하고 학교예요.','小さな家と学校の絵です。','本文にない「絵です」を補って描写関係を修復。本文を絵の中の存在へ。'),
(180,'저는 걱정해서 친구의 이름을 말해요.','心配になり友達の名前を呼びます。','名前を言うを呼ぶに補正。本文に鞄がないという直接発話を置く。'),
(170,'어머니도 우리 집을 좋아할 거예요.','母も私たちの家を喜んでくれるでしょう。','좋아하다を喜ぶに補正し、描いた対象も曖昧。本文を그림に確定。'),
(189,'어머니도 그 약속을 아주 좋아해요.','母もその約束を喜びます。','좋아하다を喜ぶへ読み替え。本文の笑う反応へ。'),
(242,'동생도 친구의 이야기를 듣고 아주 좋아해요.','弟も友達の話を聞いて喜びます。','좋아하다を喜ぶへ補正。韓国語を웃다へ。'),
(246,'동생도 아버지 옆에서 아주 좋아해요.','弟も父の隣で喜びます。','曖昧な좋아하다を訳が具体化。本文を웃다へ。'),
(252,'동생도 그 약속을 정말 좋아해요.','弟もその約束を喜びます。','訳だけ喜ぶへ。本文を次週も撮りたいという希望へ。'),
(276,'사촌은 오늘 운동을 아주 좋아해요.','いとこは今日の運動を喜びます。','好みを当日の喜びへ補正。本文を一般的な運動の好みに。'),
(299,'친구는 잘 잡고 아주 좋아해요.','友達はうまく受け取り、喜びます。','曖昧な좋아하다を喜ぶへ補正。本文を公を取って笑うへ。'),
(299,'이제 앞에는 자리가 많이 있어요.','前に広く空きがあります。','席という許可義を広い空きに補正。本文を他の人がいないへ。'),
]

def report():
    v=read(REPORTS/'k1_phase2_3_validation_result.json');files=inputs();vocab=vocab_map_local(files)
    records=[read(p) for p in sorted((PILOT/'texts').glob('*.json'))]
    by_t={r['text_number']:r for r in records};old={t:read(ROOT/'pilot/ko/k1/phase2_2/texts'/f'K1-{t:03}.json') for t in by_t}
    log=read(PILOT/'language_edits.json');counts=Counter(e['category'] for e in log)
    audits=[]
    for t,ko,ja,reason in OLD_TRANSLATION_ISSUES:
        if ko not in old[t]['text_ko'] or ja not in old[t]['translation_ja']:raise ValueError('Audit source quote mismatch: '+str(t))
        audits.append(dict(text_number=t,category='translation_fidelity',before_ko=ko,before_ja=ja,reason=reason,classification='author_identified_mismatch_not_independent_gold'))
    counts['translation_fidelity']=len(audits);counts['natural_expression_gap']=v['summary']['natural_expression_gaps']
    write(PILOT/'translation_mismatch_audit.json',audits)
    write(PILOT/'review_deferments.json',v['deferred_reviews'])
    write(PILOT/'naturalness_lint_result.json',dict(phase='2.3',warning_only=True,records=[dict(id=r['id'],warnings=r['naturalness_lint']) for r in records]))
    rows=['# K1 Phase 2.3 言語自然さレビュー反映','',
      '25本文と25日本語訳を別ディレクトリで修正。旧Phase 2.2、Core300／Expansion500／Total800、Tier200/200/100、文法32、5交換、ID、初出予定、review windows、coverageはハッシュで不変。guidelineとschemaの追加は語彙・文法の拡張ではない。','',
      '## 判定と限界','',
      f"hard errors {v['summary']['hard_errors']}、未解決token {v['summary']['unresolved_tokens']}。controlled100%／previous98%以上／120–180어절／一文10以下は全25本PASS。AとBの集計は分離。自然さwarningは確定エラーではなく、モデル二次評価も人間承認ではない。",
      '', 'coverage／grammarは現在の形態素・lemma/POS/sense解決仮説上の再現可能な検査結果。語義と自然さの独立した正解証明ではない。',
      '',f"新lint warning {v['summary']['naturalness_warnings']}件。意味レビューflag {v['summary']['semantic_review_flags']}件／{v['summary']['semantic_review_flagged_texts']}教材。修正版の訳lint flag {v['summary']['translation_fidelity_flags']}件（対訳の完全性を証明する数値ではない）。",'',
      '| 群 | 本数 | PASS | target miss | FAIL | 平均어절 | previous最小 | review 5–8達成 |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for g,row in v['groups'].items():
        c=row['counts'];rows.append(f"| {g} | {row['text_count']} | {c['PASS']} | {c['PASS_WITH_TARGET_MISS']} | {c['FAIL']} | {row['mean_eojeol']:.2f} | {row['previous_coverage_min']:.4%} | {row['review_soft_target_met']} |")
    rows+=['','Nは粒子・活用語尾・句読点を除く解決済み語彙意味単位token（未知も分母から除外しない）。Uは当該教材の新出Expansionの実token総数。controlled = 許可token/N、previous=(N−U)/N。各新出語は導入状態・ID・POS・senseで確認する。U=2,N<200の99%target missは予想され、hard98%を満たすのでblockerにしない。','',
      '## 横断集計','',
      '以下は明示的な修正hunk／旧訳の問題箇所数。regex警告数・問題教材数とは別の母数。1つのhunkに複数原因があっても主原因へ1回計上する。natural_expression_gapは省略した意味要求を別に数える。','',
      '| category | 件数 |','|---|---:|']
    tests=read(REPORTS/'k1_phase2_3_test_result.json') if (REPORTS/'k1_phase2_3_test_result.json').exists() else None
    if tests:
        rows.insert(5,f"全回帰テスト {tests['tests_run']}件、failures {tests['failures']}、errors {tests['errors']}。ログ: reports/k1_phase2_3_test_log.txt。最初の新規assertionのメッセージ期待違いは修正済みで、validatorの拒否条件は緩めていない。")
        rows.insert(6,'')
    for c,n in sorted(counts.items()):rows.append(f'| {c} | {n} |')
    rows+=['','## 発生原因と一般化した対策','',
      '- 日本語「の」の逐語転写 → conventional noun adjacency。所有を明確にする의は残す。',
      '- 使用可能lemmaだけを見て意図を別義へ押し込む → semantic frameと文脈の目的語を照合。받다は実際の譲渡、들다は物理的保持。',
      '- review quotaや好ましい文長を先に満たす → sceneの目的を先に決め、positive realization gate／vetoを選択へ反映。副詞で穴埋めしない。',
      '- genericな感情反応 → 笑う・好み・評価を区別し、自然な意味がなければ省略。',
      '- 見える対象と絵のreferentの混同、時系列省略 → 人物・物・時間を明示した二次意味レビュー。',
      '- 訳が不自然な韓国語を補正 → 韓国語確定後に全訳を独立に訳し直し、文対応と本文hashを保存。','',
      '機械lintは危険collocation、局所의、副詞密度・近接反復、習慣＋進行、指示語候補、限定義のcontextを検出するだけ。人物の目的、通常その場でする行動か、reviewだけの動機かは別工程のYES/NO/REVIEWで根拠付き評価。','',
      '## review延期','', '| 教材 | 語／ID | 状態 | 方針 |','|---|---|---|---|']
    for d in v['deferred_reviews']:
        rows.append(f"| K1-{d['text_number']:03} | {d['lemma']} / {d['vocab_id']} | {'旧段階から未消化' if d['previously_unpaid'] else '今回の自然さ修正で省略'} | 同window後半または次windowの自然な場面へ。実出現creditなし |")
    rows+=['','출구（K1-033）は旧本文のextra previous語で、旧selected reviewではなかった。家の出口としての挿入を削除したが、未払いscheduled review数には加えない。削除したincidental語は教材ごとの差分で明示する。予定やwindowは変更せず、選択・本文実使用だけを修正。','',
      '## natural_expression_gap','']
    for r in records:
        for gap in r['natural_expression_gaps']:rows.append(f"- {r['id']}: {gap['intended_event']} — {gap['cause']} {gap['resolution']}")
    rows+=['','4件のうち、本を開く3件は「定番表現を選ぶ場合の候補」で、制限内で絶対に表現できないという証明ではない。책을 펴다が標準的な表現であることは[国立国語院の相談事例](https://korean.go.kr/front/mcfaq/mcfaqView.do?mcfaq_seq=6239&mn_id=217&pageIndex=1)で確認した。これを根拠に책을 열다の全用法を禁止しない。',
      '', 'これらはhard語彙追加の要求ではない。省略・許可された簡単な行為で解決しており、現行800／32を変えるblockerではない。充電不能の細かな故障原因も未登録の機器語で説明せず、買い物に必要な状態だけを述べる。','',
      '## 語義・社会語用のレビュー','',
      '들다はすべて鞄を手に持つ／持ち上げる場面。풀は127の接着のり、299の草を別ID・overrideで区別。276の이는歯で、定冠詞・漢数詞・助詞とは別。눈/eyeの曖昧な234の文は削除し、今回の修正版に眼の用例は残らない。쓰다は書く義を保ち、193の包丁にはCore 사용하다を使う。苦い等の別senseをCore書くIDで許可しない。','',
      '아저씨 / ko_k1_0802 / adult_man_address は、glossとnotesが成人男性の呼称／叙述を許す一方、英語コードが直接呼びかけに見える。今回の180は店で働く成人男性の叙述で、未知の男性への呼びかけを生成しない。将来案はadult_man_reference等への名称見直しだが、意味範囲と恒久IDを人間が再確認してからmigrationを設計する。今回はreport onlyで一切変更なし。','',
      'K1-242の받다 warningは来客の鞄を受け取る実際の受け渡しを指す。重い鞄の保持の代用ではない。保持義を示すためだけの손으로は除き、文脈で判断する。残る副詞・指示語warningは文脈付きの小グループで確認し、全部を確定エラーへ分類しない。','',
      '## 実装・再現','',
      '`python -B scripts/k1_phase2_3.py`（保存済みの修正版sourceから25本のみ構築） → `python -B scripts/validate_k1_phase2_3.py --save` → `python -B scripts/review_k1_phase2_3_semantics.py` → `python -B scripts/report_k1_phase2_3.py`。',
      '', '自然さのregexはhard FAILへ昇格させない。retired／future／unknown identity、文法、coverage、長さ等は既存hard検査で別に判定。追加の外部依存なし。既存Kiwiへ既登録가져오다の分割hintを1つ追加し、가져올の가지+어+오誤分割を補正。raw morphologyとsense ambiguityは保持する。義や文法を追加しない。','',
      '## 次の判断','',
      'Phase 3の連続50教材検証へ条件付きで進める。hard設計は維持したまま、今回のguidelineとreview veto、文脈付きwarningの人間レビューを運用に入れる。今回の自己評価を自然さ最終承認にしない。Phase 3では実際の導入・incidental exposure・debt、scene重複、genre、負荷、語義・訳を順番に監視する。50本が通るまで300本量産へ進めない。本Phaseでは50本も300本も生成していない。','']
    for r in records:
        t=r['text_number'];o=old[t];check=next(x for x in v['results'] if x['text_number']==t)
        used_old=set(o['actually_used_review_vocab_ids']+o['extra_previous_vocab_ids']);used_new=set(r['actually_used_review_vocab_ids']+r['extra_previous_vocab_ids'])
        labels=lambda ids:', '.join(vocab[i]['lemma']+' / '+i for i in ids) or 'なし'
        rows += [f"## {r['id']}（{r['group']}）",'',f"{check['status']}。어절 {o['eojeol_count']} → {r['eojeol_count']}、N {o['coverage']['denominator_N']} → {r['coverage']['denominator_N']}、U {o['coverage']['new_tokens_U']} → {r['coverage']['new_tokens_U']}、previous {o['coverage']['previous_vocab_coverage']:.4%} → {r['coverage']['previous_vocab_coverage']:.4%}、controlled両方100%。",'',
          '| category | 修正前韓国語 | 修正後韓国語 | 理由 |','|---|---|---|---|']
        for e in log:
            if e['text_number']==t:rows.append(f"| {e['category']} | {e['before_ko']} | {e['after_ko']} | {e['reason']} |")
        rows+=['',f"新出: {labels(r['scheduled_new_vocab_ids'])}。新出token: {check['new_token_counts']}。",'',
          f"review実使用 {len(o['actually_used_review_vocab_ids'])} → {len(r['actually_used_review_vocab_ids'])}。今回選択: {labels(r['scheduled_review_vocab_ids'])}。",'',
          '旧本文から削除したprevious Expansion（incidental含む）: '+labels(sorted(used_old-used_new))+'。',
          '延期したscheduled review: '+labels([d['vocab_id'] for d in v['deferred_reviews'] if d['text_number']==t])+'。','',
          f"hard errors {len(check['errors'])}、lint warning {len(r['naturalness_lint'])}、semantic flags: {', '.join(check['semantic_review_flags']) or 'なし'}、unresolved {check['unresolved_token_count']}、translation flags {len(check['translation_fidelity_flags'])}。",'',
          '使用文法: '+', '.join(r['grammar_used'])+'。','', '### 修正版韓国語','',display_paragraphs(r['text_ko']),'','### 再翻訳した日本語','',r['translation_ja'],'',
          '### 旧訳の意味ずれ','']
        relevant=[a for a in audits if a['text_number']==t]
        for a in relevant:rows += [f"- {a['before_ko']} → 旧訳「{a['before_ja']}」: {a['reason']}"]
        if not relevant:rows.append('今回の抽出範囲では明示的な旧訳の意味ずれなし。全対訳の人間承認を意味しない。')
        rows+=['','### 二次意味レビュー','']
        for k,judgment in r['naturalness_semantic_review']['checks'].items():rows.append(f"- {k}: {judgment['verdict']} — {judgment['reason']}")
        rows+=['','モデル自己評価。母語話者・人間の確認対象を絞るための根拠であり、最終承認ではない。','']
    write(PILOT/'language_review_summary.json',dict(problem_hunk_counts=dict(counts),old_translation_mismatches=len(audits),**v['summary']))
    (REPORTS/'k1_phase2_3_language_review.md').write_text(('\n'.join(rows)+'\n').replace('定冠詞','指示連体詞'),encoding='utf-8')
    (PILOT/'README.md').write_text('# Phase 2.3 language revisions\n\nOld Phase 2.2 is immutable. Exactly the same A20+B5; no new pilot or mass run.\n\n`authored_scenes.json` contains final Korean, fresh aligned Japanese, explicit semantic evidence and review vetoes. Build with `scripts/k1_phase2_3.py`; validate with `scripts/validate_k1_phase2_3.py --save`. Run the distinct `review_k1_phase2_3_semantics.py` screening stage. Naturalness/model YES is not human approval.\n\n`review_deferments.json` retains uncredited debt. `exposure_ledger.json` separates hypothetical earlier introductions from annotated pilot occurrences. No claim of complete 500 × six exposures.\n',encoding='utf-8')

def vocab_map_local(files):return {e['id']:e for e in files['core_vocab.json']+files['expansion_vocab.json']}
def display_paragraphs(text):
    ss=[s for _,s in sentences(text)]
    return '\n\n'.join(' '.join(ss[i:i+7]) for i in range(0,len(ss),7))

if __name__=='__main__':report()
