# Phase 3.7 sentence-local canonical validation

本文は終止符ごとの連続した原文spanへ分割する。引用符は保持し、引用内の複数文も個別解析する。titleは独立したphraseとして解析する。未閉鎖引用符などは既存resolverが保守的に扱う。

語彙identityのauthorityは各sentenceの既存analyzer／resolver結果。活用・POS・同形異義語の文脈証拠、actual allowed snapshot、future／retired禁止を維持する。単なるsurface一致や唯一の許可IDだけで採用しない。

canonical_lexical_mapにはsentence番号、原文座標、surface、ID／lemma／POS／sense、sentence raw証拠を保存する。全文座標へ移したcanonical annotationsからN/U/coverageと初出・露出を計算する。raw_morphologyはsentence rawの連結であり、full_text_diagnosticおよびparagraph_diagnosticsに広域rawを別途改変せず保存する。

scope_diagnosticsは全canonical語彙spanについてsentenceとparagraph/fullのID／raw POSを比較する。ID不一致・POSだけの不一致を分離する。これらはwarningでありpermission、coverage、retry、STOPを上書きしない。semantic grammar診断もwarningのまま。

final reanalysisではsentence-local canonical map／annotations／raw／coverage／grammar形式を再計算し比較する。広域診断結果自体の差はcommit blockerではない。既存candidate gate、最大5attempt、同じhard error2回停滞停止、author review、atomic publishを継承する。失敗candidateはcreditしない。

既存frozenファイルを変更せず、新規versionで実装した。過去失敗候補のreplayはメモリ上の当時のstateに対するreport-only監査であり、新productionのstateに混ぜない。

これは汎用形態素解析器でも完全なsense disambiguationでもない。sentence-localでも証拠不足ならrejectする。人間抜き取りレビューが必要である。

## Trial-discovered limitations

Sentence-local registered ID membership is not proof of every frozen semantic restriction. The evening-only Core entry was falsely accepted as dinner. The run stopped and the exposure ledger is retained as historical actual commits, not an approved continuation state. Broad-scope POS-only counts need lexical-index alignment; current warnings include ending-span overlap artifacts. Neither limitation was patched during production.
