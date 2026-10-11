# Phase 3 再試験 — K1-002で構造的停止

## 判定

**C / FAIL（解析器修正が必要）**。新run `phase3_retry` はK1-001をcommitし、K1-002の初稿をrejectした時点で停止した。K1-003〜050、051以降、300本量産は実施していない。50本の逐次運用成立・review debt回収・genre分布について結論を出せる段階ではない。

Phase 3.1のapproved candidate gate、allowed vocabulary snapshot、限定resolver、atomic commitを再利用した。過去run・語彙800・文法32・初出予定・review windows・ID migration・自然さguidelineは変更していない。432ファイルのfreeze検証違反は0件。ledger内部のphase表示は承認済み3.1形式のschema provenanceであり、実行identityは新しいdirectory/control/ledgerで分離している。

## 逐次処理と停止規則

001のcandidateを解析・reject・repair・再解析し、PASS後のみatomic commit。その実績2語だけを002のprevious Expansionへ許可した。3.1 smokeの実績や予定上の導入済み語は流用していない。snapshotは001: Core300＋当該新出2、002: Core300＋実導入済み2＋当該新出2。登録固有名詞と固定例外は別枠。

最大5attempt。同じhard errorが2回連続で改善しなければ停止する。長さは許容範囲までの残り距離、coverageはhard floorとの差、語彙違反は同じID/lemmaの違反個数で改善を判定する。別のerrorの改善では同一errorの停滞を免除しない。5回の改善中FAILでも予算を尽くせば停止。構造的障害は試行回数を使い切る前に停止する。

| 教材 | attempt | 判定 | 어절 | 理由 |
|---|---:|---|---:|---|
|001|1|REJECT|123|`밥하고`を未登録`밥하다`へ誤解析。controlled/previous hardも失敗|
|001|2|PASS → commit|129|自然な文分割で修復。新出2lemma、2tokens|
|002|1|REJECT → run停止|135|raw `네/IC` を `너/pronoun`へ無条件alias。予定新出`ko_k1_0442`未認識|

001の129어절はdraft soft target130〜150を1下回るが、hard120〜180は満たす。filler追加で境界を調整しない。002は「はい・いいえ」を本選びの直接対話に各1回配置したが、解析のidentityが誤ったためcommit禁止。

## 停止原因 — draft再生成では解決しない

`scripts/k1_pilot_analysis.py` の `ALIASES` が `네 → 너` をPOSや文脈を見ず適用する。実際のraw morphologyは `네 / IC`（感動詞）だが、annotationは `너 / pronoun / you_informal / ko_k1_0003`。registered `네 / interjection / yes / ko_k1_0442` が消える。

全文ではなく独立した短い3probe（`네.`、`네, 책이 있어요.`、引用符付き応答）でも診断した。詳細はvalidation JSONの `analyzer_diagnostics`。モデルannotationで「はい」と申告してもaliasを正当化しない。raw POS＋登録identity＋局所contextの照合が必要。

002の機械値 controlled=100%、previous=99.2308% は誤ったannotationを前提とした値であり、正しいsense coverageの証拠として採用しない。予定語一致gateが誤承認を防いだ。002の `actual_first`・exposure・review・debt payment・genre/scene historyへのcreditはすべて0。

**修正候補（report-only）**：`네 → 너` をpronoun contractionとしてraw POSと局所統語が支持する場合だけ適用し、`IC` の `네` は登録interjectionへ解決する。alias後の登録POSとraw POSが不一致なら黙って唯一候補へfallbackせずREVIEW/reject。`네`感動詞／`네`所有代名詞／`네`数詞の対照テストを追加する。`밥하고`についてもnoun＋許可粒子と複合動詞の分割候補を対照検証する。語彙DBやgrammarの拡張は不要。今回、freeze対象の解析器を修正して停止runを再開することはしていない。

## 指定された運用指標

| 指標 | 結果・分母 |
|---|---|
|commit済み本文|1本、001のみ|
|1発PASS率|0/1 = 0%（commit済み教材の初回合格率）|
|全開始教材の初回PASS|0/2、002は構造的停止|
|平均attempt数|2.0/commit済み教材。全開始教材では3/2 = 1.5|
|candidate合格|1/3|
|retry／reject理由|unknown_or_unresolved 1、coverage_or_token_policy 3、planned_new_not_present 1。error個数であり教材数ではない|
|future vocab混入率|0/3 candidate = 0%|
|resolver REVIEW|0（全文resolver decisions。歩行場面は未生成）|
|実導入語|2: 되다、괜찮다、各001で1token|
|selected review exposure|0|
|incidental exposure|0|
|review debt|outstanding0、near-deadline0、expired0。最初のwindowがまだ開いていないため|
|naturalness warnings|1: verb argument frame（本人が教師へ名前を伝える実際の自己紹介）|
|semantic確定問題の再発|0。人間承認ではなくauthor second passでの判定|
|scene/genre重複|commit済み1本、family1。連続反復の検証には不足|

レビュー5〜8語はsoft target。001/002には開いているreview windowがないため0であり、無関係な行動を追加して数を埋めていない。数学的回収不能なdebtもないが、50本での運用は未検証。

## Hard validationとreadability

commit済み001: controlled=100%、previous=98.425197%、N=127、U=2、hard errors0、future0、unresolved0、grammar32外0。99%target missはhard98%を満たすためblockerにしない。32文、最大5어절、3〜7preferredは31/32文。2어절の「동생은 괜찮아요.」は自然な状態文として許容。短文を副詞で引き延ばしていない。

最終再解析の不一致0、ledger epoch1、001へのcreditは1回。failed evaluation前後のledger SHAは一致。検証時にもstate byteを変更していない。run integrity errors=0。これは停止runの記録が正しいという結果であり、50本生成のPASSではない。

## Phase 2.3との比較

共通番号001だけを比較。旧本文をコピーせず、弟の初登校に付き添う場面を新規作成した。本文一致: False。新版本文は129어절、previous 98.4252%。旧版は126어절、previous 0.984。旧pilotのreview実績を新runに移植していない。過剰な의、習慣進行、意味不明な좋아하다反応、filler密度のwarningは出ていない。名前を伝える文は「呼ぶ」の代用ではなく、本人紹介なのでwarning-onlyで残した。020/033/040は未生成につき比較未実施。

## Checkpoint・次の判断

10/20/30/40/50 checkpointの間隔を維持するが、今回は002で停止したため、その時点の `phase3_retry_checkpoint_002.md/json` のみ作成。未到達checkpointを成功として作らない。

**次は解析器のPOS条件付きaliasを別versionで修正・regression testし、新しいrunを001から再試験する。** この停止runやPhase 3.1を成功扱いに書き換えない。K1-003以降、50本の継続生成、300本量産へは進まない。

## Tests

全体suite 147件PASS（334.898秒）。最終更新後のfocused retry tests 14件PASS（20.779秒）。最大5回・2回停滞STOP・改善継続・失敗state不変・commit一度・停止理由保持を検証。テストPASSは制御の正常性であり、既知の네誤aliasの解決や50本文の成功を意味しない。candidate schema違反0。
