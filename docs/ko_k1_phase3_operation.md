# K1 Phase 3の実運用

Phase 2.3の入力と本文は読み取り専用で保持する。Phase 3用profileは
`config/languages/ko/k1/phase3/profile.json`。変更はpreferred文長4→3だけ。
hard minimumはない。自然な2어절文を副詞で引き延ばさない。

本文sourceを1本作る前に、`python -B scripts/k1_phase3.py next`で実stateを取得する。
新出語を軸にsceneを設計し、実導入済み・window内の語から意味上自然な候補を選ぶ。
sourceのreview_candidatesは実現可能性の肯定判断であり、露出実績ではない。
`accept`は候補を順位付けし、本文を解析・hard検証・semantic second passした後、
本文に存在するIDだけをledgerへ反映する。次のsourceはその後に作る。

初出以前の仮想実績は使わない。未導入ExpansionはNに含めた上でhard停止する。
Nは語彙意味単位token、Uは現在初出Expansionのtoken。raw形態素、正規化annotation、
文脈上のsense判定を分離する。解析一致は人間の語義・自然さ承認とは異なる。

reviewは5〜8語のsoft目標。数を満たすための事件・描写・副詞は追加しない。
incidentalも実出現・許可sense・実導入済みである場合だけcreditする。
同一教材の反復は1教材の露出として数える。

各window末端の本文を処理してからwindowを閉じる。未払いなら停止する。
これはPhase 3固有の厳格な停止規則であり、凍結windowの繰越方針は書き換えない。
近期限3教材以内30語超、または10review/教材という数的上界で収容不能なら停止する。
capacityは自然さを保証しない。window未消化は記録され、silent creditはない。

regexはwarning。confirmed semantic issueだけを5教材以内3回のpattern stopへ数える。
scene fingerprintの6field一致/Jaccard平均を直近10教材と比較し、0.85以上の
類似本文3本＋現本文なら停止する。単一カテゴリやsettingの反復だけでは止めない。

10/20/30/40/50にcheckpointを保存する。正常なら人間待ちせず次へ進む。
hard errorや指定stopが出た本文はfailed_attemptsに保存し、以降は生成しない。
050終了でも300本生成へ進まない。
