# K1 Phase 3.2 — 解析器堅牢化 / 001→002 smoke

**判定: A / Phase 3.2 PASS。** 001と002を実績ゼロの別runで順に検証し、hard PASS後だけcommitした。K1-003以降、50本生成、300本量産は実施していない。

## 原因・修正方法

旧ALIASESの`네 → 너`とPOS不一致の唯一候補fallbackが、raw IC yesをCore pronounへ誤変換していた。新versionではglobal aliasを使わず、raw POS・登録identity・局所contextを照合する。ICの明確な応答は `네 / interjection / yes / ko_k1_0442`、裸の所有用法候補はREVIEW、MMのnative数詞は넷へ区別する。

全12aliasの分類はPOS条件付き7、context条件付き4、削除1、無条件safe0。旧default sense14件を無条件適用せず、同形lemma13組のPOS/sense境界を監査した。詳細は [alias監査](k1_phase3_2_alias_audit.md) とJSONのraw evidence。

밥하고もsurfaceでcompound化しない。food列挙＋第2目的語＋predicateの根拠が揃う場合だけ名詞＋grammar25へ再分割する。根拠の薄い `밥하고 먹어요.` はREVIEW。하다 compound、registered exchange、VV＋auxiliary、counter、引用・句読点を個別に監査した。이랑/랑や新文法を許可していない。

## Freeze・versioning

過去466ファイルのhash違反0件。Phase 3 retryのcommitted001、failed002、ledger/run state/report、Phase 3.1 gate/限定resolver、正式Core300＋Expansion500、文法32、初出・review windows・ID migration・自然さguidelinesは変更していない。

新しい3ファイル `k1_phase3_2_analysis.py` / `resolver.py` / `gate.py` を作った。gateは承認済み3.1を別versionへ複製し、hard条件・planned identity比較・final reanalysis・atomic transactionを維持した。差分は新解析器の選択、max5attempt、smoke上限002、schemaの別path、phase表示3.2、engine hashをinput digestへ追加。wrapperでは前runと同じ2回停滞stopも維持する。

旧raw candidate sourceを対照入力に再使用したが、旧annotation、旧coverage、旧露出・stateは流用していない。これは不自然さを避けるために本文を作り直したテストではなく、同じ問題入力を修正後analyzerで解決する回帰smoke。001の初稿は旧123어절版であり、旧runのcommitted129어절版を上書きしていない。

## Smoke結果

|教材|attempt|어절|max文|N|U|controlled|previous|
|---|---:|---:|---:|---:|---:|---:|---:|
|K1-001|1|123|5|121|2|100%|98.347107%|
|K1-002|1|135|5|130|2|100%|98.461538%|

両本文ともfuture0、invalid0、unresolved content0、grammar32外0、planned new IDsとactual new IDs一致。001/002各1attemptでcommit。両方の99%target missは設計上予想され、hard98%を満たすためblockerではない。初稿target130〜150はsoftで、001の123は固定regression sourceを検証する目的で使用し、fillerで引き延ばしていない。

## Planned ID / surface / resolved identity

|教材|planned ID|lemma|POS|sense|実annotation surface|
|---|---|---|---|---|---|
|001|ko_k1_0373|되다|verb|become|돼|
|001|ko_k1_0413|괜찮다|adjective|okay|괜찮|
|002|ko_k1_0442|네|interjection|yes|네|
|002|ko_k1_0443|아니요|interjection|no_polite|아니요|

002の네にはraw `IC`が保存されており、Core 너への誤aliasはない。planned_new_not_present gateはそのまま維持し、ネを너へ故意に変えた対照candidateはrejectするtestもPASS。

## coverage再計算

旧failed002: N=130、U=1、機械値controlled100%、previous=99.230769%。この値は間違ったidentityを前提としていたため採用しない。修正後にrawから再解析するとN=130、U=2、previous=(130−2)/130=98.461538%。controlledも登録identity照合後に100%と再計算した。

Nは本文のlexical annotation token数（Core / Expansion / registered proper name / frozen exception / unknownを各tokenとして計数）。grammar function・句読点は除外する。Uは当該本文のplanned new Expansion IDに対応する実token数。同一語を反復すればtoken回数分Uへ加算する。異なる教材の露出creditとは別の計数。

## State integrity / transaction

新ledger `state/phase3_2_smoke_exposure_ledger.json` はepoch2、last_committed_text2、actual導入4語、異なるvocab/text露出4。旧run ledgerからの初期credit0。candidate評価前後のledger SHA一致、最終再解析一致、001/002のcredit各1回。validator実行前後もstate byte不変。incidental0、review debt0、expired0（初回review windowはまだ開いていない）。

実smokeのreject数0。別temp-state testsではfailed candidate、future、retired、予定identity不一致をrejectし、actual intro/exposure/debt/historyにcreditしないことを確認した。atomic publish前のcrashは状態不変、publish後crashはprojectionを復旧して二重creditなし。003はschema/gate双方で拒否する。

## Regression / validator

最終全体tests: 169件 PASS、failures=0、errors=0。最終focused suite 22件もPASS（full開始後に追加した旧neバグ注入1testを含む）。新suiteに33対照fixture、凍結Phase 2.3からの8文、3.1不規則活用28probeを含む。全体suiteは既存Phase1〜3.1/retryの検証も含む。詳細は `k1_phase3_2_all_test_log.txt` / `focused_test_log.txt` / `test_result.json`。

PowerShellのnative stderrリダイレクトでは終了statusとunittest summaryが一致しなかったため、Python runnerが結果とUTF-8 logを明示管理する方式で最終suiteを再実行した。採用結果はこのrunnerのstructured resultのみ。

validator errors: 0。freeze violations0。controlled違反0、previous<98違反0、grammar violations0、future0、invalid0、unresolved0。parser対照fixtureのREVIEWは期待された保守的判定であり、committed教材のunresolvedを許可するものではない。

## 限界と次の判断

完全な形態素・sense解析器ではない。単独の네 책、文脈の薄い눈/풀、raw POSと意味が食い違う약이 써요などはREVIEWで止める。新解析器はfalse positiveを防ぐためfalse negativeを許容し、モデルannotationを独立正解にしていない。自然さwarningは1件、日本語訳lint flagは0件。本人が教師へ名前を伝える文のwarningは「呼ぶ」の代用ではない。自己semantic reviewは人間承認の代替ではない。

辞書に未登録の別義までraw POSだけで完全に検出できるわけではない。restricted senseの文脈確認とsemantic second passは引き続き必要。同POS homographの限定context規則も汎用辞書の代替ではなく、より広い文脈が必要な正しい用例をREVIEWにする可能性がある。

**次は別runでK1-001〜050の連続逐次試験を再実施可能。** このsmokeの成功は50本のdebt/scene/genre成立や300本量産の証明ではない。今のrunは002で完了し、そのまま003へ継続しない。

## Smoke本文（人間レビュー用）

### K1-001 — 동생하고 학교에 가요

오늘은 동생하고 학교에 가요. 동생은 오늘 학생이 돼요. 동생은 아침에 일찍 일어나요. 저는 동생하고 아침을 먹어요. 아버지도 우리하고 밥을 먹어요. 동생은 밥하고 우유를 좋아해요.

아침을 먹고 동생은 씻어요. 저는 동생 가방을 봐요. 가방 안에 책이 있어요. 책 옆에 공책도 있어요. 동생은 가방에 우산을 넣어요. 오늘은 하늘에 해가 있어요.

하지만 저녁에는 비가 올 거예요. 우리는 집 밖으로 나가요. 학교는 우리 집 앞에 있어요. 학교 앞에 사람이 많아요. 동생은 제 옆에 서요. 동생은 선생님을 만나고 싶어요.

우리는 학교 안으로 들어가요. 교실 문 앞에 선생님이 있어요. 선생님은 동생에게 학교 이야기를 해요. 동생은 선생님에게 이름을 말해요. 선생님은 동생하고 교실에 들어가요. 교실 안에 학생이 많아요.

동생은 선생님 옆에 앉아요. 저는 동생을 보고 웃어요. 동생은 괜찮아요. 저는 학교에서 집으로 돌아가요. 아버지가 집에서 저를 기다려요. 저는 아버지에게 학교 이야기를 해요.

日本語訳:

今日は弟と学校へ行きます。 弟は今日、学生になります。 弟は朝早く起きます。 私は弟と朝ご飯を食べます。 父も私たちとご飯を食べます。 弟はご飯と牛乳が好きです。

朝ご飯を食べて、弟は顔や体を洗います。 私は弟のかばんを見ます。 かばんの中には本があります。 本の隣にはノートもあります。 弟はかばんに傘を入れます。 今日は空に太陽が出ています。

でも夕方には雨が降る予定です。 私たちは家の外へ出ます。 学校は私たちの家の前にあります。 学校の前には人がたくさんいます。 弟は私の隣に立ちます。 弟は先生に会いたがっています。

私たちは学校の中へ入ります。 教室のドアの前に先生がいます。 先生は弟に学校の話をします。 弟は先生に名前を伝えます。 先生は弟と教室に入ります。 教室の中には学生がたくさんいます。

弟は先生の隣に座ります。 私は弟を見て笑います。 弟は大丈夫です。 私は学校から家へ戻ります。 父が家で私を待っています。 私は父に学校の話をします。

### K1-002 — 도서관에서 책을 읽어요

오늘은 학교 도서관에 가요. 수업이 끝나고 책을 읽고 싶어요. 도서관 안에 학생이 많아요. 저는 창문 옆에 앉아요. 가방에서 책을 찾고 있어요. 책은 공책 아래에 있어요.

저는 가방을 열고 책을 찾아요. 선생님도 도서관 안에 있어요. 선생님이 제 옆에 앉아요. 선생님은 저에게 말해요. “책이 있어요?” 저는 선생님에게 말해요.

“네, 가방 안에 있어요.” 저는 선생님에게 책을 줘요. 선생님은 제 책을 봐요. 책에는 이야기가 많이 있어요. 저는 책을 읽어요. 하지만 책이 너무 어려워요.

모르는 말이 많이 있어요. 선생님이 저에게 다시 말해요. “책이 재미있어요?” 저는 선생님에게 답을 해요. “아니요, 책이 너무 어려워요.” 선생님은 쉬운 책을 찾아요.

저는 선생님에게 책을 받아요. 저는 선생님이 주는 책을 읽어요. 이야기가 쉽고 재미있어요. 저는 책을 보고 웃어요. 책을 읽고 선생님에게 말해요. “내일도 도서관에서 읽고 싶어요.”

저는 책을 가방에 넣어요. 도서관 밖에서 친구를 만나요. 친구도 도서관에 가고 싶어요. 내일은 친구하고 책을 읽을 거예요. 친구하고 집에 돌아가요.

日本語訳:

今日は学校の図書館へ行きます。 授業が終わって、本を読みたいです。 図書館の中には学生がたくさんいます。 私は窓の隣に座ります。 かばんの中で本を探しています。 本はノートの下にあります。

私はかばんを開けて本を探します。 先生も図書館の中にいます。 先生が私の隣に座ります。 先生は私に話しかけます。 「本はありますか？」 私は先生に答えます。

「はい、かばんの中にあります。」 私は先生に本を渡します。 先生は私の本を見ます。 本には話がたくさん載っています。 私は本を読みます。 でも本が難しすぎます。

知らない言葉がたくさんあります。 先生が私にもう一度話しかけます。 「本は面白いですか？」 私は先生に返事をします。 「いいえ、本が難しすぎます。」 先生は易しい本を探します。

私は先生から本を受け取ります。 私は先生がくれる本を読みます。 話が易しくて面白いです。 私は本を見て笑います。 本を読んで、先生に話します。 「明日も図書館で読みたいです。」

私は本をかばんに入れます。 図書館の外で友達に会います。 友達も図書館へ行きたがっています。 明日は友達と本を読む予定です。 友達と家へ戻ります。
