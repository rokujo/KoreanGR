# K1 Phase 2.1 review scheduler設計・dry-run

本文は生成・再生成していない。Phase 1.2の800語・32文法・導入予定とPhase 2の20本文・レポート・検証結果はSHA-256照合で保存した。語彙交換も未適用。

## 判定範囲

windowデータ・期限債務処理・件数容量は成立。23件を全件replayし、場面適合と日付予約を分けて評価した。移動先は未生成教材の仮の場面カードであり、本文の自然さ・実出現・coverageの実測を保証しない。

Phase 2の旧overall FAIL 12件は履歴として維持する。言語hard違反は0件、20本すべてcontrolled100%、previous98%以上、文法・長さ・一文上限を満たした。新方式では固定review欠落を言語hard failureとみなさない。

## 方式と適用優先順位

`vocab_review_windows.json`をPhase 2.1以降のreview用overlayとして使用する。初出は従来のintroduction_schedule.jsonを唯一の正式入力とし、vocab_exposure_schedule.jsonのreview_textsは歴史・比較用に限る。旧validatorと旧pilotのschedule_passは書き換えない。profileのcoverage・初出・文法・長さ仕様はそのまま使用し、固定review割当だけ新overlayを優先する。

残り150本以上：+2〜5、+6〜24、+25〜65、+66〜119、+120〜300末尾。残り90〜149本：+2〜5、+6〜19、+20〜39、+40〜69、+70〜末尾。残り45〜89本：+2〜5、+6〜15、+16〜23、+24〜L−1、+L〜末尾（L=max(35,min(60,floor(残り×.75)))）。すべて初出より後、5窓、重なりなし、最終窓の終点300。初出255の場合も5つの異なる後続教材を確保する。

1. 当該教材の新出IDを取得し、新出語の意味を中心に場面候補を作る。新出0ならreview候補の共通目的から場面を選ぶ。
2. 初出が実出現として確認された語だけを候補プールに入れる。scene affinityで粗く絞り、場面内の使い方の肯定的確認とvetoを受ける。タグ一致だけで採用しない。
3. 意味適合100×一致率、期限接近20/残り日数、期限超過債務、実出現不足4×不足本数、直近との距離で順位付け。同じscene領域（affinityの第一候補）の採用が増すと12ずつ減点、距離3未満は30減点。品詞やカテゴリが同じだけで類義語扱いにしない。係数・domainは設計初版で、自然さの証明ではない。
4. 5〜8語をsoft目標とする。scene側が同じ目的で統合できると確認した場合だけextra capacityを渡す。API上0語も許容し、語数未達のための一文追加をしない。10語超または新出含む12語超は負荷警告を返す。
5. 本文・sense・coverage検証後のconfirmed IDsだけrecordする。選択だけでは出現扱いにしない。実台帳は教材順に記録し、同教材内の複数tokenは1本。未来語・旧ID・未確認初出のreviewを拒否する。

## 未消化と最終期限

windowの期限切れは即FAILでなく債務として残し、同窓後半または後の窓で消化する。1出現は最古の未消化窓1つにしか充当しない。未開窓へ前払いしない。先行する任意の再出現も実際の異なる教材数には計上するが、分散窓の代用にはしない。3本の距離はsoftで期限を優先できる。

auditは期限まで3本の語・期限切れ債務・残り教材数では6本に到達できない語を警告する。300終了時は初出の実確認と6本以上の実出現がhard条件。分散窓未達は別途警告して、近距離だけで6本を埋めた語も点検する。301への繰越は許可しない。終盤は締切在庫からsceneを設計し、適合できない語が残れば語彙・導入期・場面設計の修正候補を報告する。deadlineは意味vetoを解除しない。

## 容量と負荷

500語×5review=2,500回、平均8.333回/300本。全ての実再遭遇をscheduled reviewだけで満たし、全教材8語上限とする場合は2,400回で100回不足し、序盤はさらに候補が少ない。一方、scheduled以外の自然なprevious Expansionの実出現も6本の条件へ数えられるため、scheduled 5〜8という目標自体は矛盾しない。runtime recordにはscheduled以外も含め、既に6本を満たした語を追加要求しない。

意味を制約しないinterval EDFで、1教材10reviewの仮容量にて2500回を配置。未配置0回。これは数的可能性の証明のみであり、実行用の固定割当ではない。

|対象|min|max|mean|median|p90|
|---|---|---|---|---|---|
|全300本review|0|10|8.333|10.0|10|
|新出含むExpansion|0|12|10|10.0|12|
|276〜300 review|0|10|8.4|10|10|

8review超は175本。最終25本の最近20本以内導入E3は0件。このEDFは全2,500回を予約扱いにした容量証明で、5〜8語に均した自然な運用のサンプルではない。自然なextra previous語の確認で実際のscheduled必要数を減らし、余剰候補・債務の分散をPhase 2.2で実測する。

## 23 conflict replay（元本文は保存）

元の場面は全件semantic vetoでreject。以下の日付は固定要求ではなく、候補探索が得た仮予約である。既存20本文は移動先として再編集せず、同語の既存出現日や同日予約を避けた。仮予約は1教材1つの場面目的にし、互いに無関係な移動案を同じ教材へ統合しない。移動先の新出語にscene affinityが合う場合だけ候補にする。helpersはその時点の導入済み登録語へ照合する。

|元教材|語 / sense|元窓|結果|窓index移動（0始まり）|仮候補|場面目的|判定|
|---|---|---|---|---|---|---|---|
|K1-150|물고기 / fish_animal|143〜161|carry_to_next_window|1→3|K1-225|川で生きた魚を観察する|conditional_scene_fit|
|K1-170|계산하다 / pay_bill|127〜180|carry_to_next_window|3→4|K1-187|必要な品を買って代金を払う|conditional_scene_fit|
|K1-170|찍다 / stamp|161〜174|carry_to_next_window|1→2|K1-182|学校の受付で紙に判を押す|placement_only_lexical_gap|
|K1-184|새롭다 / new|179〜198|carry_to_next_window|2→3|K1-212|初めての授業を受けて新しい経験を話す|conditional_scene_fit|
|K1-184|급하다 / urgent|175〜188|carry_to_next_window|1→2|K1-198|出発まで時間がなく移動を急ぐ|conditional_scene_fit|
|K1-189|이불 / bedding|183〜236|same_window_other_text|3→3|K1-192|泊まる友達の寝具を準備する|conditional_scene_fit|
|K1-189|맵다 / spicy|184〜203|carry_to_next_window|2→3|K1-222|辛い食事を注文して味を確かめる|conditional_scene_fit|
|K1-189|테이프 / adhesive_tape|187〜190|carry_to_next_window|0→1|K1-197|学校で必要なテープを買い、友達にも渡す|conditional_scene_fit|
|K1-190|버리다 / discard|170〜210|same_window_other_text|2→2|K1-194|掃除して不要な紙を捨てる|conditional_scene_fit|
|K1-190|쓰다 / bitter|185〜204|carry_to_next_window|2→3|K1-223|茶を飲んで苦い味を確かめる|conditional_scene_fit|
|K1-193|수영장 / swimming_pool|191〜194|carry_to_next_window|0→3|K1-256|プールへ行って泳ぐ予定を相談する|conditional_scene_fit|
|K1-193|미술관 / art_museum|191〜194|carry_to_next_window|0→3|K1-257|美術館へ行く道と入館を相談する|conditional_scene_fit|
|K1-234|목 / neck_throat|224〜243|carry_to_next_window|2→3|K1-250|喉が痛く病院へ行く|conditional_scene_fit|
|K1-234|감 / persimmon|228〜237|carry_to_next_window|1→3|K1-262|家族のために柿を選んで食べる|conditional_scene_fit|
|K1-234|나뭇잎 / leaf|230〜239|carry_to_next_window|1→3|K1-267|落ちた葉を観察し季節の変化を話す|conditional_scene_fit|
|K1-242|회의 / meeting_work|239〜274|same_window_other_text|3→3|K1-268|会議の開始時間と準備を確認する|conditional_scene_fit|
|K1-242|벽 / wall|226〜255|same_window_other_text|3→3|K1-244|部屋の壁の色を見て写真を飾る場所を相談する|conditional_scene_fit|
|K1-254|나뭇잎 / leaf|248〜280|same_window_other_text|3→3|K1-269|落ちた葉を観察し季節の変化を話す|conditional_scene_fit|
|K1-255|돌 / stone|249〜280|same_window_other_text|3→3|K1-271|散歩中の道の石を見て歩く場所を選ぶ|conditional_scene_fit|
|K1-255|풀 / grass|249〜280|same_window_other_text|3→3|K1-272|草が多い場所で座る場所を選ぶ|conditional_scene_fit|
|K1-276|이 / tooth|276〜300|same_window_other_text|4→4|K1-277|歯が痛いという問題を中心に病院へ行く|conditional_scene_fit|
|K1-284|테이프 / adhesive_tape|255〜300|same_window_other_text|4→4|K1-285|学校で必要なテープを買い、友達にも渡す|conditional_scene_fit|
|K1-284|던지다 / throw|281〜300|same_window_other_text|4→4|K1-286|海へ小さい石を投げ、届く場所を比べず観察する|conditional_scene_fit|

carryは次以降の窓への繰越を表す。複数窓を越えても最古の未消化債務を1回だけ充当する。元教材で使う0件、結果内訳：{'carry_to_next_window': 13, 'same_window_other_text': 10}。場面仮適合：22/23件。日付だけの候補は自然な本文成立とは数えない。

찍다(stamp)は道具語도장の不足候補があり、仮予約してもpositive gateを通さない。語彙微修正または別の自然な実現が確認されるまで未解決として残す。테이프は貼る動作を要しない「買って渡す」、이は元本文に歯痛を追加せず別教材の歯痛を主目的とする、던지다は導入済み돌を投げる別の場面に逃がす。これらは一般的な貼付・歯磨き・球遊びの語彙不足を解消したことにはならない。

## coverage policy（変更なし）

controlled coverage hard100%、previous hard98%、target99%、新出lemma最大2、新出token soft合計3。N/Uの定義はprofile.countingに従う。(N-U)/N>=.98をhardとする。U=2かつN<200なら99%target未達は計算上予想され、mass-generation blockerにはしない。controlled違反や他のhard条件は引き続きblocker。

## annotationの分類と集約

269件を50の型×語義×形態パターンに集約。分類は承認ではなく優先順位付け。

|区分|出現件数|テンプレート群数|
|---|---|---|
|benign_expected|231|31|
|requires_lexical_sense_review|11|5|
|requires_grammar_boundary_review|27|14|
|true_unresolved|0|0|

저のNP/MM・登録NNG+XSV/XSA/XSN複合・数詞直後の登録counterは期待される構造型。ただし一度は型の確認を行う。눈・일・쓰다等の同POS多義、茶の써(VV解析)、흘리다の涙義はsense確認群。안/수/거や다른の文法境界は許可構文テンプレートを確認する。未知の型・span不一致・DB不一致はtrue_unresolvedとして個別確認。

代表文脈1件＋全発生位置を新dry_run.jsonに保存し、型承認後の同条件例は一括処理する。自動生成annotationを独立した正解とはみなさない。語彙・文法・解析器・規則の版が変われば承認cacheを無効化する。269件を個別に無条件確認する運用へは戻さない。

## validator・履歴・次の判断

Phase 2.1 validator: PASS、errors 0。既存800語validatorと全テストも維持する。詳細はk1_phase2_1_validation_result.json。旧pilot validatorの12 schedule FAILは旧履歴として正常に残る。

再現コマンド：`python -B scripts/build_k1_phase2_1.py`（新成果物だけ再作成）、`python -B scripts/validate_k1_phase2_1.py --json`（設計検証）、`python -B -m unittest discover -s tests -v`（既存＋追加テスト）。

実台帳の形式は`[{"text": 1, "confirmed_ids": ["ko_k1_0373", "ko_k1_0413"]}, ...]`。各教材の実出現したExpansion全IDを渡す。`python -B scripts/validate_k1_phase2_1.py --actual-ledger <path> --through-text 150 --json`で途中の債務を点検し、300終了後だけ`--through-text 300 --final`を指定する。本文検証済みという出所は呼び出し側が保証する。パイロット20本だけの台帳で全300本の達成を推定しない。

A「800語の微修正」を先に人間レビューすることを推奨する。少なくとも닦다・붙이다・공・그림・들다は基本場面の表現幅に直接効く。採否後、IDを新規採番しbudget/tier/migration/初出の整合を別Phaseで確定してからB「Phase 2.2で20本再生成」へ進む。交換は本Phaseで適用していない。大量生成はまだ進めない。

残る人間判断：交換5組の採否、찍다(stamp)維持の必要性、scene affinityの狭さと使い方、9〜10語超を許容する場面、window繰越で失われる近距離再遭遇、annotationテンプレートの初回承認。外部依存は追加していない。

## 作成ファイルとテスト記録

- config/languages/ko/k1/vocab_review_windows.json / vocab_review_windows.schema.json
- scripts/k1_review_scheduler.py / k1_annotation_triage.py / build_k1_phase2_1.py / validate_k1_phase2_1.py
- tests/test_k1_review_scheduler.py
- reports/k1_phase2_1_scheduler_report.md / k1_phase2_1_lexical_gap_report.md
- reports/k1_phase2_1_dry_run.json / k1_phase2_1_validation_result.json / k1_phase2_1_test_result.json

変更した既存ファイル：なし。dry_run.jsonの300行は本文でなく容量確認用のID割当。これを生成用の固定scheduleへ戻さない。

- `python -B -m unittest discover -s tests -v`：PASS、40 tests。Initial full suite: 26 unchanged existing tests and 14 initial new tests. New modules subsequently amended and checked by the final focused run.
- `python -B -m unittest discover -s tests -p test_k1_review_scheduler.py -v`：PASS、15 tests。Final new/changed modules, including schema, freeze, capacity, replay, actual ledger CLI and annotation triage.
