# K1 Phase 3.1 candidate gate検証

**A. Phase 3.1 PASS — 別runで001〜050の連続試験を最初から再実施可能。**

このrunでは001だけをcommitした。002以降は生成していない。Phase 3の失敗本文・checkpoint・report・run state・露出ledger・validator結果はSHA-256でfreezeし、成功へ書き換えていない。

## Phase 3 failureの独立原因

| 原因 | 対策 |
|---|---|
| 未導入들어오다、初出051が001へ混入 | allowed snapshotによるpermission check、future IDをinvalid_usage_idsへ分離、candidate reject |
| 걸어요の걷다/walkと걸다/hangの解析曖昧性 | 正規活用＋登録sense＋局所構文・場面証拠を要求する限定resolver |
| 119어절 | draft target130〜150。副詞ではなく同じsceneの必要な行動でcoherent expansion、120〜180hardは維持 |

## Candidate gate / retry

committed state→allowed snapshot→新出・scene・review候補→draft→sentence precheck→全文raw analysis→hard QA→naturalness lint/semantic second pass→repair/regenerate→最終再解析→atomic commit→次教材。

candidateはcandidates/、rejectはfailed_attempts/へ保存。candidate段階で実ledgerをbyte単位で変更しない。retry回数はcandidate journalから取得する。標準max3。3回不合格ならrun停止。snapshot不可能、初出矛盾、analyzerの構造障害、state corruption、数学的露出不可能等は構造的停止。不正なdraft JSONも局所candidate_format rejectとし、実績を変更しない。

generatorはsnapshotと直前diagnosticsを受け取るcallback。今回のsmokeは既存失敗を意図的に再生し、future修正→length修正の順に、実feedbackを条件として使う決定的なregression callback。任意のLLMが常に3回で正しく修正できると実証したものではない。

| attempt | 結果 | 어절 | 主な診断 | ledger変更 |
|---|---|---|---|---|
| 1 | REJECTED | 119 | coverage_or_token_policy, future_expansion, length | なし |
| 2 | REJECTED | 119 | length | なし |
| 3 | PASS_PENDING_COMMIT | 135 | hard errors 0 | なし |

attempt1では旧失敗を回帰再現し、futureをreject。attempt2では「友達も家で休みたい」へ行為を調整して、方向動詞のaliasを避けた。lengthだけが残る。attempt3では窓で天気を確認、実際に撮った写真を携帯で確認、写真に花も写っていることを確認する16어절を加え、135にした。filler副詞の追加はない。

## Allowed snapshot

001: roles={'core': 300, 'current_new_expansion': 2}。Core300＋当該新出2で語彙302。実導入済みExpansionは0。固有名詞1、固定exception5を別枠で列挙。

各エントリはvocab_id・lemma・pos・sense・tier・role・allowed_inflections・forms・morphology_hintsを持つ。input digestと実state checksumを添付し、stale候補をcommitしない。予定上の以前導入済みは許可しない。Core들어가다は許可するが、들어오다を類義語として許可するaliasは存在しない。괜찮아요はnew괜찮다の通常活用で、exceptionによる迂回にはしない。

## Limited resolver / raw analysis

공원까지 친구하고 걸어요. は、걷다/verb/walkの登録、正規活用걸어요、生成intent一致、locomotion、登録場所공원＋까지、人との同行친구하고、直接目的語なしをすべて確認して解決した。raw morphologyと元annotationは保存する。生成intentだけ・場所だけでは解決しない。がばんを壁へ掛けるCase Cは을目的語でveto。未解決ならcandidate reject。正しい歩行文でも保守的条件を満たさないものはREVIEWになり得る。resolverの条件を満たすためだけに同行者を作る運用は禁止する。

活用根拠: [国立国語院・걷다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=29667)。듣다は[韓国語基礎辞典](https://krdict.korean.go.kr/jpn/dicSearch/SearchView?ParaWordNo=74104)、돕다の活用は[同辞典](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=17203)で確認。Standalone돕다はactive K1ではないため追加しない。登録Core도와주다の厳密なraw prefix groupingだけを扱う。

## Irregular morphology監査

active800のstem候補inventoryは101件。ㄷ/ㅂstemは不規則と自動認定しない。닫다・받다・입다をregular対照とした。르と登録하다 compoundも列挙。selected valid-inflection probesは28件、未知化/target認識失敗0。これは全活用・全senseの網羅的保証ではない。

| lemma | class | 修正前unresolved | 修正後unresolved | target認識 |
|---|---|---|---|---|
| 걷다 | d_irregular | 1 | 0 | True |
| 걷다 | d_irregular_past | 1 | 0 | True |
| 듣다 | d_irregular | 0 | 0 | True |
| 듣다 | d_irregular_past | 0 | 0 | True |
| 도와주다 | b_irregular_compound | 0 | 0 | True |
| 도와주다 | b_irregular_compound_auxiliary | 3 | 0 | True |
| 덥다 | b_irregular | 0 | 0 | True |
| 춥다 | b_irregular | 0 | 0 | True |
| 쉽다 | b_irregular | 0 | 0 | True |
| 어렵다 | b_irregular | 0 | 0 | True |
| 가깝다 | b_irregular | 0 | 0 | True |
| 무겁다 | b_irregular | 0 | 0 | True |
| 가볍다 | b_irregular | 0 | 0 | True |
| 뜨겁다 | b_irregular | 0 | 0 | True |
| 차갑다 | b_irregular | 0 | 0 | True |
| 빠르다 | reu_irregular | 0 | 0 | True |
| 모르다 | reu_irregular | 0 | 0 | True |
| 다르다 | reu_irregular | 0 | 0 | True |
| 고르다 | reu_irregular | 0 | 0 | True |
| 부르다 | reu_irregular | 0 | 0 | True |
| 닫다 | d_regular_negative_control | 0 | 0 | True |
| 받다 | d_regular_negative_control | 0 | 0 | True |
| 입다 | b_regular_negative_control | 0 | 0 | True |
| 공부하다 | hada_compound | 0 | 0 | True |
| 운동하다 | hada_compound | 0 | 0 | True |
| 전화하다 | hada_compound | 0 | 0 | True |
| 준비하다 | hada_compound | 0 | 0 | True |
| 사용하다 | hada_compound | 0 | 0 | True |

語彙DBのformsは変更していない。別overlayのmorphology_hintsを使用。다른の連体形境界を保持し、도와주고 싶어요の複合lemmaと希望文法を分離して検証した。auditの全語許可fixtureは実introや露出ledgerへ混ぜない。

## Sentence precheckの判断

sentence単位でfuture・unknown・retired・不許可文法形態素を診断する。全文raw解析でも同じpermissionを検証する。現在のcallbackは全文candidateを返すためprecheckは全文commit前の診断。token streaming型generatorの実装はしていない。sentence単位にprevious98%や120어절下限を適用せず、全文で検証する。

## Transaction safety

authoritative stateはcommitted record、導入、露出、debt payment、genre/scene履歴を含む単一JSON。OS writer lock＋同volumeのfsync済み一時ファイル＋atomic replaceで一度に公開する。texts/は復元可能なprojection。commit_id一致の再実行では露出を増やさず、異なるcandidateの二重commitを拒否。publish前faultで実state不変、publish後faultでprojection回復・credit重複なしをテストした。ディスク故障や電源断まで保証したとは扱わない。

本smokeのepoch=1、実導入2語、entry-text pairs=2。2つのrejectは導入・露出・review count・debt payment・genre・sceneに一切反映しない。genre/scene各1件、debt0。500語中498語は0回、新出2語は各1回。

## Smoke hard result

| 指標 | 結果 |
|---|---|
| 어절 / 最大一文 | 135 / 6 |
| N / U | 131 / 2 |
| controlled coverage | 100.00% |
| previous coverage | 98.473282% |
| 新出 | 되다 / 괜찮다、各1token、予定ID一致 |
| unresolved / future / grammar violation | 0 / 0 / 0 |
| retired / invalid usage | 0 / 0 |
| final reanalysis | PASS |
| validator errors | 0 |
| naturalness lint / semantic flags | 0 / [] |

99% target missはhard98%を満たすため非blocker。Nは語彙意味単位token、Uは本教材の初出Expansion token。助詞・語尾・許可されたbound grammarはNから除外。全token controlledなのでprevious=(N−U)/N。語義・自然さ・日本語訳はモデル自己評価だけで最終承認しない。

## K1-001 committed本文

오늘 친구하고 공원에 가요. 저는 집에서 친구를 기다려요. 친구는 버스를 타고 와요. 친구가 오면 공원에 갈 거예요. 그런데 지금 비가 많이 와요. 저는 창문으로 밖을 봐요.

길에는 사람이 적어요. 저는 우산을 가방에 넣어요. 친구가 집 앞에 도착해요. 친구는 우산이 없어요. 저는 문을 열고 친구를 봐요. 친구도 집에서 쉬고 싶어요.

친구하고 집에 들어가서 앉아요. 저는 친구에게 따뜻한 물을 줘요. 친구는 물을 마시고 웃어요. 친구가 저에게 말해요. "괜찮아요." 우리는 집에서 음악을 들어요.

친구하고 공원 이야기를 해요. 공원에는 꽃하고 나무가 많아요. 저는 공원에서 사진을 찍고 싶어요. 친구도 꽃을 보고 싶어요. 친구는 창문 앞에 서서 밖을 봐요. 세 시가 되면 밖에 나가요.

지금은 비가 안 와요. 친구하고 집에서 나가요. 공원까지 친구하고 걸어요. 공원에서 예쁜 꽃을 봐요. 친구는 꽃 옆에 서요. 저는 친구 사진을 찍어요.

친구는 제 휴대폰으로 친구 사진을 봐요. 사진에 꽃도 많이 있어요. 친구하고 공원에서 걷고 이야기를 해요.

### 日本語訳

今日は友達と公園へ行きます。 私は家で友達を待ちます。 友達はバスに乗って来ます。 友達が来たら公園へ行く予定です。 ところが今は雨がたくさん降っています。 私は窓から外を見ます。

道には人が少ないです。 私は傘をかばんに入れます。 友達が家の前に着きます。 友達には傘がありません。 私はドアを開けて友達を見ます。 友達も家で休みたいです。

友達と家に入って座ります。 私は友達に温かい水を渡します。 友達は水を飲んで笑います。 友達が私に言います。 『大丈夫です。』 私たちは家で音楽を聴きます。

友達と公園の話をします。 公園には花と木がたくさんあります。 私は公園で写真を撮りたいです。 友達も花を見たいです。 友達は窓の前に立って外を見ます。 三時になったら外へ出ます。

今は雨が降っていません。 友達と家から出ます。 公園まで友達と歩きます。 公園で美しい花を見ます。 友達は花の横に立ちます。 私は友達の写真を撮ります。

友達は私の携帯で友達の写真を見ます。 写真には花もたくさん写っています。 友達と公園で歩いて話をします。

## Tests / freeze

full suite: {'command': 'python -B scripts/run_k1_phase3_1_tests.py', 'tests_run': 134, 'failures': 0, 'errors': 0, 'ok': True, 'seconds': 262.486, 'initial_candidate_tests': {'tests': 30, 'failures': 1, 'errors': 15, 'cause': 'Duplicate grammar_used output keyword and VV-I prefix handling bug in new code; fixed implementation, no rule relaxation.', 'corrected_before_smoke': {'tests': 30, 'failures': 0, 'errors': 0, 'seconds': 44.199}}, 'log': 'reports/k1_phase3_1_test_log.txt'}

最終focused suite: {'command': 'python -B -m unittest discover -s tests -p test_k1_candidate_gate.py -v', 'tests_run': 34, 'failures': 0, 'errors': 0, 'seconds': 26.658, 'ok': True, 'scope': 'Final resolver conservative REVIEW gate and candidate/state transaction implementation'}

初回新規testsで検出した二重keywordとVV-Iタグ対応は実装修正。hard条件の緩和や期待値だけの変更ではない。元Phase3のfailed001、checkpoint001、report、run state、ledger、validationは入力freezeに含め、全hash一致。

## 次の判断

**A. Phase 3.1 PASS。別runで001〜050の逐次再試験へ進める。** 今回の証拠は001のcandidate gate・局所retry・限定resolver・transactionの成立まで。連続review window、review debt、incidental露出、scene/genre分布は50本再試験で検証する。このrunで002へ続行せず、300本量産も行わない。

## 成果物

- scripts/k1_candidate_gate.py / k1_phase3_1_resolver.py / k1_phase3_1.py / validate_k1_phase3_1.py
- tests/test_k1_candidate_gate.py / tests/fixtures/k1_phase3_1_regression_cases.json
- config/languages/ko/k1/phase3_1/morphology_hints.json / allowed_snapshot.schema.json
- docs/ko_k1_candidate_gate.md
- pilot/ko/k1/phase3_1/allowed_vocab_snapshots/ / candidates/ / failed_attempts/ / texts/K1-001.json
- state/phase3_1_smoke_exposure_ledger.json
- reports/k1_phase3_1_validation_result.json / k1_phase3_1_morphology_audit.json / k1_phase3_1_input_freeze.json
