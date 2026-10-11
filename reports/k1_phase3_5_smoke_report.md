# Phase 3.5 zero-state smoke

**C / FAIL。001〜003をcommit、004でSTOP、005未生成。006以降・50本・300本は生成していません。**

新runはepoch0・実績ゼロから開始。過去ledgerやcreditは流用していません。候補→hard/semantic gate→最終再解析→atomic commitの順です。1教材max5attemptですが、semantic FAIL/REVIEWはPhase 3.5規定で即STOPです。

| text | attempt | 状態 | 어절 | N | U | controlled | previous | semantic FAIL/REVIEW |
|---|---:|---|---:|---:|---:|---:|---:|---|
| K1-001 | 1 | COMMITTED | 134 | 133 | 2 | 100% | 98.4962% | 0 / 0 |
| K1-002 | 1 | COMMITTED | 139 | 132 | 2 | 100% | 98.4848% | 0 / 0 |
| K1-003 | 1 | COMMITTED | 138 | 131 | 2 | 100% | 98.4733% | 0 / 0 |
| K1-004 | 1 | REJECTED / STOP | 137 | 133 | 2 | 97.7444% | 96.2406% | 0 / 1 |

001〜003はfuture/invalid/unresolved/grammar違反0、planned new == actual new、120〜180어절。final reanalysisで意味diagnosticsも一致しています。new token各2でN<200のため99% target未達は予想範囲でありblockerではありません。

## STOP原因を分離

- `물어보다 / ko_k1_0378` は004では未導入。作者draftミスであり、語彙DBや初出予定を変更しません。
- `저는 물을 받고 마셔요.` の全文rawで마셔요が말/VX + 시/EPへ崩れ、Core 마시다 identityを失いました。新構造analyzer問題です。
- g09は接続先の登録述語が存在しないためREVIEW。未知語を想像で補って並列/順序PASSにしません。semantic gateがこの取り逃しを安全側で拒否しました。

004のcoverage不達もhard rejectです。単発draftミスならretry可能ですが、今回はsemantic REVIEW／構造問題STOPが優先されます。retryで隠さず残りを生成していません。run_controlのsemantic_grammar_stopを保存し、追加診断を別audit JSONへ記録しました。

ローカルsmokeの本文作者は手動sourceで、量産generatorの完成を主張しません。allowed snapshotとsentence precheckはgate側で実行していますが、作者側の事前制約適用が不十分で未導入語を混入しました。次はsnapshotを作者callbackへ先に渡すrun_one経路を使って、この差を解消する必要があります。未提出の準備草稿はcandidate／実績とは別扱いです。

## 実review/debt

003の괜찮다は作者review候補には含めましたがschedulerのselected集合には入りませんでした。実出現をincidentalとしてcreditし、開いていたwindow0へ支払いました。selected review credit=0、incidental=1、導入済みExpansion=6。debtは되다（window003〜006）1件、expired=0。004の되다/네/아니요は一切creditしていません。004で開く予定のwindowも、未commitの時計を進めて払済みにしません。

実ledger epoch3と003までの履歴をTEMPのゼロstateで再現し、ledger全体一致を確認しました。004前後のauthoritative SHAも一致。新engineでatomic before/after publish crash、idempotent commit、最終meaning check差分拒否をテストしました。

## gateの実証範囲

32 grammarの意味registry、70 fixture、bad003全文回帰は成立。過去28本文は6 FAIL候補・369 REVIEWで、任意の自然な用例への対応はまだ十分ではありません。REVIEWを全て人間承認へ回すのではなく、同型をまとめてpolicyとparser能力を改善する必要があります。

全259テスト／focused 19テストPASS、凍結687ファイル変更0。テストPASSはsmoke完了PASSを意味しません。

## 次へ進む条件

まず고直後の마셔요の補助用言誤分割とg14 EF境界を解析器で監査し、許可snapshotからfuture混入を防ぐ作者側precheckを実行前に適用します。次に8件の意味policy疑問と頻出REVIEW型の係り先・省略主体を確認し、別の実績ゼロrunで001〜005を再試験してください。現時点で001〜050の連続試験は再開しません。
