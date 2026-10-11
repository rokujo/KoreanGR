# Phase 3.9 停止原因の監査

K1-001〜012をcommitし、K1-013のauthor自己点検ファイルの入力契約違反で停止した。100本のendurance trialは未完了である。

原因は、私が既定のキー名を別名で書いたことである。解析器の構造的誤解析、語彙制限、schedulerの数学的障害による停止ではない。author callbackのメタデータ作成ミスであり、これをKorean analyzer defectと分類しない。

要求キーは `allowed_contract_read` / `content_membership_checked` / `title_checked` / `planned_new_checked` / `known_gaps_checked` / `references_checked`。提出ファイルは `future_vocab_checked` 等の別キーを持っていた。実装は別名を認めず、`StructuralStop('Author self-check missing')` を発生させた。

元のauthorファイル・例外・停止時刻を保存した。K1-013の正式candidateは0件、commitも0件で、ledgerはK1-012のままである。run controlは停止の事実に合わせてadministrative finalizationしたが、exposure ledgerのSHA-256は前後一致する。入力を修正して同runを成功扱いにする操作は行っていない。

次回の狭い再発防止策は、author出力に既定キーのJSONテンプレートをそのまま使用すること。validator / resolver / grammar / vocabulary / review paymentの変更は必要ない。このrunの停止だけからanalyzer研究を再開する根拠はない。

K1-010開始時にも、前教材commitコマンドの完了前にbeginを呼んだoperator順序エラーがあった。sequence guardが正しく拒否し、010への誤creditは発生しなかった。詳細は `k1_phase3_9_operator_ordering_incident.json` に保存した。これもengine故障として数えない。

## 測定上の注意

正式first-passは「preflight修正後の最初の正式candidateがcommitされた割合」。initial preflight findingは「作者の自己点検後、最初に返したdraft」に対する値である。内部自己点検では未導入語などの修正も行っており、rawの最初の文案がすべて適合したという主張はしない。

自己点検を完了したdraftは12本。K1-013は自己点検契約チェックで止まったため、preflight finding率の分母に入れない。完了12本中、findingあり6本（50%）、future findingあり0本（0%）。自動collectorの未監査値はtiming行13本を分母とするため、これを監査時に補正する。

実測時間にはlive authorの推論、ツール操作、ファイル作成、往復の待ち時間が含まれる。純粋な外部LLM API推論時間ではない。100本完走の条件を満たさないため、300本serial推定と正式endurance性能判定は出さない。

025 / 050 / 075 / 100 checkpointには到達していない。checkpointファイルや100本のtrajectoryを捏造しない。
