# Phase 3.3 quotation recovery audit

2登録identityだけを復元する別resolver layer。raw morphologyを変更せず、文字span・raw index・空白・POS/context・引用境界を保存する。recoveryは教材内の使用許可を与えない。

## quoted/unquoted parity

|content|registered ID|結果|
|---|---|---|
|`아니요.`|ko_k1_0443|PASS|
|`아니요, 책이 너무 비싸요.`|ko_k1_0443|PASS|
|`한국어 책이 있어요?`|ko_k1_0169|PASS|
|`네.`|ko_k1_0442|PASS|
|`네, 여기 있어요.`|ko_k1_0442|PASS|

## 証拠

아니요は元substring完全一致、VCN 아니＋EC/EF 요、発話冒頭、直後の応答句境界、registered interjection/no_politeを要求。한국어はMM 한＋NNG 국어の連続raw span、空白なしの元substring、registered noun/korean_language、名詞位置を要求する。両方とも一意のID/POS/sense、重複・隙間なしの文字partition、連続raw indices、annotation占有の一意性を必要とする。quoted/unquotedの独立syntax証拠を使い、generated annotationを証拠の代用にしない。

`아니요가...`、非応答位置、`한 국어`、内部空白・内部引用符、未閉鎖引用、raw POS不一致は自動復元しない。Core 아니다の文は아니요へ吸収しない。既に正しく登録identityへ解決されているtokenはALREADY_REGISTEREDで変更しない。これは新しいrecoveryの承認とは区別する。

## audit cases

|番号|種類|original text|recovery decision|
|---:|---|---|---|
|1|parity|`아니요.`|아니요: ALREADY_REGISTERED|
|2|parity|`"아니요."`|아니요: RECOVERED|
|3|parity|`아니요, 책이 너무 비싸요.`|아니요: ALREADY_REGISTERED|
|4|parity|`"아니요, 책이 너무 비싸요."`|아니요: RECOVERED|
|5|parity|`한국어 책이 있어요?`|한국어: ALREADY_REGISTERED|
|6|parity|`"한국어 책이 있어요?"`|한국어: RECOVERED|
|7|parity|`네.`|対象surfaceなし|
|8|parity|`"네."`|対象surfaceなし|
|9|parity|`네, 여기 있어요.`|対象surfaceなし|
|10|parity|`"네, 여기 있어요."`|対象surfaceなし|
|11|paragraphs|`친구가 말해요. "아니요, 책이 너무 비싸요." 저는 책을 봐요.`|아니요: RECOVERED|
|12|paragraphs|`저는 친구에게 말해요. "한국어 책이 있어요?" 친구가 말해요. "네, 여기 있어요." 저는 말해요. "아니요, 책이 너무 비싸요."`|한국어: RECOVERED, 아니요: RECOVERED|
|13|paragraphs|`친구가 말해요! "아니요." 저는 말해요. "한국어 책이 있어요?"`|아니요: RECOVERED, 한국어: RECOVERED|
|14|no_recovery|`아니요가 있어요.`|아니요: ALREADY_REGISTERED|
|15|no_recovery|`답은 아니요예요.`|아니요: DECLINED|
|16|no_recovery|`저는 아니요, 책을 읽어요.`|아니요: ALREADY_REGISTERED|
|17|no_recovery|`"한 국어 책이 있어요?"`|対象surfaceなし|
|18|no_recovery|`아니"요`|対象surfaceなし|
|19|no_recovery|`아니 요.`|対象surfaceなし|
|20|no_recovery|`한국 어 책이 있어요?`|対象surfaceなし|
|21|no_recovery|`"한국어책이 있어요?"`|한국어: DECLINED|
|22|no_recovery|`"아니요, 책이 비싸요.`|아니요: DECLINED|
|23|no_recovery|`"한국어 책이 있어요?`|한국어: DECLINED|
|24|unchanged_anida|`저는 학생이 아니에요.`|対象surfaceなし|
|25|unchanged_anida|`"저는 학생이 아니에요."`|対象surfaceなし|

negative fixtureは正しい韓国語教材とは主張せず、復元しない境界を検査する診断。診断を露出creditへ加えない。

## 全文

過去failed002の文字列をそのまま新gateへ通し、quoted한국어とquoted아니요を2箇所復元した。全文start/endはannotationとoriginal substringの照合で検証。残る열리다・未許可titleはhard rejectのまま。修正版002でも引用符を保持し、同じ2identityを復元してhard PASS。

全attemptでRECOVERED annotation合計4（failedとcommittedを合算した診断件数。露出数ではない）。全raw stream保存、schema violations 0。具体的なraw_parts/raw_tags/start/end/registered identity/quotation_context/evidence/decisionは[JSON audit](k1_phase3_3_quote_recovery_audit.json)とcandidate JSONにある。

## regression

Phase 3.2の全33contrast fixtures、8 frozen pilot用例、28不規則probeを新layerで再実行。旧Phase 3.2 tests自体も全suiteで維持。네のyes/所有REVIEW/数詞、밥하고/친구하고、걷다、눈/풀/쓰다、하다 compound、future、retired、planned identity、atomic commitを退行させていない。
