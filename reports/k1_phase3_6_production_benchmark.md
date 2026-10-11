# Phase 3.6 Production-lite benchmark

判定 **C: STRUCTURAL_FAIL**。commit 1/10。K1-011以降は生成していません。

K1-002 attempt 1で停止しました。K1-003〜010も未生成です。10本ベンチマークは成立していません。

## STOPの根拠

`"네, 저녁에 만나요."`は単文・引用単文では`네/IC → ko_k1_0442 / yes`ですが、今回の全文では`너/NP + 의/JKG`へ変化し、Core `ko_k1_0003 / you_informal`と所有助詞に誤解決されました。語彙identityが変化しているため、semantic roleのwarningとは別の構造障害です。作者の意図だけを根拠にyesへ上書きしていません。

予定新出ID照合は`ko_k1_0442`不足としてrejectし、002をcommitしませんでした。002で表示されたcontrolled 100% / previous 99.31%は誤identityに基づくcandidate診断値であり、成功したcoverageとして信用しません。002の新出`네 / 아니요`、同本文中のprevious `되다`、genre/scene、debt paymentにはcredit 0です。

自動gateが出したhard errorは`planned_new_not_present`です。続くfocused scope診断で、許可済みidentity同士の誤変換と分かり、オペレーターが同じcontrollerのstructural STOPを記録しました。現在の自動scope検出は全文unknownと単文PASSの差に重点があり、今回の「どちらも登録語だがidentityが違う」場合を単独で自動検出したとは主張しません。

診断は[保存済みraw・scope対照](k1_phase3_6_ne_identity_structural_diagnostic.json)を参照してください。次の修正はこの一点に限るべきです。exact応答位置の`네`に対し、句読点による所有修飾の不成立、重なる`너+의`span、登録yes、scope対照を確認する限定resolverが候補です。`네 책`や数詞用法へglobal aliasを適用してはいけません。また、両scopeで「許可語」と解決された場合も、identity差を検出するfocused parity checkを検討してください。今回はreport-onlyで、コード修正・再試験は行っていません。

001の`밥하고 고기가 있어요`は引用あり・なしの両方で同じcompound REVIEWでした。scope変化ではなく局所曖昧性として、同義内容の`밥이 있고 고기도 있어요`へrepairし、2attempt目がPASSしました。修正前candidate・診断・修正後candidateを別保存しています。これは新しいparser改造ではありません。

## Policy / engineering

語彙identity・初出・coverage・長さ・grammar32形式・明示的な未許可構文・title・最終再解析・atomic publishをhard検証します。Phase 3.5のsemantic registryは変更せず、PASS/REVIEW/heuristic FAILを診断に使用します。role分類だけでrejectせず、自然な基本用法は作者の文脈レビューで確認します。
既知の물을 받고 마셔요だけを、exact span、말/VX+시/EP+어요/EF、明示的な飲料目的語、받다の接続、登録drink義・正規活用を根拠に復元。rawは保存し、無条件aliasはありません。単文・引用・段落・全文と否定対照を回帰検証しました。
実際の作者はこのLLMであり、snapshot取得後に各本文を作成したローカルfile callbackです。外部モデルAPIの自動運転ベンチマークではありません。作者時間は思考・ファイル転送・ツール待ちを含む実elapsed wall timeで、保存済み本文の高速replayを生成速度として計測していません。
pre-run engineering/setup 818.8s。full pre-suite 274 tests / 148.4s。production開始後のcode/config差分: []。過去freeze差分: []。

## Generation / validation

committed hard errors 0、rejected attempts 2、unknown/unresolved 0、planned identity mismatch 0。1発PASS 0/1、平均attempt 2。future混入candidate 0/3、committed future 0。retry理由: {'unknown_or_unresolved': 1, 'unresolved_context_ambiguity': 1, 'coverage_or_token_policy': 3, 'planned_new_not_present': 1}。

| Text | attempt | 어절 | N / U | previous | semantic warnings | selected / incidental | seconds |
|---|---:|---:|---|---:|---:|---:|---:|
| K1-001 | 2 | 133 | 131 / 2 | 98.47% | 11 | 0 / 0 | 132.43 |

## Throughput

production wall 290.23s。per text: {"n": 1, "min": 132.43497869999555, "max": 132.43497869999555, "mean": 132.43497869999555, "median": 132.43497869999555, "p90": 132.43497869999555}。性能目安 INCOMPLETE。
stage totals (s): {"scene_planning": 35.04942049999954, "author_draft": 127.65834609999729, "morphology_vocab_analysis": 4.587038699988625, "mechanical_validation": 0.3796579000118072, "retry_repair": 46.36255450000317, "naturalness_review": 20.258823800002574, "final_reanalysis": 1.2678595000033965, "commit": 0.18497029999707593, "controller_overhead": 0.6986354999899049, "structural_diagnostics": 52.258329800002684}. between-text overhead 1.52s. Stopped text 002 is included separately in run wall.
300 serial estimate (hours): null。mean/medianは各教材の実測totalを基準とします。全run overheadを含むwall/commitベース推定: 完走前のため算定しないh。
完了本文は1本だけです。mean / median / p90はいずれも132.43sですが、n=1の参考値であり、10本のthroughputや300本の現実的な所要時間は推定できません。工程別最大はauthor draft 127.66sです。未commit 002の執筆・検証・構造診断もproduction wallに含めています。setup / pre-suite / post-stopレポート・replayは含めていません。

教材間overheadは1.52sです。残り157.79sを教材間待ちと解釈してはいけません。うち156.27sは未commit 002のactual totalです。正確なstage totalsと範囲はtiming JSONを参照してください。

## Quality / review operation

semantic warnings 11: {'REVIEW': 11}。これは曖昧分類を含み、語彙coverageとは独立です。naturalness warnings 0: {}。作者確認された問題 0、translation flags 0。
review selected actual credit 0、incidental actual credit 0、introduced 2。outstanding windows 0、near deadline 0、expired 0。creditは確認済み本文のdistinct textのみです。
debt詳細: []。5〜8 reviewはsoftで、初期候補不足の語数達成のために事件を追加しません。
genre: {'food': 1}。max scene fingerprint similarity 0.000。sentence lengths {4: 22, 5: 6, 1: 1, 3: 4, 2: 1}、preferred 3〜7比率 0.9411764705882353。

## Integrity / next step

zero-state raw replay errors: []。ledger epoch 1。failed candidatesはintroduction/exposure/debt/genre/sceneへcreditされていません。post suite: None。
人間抜き取りレビューは別ファイルを使用してください。モデル自己評価とregexを独立した品質保証とは扱いません。
50本へ進む前に、この判定で示した一点/作者promptを調整する。今回のrunを成功扱いへ書き換えない。

## 集計範囲・制約

- 試行教材2本、attemptsは001=2 / 002=1。平均は試行教材ベース1.5、完了教材ベース2.0です。1発PASSは試行教材0/2、完了教材0/1です。
- hard reject candidate 2件。committed hard error 0件。candidate内のエラーは同じ原因からのcoverage派生も含むため、6 error recordsを6つの独立失敗とは数えません。
- semantic warningsはcommitted本文11件、全3candidate合計30件。naturalness lintはcommitted本文0件。作者確認された言語問題0件は001の最終確認に限り、002は作者承認前に停止しました。
- future contamination 0/3candidate。resolverのcommit-blocking REVIEWは001初稿のcompound 1件です。未知語を許可扱いにする緩和は行っていません。
- review windowは003から開くため、debt 0 / expired 0 / selected review 0 / incidental credit 0。review運用・genre/scene連続多様性は今回のrunでは評価未了です。candidate 002のincidentalsをledgerへcreditしていません。
- pre-run full regression 274件PASS。010未到達のためafter-010 full suiteは実行していません。STOP後は001のzero-state raw replay・state整合・742 frozen files・benchmark engine/config hashを確認し、すべて差分0です。

**次の50本へは進めません。判定Cの対象は新たに見つかった`네`のscope依存誤解決だけです。semantic registryの369 REVIEWを解消する研究へ戻る必要はありません。**
