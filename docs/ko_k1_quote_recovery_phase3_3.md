# K1 Phase 3.3 — registered surface recovery

Phase 3.2の解析器と限定resolverをそのまま使用し、その結果へ別layerを適用する。
元本文・raw form/POS・start/length・引用符・句読点は変更しない。
一般的なtoken連結や新しい辞書義の追加は行わない。

## 明示的な対象

|元surface|恒久ID / POS / sense|許可raw signature|
|---|---|---|
|아니요|ko_k1_0443 / interjection / no_polite|아니/VCN + 요/EC または 요/EF|
|한국어|ko_k1_0169 / noun / korean_language|한/MM + 국어/NNG|

正しく登録identityへ解決済みのsingle tokenは変更しない。
対象2語以外へこの処理を一般化しない。

## 共通の必要証拠

- original substringが登録surfaceへ完全一致する。
- 登録ID/lemma/POS/senseの組が一意に存在する。
- raw indicesが連続し、rawの文字spanが対象を重複・隙間なしで分割する。
- raw partsの文字列も一致し、内部に空白・句読点がない。
- raw POS列が上の明示signatureに一致する。
- 置換前annotationが対象raw indexだけを各1回所有する。
- 左側は独立した語の境界。引用内ならbalanced quote内の位置を保存する。

## 個別の必要証拠

아니요は発話冒頭かつ直後がコンマ・句点等の応答境界であること。
独立応答として妥当なsyntaxを要求し、`아니요가...`や`답은 아니요...`、
`저는 아니요...`を自動再結合しない。Core 아니다は対象外。

한국어は名詞位置にあること。後続名詞への修飾、名詞用の付属助詞、
または終端の独立名詞位置を要求する。`한 국어`・`한국 어`は完全一致でなく、
`한국어책`という長い未登録文字列のprefixだけを切り出して復元しない。

`아니"요`のように内部へ引用符を挟む文字列は対象surfaceでない。
SSO/SSC/SP/SF等は外側・contextの境界であり、結合する語の一部にしない。
未閉鎖引用では復元を保留する。語の所属・意味をquote strippingで変えない。

## 出力とpermission

`quote_recovery_audit`へraw parts/tags/indices、start/end、登録identity、
quotation context、boolean evidence、decision、置換前後annotationを保存する。
判定はRECOVERED / ALREADY_REGISTERED / DECLINED。

identityの復元はその教材での使用許可ではない。future Expansionである
아니요を001で復元しても、candidate gateがfutureとしてrejectする。
Core/actual previous/planned newのallowed snapshot、planned ID一致、
coverage、grammar32、title gate、length、atomic commitのhard条件を維持する。

## 検証と限界

quoted/unquoted parity、speaker narration・複数turn・句読点隣接、
過去failed002の全文、negative boundary fixture、Phase 3.2全contrast fixture、
28不規則活用probeと既存pilot用例、failed-state isolation・atomic faultをテストする。

これは完全な韓国語解析・sense disambiguationではない。生成annotationだけで承認しない。
新しい未知のsignatureや他lemmaの分割が見つかったら、無条件fallbackを追加せず
REVIEW/rejectとして証拠を保存する。
