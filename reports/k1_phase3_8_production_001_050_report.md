# K1 Phase 3.8 最終レポート

**判定 B / GENERATOR_TUNING。50/50完走、hard条件とstate integrityはPASS。**

初稿とformal candidateを区別する。formal first-passは72%だが、初稿49/50にはpreflight findingがあり、39/50でfuture findingが出た。機械ゲートを緩めず本文repairで吸収できた。300本へは進まず、generatorの許可リスト遵守と既知の不自然な代用を改善する。

| 指標 | 結果 |
|---|---|
| committed / attempts | 50/50 / 67 |
| first-pass / mean attempts | 72% / 1.34 |
| committed controlled / previous | 全100% / 全98%以上 |
| committed future / unresolved / planned mismatch / final canonical mismatch / integrity | 全0 |
| restricted rejects / checkpoint false accepts検出 | 0 / 0 |
| basic family counts | {'breakfast_meal': 6, 'morning_time': 14, 'dinner_meal': 6, 'evening_time': 10} |
| scope warnings | 4（paragraph 2 / full 2、coverage不変更） |
| semantic / naturalness warnings | 634 / 107 |
| confirmed language issues | formal修正2教材、preformal確認2教材、commit後report-only1教材（048） |
| translation repair | formal 1件。048の訳は原文通りで、訳だけ補正しない |
| selected / incidental / introduced | 108 / 211 / 99 |
| outstanding / expired / near-deadline debt | 69 / 23 / 27 window（word数とは異なる） |
| mathematically unrecoverable | 0（各語の残り教材数判定。共同scene容量の保証ではない） |
| production wall | 7281.93秒（2.02時間） |
| mean / median / p90 | 136.95 / 124.89 / 219.31秒 |
| min / max | 60.55 / 364.84秒 |
| 300本 serial mean / median | 11.41 / 10.41時間 |
| performance / 最大stage | GREEN / author_draft |

3.7の10本partial baseline（104.79/95.19/150.46秒）比: mean +30.7%、median +31.2%。50本と10本の部分runなので参考比較。時刻はlive authorの思考・ファイル受け渡し・操作時間を含む実測で、純粋なAPIモデルlatencyではない。setup 266.06秒、pre/post full tests・最終replay・レポートはproduction wall外。

## 語義ポリシーと限定範囲

basic_sense_families.jsonに人間承認済みの朝/朝食、夕方/夕食をoverlayとして保存。元DBのlemma/POS/sense/IDを保持し、旧meal除外notesのこの2件だけを明示的に上書きする。同一IDなのでnew lemmaや800予算を増やさない。

explicit_restricted_senses.jsonは既存notesに明示された18件のみ。各source file・notes・canonical tripleを照合する。狭い禁止contextに明確に該当すればcandidate hard reject、それ以外はNO_CLEAR_VIOLATIONであり完全WSDの証明ではない。全800語の意味棚卸しは実施しない。

本runの18語対象usage86件を再確認し、明示違反を検出しなかった。未導入のregistry語は使用していない。語義negative fixturesはcanonical IDに対する狭いcontextルールの対照試験であり、未知の全語義を解決した試験ではない。

## 語彙・retry

formal retry一次原因（複数errorを一次原因にまとめる）: {'future_expansion': 4, 'unresolved_context_ambiguity': 4, 'unknown_or_unresolved': 3, 'title_permission': 4}。機械reject15attempt、作者がmechanical PASS後にrepairした2attempt。元の機械error全件内訳はvalidation_result.jsonを参照。

formal body future findings4candidateのうち3件はCore 듣다/공책の誤解決を保守的にrejectしたもの。確認できる真のbody futureは043の이제 1candidate。title policyのfindingも別に保存する。preflight future finding89は初稿での検出件数で、全件を独立WSD goldとして真の混入と認定しない。commit済みfutureは0。

## review / debt

実distinct-text exposure合計 418 = introduction99 + selected108 + incidental211。6本以上達成は22語。分布: {'6': 7, '4': 16, '0': 401, '7': 6, '5': 8, '8': 2, '2': 15, '10': 2, '3': 13, '18': 2, '1': 25, '11': 1, '21': 1, '32': 1}。0回401語は主にまだ導入予定が先の語である。

6回を超えた重複を進捗からcapすると 330/3000 credits。残り2670 creditsを次の250教材で実現する必要がある（平均 10.68 distinct Expansion/text）。この50本だけで500語×6回の成立を認定しない。

69 outstanding windowsのうち23は期限を過ぎた未消化window。繰越は仕様上許可される。衣類・眼鏡等に未消化があるが、違和感のある挿入やsilent creditはしなかった。次の連続runではdebtに合う自然なscene候補を早めに出すgenerator支援が必要。

## 自然さ・translation・diversity

formal author repairは001の名前のreferent/訳の補完、012の病人と医師の指示混同。preformal確認例は039の自転車を閉める代用と店内で持参食を食べる場面、047の旅行かばんを作る代用。修正済み。これはlexical policyやsemantic grammar warningと別に扱う。

048の紙の本に책을 열어요が残った。これは펴다不足への不自然な代用の再発で、report-onlyの修正案は動作を省略して책을 읽어요とする。元commitは改変しない。입히다（011）・지우다（027）は行為を省略して解決。新語をDBへ追加していない。

genre distribution: {'family': 2, 'short_dialogue': 2, 'objects': 2, 'transport': 3, 'food': 4, 'weather': 3, 'school': 4, 'shopping': 6, 'simple_hobby': 2, 'simple_outing': 2, 'home': 3, 'work': 3, 'small_problem': 3, 'health': 1, 'travel': 3, 'friends': 5, 'outdoor': 1, 'daily_life': 1}。直近10本との最大fingerprint similarity 0.167。fingerprintの具体的な文字列比較は意味的な似た展開を過小検出し得る。学校/家庭/食事への偏りや終盤の会話型を人間spotで確認する。

N에게 웃어요 / habitual progressiveの機械recurrence検索: {}。検出0をあらゆる自然さ問題0の証明にしない。sentence preferred compliance 98.7%、hard max違反0。

## 検証とfreeze

full regression: pre 317 PASS、post 317 PASS（各1回）。ledger zero-state replay errors []。歴史成果物とproductionコードfreeze一致。過去本文・ledgerのcreditを流用していない。050を超える本文は生成していない。

historical 3.7/005、3.6/002、3.6b/007、3.6c/001はreport-onlyで全hard PASS。夕食はbasic family、scope-only identity差は診断扱い。真のfuture negative fixturesは引き続きreject。比較対象の元ファイルは変更していない。

## 次の判断

**B: GENERATOR_TUNING。** validatorを一般的なsemantic parserへ拡張せず、初稿の許可リスト遵守と既知bad-pattern（펴다不足時の省略を含む）を作者側で強化する。抜き取りレビューで品質を確認し、debtの繰越を次のrunでも測る。今回の完走を300本の自動生成許可とは扱わない。

詳細: k1_phase3_8_validation_result.json、k1_phase3_8_timing.json、k1_phase3_8_human_spot_review.md、k1_phase3_8_automated_run_metrics.md。
