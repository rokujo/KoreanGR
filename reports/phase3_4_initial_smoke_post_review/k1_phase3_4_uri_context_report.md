# Phase 3.4 — 우리の文脈依存POS揺れ対策

**A / Phase 3.4 PASS。** 新しいactual stateゼロから001→002→003をhard PASS後に各1回だけcommitした。004以降・300本量産は行っていない。

## 原因と修正

元v3の自然な引用 `"우리 집에 올 거예요?"` は短文ではNP、段落と全文ではNNGだった。Core `우리 / ko_k1_0004 / pronoun / we` とのPOS不一致を旧gateがREVIEW・未解決としてrejectした判断を維持する。

新 `k1_phase3_4_resolver.py` は承認済み3.3 resolverの後段に置く。rawを保存し、元文字spanとcontext evidenceに基づくannotationだけを別layerで復元する。無条件NNG→pronoun alias、単文結果の全文rawへの上書き、generated annotationのみの採用はしない。

対象headは既存Core 집/home・학교/school・가족/familyの3語に限定。NNG時はexact 우리の単一raw span、空白、raw NNGのexact head、登録ID/POS/sense、우리へのparticleなし、直前400文字以内のraw NP speaker/group anchor＋主格/主題/添加particle、一意なannotation span、引用境界を要求する。全根拠が揃った場合だけRECOVERED。동네/E2・교실/Coreは今回の追加headに入れない。

raw NPの通常のweは維持する一方、`우리 안 / 우리 밖 / 우리에서` はnoun読みを否定できずREVIEWへ送る。これによりrawがNPであることだけでもCore pronounを自動承認しない。NNGで話者根拠のない短文や任意の名詞もREVIEW。正しい用法の一部を拒否するfalse negativeを許容する。

## Scope・contrast audit

|scope|raw POSとresolver decision|期待に対する結果|
|---|---|---|
|plain_question|NP → ALREADY_REGISTERED|PASS|
|quoted_question|NP → ALREADY_REGISTERED|PASS|
|speaker_and_quote|NP → ALREADY_REGISTERED|PASS|
|candidate_full_text|NNG → RECOVERED, NP → ALREADY_REGISTERED, NP → ALREADY_REGISTERED, NP → ALREADY_REGISTERED, NP → ALREADY_REGISTERED, NP → ALREADY_REGISTERED|PASS|
|candidate_paragraph|NNG → RECOVERED, NP → ALREADY_REGISTERED|PASS|
|diagnostic_full_without_quotes|NP → ALREADY_REGISTERED, NP → ALREADY_REGISTERED, NP → ALREADY_REGISTERED, NP → ALREADY_REGISTERED, NP → ALREADY_REGISTERED, NP → ALREADY_REGISTERED|PASS|
|positive_contrast|NP → ALREADY_REGISTERED|PASS|
|positive_contrast|NP → ALREADY_REGISTERED|PASS|
|positive_contrast|NP → ALREADY_REGISTERED|PASS|
|positive_contrast|NP → ALREADY_REGISTERED|PASS|
|noun_contrast|NP → REVIEW|PASS|
|noun_contrast|NP → REVIEW|PASS|
|noun_contrast|NP → REVIEW|PASS|

paragraph / full textのNNGをそのまま保存し、同じCore pronoun identityへ復元した。span offset49 / 238、raw index・前後tokens・following noun・raw話者anchor・quotation context・元annotationを[JSON audit](k1_phase3_4_uri_context_audit.json)に保存。noun対照で他のtokenも未解決になる場合があるが、우리そのものをREVIEWにすることを独立確認した。negative fixtureを自然な教材とは扱わない。

3.3 quote recoveryは変更しない。네 / 아니요 / 한국어の5組quoted/unquoted parity、複数quoted turns、punctuation、全文・paragraph、raw spanの保存を新layerで再実行。Phase 3.2の33境界fixtures、8 frozen用例、28不規則probe（걷다限定resolver含む）も通った。future/retired・planned identity・failed isolation・atomic fault・二回停滞STOPのgateは維持した。

## Smokeと再解析

001/002は元v3のraw本文のみを回帰candidateとして使用した。旧annotation・coverage・ledger/creditをimportせず、001実commit後のsnapshotだけを002に渡した。003は001/002実commit後に新規作成した家族写真の誕生日プレゼント場面。予定新出이 / 그は各1token、네の応答は実導入済み語のincidental露出。

|教材|PASS attempt|어절|N / U|controlled|previous|
|---|---:|---:|---|---|---|
|001|1|137|133 / 2|100%|98.496241%|
|002|1|135|130 / 2|100%|98.461538%|
|003|1|151|149 / 2|100%|98.657718%|

3本ともplanned IDs == actual IDs、future0 / invalid0 / unresolved0 / grammar違反0 / hard errors0。99% targetはいずれもmissするがhard98%を満たしblockerではない。003は151어절でdraft soft target130〜150を1어절上回るが、hard120〜180内なので不自然な削除・paddingを行わない。

別のtemporary zero-stateへraw sourceだけを順に再投入し、全annotation・raw・coverage・review/incidental・uri/quote auditの差分0、最終state完全一致を確認した。この再解析は本runへのcreditではない。candidate評価前後のledger SHAは全件一致。epoch3、records/texts/genre/scene history各3。validation処理でも実ledger byte不変。旧runの状態・本文・失敗結果を含むfreeze 625ファイルの変更0。

actual導入6語、異なるvocab/text実露出7組、incidental 1、selected review 0。003で初めてreview windowが開いた2語は未消化debtとして記録し、creditしない。期限切れ0、数学的回収不能0。3本smokeは50本運用のdebt回収や多様性の成功証明ではない。

|debt語ID|window index|期限範囲|
|---|---:|---|
|ko_k1_0373|0|3〜6|
|ko_k1_0413|0|3〜6|

## Tests・自然さ・限界

|suite|tests|failures / errors|結果|
|---|---:|---|---|
|all|239|0 / 0|PASS|
|focused|32|0 / 0|PASS|

validator errors 0、schema errors 0。active resolver REVIEW0。自然さlintは {'nat_restricted_sense': 6}、translation flags 0、semantic flags 0。쓰다は公책・写真の裏へ名前を書くwrite義の文脈として確認する。自己評価とraw解析は独立した人間の言語自然さ承認ではない。

有限の文脈resolverであり、一般的な韓国語POS/sense disambiguationを完成したとは扱わない。語彙800・文法32・schedule/window・ID migration・自然さguidelineは変更なし。追加依存なし。

**A：別runの実績ゼロから001〜050連続試験を再実施可能。** 今回は003で終了し、004以降へ続けない。次runにもmax5attempt・2回停滞STOP・構造STOP・10本checkpoint・050上限を引き継ぐ。300本量産許可ではない。

[validation結果](k1_phase3_4_validation_result.json) / [forward schema report](k1_phase3_4_forward_schema_report.md) / [人間レビュー本文](k1_phase3_4_smoke_review.md) / [設計説明](../docs/ko_k1_uri_context_phase3_4.md)
