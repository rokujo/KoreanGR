# K1 candidate gate（Phase 3.1）

Phase 3の失敗runは保持する。Phase 3.1は独立したrunで、smokeは001のみ。
Core300・Expansion500・grammar32・初出・window・sense・coverageを変更しない。

1. committed stateからallowed snapshotを作る。Core300、実導入済みExpansion、
   当該教材の新出0〜2、登録固有名詞、固定exceptionだけを渡す。
2. snapshotのlemma/POS/senseと活用hintを見てsceneとcandidateを作る。
3. sentenceごとに未来語・未知語・文法境界をprecheckする。文単位に本文全体の
   coverage・120語下限を課さない。全文でも独立に再解析・permission・coverageを検証する。
4. candidateのhard FAILはrejectし、診断をgenerator callbackへ返す。標準最大3attempt。
   callbackは別scene・視点・省略・許可表現への修正、または再生成を選べる。
5. 全hard条件PASS、自然さsecond pass、最終raw再解析後にだけcommitする。

controlled100%、previous98%、新出2lemma、grammar32、120〜180어절、
一文hard10、future/retired/unresolved禁止は維持する。99% missはblockerではない。
draft目標130〜150。長さ修正は同じ目的の行動・必要な会話・問題解決の過程。
副詞の埋め草を足さない。自然に延ばせなければ再生成する。

candidateは`candidates/`、rejectは`failed_attempts/`へ保存。
snapshotとcandidate journalは露出実績ではない。snapshotには生成前state checksumがあり、
stale candidateや改ざん候補をcommitできない。future等は`invalid_usage_ids`に入り、
`incidental_previous_vocab_ids`には実permissionを通ったprevious Expansionだけが入る。

## 限定resolver

걷다/walkが登録・許可済みで、surfaceが列挙した正規活用で、生成intentが一致し、
locomotion scene・登録場所＋到達/場所助詞・人との同行・目的語なしをすべて満たす時だけ、
걸-のraw解釈を걷다候補へ正規化する。raw stream、元annotation、各判断根拠は残す。
`걸어요=걷다`というaliasはない。`가방을 벽에 걸어요`は目的語でveto。
意図だけ・経路だけ・同行だけでは足りない。保守的なので正しい歩行文もREVIEWになり得る。

形態素hintは別overlay。語彙DBのforms/senseを変更しない。
도와주다等は登録compoundの厳密なraw prefixだけをgroupし、後続助動詞の文法境界は保つ。
Standalone 돕다を新規許可しない。監査の全語許可fixtureを実初出へ混ぜない。

## Transaction / crash recovery

authoritative ledgerはcommitted record、導入、露出、debt payment、genre/scene履歴を含む
単一JSON。OS writer lock下でfinal reanalysis後、同じvolume上の一時ファイルをfsyncし、
`os.replace`で一度に公開する。`texts/`はこのstateから復元できるprojection。
publish前の失敗はcreditなし。publish後のprojection失敗はrecoverで復元し、
同じcommit_idの再実行ではcreditを増やさない。異なるcandidateの二重commitは拒否する。
OS process-crash安全性をテストする。ディスク故障・電源断まで完全に保証したとは扱わない。

candidate stageではexposure ledgerをbyte単位で不変にする。retry件数は別journalから数える。
最大retry超過、snapshot/初出矛盾、analyzer構造障害、state corruption等でrun停止する。
実露出6教材への数学的可能性は残りの異なる教材数で確認する。
review 5〜8soft目標をhard capacityへ読み替えない。

smoke generatorはPhase 3の失敗を意図的に再生し、future修正→length修正のfeedbackを使う
決定的callback。candidate gateの安全性を示すもので、任意のLLMが常に3回で直せる証明ではない。
自然さのモデルsecond passは人間承認ではない。
