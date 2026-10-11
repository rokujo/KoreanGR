# Phase 3.8 Sense policy source audit

| ID | lemma / allowed sense | frozen source | notes |
|---|---|---|---|
| ko_k1_0073 | 점심 / lunch | config/languages/ko/k1/core_vocab.json | 昼食を中心義に採用。正午の厳密な時刻義は未許可。 |
| ko_k1_0078 | 분 / minute | config/languages/ko/k1/core_vocab.json | 時間単位のみ。敬称분は未登録。 |
| ko_k1_0080 | 월 / calendar_month | config/languages/ko/k1/core_vocab.json | 暦の月のみ。期間はExpansion 달/month_duration。 |
| ko_k1_0127 | 차 / tea | config/languages/ko/k1/core_vocab.json | 飲み物のお茶のみ。自動車の略称차は未登録。 |
| ko_k1_0133 | 말 / speech | config/languages/ko/k1/core_vocab.json | 言葉・発言のみ。馬は未登録。 |
| ko_k1_0135 | 일 / work | config/languages/ko/k1/core_vocab.json | 仕事・作業のみ。日付の일と事件の일はこの義では未許可。 |
| ko_k1_0153 | 눈 / snow | config/languages/ko/k1/core_vocab.json | 雪のみ。目はExpansionの別sense。 |
| ko_k1_0178 | 쓰다 / write | config/languages/ko/k1/core_vocab.json | 書くのみ。使う・かぶるはこの義では未許可。 |
| ko_k1_0229 | 찍다 / take_photo | config/languages/ko/k1/core_vocab.json | 写真を撮るのみ。印を押すはExpansionの別sense。 |
| ko_k1_0808 | 닦다 / wipe_clean | config/languages/ko/k1/expansion_vocab.json | 清掃のために磨く・拭く動作のみ。歯磨き、机や物を拭く場面。抽象的な腕前を磨く義は許可しない。 |
| ko_k1_0810 | 공 / ball | config/languages/ko/k1/expansion_vocab.json | 遊び・運動に使うボールのみ。同音の抽象義や漢字語の構成要素は許可しない。 |
| ko_k1_0389 | 보이다 / be_visible | config/languages/ko/k1/expansion_vocab.json | 見えるの自動詞義のみ。見せるの使役義は未許可。 |
| ko_k1_0495 | 표 / ticket | config/languages/ko/k1/expansion_vocab.json | 交通・入場の切符のみ。表・票の意味は未許可。 |
| ko_k1_0511 | 기사 / driver | config/languages/ko/k1/expansion_vocab.json | 運転手のみ。新聞記事・騎士の意味は未許可。 |
| ko_k1_0812 | 들다 / hold_lift_by_hand | config/languages/ko/k1/expansion_vocab.json | 手に持つ・持ち上げる物理的動作だけを許可する。가방을 들어요 / 책을 들어요。費用がかかる・気に入る・年を取る・中へ入る系・その他の辞書上の別義は自動許可しない。lemmaが同じでも別senseは未許可。全用例で対象物と手による保持・持ち上げの文脈を確認する。 |
| ko_k1_0809 | 붙이다 / attach_stick | config/languages/ko/k1/expansion_vocab.json | 紙・テープなどを対象へ貼り付ける物理的動作のみ。火をつける等の別義は許可しない。 |
| ko_k1_0804 | 충전하다 / charge_battery | config/languages/ko/k1/expansion_vocab.json | Phase 1.2で正式採用。電気機器の充電のみ。補助構文や専門的な電気説明へ拡張しない。 |
| ko_k1_0786 | 꿈 / dream_sleep | config/languages/ko/k1/expansion_vocab.json | 睡眠中の夢のみ。将来の夢・希望の抽象義は未許可。 |

全18件で元canonical tripleとnotesが一致。新しいpolysemy推測による制限は加えない。朝食/夕食の2件は人間承認のbasic familyとして別overlay。

本runで明確なrestriction違反0、NO_CLEAR_VIOLATIONは全意味の自動承認ではない。言語品質・訳・diagnosticは別に報告する。
