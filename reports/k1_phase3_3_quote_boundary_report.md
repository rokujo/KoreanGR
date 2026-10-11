# Phase 3.3 — quote boundary recovery

## 判定

**A / Phase 3.3 PASS。** 新run `phase3_3` でactual exposureゼロから001、002の順に検証し、hard PASS後にだけ各1回atomic commitした。003以降は生成していない。次は別runで001〜050の連続試験を再実施可能。このsmoke runを003以降へ継続せず、300本量産にも進まない。

## 修正

frozen `k1_phase3_2_analysis.py` と `k1_phase3_2_resolver.py` の結果へ、`k1_phase3_3_resolver.py` の登録surface復元layerを追加した。rawは編集しない。対象は아니요/ko_k1_0443/interjection/no_polite、한국어/ko_k1_0169/noun/korean_languageの2組だけ。raw indicesと元文字spanが隙間・重複なく連続し、内部空白/句読点なし、完全登録一致、POS列・局所構文が支持する場合のみannotationを復元する。

아니요は発話冒頭の否定応答＋後続句境界。コンマ付きのVCN+ECだけでなく、句点で終わるVCN+EFも対照testsで確認して明示した。Core 아니다の非応答用法へ広げない。한국어はMM+NNGの名詞位置だけを復元し、`한 국어`等の実際の空白は跨がない。quotes/SSO/SSC/SP/SF等は外側境界として残す。

任意token連結・無条件alias・唯一候補fallback・generated sense信用を導入していない。元annotationもauditに保存する。復元IDがfutureなら元のpermission gateでrejectする。語彙800、grammar32、初出・window・ID migration、自然さguidelineは変更なし。新依存なし（既存Kiwi/jsonschemaを使用）。

## parity・全文

5組のquoted/unquoted対照が全PASS。speaker narration、複数quoted turns、quote前後のpunctuation、smart quote、過去failed002全文でoffsetを照合した。10種類のunsafe境界fixtureではRECOVEREDを出していない。

|content|registered ID|結果|
|---|---|---|
|`아니요.`|ko_k1_0443|PASS|
|`아니요, 책이 너무 비싸요.`|ko_k1_0443|PASS|
|`한국어 책이 있어요?`|ko_k1_0169|PASS|
|`네.`|ko_k1_0442|PASS|
|`네, 여기 있어요.`|ko_k1_0442|PASS|

raw morphologyはPhase 3.2と同一。rawの誤分割を隠すのではなく、別annotation layerへidentityと証拠を追加した。K1-002のquoted `"네, 여기 있어요."` は3.2のIC処理を維持し、quoted `"아니요, 책이 너무 비싸요."` は正しくno_politeへ復元。quoted `"한국어 책이 있어요?"` もCore nounへ復元。

## smoke / 通常のdraft repair

元本文のraw sourceだけをfreeze履歴から再利用した回帰smoke。過去annotation、誤coverage、ledgerや予定上の露出は一切流用しない。新state epoch0、001commit後epoch1で初めて002のallowed snapshotを構築した。

|教材|attempt|判定|어절|hard error種類|
|---|---:|---|---:|---|
|001|1|PASS → commit|140|0|
|002|1|REJECT|133|coverage_or_token_policy, future_expansion, title_permission, unknown_or_unresolved|
|002|2|PASS → commit|133|0|

002 attempt1は元failed candidate全文をそのまま使い、quote identityは修復したが、future 열리다と未許可の未来連体title `동생에게 줄 책` はrejectした。planned 네/아니요はこの失敗candidateでも両方認識される。open-stateの`열려 있어요`に付随する未許可/未解決形態素も残して記録した。失敗後のstate SHAは不変。

attempt2はtitleを`동생에게 책을 줘요`へ、本文の`가게 문이 열려 있어요.`をCoreの`저는 가게 문을 열어요.`へ変更し、日本語訳も「私は店のドアを開けます。」へ更新した。自然な入店の行動であり、引用符を削除して回避していない。future語や文法を許可したのではない。titleも同じallowed vocabulary/grammar policyで再検証した。

## 最終hard result

|教材|PASS attempt|어절|N / U|controlled|previous|結果|
|---|---:|---:|---|---|---|---|
|001|1|140|136 / 2|100%|98.529412%|PASS|
|002|2|133|131 / 2|100%|98.473282%|PASS|

future 0、invalid 0、unresolved 0、grammar violations 0、committed hard errors 0。planned ID == actual IDは両教材で一致。新出tokenは各教材2、99% target missはhard98%を満たすためblockerではない。

001→002のfresh raw reanalysis mismatch0、candidate/recovery schema errors 0、validator errors 0。N/Uは修復後annotationから再計算し、過去のcoverage値を採用していない。

## state safety

ledger epoch=2、records/text projection/genre history/scene history各2。実導入4語、異なるvocab/text露出5組。failed attemptはactual first/exposure/review/debt/genre/sceneへcreditしていない。001/002のcommitは各一度、idempotent recoveryを維持。

selected review 0、incidental 1、outstanding debt 0、expired debt 0。002の実際に出たprevious 괜찮다だけがincidentalとしてcreditされる。review windowが開く前の2本文smokeであり、50本のdebt回収成立までは主張しない。

原Phase 3 sequential v2停止run、committed001、failed002、3.1/3.2 enginesを含む546ファイルのfreeze変更0。元runのC/FAIL・epoch1・停止statusはそのまま保存。新しい結果だけをPhase 3.3へ保存した。

## tests

|suite|tests|failures / errors|結果|時間|
|---|---:|---|---|---|
|all|198|0 / 0|PASS|187.061秒|
|focused|19|0 / 0|PASS|17.373秒|

Phase 3.2全fixturesを新layerで検証し、旧suiteも含め全PASS。negative POS、原文字列space、punctuation、欠落identity、Core 아니다、future permission、planned mismatch、retired、title、failed-state isolation、before/after atomic publish faultを含む。最初の開発testで未対応EF signatureとfixture件数の誤りを検出し、smoke開始前に修正した。最終suiteの成功で旧失敗履歴を書き換えていない。

## 限界と次

完全な韓国語解析・sense disambiguationを実装したとは扱わない。2 identity以外の未知signature、未閉鎖引用などは従来通りREVIEW/reject。自然さのsemantic自己評価も独立した人間承認ではない。自然さlint warnings 3、translation fidelity flags 0はhuman review対象の絞り込みに使う。

**A — 別runで001から050を連続再試験できる。** そのrunでもmax5attempt、2回停滞STOP、構造的問題STOP、10本checkpoint、050上限を維持する。Phase 3.3では003以降と300本量産は実施しない。

詳細: [validation JSON](k1_phase3_3_validation_result.json)、[quote recovery audit](k1_phase3_3_quote_recovery_audit.md)、[設計説明](../docs/ko_k1_quote_recovery_phase3_3.md)。
