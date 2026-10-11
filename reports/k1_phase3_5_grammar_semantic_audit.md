# Phase 3.5 grammar32意味監査

語彙800・文法32・ID・予定表・window・過去runは不変です。意味範囲のauthorityはgrammar.jsonと凍結K1文書のみです。新registryは別overlayであり、一般韓国語知識による許可意味の追加ではありません。

32項目を監査。狭いauto PASS経路を持つ項目は32、構造中心は11、文脈heuristicは21です。全32項目にREVIEW経路があります。registryで明示した意味policy疑問は8項目です。自動PASS可能数は、あらゆる用例を自動判定できる数ではありません。

## 32項目の監査表

| grammar ID | surface | frozen meaning / notes | allowed functions | 別意味・未許可候補 | auto PASS | REVIEW | fixture数 |
|---|---|---|---|---|---|---|---|
| ko_k1_g01 | 이다: 이에요/예요 | 〜です / 名詞述語。받침あり이에요、なし예요。過去였어요/이었어요はg03と組み合わせる。否定はCore 아니다でN이/가 아니에요。 | identity | change, existential | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g02 | -아요/어요 | 〜ます・〜です（現在） / 動詞・形容詞の해요체。하다→해요等の縮約・不規則活用を認める。独立した新文法を追加しない。 | polite_present | unapproved_speech_level | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g03 | -았/었어요 | 〜ました・〜でした / 했어요等の縮約を認める。経験・過去連体形や大過去-았었-は未許可。 | simple_past | double_past, independent_experience | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g04 | -(으)ㄹ 거예요 | 〜する予定です / 予定中心。推量の多用は避ける。거/것のこの構文内用法だけ許可。自由な名詞化は不可。 | future_plan | epistemic_conjecture | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 2 |
| ko_k1_g05 | -고 있다 | 〜しています / 進行のみ。着用・結果状態や-아/어 있다は未許可。있다は補助用言として文法内で認可。 | ongoing_action | result_state, habitual_only | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 4 |
| ko_k1_g06 | -고 싶다 | 〜したいです / 動詞に接続。本人の希望・相手への質問を中心にする。第三者の-고 싶어하다は未許可。 | own_wish, question_to_addressee | third_person_desiderative_derivation | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 2 |
| ko_k1_g07 | 안 | 〜しません・〜くありません / 短形否定。名詞+하다語では공부 안 해요等を認めるが、否定できない語に機械的に付けない。-지 않다は未許可。 | short_negation | long_negation | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g08 | 못 | 〜できません / 動詞の不可能のみ。能力・状況による不可能。形容詞への一律付加は禁止。 | capacity_or_circumstance_inability | adjective_inability | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g09 | -고 | 〜して・〜で（並列・順序） / 2事態までを優先。長い列挙は避ける。 | parallel, sequence | resultative_state | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 1 |
| ko_k1_g10 | -지만 | 〜ですが / 対比・逆接。1文の接続節は通常1つ。 | contrast | mere_sequence | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 1 |
| ko_k1_g11 | -아/어서 | 〜なので・〜して（順序） / 理由と密接な順序。理由用法の後ろの命令・勧誘、接続直前の過去-았/었-は避ける。 | reason, related_sequence | unrelated_sequence, reason_followed_by_instruction | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 3 |
| ko_k1_g12 | -(으)니까 | 〜なので / 理由。命令・勧誘への接続も許可。発見用法は未許可。 | reason | discovery | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 1 |
| ko_k1_g13 | -(으)면 | 〜なら・〜したら / 具体的な条件のみ。反実仮想・複雑な仮定は避ける。 | concrete_condition | counterfactual, complex_hypothetical | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 2 |
| ko_k1_g14 | -(으)세요 | 〜してください / 依頼・指示のみ。一般的な尊敬-(으)시-や드리다の派生を許可しない。命令対象は動作動詞を中心にする。 | request, instruction | generic_honorific_statement | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 1 |
| ko_k1_g15 | -(으)ㄹ까요 | 〜しましょうか・〜でしょうか / 勧誘・意向確認を中心にする。複雑な推量質問は避ける。 | invitation, intention_check | complex_conjecture | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 1 |
| ko_k1_g16 | -(으)ㄹ 수 있다/없다 | 〜できます・できません / 수はこの構文専用の依存名詞。있다/없다の補助用法のみ許可。自由な수の語義は不可。 | ability | epistemic_possibility | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 2 |
| ko_k1_g17 | -아/어야 하다 | 〜しなければなりません / 義務の基本形。-아/어야 되다や-아/어야等の別構文は未許可。 | obligation | necessary_condition_inference | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g18 | -아/어 보다 | 試しに〜してみます / 試行のみ。보다は補助用法を文法内で許可。経験-아/어 봤다はg03と組み合わせ可。一般的な補助動詞構文への拡張は不可。 | trial | visual_perception, generic_auxiliary | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g19 | 은/는 | 主題・対比 / 話題を示す。隠れた対比の説明負荷は避ける。 | topic, contrast_topic | adnominal_ending | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g20 | 이/가 | 主語 / 아니다の補語にも使用。누구+가→누가、나+가→내가、저+가→제가、너+가→네가を同一語に正規化。 | subject, negative_copula_complement | unapproved_complement | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 2 |
| ko_k1_g21 | 을/를 | 目的語 / 目的語の基本用法のみ。数え方では助詞を語彙に含めない。 | direct_object | path_extent, time_extent | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 2 |
| ko_k1_g22 | 에 | 場所・行先・時点 / 存在の場所、移動の行先、時点。数量당等の拡張は未許可。 | existence_location, destination, point_time | quantity_per_unit, cause, recipient | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 4 |
| ko_k1_g23 | 에서 | 動作の場所 / 動作の場所のみ。起点は追加候補として保留。 | action_location | source, agent | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 3 |
| ko_k1_g24 | 도 | 〜も / 単純な追加。疑問語+도等は아무 N도の許可範囲以外へ拡張しない。 | simple_addition | scalar_even, unapproved_indefinite_negation | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 3 |
| ko_k1_g25 | 하고 | 〜と（名詞並列・共同） / 接続・共同格。用言하다+고と区別する。와/과・(이)랑は未許可。 | nominal_coordination, companionship | quotative, verbal_hada_group | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 3 |
| ko_k1_g26 | -(으)ㄴ | 〜い・〜な（形容詞連体） / 形容詞のみ。있다/없다の있는/없는は個別異形。動詞過去連体形は未許可。連体節の深い埋め込みは避ける。 | adjective_attributive, existential_attributive | verb_past_attributive | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g27 | -는 | 〜する（動詞現在連体） / 現在連体形のみ。動詞の-(으)ㄴ/-(으)ㄹはこの項目では未許可。 | verb_present_attributive | verb_past_attributive, verb_future_attributive | 狭いframeのみ（hard） | 根拠不足時に必須 | 1 |
| ko_k1_g28 | 에게/한테 | 人に（受け手・相手） / 해요체では한테優先。에게서/한테서は未許可。 | recipient, counterparty | source, nonhuman_destination | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 4 |
| ko_k1_g29 | 의 | 〜の（所有） / 所有・所属のみ。나의→내、저의→제を同一語に正規化。이/그/저の指示連体詞と混同しない。 | ownership, belonging | subjective_genitive, material, generic_relation | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 3 |
| ko_k1_g30 | -(으)로 | 〜で（手段）・〜へ（方向） / 名詞に接続。母音・ㄹ받침の後は로、それ以外の받침は으로。交通手段・道具・移動方向に限定。資格・材料・原因・結果義、(으)로써/로서は未許可。 | transport, instrument, direction | role, material, cause, change_result | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 9 |
| ko_k1_g31 | 부터 / 까지 | 〜から・〜まで（起点・終点） / 時間・場所の区間の開始と終わりに限定。この一対を1文法項目と数える。場所起点は집에서부터等の에서との組合せを優先。強調の「〜さえ」までへ拡張しない。 | temporal_start_end, spatial_start_end | scalar_even | 狭いframeのみ（heuristic） | 根拠不足時に必須 | 3 |
| ko_k1_g32 | 만 | 〜だけ（限定） / 名詞等の単純な限定のみ。숫자 만「万」と区別。-기만、만에、-(으)ㄹ 만하다等の別構文は未許可。 | simple_nominal_limit | ten_thousand, nominalization_only, elapsed_time, worth_doing | 狭いframeのみ（hard） | 根拠不足時に必須 | 4 |

接続詞は原因・密接な順序・具体的条件等、各frozen noteにある関係のみ認可します。理由・発見、条件・反実仮想、能力・推量、進行・結果状態を同一surfaceという理由で統合しません。

## 機械検証と限界

全32正例＋37意味対照＋1前段境界、70 fixtureの期待結果はすべて一致しました。短文だけでなく、最初の誤PASS003の全文でもg30 roleをFAILにしました。修正文 `저는 어머니에게 사진을 주고 싶어요.` は全意味check PASS、g30なしです。

作者のfunction申告は分類の入力にしません。raw span、登録lemma/POS/sense、dependent名詞、述語frame、局所文脈を保存します。rawは変更しません。PASSと同じsurfaceでも、lexical frameを替えたnegativeを検証しました。

g14の凍結正例はraw EF/세요になり、旧形態gateにunresolvedが残る場合があります。semantic overlayは依頼候補を検出しますが、形態gateを通ったことにはしません。70 fixtureの成功は対象意味checkまたは前段rejectの期待結果であり、全文語彙・形態PASSではありません。

만에のnegativeはraw NNB/만として返り、g32へ対応せず前段unresolvedでrejectされます。初期fixtureが要求していた「g32 REVIEW」を、raw根拠に合う「前段reject」へ修正しました。hard ruleや意味範囲は緩めていません。初期の失敗テスト結果・logも別ファイルに保存しました。

있는/없는はg26の明示異形として対応づけ、元g27候補を診断に保存します。g04の内部copula、g31明示形에서부터は親構文への限定委譲です。単独에서の起点を認可していません。

## 過去28本文のreport-only監査

Phase 2.3 25本＋Phase 3.4 clean 3本。{'PASS': 2759, 'REVIEW': 369, 'FAIL': 6}。28/28にREVIEW候補があります。REVIEWは誤用確定ではなく、局所frameの不足・係り先・省略主語・広い所属関係などのfalse negativeも含みます。大量正常用例を自動承認できたとは結論しません。現gateの保守性を可視化した結果です。

| source | id | PASS | REVIEW | FAIL候補 |
|---|---|---:|---:|---:|
| pilot/ko/k1/phase2_3/texts/K1-001.json | K1-001 | 99 | 8 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-020.json | K1-020 | 95 | 17 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-033.json | K1-033 | 107 | 11 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-040.json | K1-040 | 92 | 15 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-085.json | K1-085 | 99 | 13 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-103.json | K1-103 | 104 | 11 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-110.json | K1-110 | 97 | 9 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-111.json | K1-111 | 98 | 13 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-127.json | K1-127 | 105 | 11 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-150.json | K1-150 | 93 | 9 | 1 |
| pilot/ko/k1/phase2_3/texts/K1-170.json | K1-170 | 98 | 18 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-180.json | K1-180 | 106 | 13 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-184.json | K1-184 | 93 | 12 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-189.json | K1-189 | 95 | 22 | 1 |
| pilot/ko/k1/phase2_3/texts/K1-190.json | K1-190 | 97 | 17 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-193.json | K1-193 | 92 | 11 | 1 |
| pilot/ko/k1/phase2_3/texts/K1-234.json | K1-234 | 99 | 13 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-242.json | K1-242 | 94 | 15 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-246.json | K1-246 | 88 | 18 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-252.json | K1-252 | 83 | 19 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-254.json | K1-254 | 89 | 14 | 2 |
| pilot/ko/k1/phase2_3/texts/K1-255.json | K1-255 | 96 | 16 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-276.json | K1-276 | 96 | 14 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-284.json | K1-284 | 94 | 17 | 0 |
| pilot/ko/k1/phase2_3/texts/K1-299.json | K1-299 | 91 | 13 | 0 |
| pilot/ko/k1/phase3_4_corrected_smoke/texts/K1-001.json | K1-001 | 115 | 8 | 0 |
| pilot/ko/k1/phase3_4_corrected_smoke/texts/K1-002.json | K1-002 | 121 | 4 | 0 |
| pilot/ko/k1/phase3_4_corrected_smoke/texts/K1-003.json | K1-003 | 123 | 8 | 1 |

### 新たな定義外用法の候補

以下6件はg23の起点frameとして自動FAILにしました。起点が明確な `학교에서 집으로 와요` はfrozen definition外です。出発・降車の表現については動作場所との境界を含め人間が確認してください。6件すべてを独立goldで誤用確定したとは扱いません。過去本文・過去PASS・ledgerは上書きしていません。

| source | 原句 | 根拠 |
|---|---|---|
| pilot/ko/k1/phase2_3/texts/K1-150.json | 학생이 버스에서 내려요. | Origin + explicit destination/return/departure/vehicle-exit frame; g23 source explicitly reserved |
| pilot/ko/k1/phase2_3/texts/K1-189.json | 버스에서 내려서 그림을 봐요. | Origin + explicit destination/return/departure/vehicle-exit frame; g23 source explicitly reserved |
| pilot/ko/k1/phase2_3/texts/K1-193.json | 어머니는 방금 시장에서 돌아왔어요. | Origin + explicit destination/return/departure/vehicle-exit frame; g23 source explicitly reserved |
| pilot/ko/k1/phase2_3/texts/K1-254.json | 버스는 아침에 집 앞에서 출발해요. | Origin + explicit destination/return/departure/vehicle-exit frame; g23 source explicitly reserved |
| pilot/ko/k1/phase2_3/texts/K1-254.json | 우리는 버스에서 내려서 같이 걸어요. | Origin + explicit destination/return/departure/vehicle-exit frame; g23 source explicitly reserved |
| pilot/ko/k1/phase3_4_corrected_smoke/texts/K1-003.json | 동생도 학교에서 집으로 와요. | Origin + explicit destination/return/departure/vehicle-exit frame; g23 source explicitly reserved |

Phase 3.4 clean003の `아버지는 어머니에게 사진을 받아요.` は人を出所とするg28のpolicy REVIEWです。第三者の希望、되다補語、抽象的genitiveも疑問として分離しました。

### gate改善が必要な正常用例候補

387件だった初期REVIEWを、縮約所有の重なるspan、있는/없는の明示異形、場所での걷다/뛰다と移動起点の対照で369件まで減らしました。許可意味を増やしたのではなく、frozen例外と局所frameを正しく扱いました。残るREVIEWには `공책에 답을 써요`、省略された本人の希望、抽象的所属、助詞から先の形容詞を飛ばす係り先などがあります。意味policyの確認とparserの改善を分けて進めます。

## regression

全suite 259件、focused 19件、いずれもPASS。Phase 3.1〜3.4のresolver、alias、quote、우리、grouping、同形義、future/retired/planned identity、atomic/failed isolation、実candidate schemaの001〜050対照も維持しています。

## 判定

C / FAIL。意味誤用の遮断・保存・無creditは成立しましたが、smokeは004で停止し、005までの成功条件を満たしていません。50本連続試験へは進めません。
