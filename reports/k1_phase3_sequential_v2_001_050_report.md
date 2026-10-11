# Phase 3 sequential v2 — K1-002で停止

## 判定

**C / FAIL：引用境界を含む解析器の修正が必要。** 新run `phase3_sequential_v2` は実績ゼロから開始し、001の第2candidateをhard PASS後に1回だけatomic commitした。002の第1candidateはrejectし、独立した短い対照probeで構造的問題を再現した時点で停止した。003〜050、051以降、300本量産は行っていない。元のPhase 3 / retry / 3.1 / 3.2の成功・失敗履歴を書き換えていない。

## 採用した制御と実処理

承認済み3.2 analyzer/resolverを直接importする別run adapter。approved gateを複製した差分はrun名、50上限、source schema参照、engine digest対象。snapshotはCore300＋このrunの実導入済みExpansion＋当該教材のplanned新出語だけ。max5attempt、同じhard errorが2回連続で改善しなければSTOP、candidateはstateを変更せず、hard PASSのfinal raw reanalysis後にだけatomic publish。10本ごとcheckpointを維持し、問題がなければ承認待ちせず継続する。

今回は構造的問題を発見したため、002のretry回数を使い切る前に停止した。引用符を外して解析器の欠陥を隠すための再生成は行わず、run内で解析器・語彙・文法・初出・windowを変更しなかった。draft target130〜150、hard120〜180、新出≤2、U soft3、controlled100%、previous≥98%、sentence max10を維持。長さ合わせのfillerを追加していない。

|教材|attempt|判定|어절|error種類|
|---|---:|---|---:|---|
|001|1|REJECT|140|coverage_or_token_policy, future_expansion|
|001|2|PASS → commit|140|0|
|002|1|REJECT|133|coverage_or_token_policy, future_expansion, planned_new_not_present, title_permission, unknown_or_unresolved|

001 attempt1の끝내다は未導入語で、Core 끝나다の自然な文 `공부가 끝나서 저도 쉬어요.` へ修正してattempt2 PASS。これはcandidate内の局所repairで解決できた。002には未導入열리다と未許可の未来連体修飾を使ったtitle `동생에게 줄 책` もあり、これらはdraft側の別問題。構造的停止の根拠と混同しない。

## 構造的停止の根拠

|対照|raw / 解決|結果|
|---|---|---|
|`아니요, 책이 너무 비싸요.`|IC → 아니요 / interjection / no_polite|正しく認識|
|`"아니요, 책이 너무 비싸요."`|VCN 아니＋EC 요 → Core 아니다、요未解決|予定新出 ko_k1_0443 が欠落|
|`한국어 책이 있어요?`|한국어 / noun / korean_language|正しく認識|
|`"한국어 책이 있어요?"`|MM 한＋NNG 국어 → 하나、국어未解決|登録Core ko_k1_0169 のidentity欠落|
|`"네, 여기 있어요."`|IC 네 → interjection / yes|3.2の修正は機能|

引用符あり/なしで同じ自然な直接応答・質問のidentity解決が変わる。モデルannotationを付け直して承認しない。003以降へ進まず、[diagnostics JSON](k1_phase3_sequential_v2_analyzer_diagnostics.json)へ8probeのraw形態素とannotationを保存。probeは教材/露出ではない。

**修正候補（report-only）：** 次の別versionで、引用符・句読点境界を保ったままregistered surfaceとraw spanの再結合候補を検討する。아니요のIC / VCN+요候補には直接否定応答のsyntaxを要求する。한국어のMM+NNG分割には空白なしの完全登録lemma一致と名詞位置を要求し、`한 국어 ...` を同一視しない。無条件aliasや唯一登録候補fallbackを導入せず、quoted/unquoted同じ対照fixtureを文・段落・全文で検証する。語彙DB・POS・senseを変える必要はない。

## 指定指標

|指標|結果・分母|
|---|---|
|commit数|1（001のみ）|
|1発PASS率|0/1 committed教材 = 0%。開始済みでは0/2|
|平均attempt数|2.0 / committed教材。全開始済みでは3/2 = 1.5|
|candidate数 / reject数|3 / 2|
|future vocab混入率|2/3 candidate = 66.67%。commit済みでは0/1|
|resolver REVIEW|0（resolver decisionで明示REVIEWの件数）|
|raw unresolved content（reject側）|4。REVIEW件数0は解析完全性を意味しない|
|実導入語|2: 되다 / 괜찮다、各001で1token|
|actual selected review exposure|0|
|incidental exposure|0|
|review debt|outstanding0 / near-deadline0 / expired0|
|naturalness lint|2（{'nat_restricted_sense': 2}）|
|semantic確定問題の再発|0、ただし人間承認は未実施|
|scene / genre|work1。直近10本類似判定の比較pair0、連続多様性は未検証|

retry理由分布は同じcandidate内の複数error・派生coverage errorも個別に数える。独立原因数や教材数とは異なる。

|error code|件数|
|---|---:|
|future_expansion|2|
|coverage_or_token_policy|10|
|unknown_or_unresolved|4|
|planned_new_not_present|1|
|title_permission|1|

## Hard validation・state integrity

commit済み001: 140어절、35文、最長5어절、N136、U2、controlled100%、previous134/136 = 98.529412%。99% target missはhard98%を満たすためblockerではない。3〜7 preferred compliance34/35 = 97.14%、1어절の`괜찮아요.`は自然な短い応答として許容。未導入/future/retired/invalid/unresolved/grammar32外は0。

fresh再解析mismatch0。epoch1/cursor1/records1/text projection1、導入/露出/genre/scene更新は1回のみ。失敗candidateの評価前後ledger SHAは全件一致。002のactual first、review、incidental、debt payment、genre/sceneへのcreditはすべて0。現在のdeadlineはまだ開いていないので、debt0はwindow運用の成功証拠ではない。

integrity errors=0、candidate schema errors=0、frozen入力508ファイルの変更/欠落0。新adapter safety testsは9件PASS（実際のテスト結果JSON参照）。全50本のPASSではない。

## Naturalness・読みやすさ

001は新規に書いた「翌日の初授業を友人と練習する」scene。不要な의や、好き＝喜ぶの万能反応、習慣の進行形化、reviewのためだけの別事件はない。쓰다の2warningは公책への書き取りであり、別義への拡張はしていない。warning-onlyで記録し、人間による韓国語自然さ承認の代替にしない。日本語訳は本文修正後に対応文を更新し、끝나다を「勉強が終わる」と訳した。translation lint flags0。natural_expression_gap0、펴다の継続監視は残し、今回は実例0。

露出分布0回498語 / 1回2語。genre work1、平均/最小/最大140어절。最初のreview windowが開く前に止まったため、5〜8review、incidental、500×6への進捗、debt回収、scene重複、genreバランスの実運用成立は判断不能。

## Phase 2.3比較・checkpoint

001だけを比較。Phase 2.3本文をコピーせず、別sceneとして生成した（本文一致false）。旧pilotのreview実績は引き継がない。comparisonのcoverage/eojeolはvalidation JSONに記録。020/033/040には到達していないので比較していない。

10/20/30/40/50のcheckpointは未到達で、成功checkpointを捏造しない。停止時点の[checkpoint002](phase3_sequential_v2_checkpoint_002.md)を保存した。

## 次の判断

**C — analyzerの引用境界・登録lemmaの分割回復を別versionで修正し、対照testsと001〜002 smokeを通した後、新しい別runで001から連続再試験する。** この停止runを修正成功へ書き換えない。K1-003以降・300本量産は許可済み扱いにしない。
