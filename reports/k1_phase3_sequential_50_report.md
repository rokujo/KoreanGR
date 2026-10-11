# K1 Phase 3 連続運用検証：001で停止

**C. FAIL — 生成前の語彙確認と解析境界の対策が必要。**

K1-001を新規生成・検証した時点でImmediate stopが発動した。生成試行1本、確定本文0本。002〜050は生成していない。失敗本文を修正して続行することも行っていない。これは今回の停止規則を適用した結果であり、review window方式の不成立を示す結果ではない。

## Generation result

| 指標 | 結果 |
|---|---|
| 本文生成試行 | K1-001、1本 |
| hard PASS・ledger反映 | 0本 |
| 停止位置 | K1-001、hard検証直後 |
| 停止理由 | 未導入語、未解決内容語、本文119어절 |
| 010/020/030/040/050 checkpoint | 未到達のため未作成 |
| 停止時checkpoint | reports/phase3_checkpoint_001.md |

## Hard validation

| 指標 | 001の失敗試行 |
|---|---|
| 어절数 | 119（120〜180外） |
| 文数 / 一文最大 | 30 / 5（hard上限内） |
| N / U | 115 / 2 |
| controlled coverage | 98.260870%（100%違反） |
| previous coverage | 96.521739%（98%違反） |
| 新出lemma | 되다 / 괜찮다、2lemma・各1token |
| 未導入Expansion | 들어오다 / come_in / ko_k1_0386、1token、正式初出051 |
| 未解決内容語 | 걸어요、意図は걷다、解析候補걸다 |
| 認識された文法32外 | 0 |
| 未解決文法形態素 | 0 |
| retired ID/sense | 0 |
| validatorエラーメッセージ | 8件（原因を重複検出したものを含む） |

独立原因は3つ。未導入語1token、未解決token1個、本文長不足。新出U=2自体はfloor(115×.02)=2というhard上限内であり、99% missだけなら停止しない。今回のprevious低下は未知・未許可tokenによる。全tokenがcontrolledの場合に限りprevious=(N−U)/Nが成立する。今回の実計算はcontrolled=113/115、previous=111/115。

失敗JSONのgrammar_pass=falseは未解決token全体を保守的に扱った初回pipelineのflag。再解析では未解決の걸はVV内容語であり、grammar32外の実違反とは区別する。自然な「歩く」の語義を別義「掛ける」で許可したことにはせず、未解決として停止した。

## Vocabulary introductions / actual state

予定001は되다・괜찮다。失敗本文内には各1tokenあるが、本文全体がhard FAILなので導入済みにしない。実導入0、500語のactual_first_textはすべてnull、actual_textsはすべて空。Core300 / Expansion500 / Total800、E1/E2/E3=200/200/100、grammar32は保持した。

## Exposure / debt

| 指標 | 実績 |
|---|---|
| selected review exposure | 0 |
| incidental exposure | 0 |
| exposure分布 | 500語すべて0回（未開始） |
| review debt / near-deadline / expired | 0 / 0 / 0 |
| active review windows | 0（実導入なし） |
| defer | 0 |

001に既知Expansionはない。失敗JSONのincidental_previous_vocab_idsにあるko_k1_0386は、初回annotation候補の分類であって実incidental実績ではない。validatorはfutureとして検出し、実ledgerに一切反映していない。以後のrunではunintroduced IDsをこの候補欄からも除外し、invalid_usage_idsに分離する修正案があるが、本runの失敗履歴は保持する。逐次review運用・deadline収容力・500語×6回への進捗は今回まだ実証できていない。

## Naturalness

失敗試行のregex warningは0。モデルの8項目second passはYESだったが、hard QAに失敗している。人間承認でも自然さの保証でもない。confirmed naturalness issueの再発を観測する連続実績はない。今回の3停止原因をregex warningやsemantic pattern stopへ混同しない。

natural_expression_gapの本run実イベントは0。펴다はPhase 2.3の候補履歴として継続監視、実再発0、語彙追加なし。열다をすべて不自然とみなす包括禁止も加えていない。

## Diversity / readability

失敗試行はsimple outing 1本、雨待ち→公園。確定genre実績0本。直近10本比較の過去本文がないため、scene similarity・重複率はN/A。1本でgenreの幅やscene反復の少なさを評価しない。

失敗試行の文長分布: {1: 1, 3: 5, 4: 17, 5: 7}。平均本文長は119어절（試行1本のみ）。3〜7어절の文は29/30。1어절の「괜찮아요.」は自然な応答でありhard minimumはない。副詞で延長しない。

## Phase 2.3との比較

001のみ比較可能。020/033/040は今回未生成。Phase 2.3の学校場面をコピーせず、家で雨を待って友達と公園へ行く新規場面にした。明示的な의、filler副詞の過密、借りる意味の물어보다等は失敗試行にない。ただし既知語制御を維持できず、自然さguidelineだけでは語彙hard ruleの代替にならない。

Phase 2.3 previous=98.400000%、本試行=96.521739%。reviewはいずれも0。本文一致なし。差分JSON: pilot/ko/k1/phase3/phase2_3_comparison.json。

## 問題 → 原因 → report-only修正候補

| 問題 | 原因 | 修正候補 |
|---|---|---|
| 들어오다混入 | Coreの들어가다から自然な方向動詞へ生成側が置換してしまった。初出051の確認不足 | 生成前に実導入済みID集合と許可surface/活用候補を提示し、方向動詞をlemma別に照合。001なら場面を家に入る側の視点で設計する。語彙DBを拡張しない |
| 걸어요未解決 | 걷다の不規則活用と걸다の同形surface。raw解析のsense解決限界 | 「目的地まで／人と 걸어요」等の明示的文脈で限定したsense resolver候補を別テストする。汎用aliasや自動걷다許可にしない。歩行場面の人間確認を残す |
| 119어절 | 手動draftの長さ見積りが不足 | draft作成前にscene内の出来事・短い会話の情報量を計画し、目安130〜150程度の余白を確保。文数合わせの副詞は追加しない |
| 失敗候補欄にfutureをincidentalとして表示 | annotationのprevious roleが予定番号を前提とする部分が残る | actual permission確認後だけincidental欄へ格納し、invalid_usage_idsを別欄へ出す。既存失敗記録は変更しない |

上記は生成制御・解析・表示の修正候補。introduction scheduleの不整合や800語不足が証明された結果ではない。本文を自然にするための語彙追加・schedule変更は行っていない。

## Validator / tests / freeze

データ・run整合validator: errors 0。これは失敗検出と停止・credit抑止の整合性PASSであり、本文実験PASSではない。experiment_pass=false。

既存を含むfull suite: 95 tests、failures 0、errors 0。最終のPhase 3 helper/stop guard変更後のfocused suite: 16 tests、failures 0、errors 0。full suiteは追加5テストの作成前にdiscoveryしていたため95件、最終focusedは16件。

元config・旧本文・旧reports・旧validator/testsはSHA-256 freezeで検査。Phase 3専用profile/schemaでpreferred_minを3にした。旧profileは4のまま保存。その他のcoverage・新出上限・grammar・ID・windowsを変更していない。

## Recommendation

**C. FAIL。生成前の語彙照合、歩行活用の限定sense解決、draft長さの見積りを改善して、別runとして001から再試験する必要がある。** 本runは停止状態のまま保存する。50〜100本への拡大や300本量産へ進める証拠は得られていない。停止条件を外して002以降を生成することはしない。

## 主な成果物

- config/languages/ko/k1/phase3/profile.json / profile.schema.json
- pilot/ko/k1/phase3/sources/K1-001.json / failed_attempts/K1-001.json
- state/phase3_run.json / phase3_k1_001_050_exposure_ledger.json / phase3_naturalness_issue_ledger.json
- scripts/k1_phase3.py / validate_k1_phase3.py / run_k1_phase3_tests.py / report_k1_phase3_stop.py
- tests/test_k1_phase3.py / docs/ko_k1_phase3_operation.md
- reports/k1_phase3_001_050_review.md / phase3_checkpoint_001.md
- reports/k1_phase3_run_integrity_validation.json / k1_phase3_sequential_50_validation_result.json
- reports/k1_phase3_test_result.json / k1_phase3_test_log.txt / k1_phase3_input_freeze.json
