# Phase 3.8 lexical policy

sentence-local canonical identity が語彙permission・N/U・coverageの基準。paragraph/full morphologyは保存する診断であり、scope差のみでrejectしない。

## 承認されたbasic sense family

| ID | lemma | 許可するfamily |
|---|---|---|
| ko_k1_0072 | 아침 | morning_time / breakfast_meal |
| ko_k1_0074 | 저녁 | evening_time / dinner_meal |

`basic_sense_families.json` はactive DBへのmetadata overlayである。旧Core JSONの2つのmeal除外notesのみを上書きする。元JSON・過去run・ID・件数・初出を変えない。canonical tripleのsenseコードも元のmorning/eveningのまま、usage functionを別に記録する。meal用法を別新出語として数えない。점심、밥など他語のmeaningを拡張しない。

## Explicit restrictions

`explicit_restricted_senses.json` は既存notesに明記された意味上の対照18エントリだけを対象とする。各エントリは元ファイルとnotesの全文を持つ。POSのみ・文法構文のみの制限は既存のanalyzer/grammar form gateへ委ねる。呼称・丁寧さはnaturalness reviewへ委ねる。通常gloss、一般的な多義性、警告の多さを新たなhard restrictionの根拠にしない。

local negative context + canonical IDが揃った場合だけ明確なviolationとしてcandidate rejectする。例えば写真義の찍다に対する도장을 찍어요、writeの쓰다に対する모자를 써요、hold/liftの들다に対する마음에 들어요。別IDが正しく解決された場合にlemmaだけでこの制限を適用しない。pattern未検出は完全なsense証明を意味せず、author reviewと抜き取り人間レビューを併用する。語義解析器・全800語inventoryではない。

candidate errorは最大5attemptの局所repair。failed attemptはactual creditなし。同じ本文ミスが2回出たことだけでSTOPする旧production adapterは今回使用しない。5回で解決しない、validator矛盾、state/ledger/schema破損、数学的達成不能等はSTOP。

## Scope diagnostics alignment

sentence側とparagraph/full側ともlexical annotationに属するmorph_indicesを比較する。片側だけに重なったEF/ETM等を混ぜない。registered ID差・POS差は引き続きwarningで、canonical・coverage・permissionを上書きしない。

## Timing and review

benchmarkはlive local LLM author/file callbackの経過時間。モデル思考・tool transportを含み、API単独latencyではない。開発・pre/post full tests・最終replayはproduction時間から分離する。formal first-passとinitial draft preflight findingを別に示す。

10本ごとのauditはexplicit registryのcommitted occurrencesだけを再チェックする。全語semantic auditは行わない。自然なmeal usage、semantic grammar warning、scope warningはquality errorと数えない。
