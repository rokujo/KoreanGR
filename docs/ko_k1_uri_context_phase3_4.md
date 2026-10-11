# K1 Phase 3.4 — 우리 identityとrun schema

`k1_phase3_4_resolver.py` は承認済み3.3 layerの後に動く。raw morphologyのform・POS・offset・indexを編集しない。対象は既存 `ko_k1_0004 / 우리 / pronoun / we` のみ。新senseや使用許可を増やさない。

## NNGからの限定復元

原文のexact 우리、単一raw span、原文境界、raw indexの一意なannotation対応、登録ID/POS/sense一致を要求する。우리の直後に空白があり、Coreの집・학교・가족がexact NNG headとして続く場合だけ候補にする。우리自身へのparticleは認めない。

さらに先行400文字以内のraw NP `나 / 저 / 우리` と、直接付いた主格・主題・添加のparticleを、speaker/group参照の根拠として要求する。generated annotation、intent、単文で得たNP結果を全文NNGの代わりに使わない。発話・語境界をまたいで結合せず、未閉じ引用も復元しない。

NNG復元の条件が不足すればREVIEW。単文で正しい우리 집がNNGになり、話者参照が省略されている場合も自動承認しない。このfalse negativeを許容する。

## NPと対照例

raw NPの通常のwe用法は従来のidentityを維持する。ただし `우리 안 / 우리 밖` と우리自身の場所particle用法（例：우리에서）はnoun senseとの区別が不十分なためREVIEWとし、Core pronoun IDを取り除く。「我々の内部」等の正しい読みがある場合でも、ここでは人間確認を優先する。

동네はactive E2だが初期に使えず、교실も追加復元headへ入れない。任意の名詞を許可する仕組みではない。例外overlayは `config/languages/ko/k1/phase3_4/uri_pronoun_modifier_contexts.json`。

全recoveryに原文span・raw POS・解析scope・前後token・following noun・登録identity・raw話者anchor・判断・元annotationを保存する。原文への物理span照合と生解析の保存をtestsで検証する。

## Schemaとcontrolの分離

`build_k1_phase3_4_schemas.py` はgeneric `K1-xxx` の文字形式と、run契約の1〜50のenum・text_number範囲・ID/番号の一致を組み合わせる。candidate全体のJSON Schema検証を行う。smokeでもcandidate schemaは001〜050を受理し、実行は別のcontrol `max_text=3` で003に止める。future run用の契約はbuilderの明示的なrange引数から生成する。smoke固有のregexを複製しない。

source sceneは正式なreview-window `scene_catalog` の17値をそのまま使う。weatherはvocab tag/genreとして使用できるがsceneではnatureへ対応する。sceneを増やさない。genreはPhase 3の人間指定と既存承認済みpilotの値から19値へ限定し、未知のnews等を通さない。genre quotaは追加しない。

## 範囲と限界

新依存は追加しない。Kiwi/jsonschemaを継続使用する。完全なsense disambiguatorではなく、有限の文脈resolverと対照testsである。語彙・文法・予定・window・ID migration・自然さguidelineはfreezeを維持する。self-reviewは人間の言語自然さ承認ではない。

grammar IDが32項目内でも、その項目の許可義を満たす証拠にはならない。初回smokeの003で선물로のrole義を見落としたため、初回runを保存してpost-semantic FAILとし、別zero-state smokeでrecipientの에게へ修正した。補助validatorはこの実例を検出するが、すべてのparticle senseを完全に自動判定したとは扱わない。
