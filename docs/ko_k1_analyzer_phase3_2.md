# K1 Phase 3.2 identity / grouping policy

解析器は完全な韓国語意味解析器ではない。raw morphology、局所統語、登録identityを証拠として保存し、曖昧ならREVIEWにする。

1. surface全体の文字列置換は禁止。旧ALIASES 12件は全件監査し、raw POSと局所contextで適用する。
2. 感動詞네はIC＋応答境界を確認し、yesの登録IDへ解決する。裸の네 책はICでも所有用法の可能性がありREVIEW。数詞네はMM/NR＋後続名詞の根拠から넷へ解決する。
3. alias後の登録POS不一致を「辞書候補が唯一だから」で救済しない。必要な韓国語POS bridgeは있다/없다/필요하다、다른の連体形、数詞に続くcounterに限定し、明示する。
4. 同POSの同形語は全体default senseを使わない。눈/풀/다리/배は限定した局所contextの正の根拠を求める。生成annotationやsense overrideだけでは承認しない。
5. noun＋하고、登録N/XR＋XSV/XSA、登録compoundの隣接raw indexと形を区別する。ECや引用・空白を跨ぐ一般的なcontent連結は禁止。
6. 밥하고の誤分割を救済できるのは、登録food名詞の列挙、明示的な第2目的語、food predicateの根拠が揃う場合。raw streamは書き換えず、annotationとboundary decisionに証拠を残す。単なる밥하고 먹어요はREVIEW。
7. VV＋auxiliaryは登録compoundの形・raw signatureが揃った場合だけまとめる。묻어 봐요を물어보다にしない。試行-아/어 보다と希望/進行などのgrammar機能を勝手にlexical compoundへ結合しない。
8. bound noun/counterは局所数詞・raw POSで判定する。이랑/랑はgrammar32外なので今回もreject。引用符は新文法を許可しない。登録固定例外の完全一致spanだけは引用境界でも認識する。
9. 걷다/걸다限定resolverは3.1の証拠条件を維持する。登録compoundやresolver成功はfuture vocabularyの許可を意味しない。
10. planned IDと実使用identityのgate、hard coverage、unresolved禁止、atomic commitは維持する。engine変更もinput digestで検出する。

raw POS自体が間違う場合もある。例えば薬の苦さを言う약이 써요がVVとして解析されれば、writeへの唯一候補fallbackをせずREVIEWにする。これはfalse negativeを許容する方針であり、全文からsenseを完全自動解決したという主張ではない。
