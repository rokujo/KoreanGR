# K1 Phase 3.2 alias / POS / grouping監査

旧 `scripts/k1_pilot_analysis.py` と旧runはfreezeしたまま、新version `scripts/k1_phase3_2_analysis.py` / `resolver.py` を作成。文字列だけのglobal aliasを使用せず、raw morphologyを保持し、登録lemma/POS/sense、局所統語、適用条件を照合する。

## 全ALIASES 12件

|分類|件数|
|---|---:|
|safe_surface_normalization（無条件で安全）|0|
|pos_conditioned_alias|7|
|context_conditioned_alias|4|
|unsafe_alias_remove|1|
|review_required（静的alias分類）|0|

context条件を満たさない個別用例はREVIEWになる。無条件に安全なglobal文字列置換は認めない。削除対象は実surfaceでない `네_numeral` の旧key。`네 → 너` のglobal適用も廃止し、限定したNP所有用法候補の枝だけを残す。

|旧surface|旧target|分類|新条件|
|---|---|---|---|
|이거|이것|pos_conditioned_alias|raw NP; registered pronoun identity; no global text replacement|
|그거|그것|pos_conditioned_alias|raw NP; registered pronoun identity; no global text replacement|
|저거|저것|pos_conditioned_alias|raw NP; registered pronoun identity; no global text replacement|
|내|나|context_conditioned_alias|raw NP plus possessive nominal context; raw IC/MM cannot use this pronoun alias|
|네|너|context_conditioned_alias|raw NP plus possessive nominal context; raw IC/MM cannot use this pronoun alias|
|제|저|context_conditioned_alias|raw NP plus possessive nominal context; raw IC/MM cannot use this pronoun alias|
|한|하나|pos_conditioned_alias|raw MM/NR plus following nominal; registered numeral; no sense extension|
|두|둘|pos_conditioned_alias|raw MM/NR plus following nominal; registered numeral; no sense extension|
|세|셋|pos_conditioned_alias|raw MM/NR plus following nominal; registered numeral; no sense extension|
|스무|스물|pos_conditioned_alias|raw MM/NR plus following nominal; registered numeral; no sense extension|
|네_numeral|넷|unsafe_alias_remove|Synthetic key never a surface; replace with explicit 네 MM/NR contextual branch|
|다른|다르다|context_conditioned_alias|exact attributive surface, raw MM, following nominal; explicit adjective bridge + g26|

`스무 → 스물` の登録lemma認識はその語の初出許可を意味しない。future/retired permissionはcandidate gateで別に検証する。

## 네の誤aliasと修正

旧解析は `네 / IC` を辞書参照前に `너`へ変換し、compatibleなPOS候補がなくても唯一のCore pronounを採用していた。新解析は以下を分離する。

- `네.` / `네, 책이 있어요.` / 引用内の`"네."`: raw IC＋応答境界から、登録interjection yes `ko_k1_0442`。
- `네 책`: 実KiwiではICになる。この裸の列には所有用法の可能性が残るため、yesにも너にも決めずREVIEW。モデルの所有用法申告だけでは承認しない。
- raw NPとしての네＋後続名詞が確認できた場合: 所有縮約の너候補。synthetic raw POS対照testで条件を検証。現実の`내 책`/`제 책`はKiwiがNP＋JKGを出すため、そのraw境界を使う。
- `네 사람이 와요.`: raw MM＋後続名詞から数詞넷。pronounへglobal aliasしない。

## unique fallback・surface normalization・sense全体

唯一の登録entryでもraw POSに不適合なら採用しない。POS filter後に複数候補が残れば、局所根拠がない限りREVIEW。必要なPOS bridgeは있다/없다/필요하다の既存DB adjective、exact 다른の連体形、数詞contextのcounterに明示限定する。

旧DEFAULT_SENSE 14件は監査履歴として残し、新versionでは無条件に使わない。active800には同形lemma13組があり、저/일/개/쓰다/이/팔/봉지/달/새のPOS境界と、눈/다리/배/풀の同POS sense境界を区別する。後者は限定局所contextの正の根拠が必要。sense overrideもPOS・contextを上書きできない。

예: `눈이 와요.`→snow、`눈이 아파요.`→eye、`눈이 있어요.`→REVIEW。`풀로 종이를 붙여요.`→glue、`나무 아래에 풀이 있어요.`→grass、`풀이 있어요.`→REVIEW。`약이 써요.`はKiwiがVVを返すため、writeへ誤承認せずREVIEW。VA/bitterへ勝手にtag変更することもしていない。

## 밥하고とgrouping全体

旧001初稿の `밥하고` はNNG 밥＋XSV 하＋EC 고に分割された。旧実装は未登録compound 밥하다へまとめていた。新実装では登録compoundがない場合に、登録food名詞の明示的な列挙（第2food名詞＋目的格）とfood predicateが揃えば、밥とgrammar25の하고へ再分割する。raw streamは変更せず、使用したraw indicesと根拠をboundary decisionに保存する。

`밥하고 국을 먹어요.` / `동생은 밥하고 우유를 좋아해요.`はRESOLVED。`밥하고 먹어요.`は第2目的語がなく、別の動詞解釈も排除できないためREVIEW。`친구하고 가요.`はraw noun＋JKBを保つ。`공부하고 있어요.`は登録공부하다のNNG＋XSVと進行grammar05を分離する。

|境界|新方針|
|---|---|
|N + 하고|raw JKB/JC -> g25; missegmented XSV+EC only with explicit food enumeration evidence; otherwise REVIEW|
|N + 이랑/랑|not grammar32; REVIEW/reject; not rewritten to 하고|
|하다 compound|adjacent NNG/XR + XSV/XSA; full registered lemma + matching verb/adjective POS|
|VV + auxiliary|registered exchange/ask prefix with exact surface+raw signature; otherwise grammar09/05/06/18 separately|
|registered compound|consecutive raw lexical indices in one eojeol; no EC/punctuation skipping, no productive synonym alias|
|bound noun/counter|raw NNB/NNG, registered counter and local numeric evidence; closed grammar constructions explicitly recognized|
|quotation|quoted IC response may resolve; frozen expressions exact registered spans; quotation licenses no extra grammar|
|punctuation adjacent|punctuation defines context boundaries, never a cross-boundary alias or compound license|

助詞・EC・引用符を飛ばして複数contentを連結する一般的groupingは廃止。登録lemmaに一致してもraw indicesが隣接し、対応するPOSと形態が合う必要がある。交換compoundは도와/빌려/돌려の形とraw VV＋EC＋VV/VXを照合。물어보다は물어という形を追加照合し、`묻어 봐요.`をaskへ変換しない。등록fixed exceptionは完全一致spanだけを引用符内でも認識し、grammar32の迂回範囲を広げない。이랑/랑は依然仕様外。

## 対照fixture結果

PASSはその短いparser fixtureの解析を意味し、教材lengthや学習履歴を満たすという意味ではない。parser fixtureではactive登録800を照合対象にした。実教材のactual permissionは別gate testとsmoke snapshotで検証した。REVIEW期待を満たすことはregression成功だが、その用例を教材commitする許可ではない。

|ID|raw text|期待|結果|照合|
|---|---|---|---|---|
|yes_standalone|네.|PASS|PASS|OK|
|yes_clause|네, 책이 있어요.|PASS|PASS|OK|
|yes_quoted|"네."|PASS|PASS|OK|
|possessive_ambiguous_raw_ic|네 책|REVIEW|REVIEW|OK|
|four_people|네 사람이 와요.|PASS|PASS|OK|
|rice_hago_without_second_object|밥하고 먹어요.|REVIEW|REVIEW|OK|
|rice_soup_enumeration|밥하고 국을 먹어요.|PASS|PASS|OK|
|rice_milk_preference|동생은 밥하고 우유를 좋아해요.|PASS|PASS|OK|
|friend_particle|친구하고 가요.|PASS|PASS|OK|
|study_progressive|공부하고 있어요.|PASS|PASS|OK|
|noun_study|공부가 어려워요.|PASS|PASS|OK|
|polite_possessive|제 책이에요.|PASS|PASS|OK|
|plain_possessive|내 책이에요.|PASS|PASS|OK|
|different_attributive|다른 책을 읽어요.|PASS|PASS|OK|
|unregistered_rang|친구랑 가요.|REVIEW|REVIEW|OK|
|unregistered_irang|학생이랑 가요.|REVIEW|REVIEW|OK|
|auxiliary_try|책을 읽어 봐요.|PASS|PASS|OK|
|registered_exchange|친구를 도와주고 싶어요.|PASS|PASS|OK|
|registered_ask|선생님에게 물어봐요.|PASS|PASS|OK|
|item_counter|사과 두 개를 사요.|PASS|PASS|OK|
|dog_noun|개가 집 앞에 있어요.|PASS|PASS|OK|
|tooth_noun|이가 아파요.|PASS|PASS|OK|
|this_determiner|이 책이 좋아요.|PASS|PASS|OK|
|write_verb|이름을 써요.|PASS|PASS|OK|
|bitter_raw_pos_conflict|약이 써요.|REVIEW|REVIEW|OK|
|snow_context|눈이 와요.|PASS|PASS|OK|
|eye_context|눈이 아파요.|PASS|PASS|OK|
|eye_snow_ambiguous|눈이 있어요.|REVIEW|REVIEW|OK|
|glue_context|풀로 종이를 붙여요.|PASS|PASS|OK|
|grass_context|나무 아래에 풀이 있어요.|PASS|PASS|OK|
|punctuation_adjacent|"네!" 책이 있어요.|PASS|PASS|OK|
|registered_exception_quoted|“안녕하세요.”|PASS|PASS|OK|
|bury_try_not_ask|묻어 봐요.|REVIEW|REVIEW|OK|

## Regression tests

最終全体test: 169件、PASS、failures=0、errors=0。最終focused suiteは22 test methods（full suite開始後に追加した旧neバグ注入testを含む）。対照fixture33件、Phase 2.3の実本文から採った8文、Phase 3.1の不規則活用28probeを検証した。raw stream保持、raw index重複なし、限定walking resolver、future/retired拒否、planned identity mismatch、candidate state不変、retry隔離、atomic crash前後/idempotent commitを確認。

完全なsense disambiguation、韓国語の全活用・全結合辞書、人間の自然さ承認を実装したという主張ではない。新runはこの2本文だけであり、初期50本全体のfalse-negative率はまだ未検証。
