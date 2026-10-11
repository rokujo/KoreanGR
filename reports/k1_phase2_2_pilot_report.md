# K1 Phase 2.2 — 比較20本＋新5語初出5本

承認された25本だけを生成。A20とB5を分離して集計した。正式な800語・32文法・ID migration・coverage・introduction/windowを変更していない。既存Phase 2の20本文・レポート・validationも変更なし。

機械条件：PASS。全体errors=0。自然さ・語義・日本語訳は人間未承認。

## A / B 別の結果

|群|本数|PASS|TARGET_MISS|FAIL|平均어절|previous最小|review5〜8達成|
|---|---|---|---|---|---|---|---|
|A|20|6|14|0|134.70|98.413%|16/20|
|B|5|0|5|0|134.80|98.462%|5/5|

|群|previous分布 (%)|controlled違反|文法hard違反|scheduled review conflict|
|---|---|---|---|---|
|A|{'min': 98.4126984126984, 'max': 100.0, 'mean': 98.891, 'median': 98.48484848484848, 'p90': 100.0}|0|0|1|
|B|{'min': 98.46153846153847, 'max': 98.51851851851852, 'mean': 98.491, 'median': 98.49624060150376, 'p90': 98.51851851851852}|0|0|0|

A番号：001, 040, 085, 103, 150, 170, 180, 184, 189, 190, 193, 234, 242, 246, 252, 254, 255, 276, 284, 299。

B番号：020, 033, 110, 111, 127。双方の番号はデータから取得し、BをA比較成績へ混ぜていない。

2 new tokensでN<200ならprevious99%を達成できない。hard98%を満たすTARGET_MISSは設計上の期待結果で、大量生成blockerではない。全25本でcontrolled100%、previous98%以上、120〜180어절、文最大10、32文法内、新出最大2lemma・soft3tokenを検査。

本報告のPASS/TARGET_MISSは言語hard条件の成績。K1-103だけschedule_pass=falseで권（冊）が未消化。写真会話に冊数の一文を足さず、借りる・読書する場面への繰越候補をreview_deferments.jsonへ保存。元windowは変更せず、次の出現は未確認のまま残す。

## A：Phase 2との直接比較

旧20本も言語hard failureは0だった。旧overall FAIL12本は固定reviewの23 conflictによる。新方式の選択済みreviewとの衝突を別に比較する。

|番号|旧→新어절|旧→新previous|旧固定review→新review|旧conflict→新conflict|実使用Expansion|
|---|---|---|---|---|---|
|001|124→135|98.35%→98.51%|0→0|0→0|2|
|040|124→135|99.19%→99.24%|6→6|0→0|10|
|085|124→135|100.00%→100.00%|8→7|0→0|12|
|103|124→132|98.39%→98.46%|7→7|0→1|13|
|150|122→134|98.36%→98.51%|8→3|1→0|12|
|170|127→136|100.00%→100.00%|12→7|2→0|8|
|180|124→135|98.37%→98.47%|10→5|0→0|14|
|184|128→134|98.44%→98.46%|10→8|2→0|17|
|189|125→133|98.37%→98.41%|10→7|3→0|14|
|190|123→136|98.36%→98.47%|10→8|2→0|17|
|193|123→131|98.37%→98.45%|10→6|2→0|17|
|234|129→132|98.46%→98.43%|11→4|3→0|20|
|242|125→139|98.33%→98.52%|11→7|2→0|17|
|246|131→132|98.40%→98.45%|11→5|0→0|19|
|252|131→134|98.44%→98.48%|11→6|0→0|16|
|254|127→135|98.44%→98.48%|11→5|1→0|17|
|255|130→137|98.41%→98.47%|11→4|2→0|14|
|276|125→135|100.00%→100.00%|12→8|1→0|19|
|284|127→139|100.00%→100.00%|12→7|2→0|18|
|299|135→135|100.00%→100.00%|12→8|0→0|14|

全20本文を変更した。特に040はオレンジ退役後の비누初出、150はバスの開閉、170は絵の描き直し、299は球遊びへsceneを選び直した。したがって自然さの変化をschedulerだけの因果効果とみなさない。

旧23 conflictの扱い（同番号で用いた／別pilotで用いた／未選択・債務保持／退役）。「未選択」は6露出達成を意味せず、次の自然な教材とwindowで回収する。

|旧番号|lemma / sense|新方式の扱い|別pilotでの実使用番号|
|---|---|---|---|
|150|물고기/fish_animal|not_selected_debt_retained|—|
|170|계산하다/pay_bill|not_selected_debt_retained|—|
|170|찍다/stamp|retired_from_active_K1|—|
|184|새롭다/new|not_selected_debt_retained|—|
|184|급하다/urgent|not_selected_debt_retained|—|
|189|이불/bedding|not_selected_debt_retained|—|
|189|맵다/spicy|not_selected_debt_retained|—|
|189|테이프/adhesive_tape|other_pilot_actual|284|
|190|버리다/discard|not_selected_debt_retained|—|
|190|쓰다/bitter|not_selected_debt_retained|—|
|193|수영장/swimming_pool|other_pilot_actual|276|
|193|미술관/art_museum|not_selected_debt_retained|—|
|234|목/neck_throat|not_selected_debt_retained|—|
|234|감/persimmon|not_selected_debt_retained|—|
|234|나뭇잎/leaf|not_selected_debt_retained|—|
|242|회의/meeting_work|not_selected_debt_retained|—|
|242|벽/wall|not_selected_debt_retained|—|
|254|나뭇잎/leaf|not_selected_debt_retained|—|
|255|돌/stone|other_pilot_actual|299|
|255|풀/grass|other_pilot_actual|299|
|276|이/tooth|same_text_actual|—|
|284|테이프/adhesive_tape|same_text_actual|—|
|284|던지다/throw|other_pilot_actual|299|

## B：新5語の初出自然さ

|番号|対象語|新出token合計U|対象token|N|previous|review|conflict|
|---|---|---|---|---|---|---|---|
|020|닦다|2|1|135|98.519%|7|0|
|033|공|2|1|133|98.496%|5|0|
|110|들다|2|1|134|98.507%|5|0|
|111|그림|2|1|131|98.473%|7|0|
|127|붙이다|2|1|130|98.462%|7|0|

020は机の水を拭く。033は誕生日のボールの受け渡し。110は階段で友達の荷物を持つ。111は絵で家と学校を話す。127は糊で写真を貼る。対象語は各1token、同回のもう一つの新出語も各1token。場面の目的・対象・解決に関与させ、初出内反復を増やしていない。

早期Bの制約にも注意：020では이/toothや칫솔は未導入なので歯磨きはしない。033では던지다が未導入なので球の投擲はしない。111では그리다が未導入なので描画はしない。127では테이프が未導入なので풀/glueを用いる。既出後のAで標準場面を検証した。

## lexical gapが解消された用例

**이＋닦다（K1-276）**

저는 욕실에서 이를 먼저 닦아요.

**테이프＋붙이다（K1-284）**

그리고 작은 테이프를 저에게 줘요.
저는 이것을 상자에 천천히 붙여요.

**던지다＋공（K1-299）**

친구는 작은 공을 가지고 와요.
친구는 저에게 공을 먼저 던져요.
저는 공을 잡고 많이 웃어요.
다시 친구에게 공을 천천히 줘요.
친구는 저에게 공을 또 던져요.
하지만 공이 나무 뒤로 가요.
우리는 나무 뒤에서 공을 찾아요.
거기에 작은 공이 하나 있어요.
저는 공을 천천히 다시 주워요.
저는 친구에게 공을 다시 던져요.

**미술관/그리다＋그림（K1-189）**

저는 미술관에 가고 싶어요.
저는 그림을 보고 싶어요.
집에서도 공책에 그림을 자주 그려요.
오늘은 그림을 같이 보고 싶어요.
저는 그림의 이야기를 천천히 설명해요.

**가방/책＋들다（K1-110）**

그래서 친구의 가방을 먼저 들어요.

들다は手で荷物を持つ中心義だけ。Core찍다/take_photoを使用し、stamp義・도장・배터리等の未採用語は使わない。生解析のsenseラベルだけで別義を承認しない。

## 語彙負荷・高速多読ゾーン

A選択review分布：`{'min': 0, 'max': 8, 'mean': 5.9, 'median': 6.5, 'p90': 8}`。

A実使用Expansion（extra既出込み）分布：`{'min': 2, 'max': 20, 'mean': 14.5, 'median': 15.0, 'p90': 19}`。

B選択review分布：`{'min': 5, 'max': 7, 'mean': 6.2, 'median': 7, 'p90': 7}`。

B実使用Expansion（extra既出込み）分布：`{'min': 9, 'max': 14, 'mean': 11.4, 'median': 11, 'p90': 14}`。

5〜8はsoft目標。001は先行語がなく0、150/234/255は自然に承認できる候補が3/4/4であり、数のための副次事件を足さなかった。選択reviewの減少と本文全体のExpansion密度は別指標として監視する。

|高速番号|어절|review|全実使用Expansion|最近20本のE3|previous|自己評価|
|---|---|---|---|---|---|---|
|276|135|8|19|0|100.00%|単一の問題・目的。人間による速度評価は未実施。|
|284|139|7|18|0|100.00%|単一の問題・目的。人間による速度評価は未実施。|
|299|135|8|14|0|100.00%|単一の問題・目的。人間による速度評価は未実施。|

高速3本は新出0。最近20本に初出したE3の集中なし。ただし既出語でも読者が自動化できている保証はなく、実読速度・疲労は人間で確認する。

## annotation・解析の限界

25本：378候補を49型へ整理。`{'benign_expected': 321, 'requires_lexical_sense_review': 9, 'requires_grammar_boundary_review': 48, 'true_unresolved': 0}`。

|群|annotation候補数|まとめた型数|カテゴリ別件数|
|---|---|---|---|
|A|302|47|{'benign_expected': 253, 'requires_lexical_sense_review': 7, 'requires_grammar_boundary_review': 42, 'true_unresolved': 0}|
|B|76|16|{'benign_expected': 68, 'requires_lexical_sense_review': 2, 'requires_grammar_boundary_review': 6, 'true_unresolved': 0}|

旧269件との比較対象はAのみ。Bの5本文を足した25本合計を旧20本の件数と直接比較しない。表現量と解析ヒントも変わっているため単純な改善率とはしない。

benign_expected／lexical sense／grammar boundary／true unresolvedを分離。저・제の構造上明確な代名詞は型でまとめ、일・풀・이の文脈義、들다の物理義、compoundと助数詞は条件を限定してレビューする。型の承認を全用法へ拡張しない。raw未解決内容語は全本文0。

既存Kiwiと規則は変更せず、Phase 2.2専用に수건/제일/물어보/오래되の登録語ヒントと、묻+어+보→登録lemma 물어보다の一어절内groupingを追加。raw形態素と境界レビューを保存した。묻다単独は依然未許可。新たな外部依存は追加していない。

草稿では禁止-기/-지 않다/-게、未来連体、未導入語が検出され本文を修正した。さらに人間的な語義監査で일/workを一般活動の名詞化に流用する文、들다を「気に入る」にする文も除いた。自動ラベル一致だけでは語義の正しさを保証できない実例である。

## schedulerの運用証拠と残る条件

新出アンカー→scene→作者承認したreview候補→schedulerの意味適合・期限・過去回数・距離・意味領域分散の順位付け→本文→再解析の順で記録。候補判定はauthor judgementで、全候補プールを無理に本文へ入れない。selectionスコアと除外理由を各JSONに保存し、validatorが履歴から再計算する。

先行未生成回はintroduction-onlyの仮種まき。架空の背景reviewは作っていない。exposure_ledgerは仮定と25本の生成annotationに基づく出現を分離した。期限債務は現実の300本連続運用の測定ではない。500語×6つの異なる本文での最終実出現は、25本では証明しない。

medium confidence：아저씨の呼称語用、미술관/박물관の区別、결국の結末での自然さ、관심の関心対象の文脈を人間で確認。今回はいずれも文脈に役割があるが、自動PASSを母語話者承認に置換しない。

## 最終判断・成果物

**機械hard条件を通過し、少数パイロットの人間レビューへ進める。全300本の大量生成には進めない。** B5で初出の中心性を実本文として検査できた。次はA/Bの自然さと訳、語義境界、5〜8reviewの成立、本文全体のExpansion密度を確認する。連続生成時のwindow債務と最終6露出は別途必要。

凍結manifest：k1_phase2_2_input_freeze.json。本文：pilot/ko/k1/phase2_2/texts/ の25 JSON。

検証：k1_phase2_2_validation_result.json。比較：k1_phase2_2_comparison.json。型別annotation：k1_phase2_2_annotation_triage.json。人間レビュー：k1_phase2_2_pilot_review_A.md / _B.md。

再現：`python -B scripts/build_k1_phase2_2.py`、検証：`python -B scripts/validate_k1_phase2_2.py --save`。再現は承認済み25本だけを上書きし、旧pilotと正式DBを更新しない。

テスト：[{"command": "python -B -m unittest discover -s tests -v", "status": "PASS", "tests": 63, "elapsed_seconds": 176.579, "scope": "Full regression suite before final narrative clarity edits and fourth registered segmentation hint; followed by focused final verification."}, {"command": "python -B -m unittest discover -s tests -p test_k1_phase2_2.py -v", "status": "PASS", "tests": 12, "elapsed_seconds": 32.158, "scope": "Final 25-text corpus, final analyzer policy, raw QA, A/B selection, malformed data and sparse-history tests."}]
