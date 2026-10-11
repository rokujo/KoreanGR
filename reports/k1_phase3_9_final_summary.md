# Phase 3.9 — 停止runの結果

**D / STRUCTURAL_FAIL（author callback入力契約違反による制御STOP）**。K1-001〜012の12本をcommitし、K1-013で停止した。100本endurance trialは未完了である。K1-014以降を生成しておらず、300本continuationへ進めない。

停止原因は、私が自己点検JSONの既定キーを誤って別名で記載したこと。解析器の誤解析、validatorの矛盾、schedulerの数学的不成立は確認されていない。controllerはcandidate提出前に停止し、K1-013へのcreditは0件だった。入力ミスと制御STOPを、Korean analyzer defectと混同しない。

## 実績

| 指標 | 結果 |
|---|---:|
| committed | 12 / 100 |
| 正式attempt総数 | 14 |
| 正式first-pass commit | 10 / 12 = 83.33% |
| mean attempts | 1.17 |
| 初回preflight findingあり | 6 / 12 = 50% |
| 初回preflight future findingあり | 0 / 12 = 0% |
| true formal future | 0 |
| committed future / unresolved / planned mismatch | 各0 |
| committed hard error / final canonical mismatch | 各0 |
| restricted-sense false acceptance | 機械再監査上0 |
| author naturalness repair | 1回（K1-008の借り物referent） |
| mechanical reject | 1回（K1-012のprevious coverage不足） |
| post-commit言語品質指摘 | 1件（K1-009、作者再読。独立goldではない） |
| post-commit追加レビュー候補 | 1件（K1-003の「종이에 말을 써요」） |
| 確認済みtranslation issue | 作者再読上0 |
| semantic grammar diagnostics | 142件。hard blockerにしていない |
| naturalness lint warnings | 9件（restricted_sense 6、reference_clarity 3） |

初回preflight率は、作者自己点検**後**に返されたdraftを測る。内部自己点検では未導入語などを修正しているため、rawの最初の文案にfutureがなかったとは主張しない。K1-013は自己点検契約が通らずpreflight未実施なので、分母から除外する。監査前collectorの13行分母値は別途保存する。

K1-012の初回正式candidateはN=146、U=3、previous=97.945%でrejectした。同じ通院・帰宅場面に沿う行動を加え、再candidateはN=151、U=3、previous=98.013%、157어절でPASSした。閾値を緩めず、失敗candidateへcreditしていない。

## Exposure / scheduler

| 指標 | 結果 |
|---|---:|
| 実際に導入済みExpansion | 24語 |
| selected review credits | 23 |
| incidental credits | 25 |
| current introduction credits | 24 |
| effective distinct Expansion credits | 72 |
| capped exposure progress | 72 / 3000 = 2.4% |
| remaining credits | 2928 |
| remaining texts to 300 | 288 |
| required_future_credit_rate | 10.1667 / text（soft GREEN） |
| outstanding windows | 5 |
| expired / recovered expired | 0 / 0 |
| near-deadline debt | 1 window（남편、期限015） |

同一本文内の複数tokenは1credit。effective creditには初出も含める。previous-only creditは48、effective平均は6/text。露出分布は0回476語、1回5語、2回5語、3回7語、4回1語、5回4語、6回2語。未導入476語の0回を欠落creditとして補完しない。

025 / 050 / 075 / 100には到達していないため、checkpoint trajectoryや100本時点のprojectionは未検証。12本時点のsoft GREENから長期scheduler成立を結論しない。

## Natural-expression gaps / diversity

生成中に記録したgapは2件：007の펴다、011の입히다。いずれもその動作を省略し、近い動詞へ無理に置換しなかった。commit後の009再読では、風を自然に描写する불다の不足を追加で記録した。`밖에는 비하고 바람이 있어요` のinventory風表現はreport-onlyで指摘し、次回は風の描写を省略する案を出す。既存本文や語彙DBは変更しない。

genreはfriends / short_dialogue / family / simple_outing / transport / food / school / objects / weather / work / home / healthが各1本。最大fingerprint similarityは0.0167。ただしlabel文字列の違いがスコアを小さくするため、これを意味的多様性の証明と扱わない。初期本文では本・家族・待機・着席会話の背景が複数回使われる。目的は変わるが、100本での展開反復は未検証。

平均140.08어절、範囲124〜179。sentence長分布は1어절8文、2어절1文、3어절31文、4어절242文、5어절110文、6어절10文。preferred 3〜7への適合は393/402=97.76%。自然な短い応答へ不要語を足していない。

## Timing

| 指標 | 秒 |
|---|---:|
| production wall（停止した013の作業も含む） | 3628.01（約1.01時間） |
| committed 12本 mean | 278.81 |
| median | 215.17 |
| p90（nearest-rank） | 487.30 |
| min / max | 110.63 / 688.96 |
| author_draft合計 | 1311.19 |
| scene_planning合計 | 932.34 |
| naturalness_review合計 | 664.98 |
| preflight repair合計 | 153.82（wallの4.24%） |
| formal retry repair合計 | 209.54（wallの5.78%） |

最大stageはauthor_draft。次の速度最適化対象はgenerator / author運用であり、validatorのhard条件を緩めることではない。Phase 3.8のmean136.95 / median124.89 / p90 219.31秒より、今回の部分実測は遅かった。自己点検後のfinding率が下がったことだけで速度改善を主張できない。

engineering/setupはproduction前の約533.76秒、pre full regressionを含む。post regression・ledger replay・report作成はproductionから除外した。時間はlive authorの推論・ツール往復・ファイル操作等を含む実測で、純粋な外部LLM API時間ではない。100本完走条件を満たさないため、300本mean/median estimateは**未算出**、正式performance判定もINCOMPLETEとする。

## Integrity / 判定

pre / post full regressionは各323件PASS。機械的hard・freeze・projection・zero-state ledger replayの確定結果は [validation result](k1_phase3_9_validation_result.json) を参照する。停止時のledger SHAはadministrative finalization前後一致。過去Phaseのfreeze成果物と今回のmechanical evaluate / atomic commitを変更していない。

今回のDはauthor callback契約作成ミスによる未完了runの判定であり、解析器研究やgrammar意味分類hard化を提案するものではない。次回は既定自己点検JSONテンプレートをそのまま使用し、同じproduction-lite pipelineで**新しいzero-state trial**を行うのが狭い修正となる。このrunを100本成功扱いにせず、final K1 corpus候補にも認定しない。

詳細：[停止監査](k1_phase3_9_stop_analysis.md)、[author契約事故](k1_phase3_9_author_contract_stop.json)、[review監査](k1_phase3_9_review_audit.json)、[本文spot review](k1_phase3_9_human_spot_review.md)。
