# Phase 3 sequential v3 — K1-002で構造的STOP

## 結果

**C / FAIL：解析器の追加修正が必要。** 承認済みPhase 3.1〜3.3を採用し、別run `phase3_sequential_v3` を実績ゼロから開始した。001のattempt2だけをhard PASS・最終再解析後にatomic commitした。002のattempt2で全文と単文のPOS解決が変わる構造問題を独立再現し、停止した。003〜050を生成していない。051以降・300本量産も行っていない。

旧3.3の001/002やledgerのcreditは流用しない。新しい本文と訳を作成し、このrunの001実績だけを002snapshotへ含めた。過去の成功・停止履歴はfreeze照合で変更なし。

## Candidate gateと処理履歴

Core300＋実導入済みExpansion＋当該教材planned newだけをsnapshot化。max5attempt、同じhard errorが2回連続で改善しなければSTOP、analyzer構造問題でSTOPを維持。candidate評価はledgerを変更しない。hard PASSの最終再解析後だけcommitする。新adapterのsafety testsは9件PASS、failures0/errors0。

|教材|attempt|結果|어절|hard error code|
|---|---:|---|---:|---|
|001|1|REJECT|136|coverage_or_token_policy, unknown_or_unresolved, unresolved_context_ambiguity|
|001|2|PASS → commit|137|0|
|002|1|REJECT|解析前|candidate_format|
|002|2|REJECT|135|coverage_or_token_policy, unknown_or_unresolved, unresolved_context_ambiguity|

001初稿の `이야기해요` は未登録 `이야기하다`。`이야기를 해요` に修正してCore noun＋하다で自然に表現できた。DB・意味・文法を拡張していない。002初稿はscene enumにない `weather` により解析前のformat reject。登録scene `nature` へmetadataだけを修正した。002の次稿は登録Core `우리` のPOS identityを全文解析で失った。異なるエラーなので「同じhard errorが2回停滞」は発動せず、構造問題の即時STOPが発動した。attempt上限を使い切るまで構造問題を隠す再生成は行わない。

## 構造的STOPの独立再現

問題の文は `"우리 집에 올 거예요?"`。登録identityは `우리 / pronoun / we / ko_k1_0004`。

|解析スコープ|raw POS|identity/結果|
|---|---|---|
|引用符なし単文|NP|Core pronounとして解決|
|引用符あり単文|NP|Core pronounとして解決|
|短い話者叙述＋引用|NP|Core pronounとして解決|
|candidate内の該当段落|NNG（offset49）|未解決・REVIEW|
|candidate全文|NNG（offset238）|未解決・REVIEW|
|全文から引用符を除いた診断用対照|NP|未解決0|

短いquoted/unquoted probeのparityは通るが、段落と全文で失敗する。sentence16のprecheckはPASSした。したがって「引用符を付けると必ず失敗」ではなく、引用を含むより長い局所文脈でraw POSが不安定になる問題。raw morphologyを保存し、誤POSを唯一の登録候補へ無条件fallbackしなかったため、gateが安全にrejectした。引用符除去は診断だけであり、本文を改変して解析問題を回避・commitしていない。

11probeのraw span・annotation・REVIEWを[diagnostics JSON](k1_phase3_sequential_v3_analyzer_diagnostics.json)に保存。probesは教材でも露出creditでもない。`우리 안에 개가 있어요.` は曖昧な対照で、rawがNPになるため、これだけで「檻」義の正しい拒否を実証したとは扱わない。Coreのpronoun以外を自動許可しない。

既存3.3の `네 / yes` と `아니요 / no_polite` はquoted formを含め正しく認識された。002の予定新出 `ko_k1_0442 / ko_k1_0443` はactual identityと一致したが、別のCore identityの未解決を理由に本文全体をrejectした。

## 指定指標

|指標|結果・分母|
|---|---|
|commit数|1本（001のみ）|
|1発PASS率|0/1 committed = 0%。開始済み教材ベースも0/2。一般化できる標本数ではない|
|平均attempt数|2.0 / committed教材。開始済み教材ベース4/2 = 2.0|
|全candidate / reject|4 / 3|
|future vocab混入|raw解析済み0/3。全journalのfuture検出0/4（1件はformat rejectで未解析）|
|commit済みfuture/invalid|0 / 0|
|resolver REVIEW|2（candidate resolver decisionsのREVIEW数）|
|reject側unresolved content|2。commit側0|
|review / incidental実露出|0 / 0|
|review debt|outstanding0 / near-deadline0 / expired0|
|実導入Expansion|2語：되다 / 괜찮다、各001の1token|
|実露出分布|0回498語、1回2語|
|自然さlint|2件、`nat_restricted_sense`（答えを書く쓰다の文脈）|
|confirmed semantic issue / 再発|0 / 0。ただし人間承認は未実施|
|natural_expression_gap|commit本文0。펴다は継続追跡、今回実例0|
|genre / scene|school1、比較pair0。連続多様性は検証できない|

retry理由はerror code出現数であり、coverageの派生errorも数える。独立原因数や教材数とは異なる。

|error code|件数|
|---|---:|
|unknown_or_unresolved|2|
|unresolved_context_ambiguity|2|
|coverage_or_token_policy|6|
|candidate_format|1|

## Hard validation・coverage

commit済み001: 137어절、35文、最長5어절。N=133、U=2、controlled100%、previous 131/133 = 98.496241%。99% target missはhard98%を満たすためblockerではない。preferred3〜7の達成率は97.14%、hard max違反0。文法32外・future・retired・invalid・未解決はすべて0。

002 attempt2は135어절、N130、U2、controlled129/130 = 99.230769%、previous127/130 = 97.692308%。未解決1tokenをcontrolledにもpreviousにもcreditしていない。identityが未解決のまま `(N-U)/N` を使ってhard PASSとは扱わない。hard coverage違反として保存した。

fresh raw reanalysisで001のannotation・identity・coverageの差分0。candidate評価前後のledger SHAは全4件一致。failed attemptは導入・露出・review/debt・genre・sceneへcreditしない。epoch1 / cursor1 / record1 / text projection1。報告処理でもledger byte不変。integrity errors=0、実journal schema errors=0、freeze 583ファイルの変更・欠落0。

Core300 / Expansion500 / Total800 / tiers200/200/100 / grammar32、初出予定・review windows・coverage・ID migration・意味制限・自然さguidelineを変更していない。review windowが開く前の停止なので、debt0やincidental0はwindow運用成功の証拠ではない。

## 自然さ・訳・比較・checkpoint

001は韓国語の授業で難しい問題を理解して答えを書く場面。意味のないreview文、不要な의、習慣への進行形、좋아하다の万能反応は使用していない。천천히は難しい問題への説明の速さとして使う。쓰다の2warningは공책に答えを書く文脈として記録し、別義を認可しない。semantic self-reviewのYESと訳lint flags0は人間レビューの代替ではない。

Phase 2.3の001と本文は一致せず、新規sceneを生成した。旧本文のcoverage/어절/reviewとの差はvalidation JSONの `phase2_3_comparison` に保存。020/033/040へは未到達。10/20/30/40/50のcheckpointは未到達で作らず、停止時点の[checkpoint002](phase3_sequential_v3_checkpoint_002.md)を保存した。

## 次の修正候補（report-only）

1. 別analyzer versionで、Core `우리` のpronoun/NNG境界を原文字列・POS・名詞修飾位置・発話目的・引用境界・前後の人物参照から限定解決する。NNG→pronounのglobal aliasは不可。「檻」等の別senseを予算内へ追加しない。
2. 短文だけでなく、実段落と全文のquoted/unquoted identity parityをfixture化する。rawを保存し、単文解析が正しいという証拠だけで全文の誤POSを上書きしない。証拠不足はREVIEWを維持する。
3. 別run adapter作成時にcandidate schemaのID pattern更新を見落とした。複製元smoke schemaの `^K1-00[12]$` が残り、003〜050の48IDを拒否することを診断した。今回保存した001/002 journalはschema PASSだが、次の50本run前に50ID全域のpositive/negative contract testが必要。このrunのpinned schemaは書き換えない。

**C：analyzer境界とforward schemaの修正・対照tests・001〜002 smoke後、別の実績ゼロrunで連続試験をやり直す。** この停止runを成功に書き換えず、003以降や300本量産へ進まない。
