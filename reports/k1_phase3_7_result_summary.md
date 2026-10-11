# Phase 3.7 結果 — D / SENTENCE_LOCAL_STRUCTURAL_FAIL

001〜010の10本をcommitした後、011のdraft段階で停止した。050までは完走していない。011はpreflightのみで、formal candidate／初出／露出creditはない。012以降は生成していない。

## sentence-local方針の検証

各sentenceを独立解析し、canonical mapからpermission、N/U、coverageを計算する。paragraph／full rawは改変せず診断欄に保存する。広域不一致はreject／retry／STOPへ接続していない。titleは独立phrase、final reanalysisはcanonical結果を比較する。既存resolver、800語、32文法、schedule／windows、ID、自然さpromptは変更していない。

既存301件＋新規9件＝310件のfull regressionが、開始前・終了後ともPASSした。旧Phase 3.6 failed002、3.6b failed007、3.6c failed001は、report-only replayでいずれもmechanical PASSした。旧3.6cの2つの저について、sentenceはCore0002、paragraph/fullはExpansion0446という4viewの差をwarningに留められた。旧creditは新stateに混ぜていない。

## 停止原因と訂正

005の`집에서 가족하고 저녁을 먹을 거예요.`は自然な韓国語だが、frozen Core0074は「夕方・晩の時間義のみ。夕食義は未許可」である。author reviewでこれを見落とし、sentence-local identity gateも`evening`として誤PASSさせた。

この不適合はscope disagreementではなく、registered IDのmembership／POS確認だけでは許可senseを保証できないというfalse acceptanceである。production開始後にcode／configを修正せず、engine defectとしてSTOPした。005本文、元coverage、ledger、010 checkpointを上書きしていない。

005の1tokenを未許可senseとして除外した外部監査で、N=142、U=2、controlled=99.30%、previous=97.89%。hard条件に不適合となる。保存済みのmechanical hard errors=0を、語義まで適合した証明と扱ってはならない。010 checkpointは発見前のmechanical結果であり、この監査で適合承認を限定する。

停止後のreport-only対照例では、`아침을 먹어요.`と`저녁을 먹어요.`が期待REJECT／実際PASSとなった。一方、朝・夕方の時間用法、`점심을 먹어요.`、`밥을 먹을 거예요.`は期待どおりPASSした。この未カバー境界は310件PASSとは別に報告する。朝食義は011の未commit draftにもあったが、commit済み不適合件数には含めない。

修正候補は、snapshotへ既存gloss／notesの制限を明示し、まず時間義限定の아침／저녁＋食事目的語用法を狭い対照fixtureで防ぐこと。005の自然な代替は`집에서 가족하고 밥을 먹을 거예요.`。どちらも今回未適用で、DBの意味拡張・過去runの書換えは行っていない。

## Trial指標

| 指標 | 結果 |
|---|---|
| commit | 10/50、011でSTOP |
| formal attempts | 12、平均1.2/commit |
| 最初のformal candidateからcommit | 8/10＝80% |
| 最初のmechanical candidate PASS | 9/10＝90% |
| retry一次原因 | 003のsentence-local名詞／連体形境界1件、009の訪問先reference clarity1件 |
| formal future / unresolved（commit時の機械値） | 0 / 0 |
| 新出ID mismatch / final canonical mismatch | 0 / 0 |
| 後監査の未許可sense | 005の1token、coverage hard不適合1教材 |
| semantic grammar warnings | 141、hard gateへ戻していない |
| naturalness lint warnings | 6、文脈確認で適否を判断 |
| confirmed Korean自然さ崩壊 | 発見なし。ただし独立した人間レビューではない |
| confirmed lexical-policy defect | 1件。author reviewも見落とした |
| selected review / incidental | 22 / 2（保存済みledgerの値） |
| introduced Expansion | 20（保存済みledgerの値） |
| outstanding / expired debt | 2 / 0、数学的回収不能0 |
| exposure分布 | 0回480語、1回4語、2回9語、3回6語、4回1語 |
| genre | 9種。family2本、他8種は各1本 |
| 直近10本のmax fingerprint similarity | 0.167（粗いfingerprint指標であり意味類似の完全判定ではない） |
| 同型のconfirmed自然さ問題3本以上 | 発見なし |

「80%」はpreflight repair後の正式候補の初回commit率であり、生成直後draftの無修正PASS率ではない。初期preflightは11/11 draftで何らかのfindingを記録し、true future findingは23token／9draft（うちcommit対象10本では16token／8draft）だった。011分は未提出である。preflightとrepairはstateを変更せず、時間には含めた。

debtは最後のcommit010時点で엄마（期限013）と되다の第2window（期限025）。期限切れ・数学的回収不能はない。しかし50本の長期運用成立は未証明であり、005のfalse-PASS creditを含むledgerを適合済み継続stateとして流用しない。

## scope warningの測定上の限界

保存されたscope warningは390件（paragraph195／full195）、registered-ID mismatchは0、すべてPOS-onlyだった。停止後の整列監査で、390件すべてが、sentence側はlexical annotationのraw indicesだけを比較し、広域側は同じHangul spanに重なるEF／ETM等まで拾った比較方法のartifactと確認した。両側をlexical annotation indicesで揃えた実不一致は0件だった。

元diagnosticsとcodeは変更していない。390件を実際のPOS instability、韓国語の誤り、STOP理由として数えない。歴史的3.6cの저のregistered-ID差は別であり、同じsurfaceの広域誤解析をwarning化できた実例である。今後diagnostic集計のalignmentを揃える修正はreport-only候補とする。

## 速度とintegrity

Production wallは1314.59秒（約21分55秒）。commit済み10本のmean104.79、median95.19、p90 150.46、min70.89／max165.84秒。partial medianの参考評価はGREENだが、50本完走の性能判定ではない。最大時間stageはscene planning（588.51秒）。次の速度最適化対象はgenerator側である。

wallには未完了011のdraft／障害発見時間も含む。engineering、pre/post full tests、終了後のreplay／報告作業は除外した。011のauthor-stage時間には語義障害の診断も含むため、純粋なdraft latencyと同一視しない。50本未完走なので300本mean／median serial estimateは出さない。

停止時ledger hashは不変、epoch=10。failed003 candidateはcreditしていない。零stateからの10本replayは内部整合／再現性検査を通過したが、005の意味適合性を証明するものではない。旧成果物hash・production code/config/promptの変更は0件。committed本文の適合承認と、checksum／transactionの内部整合は分ける。

## 次の判断

**D / SENTENCE_LOCAL_STRUCTURAL_FAIL。** sentence-local authorityへの変更は過去scope blockerを吸収した。一方、未許可語義のfalse acceptanceを残したまま50本・300本へ進めない。語彙や文法の拡張ではなく、確認済みの時間／食事sense境界とauthorへの制限提示を狭く直し、別zero-state runで再試験することを提案する。今回の停止runを成功へ書き換えない。

Meaning-preserving report-only alternative: `저녁에 집에서 가족하고 밥을 먹을 거예요.` uses evening as time and ? as meal. It is not applied to the frozen committed text.
