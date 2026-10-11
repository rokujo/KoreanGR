# K1 grammar32 semantic gate（Phase 3.5）

意味範囲の根拠は `config/languages/ko/k1/grammar.json` と凍結されたK1文書だけです。一般的な韓国語で正しくても、その意味を追加許可しません。語彙・文法DB、ID、予定表は変更していません。

`grammar_semantics.json` は32項目の監査overlayです。source SHAと各 frozen_definition の一致を確認します。意味分類は原形を保存したraw morphology、登録lexical identity、助詞に係る名詞と述語の局所関係を使います。作者の「方向です」などの申告は入力にしません。

候補処理は形態・語彙解析 → grammar ID/set検証 → semantic grammar gate → naturalness lint／scene review → 最終raw再解析 → atomic commitです。bodyとtitleを同じ意味gateに通します。全文gateを採用し、文単位precheckは従来の語彙・resolver検査を維持しています。

- PASS: 登録済みの許可意味に一致する局所frameの証拠がある。
- FAIL: 明確な未許可意味。例: 선물로 주다 のrole、학교에서 집으로 오다 のsource。
- REVIEW: 一意化できない、局所frame未対応、または凍結定義が曖昧。

FAILとREVIEWの両方がhard rejectです。Phase 3.5 smokeではいずれもrunを停止します。失敗候補のstate、導入、review、debt、genre、sceneへのcreditはゼロです。最終再解析では semantic_grammar_checks も比較します。

これは完全な意味役割解析器ではありません。32項目すべてに狭いauto PASS経路がありますが、任意の32文法用例を自動承認できるという意味ではありません。11項目は局所構造中心、21項目は語彙・意味関係を含むheuristicです。全項目にREVIEW経路があります。confidenceはルールの決定指標であり、校正された確率ではありません。

`있는/없는`はg26の明示異形として、raw上のg27候補から意味overlayでg26へ対応づけます。rawは変更せず morphological_grammar_id を残します。g04内の거のcopulaとg31の明示された에서부터は、親構文の条件を別途検証する構成要素として扱います。単独에서にsource許可を追加しません。

70 fixtureの期待結果は対象grammarの意味判定、または前段境界でのrejectです。全文語彙・形態PASSを意味しません。凍結g14例の `기다리세요` はraw EF/세요として返り、従来解析器にunresolvedが残る場合があります。semantic overlayは意味候補を検出してもそのunresolvedを消しません。만에のraw NNB/만も同様に前段rejectを要求します。

過去28本文の再監査はreport-onlyです。全800の登録identityを参照して再解析しますが、逐次導入の許可やcoverageの再承認、実績の移入はしません。REVIEWは誤用確定ではありません。文脈追跡、述語の係り先、所有の範囲などに未対応の自然な用例も含みます。

Phase 3.5では004でsemantic REVIEWと構造的raw誤解析を検出して停止しました。005以降の生成・creditはありません。新gateは取り逃しを防止していますが、smoke005完了条件は未達です。詳細はPhase 3.5レポートを参照してください。
