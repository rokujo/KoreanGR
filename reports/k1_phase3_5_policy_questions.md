# Phase 3.5 needs_human_policy

registryに8件の意味範囲疑問を記録しています。下記の用法は確認前に自動許可しません。今回はgrammar.json、ID、allowed functionを拡張していません。

| ID / surface | frozen記述 | 確認事項 | 現在の処理 |
|---|---|---|---|
| ko_k1_g03 / -았/었어요 | 했어요等の縮約を認める。経験・過去連体形や大過去-았었-は未許可。 | g03 excludes experience in notes, while g18 explicitly licenses experiential tried-past with g03. Trial past is not auto-approved until the interpretation is confirmed. | REVIEW、commit禁止 |
| ko_k1_g04 / -(으)ㄹ 거예요 | 予定中心。推量の多用は避ける。거/것のこの構文内用法だけ許可。自由な名詞化は不可。 | Plan centered and avoid frequent conjecture do not precisely define the permitted amount of conjecture. No automatic conjecture permission. | REVIEW、commit禁止 |
| ko_k1_g06 / -고 싶다 | 動詞に接続。本人の希望・相手への質問を中心にする。第三者の-고 싶어하다は未許可。 | Own wishes / questions to others are centered, but bare third-person -고 싶다 is not expressly banned. Treat it as needs_human_policy. | REVIEW、commit禁止 |
| ko_k1_g15 / -(으)ㄹ까요 | 勧誘・意向確認を中心にする。複雑な推量質問は避ける。 | meaning_ja includes 〜でしょうか but notes center on invitation/intention and avoid complex conjecture. Predictive questions are not auto-approved. | REVIEW、commit禁止 |
| ko_k1_g20 / 이/가 | 아니다の補語にも使用。누구+가→누가、나+가→내가、저+가→제가、너+가→네가を同一語に正規化。 | Notes explicitly admit 아니다 complements but do not explicitly settle 되다 complements. Core 되다 remains active; no lexical change. | REVIEW、commit禁止 |
| ko_k1_g24 / 도 | 単純な追加。疑問語+도等は아무 N도の許可範囲以外へ拡張しない。 | Simple addition is allowed; the reference to the permitted scope of 아무N도 does not define that scope. Scalar/indefinite readings need policy. | REVIEW、commit禁止 |
| ko_k1_g28 / 에게/한테 | 해요체では한테優先。에게서/한테서は未許可。 | 受け手・相手 does not explicitly authorize a source with 받다. Bare recipient/source ambiguity is REVIEW, not automatic source permission. | REVIEW、commit禁止 |
| ko_k1_g29 / 의 | 所有・所属のみ。나의→내、저의→제を同一語に正規化。이/그/저の指示連体詞と混同しない。 | 所有・所属 does not delimit abstract content relationships. Concrete ownership is auto-checkable; broader relation needs policy. | REVIEW、commit禁止 |

## 文脈境界の追加確認（policy件数8とは別）

g21の「目的語の基本用法」と、経路・時間extent、여행을 가다のevent-objectの境界を確認してください。対照fixture `길을 걸어요` は許可範囲・歩行lemma双方の根拠が不足するためREVIEWです。独立に「基本目的語」範囲が確定していない用例をFAILにしない方針です。

g23の起点は明示的に保留されているため、単なるpolicy曖昧性ではありません。ただし出発/降車が起点か動作場所かは文脈の確認が必要です。必要なら将来の定義修正を別途審査してください。今回のFAIL候補を理由に起点を自動追加しません。

文脈不足のREVIEWと、意味範囲のneeds_human_policyを分離しています。369件をそのまま人間へ全件確認させる運用にはしません。頻出型（g22書込み場所、g29抽象所属、g06省略主語、g28出所、g05現在証拠）をまとめて仕様・係り先処理を確認します。

## 技術blocker（意味policyとは別）

004のCore 마시다の `마셔요` が말/VX + 시/EPとして解析されました。対照probeでは対象の接続文をsentence／quoted／narration／paragraph／fullの全scopeで同様に誤解析しました。今回の根拠はscope差や引用符差ではなく、고直後の補助用言候補との競合です。新たな無条件aliasで救済せず、raw span・局所構文・限定identity復元の対照を次修正で設計すべきです。g14 EF/세요の前段unresolvedも監査履歴に残しています。これらは語彙・文法範囲を広げる理由ではありません。
