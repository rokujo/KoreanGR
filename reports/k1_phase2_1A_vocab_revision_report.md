# K1 Phase 2.1A — 800語の最終微修正

人間レビューで承認された5交換を適用。Core300 / Expansion500 / Total800、E1/E2/E3=200/200/100、32文法を維持した。短い検証例13文のみを追加し、20教材の本文生成・再生成は行っていない。全300本文も生成していない。

## 5交換の最終内容と恒久ID

|退役語 / ID / sense|採用語 / 新ID / sense|rank|tier|category|旧初出→新初出|
|---|---|---|---|---|---|
|오렌지 / ko_k1_0363 / orange|닦다 / ko_k1_0808 / wipe_clean|363|E1|verbs|040→020|
|찍다 / ko_k1_0603 / stamp|붙이다 / ko_k1_0809 / attach_stick|603|E2|verbs|155→127|
|포도 / ko_k1_0365 / grape|공 / ko_k1_0810 / ball|365|E1|places_objects|041→033|
|오르다 / ko_k1_0577 / rise_climb|그림 / ko_k1_0811 / drawing_picture|577|E2|places_objects|141→111|
|가져다주다 / ko_k1_0571 / bring_to_someone|들다 / ko_k1_0812 / hold_lift_by_hand|571|E2|verbs|138→110|

ID0808〜0812を新規採番し、next_sequence=813。retired IDsは累計12件。旧IDへのaliasは作成しない。rankは旧語の表示スロットを継承し、1〜800の一意な表示順を維持する。rankとIDと初出順は別の役割である。Phase 1.2の7交換の対応レコードはそのまま保持し、今回5件を追加した。K2候補台帳への記録のみで、K2の語彙体系・教材計画は設計していない。

Core 찍다/take_photoは同じID・内容のままactive。ko_k1_0603/stampだけ退役。도장は追加しない。배터리/요즘/동안/묻다/걸어가다/이야기하다も追加せず、Phase 2.1レポートの候補履歴を保持した。

## 들다の許可義

`들다 / verb / hold_lift_by_hand`＝「手に持つ・持ち上げる」だけを許可。費用・好み・加齢・中へ入る等の別義は未登録であり、lemmaが同じでも許可しない。DBのnotesとprofile.lexical_sense_policyへ制限を保存し、raw annotationは全用例でrestricted_sense_context_reviewを返す。

意味解決はlemma/POS/senseの完全一致で照合し、未登録senseを拒否する。単一エントリしかなくても、解析器のlemma判定だけでは文脈義を承認しない。Core 들어가다等の別lemmaの許可と混同しない。

## 初出の再査定

退役元の初出をそのままコピーせず、同tierの導入枠を5組入れ替えた。500語全体の初出台帳を再生成し、日別新出数と空き枠を維持した。その他490語の初出は変更していない（退役5・新5・既存の移動5を区別）。

|新語|新初出|位置を交換した既存語|既存語の初出差分|場面判断|
|---|---|---|---|---|
|닦다|K1-020|비누|020→040|수건と同じ回で拭く・清掃する場面を扱う。|
|붙이다|K1-127|가위|127→155|풀（糊）と同じ工作場面で貼る動作を導入。|
|공|K1-033|잠깐|033→041|어떻다と同じ回でボールの状態を尋ねる。|
|그림|K1-111|건물|111→141|동네と同じ回で町の絵を見て話す。|
|들다|K1-110|엘리베이터|110→138|층と同じ回で荷物を持ち、階を移動する。|

닦다はE1前半20、공はE1前半33。E2は들다110、그림111、붙이다127で、E2導入期103〜219の早めの範囲へ置いた。移動した既存5語も元の導入可能範囲に収まる。場面案は初出位置の編集上の根拠であり、教材本文の成立を証明したものではない。

最終初出255、256〜300の45本は新出0。255本×2枠=510枠に500語を配置し、余裕10枠。新出0は2本、新出1は6本、新出2は247本（001〜255）。276〜300の高速多読ゾーンも新出0のまま維持。

## categoryはsoft distribution

|category|変更前|変更後|差分|
|---|---|---|---|
|abstract_body_emotion|40|40|0|
|adjectives|65|65|0|
|adverbs_connectors|50|50|0|
|food_nature|50|48|-2|
|people_social|40|40|0|
|places_objects|90|92|2|
|school_work_transport_info|30|30|0|
|time_counters_units|35|35|0|
|verbs|100|100|0|

food_natureは50→48、places_objectsは90→92、verbsは100のまま。カテゴリ件数はhard exactではなく、教材設計・監視用のsoft目標。差分が15語超または25%超ならwarning、未知カテゴリもwarning。Core/Expansion/TotalとTier件数は引き続きhard条件。

## flexible review windows

Phase 2.1のwindow生成規則・自然さ優先・5〜8review soft目標・繰越債務・最終6教材の実出現条件を維持。500 active語について初出と5窓を再作成した。退役12語のactive windowは存在しない。位置を変更した既存5語の窓も新初出に合わせた。

|新語|初出|review windows|
|---|---|---|
|닦다|20|22〜25 / 26〜44 / 45〜85 / 86〜139 / 140〜300|
|붙이다|127|129〜132 / 133〜151 / 152〜192 / 193〜246 / 247〜300|
|공|33|35〜38 / 39〜57 / 58〜98 / 99〜152 / 153〜300|
|그림|111|113〜116 / 117〜135 / 136〜176 / 177〜230 / 231〜300|
|들다|110|112〜115 / 116〜134 / 135〜175 / 176〜229 / 230〜300|

active vocab_exposure_schedule.jsonは歴史版への参照とactive windowの入口だけに変更した。具体的な旧review_textsはsnapshot内に保存し、現在のhard要求には使用しない。coverage evaluatorとannotationは正式なintroduction_schedule.jsonから初出を読み、退役語を新語へalias解決しない。

意味を制約しない10review/教材の容量確認で全2,500窓が成立し、初出込み最低6教材の仮配置が可能。これは数的確認であり、実際の出現や自然さの達成ではない。scheduled以外の自然なprevious語出現も、確認後に実台帳へ数えられる。

## lexical gapの短い検証例

各組2〜3文、合計13文。120〜180어절の教材ではなく、短い用法確認である。Kiwiの形態素証拠・規則検証・語義宣言を分け、モデル注釈を独立した正解とみなさない。이를の이をKiwiがNP/NNBと解析したため、2文の文脈義toothを明示指定し、POS不一致を要レビューとして保存した。名詞の語義を新たに自動推定できたとは扱わない。既存Phase 2と同じ依存を使用し、新しい外部依存は追加していない。

### 이 + 닦다：歯を磨く・物を拭くを씻다へ不自然に置換せず直接表す。

아침에 이를 닦아요.
저는 칫솔로 이를 닦아요.
수건으로 책상을 닦아요.

短例検証：PASS。controlled=100%、未解決・文法違反なし（規則の検査範囲）。検証用仮導入時点K1-207。

### 테이프 + 붙이다：「使う」だけにぼかさず、貼る動作を目的にできる。

종이에 테이프를 붙여요.
친구도 테이프를 붙여요.
테이프로 종이를 책에 붙여요.

短例検証：PASS。controlled=100%、未解決・文法違反なし（規則の検査範囲）。検証用仮導入時点K1-186。

### 던지다 + 공：荷造りへ投げる挿話を加えず、球遊びを小場面の主目的にできる。

친구에게 공을 던져요.
친구가 공을 받아요.

短例検証：PASS。controlled=100%、未解決・文法違反なし（規則の検査範囲）。検証用仮導入時点K1-228。

### 미술관 / 그리다 + 그림：展示・描画を写真だけへ寄せず表現できる。

미술관에서 그림을 봐요.
집에서 그림을 그려요.
그림은 책상 위에 있어요.

短例検証：PASS。controlled=100%、未解決・文法違反なし（規則の検査範囲）。検証用仮導入時点K1-190。

### 가방 / 책 + 들다：移動・所有の別動詞でぼかさず、手で保持・持ち上げる動作を表す。

가방을 들어요.
저는 한 손으로 책을 들어요.

短例検証：PASS。controlled=100%、未解決・文法違反なし（規則の検査範囲）。検証用仮導入時点K1-111。

これで語彙不足の原因を直接補える。元23 conflictの全てが語彙交換だけで消えるわけではなく、無関係な語の固定割当はwindow方式で避ける。stamp義退役により도장不足をK1で解く必要がなくなった。

## 履歴・validator・次の判断

修正前126ファイルをreports/phase2_1_snapshotへSHA-256台帳付きで保存。Phase 1/1.1/1.2/2/2.1のレポート・validation・pilot20本文は元位置でも変更なし。過去freezeの相対パスはsnapshot rootで解決し、過去validator/testsは過去DBに対して動かす。active版のコード・Schemaは更新し、履歴版は書き換えない。

Phase 2.1A validator：PASS、errors=0。Core300、Expansion500、Total800、Tier200/200/100、新5語active、旧5語non-active、Core写真義維持、ID非再利用、語義衝突なし、初出255以前、500語×5window、coverage・32文法不変を検証。

コマンド：`python -B scripts/validate_k1_vocab.py`（active revisionへdispatch）、`python -B scripts/validate_k1_phase2_1A.py --check-examples --json`、`python -B -m unittest discover -s tests -v`。歴史版は`python -B reports/phase2_1_snapshot/scripts/validate_k1_phase2_1.py`。再現は`python -B scripts/build_k1_phase2_1A.py`。旧generatorはactive revision上で上書きを拒否する。

**PASS後、Phase 2.2へ進める。** 保存済みselection.jsonの同じ20番号で比較し、新DBの新出・未導入制約に合わせてsceneとreviewを選び直す。最初の20本文だけを生成する指示ではない。比較対象番号は1,40,85,103,150,170,180,184,189,190,193,234,242,246,252,254,255,276,284,299。本Phaseでは再生成していない。全300本の大量生成は未承認。

Phase 2.2では5組の標準場面の自然さ、들다の語義境界、5〜8reviewと自然なextra出現での実露出、window繰越と締切在庫を確認する。新5語の初出20/33/110/111/127は元20番号に含まれないため、同じ20本文で初出パイロットを済ませたと主張せず、短例検証と既出語としての再利用を分ける。

## 成果物・差分記録

更新：expansion_vocab / id_migration / k2_candidates / expansion_replacement_proposals / introduction_schedule / profile / vocab_review_windows / vocab_exposure_scheduleと対応Schema。Core・文法・固有名詞・lexical exceptionsはbyte単位で維持。

追加：lexical_gap_checks.json、build/validate/report_k1_phase2_1A.py、k1_history.py、Phase 2.1Aテスト、k1_phase2_1A_changes.json、k1_phase2_1A_validation_result.json、本レポート。既存のvalidator・coverage・annotation・履歴ルーティングとテストの参照先を更新。変更前はsnapshotへ保存。

## テスト実行記録

- `python -B -m unittest discover -s tests -v`：PASS、51 tests。
- `python -B -m unittest discover -s tests -p test_k1_phase2_1A.py -v`：PASS、10 tests。
