# Phase 3.9a 結果要約

**D / STRUCTURAL_FAIL。66/100 commit、K1-067で停止。068以降は生成していない。**

今回のauthor contract retry修正と少数known-gap promptは実装・回帰テストを通過した。停止原因はcontract typoではなく、予定新出 `졸리다` の登録adjectiveと単文Kiwi VVの不整合である。production中に解析器を変更せず、067の候補をcreditしなかった。

| 指標 | 結果 |
|---|---:|
| commit | 66/100 |
| formal attempts | 80（commitした66本は79、停止067は1） |
| formal first-pass | 55/66 = 83.33% |
| mean attempts/committed text | 1.197 |
| author_contract_retry_count | 0 |
| production contract failures recovered | 0（fixtureでの回復検証とは別） |
| contract max3 exhaustion | なし |
| 初回返却済みdraftのfinding | 28/67 = 41.79% |
| 初回返却済みdraftのapparent future finding | 3/67 = 4.48% |
| committed future / unresolved | 0 / 0 |
| committed hard errors / planned mismatch / final canonical mismatch | 0 / 0 / 0 |
| selected review / incidental | 153 / 559 credit |
| actual introduced Expansion | 131語 |
| effective distinct Expansion credits | 843（初出を含む、同一教材同一語は1） |
| capped exposure progress | 554/3000 |
| required_future_credit_rate | 2446 / 234 = 10.453、GREEN（soft） |
| outstanding / near deadline / expired debt | 65 / 13 / 14 windows |
| recovered expired / ever expired | 35 / 49 windows |
| saved known-gap events | 2（027: 지우다、061: スープの汁を表す국물不足を省略） |
| production wall | 15460.65秒 = 約4.295時間 |
| committed sec/text mean / median / p90 | 223.42 / 188.69 / 328.05 |
| committed sec/text min / max | 104.09 / 607.16 |
| 300本serial推定 | 未算出：100本未完走 |
| performance正式色判定 | INCOMPLETE：100本未完走 |

正式validatorのfuture flagは失敗066に1件あったが、元のsurfaceは予定新出 `목마르다` の活用であり、`목 + 마르다` への分割に起因する。これはreport-onlyの作者確認で、意図した語彙の真の未導入使用とは区別する。validatorの結果を成功へ書き換えず、短い自然文へrepair後PASSした。001の그것、042の봉지も含め、apparent finding率を真のfuture使用率と同一視しない。

## contract・品質・履歴

pre/post full suiteは各331 PASS、failures/errors/skips=0。schemaのkeyは旧正式実装から移行し、controller/author template/testsが同じJSON Schemaを読む。missing/misspelling/extra/type/許可値/parse errorをstate-safeに回復する。本文・訳・titleのdigestを保持、contract-only failureをformal attemptへ数えず、最大3回を別管理する。実本番でtypoが回復した実績はないため、テスト成功と本番実績を分ける。

K1-027の1文と訳に、作者のUnicode転送ミスによる文字化けがcommit後に見つかった。明確なlanguage/content quality問題1 incident、translation問題1 incidentとして記録する。同じincidentにより、紙の交換のreferent明示も欠けた。mechanical coverageではpunctuationとして扱われ、当該spanに語彙creditはない。凍結本文とledgerは上書きせず、人間spot reviewへ含める。機械hard PASSだけでfinal corpus品質PASSとは言わない。

known-gap 2件は保存済みの観察イベント数であり、内部下書き全体の完全なgap監査ではない。wind/messageの新negativeはauthor支援のみ。語彙800・文法32・初出・windows・sense registryは変更していない。過去Phase 3.9その他のfreeze成果物を今回の成功へ書き換えていない。

## scheduler・diversity・速度

025→050→停止066の必要平均は10.211→10.408→10.453と上昇。expired回収35 windowsは実績だが、残り100本試験は未完了で長期成立を承認できない。065〜066で回収した一方、未消化65 windowsは依然保持する。75/100 checkpointは到達していないので作成しない。

genreは18種類。fingerprintの低い類似度だけで意味的重複なしとは断定しない。ホテル準備・写真の共有・家族の食事・忘れ物等の再利用は、人間spot reviewでgoal/problem/resolutionの違いを確認する。review quotaのための副次事件を避け、vetoをdeadlineより優先した。

最大計時stageはscene_planning（6049.80秒）。scene planning＋author draft＋naturalness reviewは約75.0%のproduction wallを占める。ただしscene_planningはbegin→plan受理であり、sceneと最初の本文案を同じauthor応答で作成した時間も一部含む。author_draftはplan受理後の時間。両者を純粋な独立LLM latencyへ分解したbenchmarkではない。

preflight repairはwallの約7.77%、formal retry repairは約1.43%。contract retry overheadは0。pre-run engineering/setup（pre full suiteを含む）とpost regression/replay/reportingはproduction wall外。partialの平均は3.8 full50の136.95秒より遅いが、標本・負荷・計測待機が違うため正式な100本速度改善とは判定しない。

## 次に進めるか

**101〜300 continuationには進めない。** 次の修正候補は `졸리다` の登録POSとKiwi POSとの限定互換の一点。新しい一般semantic parserや全800語の語義監査へ広げない。変更は今回のrunへ適用せず、別開発版でpositive/negative・planned identity・failed-state isolationを確認してから、別zero-state enduranceを検討する。027のartifact修正も別版で扱う。

数値の詳細・freeze/integrity・ledger replay結果はvalidation JSON、韓国語本文＋日本語訳はhuman spot review、contractと停止の根拠はそれぞれ専用レポートに保存する。
