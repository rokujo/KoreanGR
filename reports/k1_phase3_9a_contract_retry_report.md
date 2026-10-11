# Phase 3.9a author contract retry

## 採用した変更

`config/languages/ko/k1/author_selfcheck.schema.json` がkey・型・許可値の単一source of truth。既存Phase 3.9実装から6つの正式keyを移行し、今回の都合で新しいkey名を発明していない。controller・self-checkテンプレート生成・testsが同じschemaを読む。追加プロパティは禁止。6項目はbooleanかつtrue、notesのみ任意stringであり、独自enumは追加していない。

JSON parse error / required不足 / 誤綴り / extra key / wrong type / 不正な許可値はcontract journalと計時にだけ記録し、formal candidate submission・attemptにはしない。Korean/JA/titleをdigestで固定し、正式schemaでself-checkだけ再出力する。3回の失敗でAUTHOR_CONTRACT_STRUCTURAL_FAIL。formal max5とは別予算。

内容変更はcontract-only retryでは拒否する。contract受理後の通常prose repairは別工程。失敗中はledger byte hash・epoch・intro・review・debt・genre・sceneに変化がない。

## 回帰検証

既存323テストに8テストを追加。各テスト内で複数のnegativeを照合するため、fixture件数とtest method件数を混同しない。

- 既存正式key移行の一致。
- missing / misspelling / extra / wrong string型 / false許可値 / malformed JSON / object以外。
- 旧Phase 3.9 K1-013の誤key → 同じbodyで正しいschema → 継続。
- 3回失敗の上限とstate無変更。
- Korean/JA/titleを変えたcontract-only retryの拒否。
- controllerの1回目contract error → 2回目correct。formal attempts=0、ledger byte不変、run status不変。
- mechanical evaluate / atomic commitが旧3.9と同じ、planner health/proposalsは旧関数そのもの。
- 確認済みwind / message / paper-book gapのauthor warningと自然な省略例。

pre full suite=331 PASS（310.96秒）、post full suite=331 PASS（168.42秒）。毎候補full suiteは実行していない。履歴replayはreport-onlyで過去成果物を書き換えていない。

## 本番で確認できた範囲

正式runでは66本commit、67で別のPOS整合構造障害により停止。production author_contract_retry_count=0、recovered=0、contract exhaustion=false。したがって回復機構は実装・fixtureで検証済みだが、productionで実際のtypoを回収したという実績はない。試験のために故意のtypoをproductionへ混入していない。

## 変更範囲の限界

wind/messageの少数negative patternをauthor promptへ足した。新しいhard語義制限やsemantic parserは追加していない。validator・語彙800・文法32・schedule・review credit規則は維持した。production開始後にcode/config/promptを変更していない。
