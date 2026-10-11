# Phase 3.6a Production-lite benchmark

判定 **A: PRODUCTION_READY_FOR_50**。commit 10/10。K1-011以降は生成していません。

## Policy / engineering

語彙identity・初出・coverage・長さ・grammar32形式・明示的な未許可構文・title・最終再解析・atomic publishをhard検証します。Phase 3.5のsemantic registryは変更せず、PASS/REVIEW/heuristic FAILを診断に使用します。role分類だけでrejectせず、自然な基本用法は作者の文脈レビューで確認します。
既知の물을 받고 마셔요だけを、exact span、말/VX+시/EP+어요/EF、明示的な飲料目的語、받다の接続、登録drink義・正規活用を根拠に復元。rawは保存し、無条件aliasはありません。単文・引用・段落・全文と否定対照を回帰検証しました。
実際の作者はこのLLMであり、snapshot取得後に各本文を作成したローカルfile callbackです。外部モデルAPIの自動運転ベンチマークではありません。作者時間は思考・ファイル転送・ツール待ちを含む実elapsed wall timeで、保存済み本文の高速replayを生成速度として計測していません。
pre-run engineering/setup 640.9s。full pre-suite 286 tests / 126.8s。production開始後のcode/config差分: []。過去freeze差分: []。

## Generation / validation

committed hard errors 0、rejected attempts 8、unknown/unresolved 0、planned identity mismatch 0。1発PASS 3/10、平均attempt 1.9。future混入candidate 0/19、committed future 0。retry理由: {'unknown_or_unresolved': 10, 'unresolved_context_ambiguity': 4, 'coverage_or_token_policy': 24}。

| Text | attempt | 어절 | N / U | previous | semantic warnings | selected / incidental | seconds |
|---|---:|---:|---|---:|---:|---:|---:|
| K1-001 | 2 | 129 | 127 / 2 | 98.43% | 6 | 0 / 0 | 214.56 |
| K1-002 | 3 | 132 | 130 / 2 | 98.46% | 9 | 0 / 0 | 110.56 |
| K1-003 | 2 | 133 | 129 / 2 | 98.45% | 12 | 0 / 2 | 111.30 |
| K1-004 | 1 | 126 | 119 / 2 | 98.32% | 7 | 2 / 0 | 90.74 |
| K1-005 | 3 | 128 | 124 / 2 | 98.39% | 12 | 2 / 0 | 118.50 |
| K1-006 | 1 | 128 | 123 / 2 | 98.37% | 8 | 2 / 1 | 93.99 |
| K1-007 | 1 | 125 | 121 / 2 | 98.35% | 11 | 4 / 0 | 86.59 |
| K1-008 | 2 | 143 | 139 / 2 | 98.56% | 10 | 3 / 0 | 134.58 |
| K1-009 | 2 | 170 | 161 / 3 | 98.14% | 17 | 4 / 1 | 158.55 |
| K1-010 | 2 | 157 | 154 / 3 | 98.05% | 19 | 3 / 1 | 163.63 |

## Throughput

production wall 1294.93s。per text: {"n": 10, "min": 86.58579620000091, "max": 214.56055500000366, "mean": 128.30100954000082, "median": 114.90289805000066, "p90": 163.62730820000434}。性能目安 GREEN。
stage totals (s): {"scene_planning": 470.1223413000189, "author_draft": 408.5818893000178, "morphology_vocab_analysis": 21.41865870001493, "mechanical_validation": 3.726353999969433, "retry_repair": 171.6247485000058, "naturalness_review": 181.36642089999077, "final_reanalysis": 11.639623900002334, "commit": 7.461881399991398, "controller_overhead": 7.0681773999967845}。between-text/controller外のwall 11.92sもrun wallへ含めています。
300 serial estimate (hours): {"estimated_300_mean_hours": 10.691750795000068, "estimated_300_median_hours": 9.575241504166721}。mean/medianは各教材の実測totalを基準とします。全run overheadを含むwall/commitベース推定: 10.791092367500035h。
10本の初期E1・ローカル作者経路という小標本です。後期の語彙負荷、人間レビュー、将来のAPI呼び出し待ち、再修正・全300本の最終露出監査を含む納期保証ではありません。

## Quality / review operation

semantic warnings 111: {'REVIEW': 106, 'FAIL': 5}。これは曖昧分類を含み、語彙coverageとは独立です。naturalness warnings 4: {'nat_reference_clarity': 2, 'nat_restricted_sense': 2}。作者確認された問題 0、translation flags 0。
review selected actual credit 20、incidental actual credit 5、introduced 20。outstanding windows 2、near deadline 0、expired 0。creditは確認済み本文のdistinct textのみです。
debt詳細: [{"vocab_id": "ko_k1_0446", "window_index": 1, "window": {"from": 10, "to": 28}}, {"vocab_id": "ko_k1_0476", "window_index": 0, "window": {"from": 10, "to": 13}}]。5〜8 reviewはsoftで、初期候補不足の語数達成のために事件を追加しません。
genre: {'weather': 1, 'short_dialogue': 1, 'shopping': 1, 'transport': 1, 'food': 1, 'home': 1, 'school': 1, 'small_problem': 1, 'family': 1, 'simple_hobby': 1}。max scene fingerprint similarity 0.167。sentence lengths {4: 212, 1: 5, 3: 55, 5: 58, 2: 7, 6: 7, 7: 1}、preferred 3〜7比率 0.9652173913043478。

## Integrity / next step

zero-state raw replay errors: []。ledger epoch 10。failed candidatesはintroduction/exposure/debt/genre/sceneへcreditされていません。post suite: {'tests': 286, 'failures': 0, 'errors': 0, 'skipped': 0, 'seconds': 115.15888239999913, 'success': True}。
人間抜き取りレビューは別ファイルを使用してください。モデル自己評価とregexを独立した品質保証とは扱いません。
次の001〜050 production trialへ進める。今回の承認は10本のみであり、続きは生成しない。

## Identity parity / next optimization

Unresolved structural scope mismatches: 0; safely converged scope diagnostics: 2; body NE recoveries: 2. Explicit registry/syntax/probe evidence only; raw preserved.
Largest stage: scene_planning; optimization target: generator/author: scene planning, constrained draft and localized repair; validator is not the primary cost.

## 今回の限定修正と回帰根拠

今回変更したresolverはresponse useの네のみ。元文字列のexact `네`、同じ1文字spanに重なる連続raw `너/NP + 의/JKG`、発話冒頭、直後の応答句読点、所有対象となる直接後続名詞がないこと、登録0442/yes、独立short-scopeのraw ICとyes identityをすべて要求する。raw morphologyは保存し、別resolver layerだけで復元する。generated annotationは判定根拠にしていない。

単文・引用単文・段落・全文のfocused identity parityを、予定新出語とリスクsurfaceに追加した。復元前の登録identity差も記録するので、unknownではない誤identityを検出できる。安全に収束しなければ構造STOPとなる。一般alias、NP→IC変換、単文rawによる全文rawの上書きは行わない。

Phase 3.6 failed002の全文はfixtureとして旧annotationを使わず再解析し、`"네, 저녁에 만나요."`を0442へ復元できた。独立・引用の応答6対照、`네 책`・`네 가방`・`네 사람이 와요.`の非yes対照、아니요/한국어/우리、마셔요、걷다、grouping、future/retired/planned identity、atomic isolation、001〜050 forward schemaを含め、pre/postとも286 tests PASS。詳細は `k1_phase3_6a_ne_identity_audit.json`、`k1_phase3_6a_pre_regression.json`、`k1_phase3_6a_post_regression.json`。

production本文の004と009でも、全文rawの너＋의と単文ICの差を全条件の証拠付きで復元した。構造的に未解決のscope mismatchは0、復元成功は2件。009初稿の`"네, 사과도 넣어요."`はshort-scopeもICを支持せず、resolverが正しく拒否した。これはscope差ではなく局所的な証拠不足なので、独立した`"네."`と説明文へrepairし、新candidateの全文再解析を経てcommitした。failed candidateはcreditしなかった。

## Retry・品質の内訳

19 attemptsのうちhard rejectは8。一次原因で数えると語彙/POS/活用または局所形態境界7件、네 short-scope証拠不足1件。別途、mechanical PASS後に005の訳の`고기도`の焦点を「私にも肉」から「私に肉も」へ直した1件があり、追加attemptは合計9件。コード別のerror件数にはcoverageなどの派生エラーも含むため、38 diagnosticsを38回のretryとは数えない。future混入は全19 candidatesで0、1発commitは3/10（30%）、平均attemptは1.9、最大3で上限5以内。

003初稿の쓰다(use)はCore/write義の逸脱として作者が確認し、사용하다と簡単なタイトルへ直した。確認済みのdraft言語問題1件、訳の修正1件で、いずれもcommit前に解消。最終committed本文の確認済み言語問題0、訳の未解決flag0という集計とは分ける。詳細は `k1_phase3_6a_run_observations.json`。モデル確認を独立goldや人間承認と扱わず、10本の人間抜き取り用本文を別ファイルに保存した。

自然さlint4件は、002のここ（机上）2件と007の쓰다/write（紙へ名前を書く）2件。参照先・語義を作者レビューで確認した。semantic warnings111件（REVIEW106・heuristic FAIL5）は診断であり、hard errorやcoverage欠損ではない。선물로の通常用法も作者文脈レビューを経て許容した。369 REVIEWの解消や意味role hard gateへの逆戻りは行っていない。

## Timingの精度と速度改善対象

production wallは1294.93秒（約21分35秒）。mean128.30、median114.90、nearest-rank p90 163.63秒／本、範囲86.59〜214.56秒。中央値はGREEN。300本のserial外挿はmean10.69時間・median9.58時間だが、初期10本からの概算であり量産許可や納期保証ではない。

最大の計測phaseはscene_planning 470.12秒、author_draft408.58秒。planning＋draft＋repair合計1050.33秒に対し、形態/語彙解析21.42秒・mechanical validation3.73秒・final reanalysis11.64秒。次の速度改善対象はvalidatorでなくgenerator側のscene planning、制約を明示した初稿、局所repairである。

これらは実際のローカルLLM/file callbackのelapsed計測で、純粋なモデル推論時間を分離したAPI benchmarkではない。001のplanningにはcontext復帰とcontroller読取りの時間も含め、黙ってsetupへ除外していない。002は初期planとdraftを同時に書いたため、planning38.39秒に初期draft作成を含む。stage値は操作phaseの実測として保持し、正確なplanning/draft分離とは主張しない。per-text totalとwallには全工程を含む。実装・pre full suite・post full suite・ledger replayはproduction外に分離した。

## Review運用と次の試験

新規導入20語、selected review credit20語教材組、incidental credit5語教材組。reviewは0〜4語／本で、初期の自然な候補数に従いsoft5〜8を埋めるための別事件を追加していない。debtは저の第2window（010〜028）と권の第1window（010〜013）の2件。期限切れ0、回収不能0で、次のrunでは別zero-stateから同じ逐次計画を検証する。今回の010後に仮想creditを追加していない。

10 genreを各1本、fingerprint最大類似度0.167。簡単なfingerprint比較であり、完全な意味類似判定ではない。図書館・初授業・本の捜索で基本語が繰り返されても、目的と問題・解決は異なる。自然な短文12件（1〜2어절）も引き延ばさず、3〜7어절比率96.52%、hard max違反0。

判定はA **PRODUCTION_READY_FOR_50**。正常なcandidate修正を品質崩壊とはみなさず、最終hard PASS・状態整合・構造問題なしを根拠とする。一発率30%は改善余地として残り、次の50本trialでは制約付き初稿の精度とdebtを重点確認する。今回は001〜010で終了し、011以降と300本は生成していない。
