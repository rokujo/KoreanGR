# Phase 3 人間レビュー用本文

このrunの逐次実績。自然さ・語義・訳のモデル確認は人間承認ではありません。

## K1-001 공원에서 만나요

오늘 친구하고 공원에 가요. 저는 집에서 친구를 기다려요. 친구는 버스를 타고 와요. 친구가 오면 공원에 갈 거예요. 그런데 지금 비가 많이 와요. 저는 창문으로 밖을 봐요.

길에는 사람이 적어요. 저는 우산을 가방에 넣어요. 친구가 집 앞에 도착해요. 친구는 우산이 없어요. 저는 문을 열고 친구를 봐요. 친구도 집에 들어오고 싶어요.

친구하고 집에 들어가서 앉아요. 저는 친구에게 따뜻한 물을 줘요. 친구는 물을 마시고 웃어요. 친구가 저에게 말해요. "괜찮아요." 우리는 집에서 음악을 들어요.

친구하고 공원 이야기를 해요. 공원에는 꽃하고 나무가 많아요. 저는 공원에서 사진을 찍고 싶어요. 친구도 꽃을 보고 싶어요. 세 시가 되면 밖에 나가요. 지금은 비가 안 와요.

친구하고 집에서 나가요. 공원까지 친구하고 걸어요. 공원에서 예쁜 꽃을 봐요. 친구는 꽃 옆에 서요. 저는 친구 사진을 찍어요. 친구하고 공원에서 걷고 이야기를 해요.

### 日本語訳

今日は友達と公園へ行きます。 私は家で友達を待ちます。 友達はバスに乗って来ます。 友達が来たら公園へ行く予定です。 ところが今は雨がたくさん降っています。 私は窓から外を見ます。

道には人が少ないです。 私は傘をかばんに入れます。 友達が家の前に着きます。 友達には傘がありません。 私はドアを開けて友達を見ます。 友達も家に入りたいです。

友達と家に入って座ります。 私は友達に温かい水を渡します。 友達は水を飲んで笑います。 友達が私に言います。 『大丈夫です。』 私たちは家で音楽を聴きます。

友達と公園の話をします。 公園には花と木がたくさんあります。 私は公園で写真を撮りたいです。 友達も花を見たいです。 三時になったら外へ出ます。 今は雨が降っていません。

友達と家から出ます。 公園まで友達と歩きます。 公園で美しい花を見ます。 友達は花の横に立ちます。 私は友達の写真を撮ります。 友達と公園で歩いて話をします。

新出: 되다 / ko_k1_0373, 괜찮다 / ko_k1_0413

選択review: なし

incidental: 들어오다 / ko_k1_0386

defer: なし

Coverage: {'denominator_N': 115, 'new_tokens_U': 2, 'controlled_vocab_coverage': 0.9826086956521739, 'previous_vocab_coverage': 0.9652173913043478, 'target_99_met': False} / 119 어절

Warnings: []

Semantic review: {'stage': 'naturalness_semantic_review', 'origin': 'author_second_pass_not_independent_gold', 'checks': {'coherent_goal': {'verdict': 'YES', 'reason': '公園で会う目的を雨待ちから外出まで維持。'}, 'plausible_actions': {'verdict': 'YES', 'reason': '雨の間は家で待ち、やんでから近い公園へ行く。'}, 'no_review_only_actions': {'verdict': 'YES', 'reason': '初回でreviewはない。'}, 'natural_arguments': {'verdict': 'YES', 'reason': '写真を撮る・水を渡す等の通常の目的語。'}, 'clear_references': {'verdict': 'YES', 'reason': '私と友達を明示し、人物の切替を保つ。'}, 'necessary_genitives': {'verdict': 'YES', 'reason': '所有助詞を追加しない。'}, 'meaningful_adverbs': {'verdict': 'YES', 'reason': '今は雨の状態対比に必要。数合わせ副詞はない。'}, 'simple_natural_construction': {'verdict': 'YES', 'reason': '短い応答と単純現在を中心にする。'}}, 'flags': [], 'human_approved': False, 'approval_policy': 'Human/context review required; regex and model judgments are screening only.'}

Hard errors: ['Body length outside 120..180', 'Future Expansion ko_k1_0386', 'Token 198: uncontrolled vocabulary or future introduction', 'Token 91: uncontrolled vocabulary or future introduction', 'Unconfirmed previous Expansion ko_k1_0386', 'Unresolved 걸 / 걸다', 'controlled_vocab_coverage below hard 100%', 'previous_vocab_coverage below hard 98%']。失敗試行はledger未反映、日本語訳もdraft。

