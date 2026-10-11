# KoreanGR — Korean K1 Graded Reader

非常に簡単な韓国語の大量多読教材を生成するための、語彙・文法・逐次生成・検証の研究プロジェクトです。

- Core 300 / Expansion 500 / Total 800、E1/E2/E3 = 200/200/100。
- 許可文法32、本文120〜180어절、一文hard max10어절。
- controlled vocabulary coverage 100%、previous vocabulary coverage hard98% / target99%。
- sentence-local canonical解析、candidate gate、atomic commit、flexible review windowsを使用。
- semantic grammarの意味role分類はdiagnosticであり、productionのhard gateではありません。

最新のPhase 3.9aは66/100本commit後、K1-067の`졸리다`登録POSと解析POSの不整合で停止しました。判定はD / STRUCTURAL_FAIL。全300本の量産はまだ行っていません。

詳細は [最新レポート](reports/k1_phase3_9a_production_001_100_report.md)、[検証結果](reports/k1_phase3_9a_validation_result.json)、[contract retry設計](docs/ko_k1_phase3_9a_run_design.md)を参照してください。

## GitHub軽量版

コード・確定DB・docs・reports・テストコードを保存しています。大きな生成/解析履歴の`pilot/`と実ledgerの`state/`はGit管理外です。元workspaceの履歴は削除していません。

**既存の語彙validatorも過去pilotのfreeze照合を含むため、履歴なしではFAILします。全回帰テスト・過去run再生にも、別途pilot/state履歴が必要です。** 軽量cloneだけで全331件や完全なvalidatorが通るとは保証しません。保存範囲と復元方法は [GitHub保存方針](docs/github_repository.md)にあります。

```powershell
python -m pip install -r requirements-phase2.txt
python -B -X utf8 -m unittest discover -s tests -p test_lexical_coverage.py -v
```

`config/`にDB・Schema・予定表、`scripts/`にvalidator/generator/scheduler、`tests/`にテスト、`docs/`に設計、`reports/`に各Phaseの検証結果を置いています。

以下は過去Phaseの操作記録です。過去のbuild/generatorを現行DBやfreeze成果物へ無条件に適用しないでください。

## Phase 2.1Aの記録

現行DBはCore300 / Expansion500 / Total800、E1/E2/E3=200/200/100、文法32。5交換を正式採用し、新ID0808〜0812を採番しました。次のIDは0813。Coreの찍다/take_photoは維持し、stamp義だけを退役させました。

```powershell
python -B scripts/validate_k1_vocab.py
python -B scripts/validate_k1_phase2_1A.py --check-examples --json
python -B -m unittest discover -s tests -v
python -B scripts/build_k1_phase2_1A.py
```

詳細は [Phase 2.1Aレポート](reports/k1_phase2_1A_vocab_revision_report.md)、検証結果は [validation JSON](reports/k1_phase2_1A_validation_result.json) を参照してください。13文の短い用法例のみ追加し、20本文の再生成は行っていません。PASS後に保存済みの同じ20教材番号でPhase 2.2比較へ進めます。全300本の大量生成は未承認です。

初出は `introduction_schedule.json` を正式入力とします。最終初出255、256〜300は新出0。reviewは `vocab_review_windows.json` の柔軟な窓で選び、5〜8語をsoft目標とします。categoryはsoft distributionです。coverageはcontrolled hard100%、previous hard98% / target99%を維持。`들다`は手に持つ・持ち上げる義だけで、同lemmaの他義を自動許可しません。

修正前126ファイルは `reports/phase2_1_snapshot/` にSHA-256台帳付きで保存しました。元のPhase 1〜2.1レポート・validation・20本文も変更していません。旧freezeの相対パスはsnapshot rootで解決します。履歴検証は以下の読取専用コマンドで行います。

```powershell
python -B reports/phase2_1_snapshot/scripts/validate_k1_vocab.py
python -B reports/phase2_1_snapshot/scripts/validate_k1_phase2_1.py
```

active `vocab_exposure_schedule.json` は歴史版への参照だけを保存し、具体的なreview_textsをhard要求にしません。旧generator・旧レポート再生成コマンドは現行DBで上書きを拒否します。既存テストは歴史DBへ明示的に固定し、Phase 2.1Aテストは現行DBを検証します。旧Schemaと旧コードはsnapshot内で保持しています。

以下はPhase 1.2時点の操作説明です。過去の再生成コマンドは現行データへ適用しないでください。

## Phase 1.2の記録

韓国語K1のCore 300・Expansion 500と、300教材分の導入・再遭遇計画です。7組の入替を正式採用し、500語それぞれを初出込み6つの異なる教材へ配置しました。教材本文は生成していません。

```powershell
python -m pip install -r requirements-dev.txt
python -B scripts/validate_k1_vocab.py
python -B scripts/validate_k1_vocab.py --json
python -B -m unittest discover -s tests -v
python -B scripts/audit_phase1_2_changes.py --run-tests
python -B scripts/audit_phase1_1_changes.py
```

データは `config/languages/ko/k1/`、詳細は `reports/k1_vocab_design_report_phase1_2.md`、検証結果は `reports/k1_vocab_validation_result_phase1_2.json` にあります。全ファイル差分は `reports/k1_vocab_changes_phase1_2.json` と同名 `.patch` に保存します。

- `core_vocab.json`: 한국を予算外の固有名詞へ移し、아니다を採用した300語。原案は `core_vocab.source.json` に保存。
- `expansion_vocab.json`: 確定500語。E1/E2/E3は200/200/100。categoryは配分用、tagsは教材用途用。
- `id_migration.json`: 旧7 IDを永久欠番にし、新ID0801〜0807を採番した対応台帳。rankは旧スロットを維持。IDとrankは独立です。次の新IDは0808。
- `k2_candidates.json`: 外した7語の候補記録のみ。K2語彙DBは設計していません。
- `expansion_replacement_proposals.json`: 入替の採用履歴。active語彙へ重ねて結合しません。
- `introduction_schedule.json`: 全300本の初出配置。新出最大2、全語の初出は255本目まで。001〜275の許可期間には550枠中50枠の余裕があります。
- `vocab_exposure_schedule.json`: 全500語の初出・review教材番号、全300本の負荷・Tier別統計。予定であり、実際の出現実績ではありません。
- `grammar.json`: 32項目。固有名詞・定型句は別台帳で許可範囲を制御。

`controlled_vocab_coverage_hard_min=1.0` は許可・導入時点を満たす語彙tokenの割合です。`previous_vocab_coverage_hard_min=0.98` / `previous_vocab_coverage_target=0.99` は当該教材より前に導入済みのtokenの割合です。学習者が覚えているかは推定しません。

Nは正規化した語彙token総数、Uは当該教材で初出するExpansionのtoken総数。助詞・語尾・許可文法機能・句読点はNから除き、未解決語や許可外語は除かずエラーにします。controlled coverageの成立後、previous coverageは `(N-U)/N`。新出tokenのhard上限は `floor(N/50)`、soft maximumは総数3です。詳しいspan規則・複合語の扱いはprofileとレポートを参照してください。

`scripts/lexical_coverage.py` はID・文法機能を確定済みの注釈tokenを検査する関数です。韓国語の生テキスト解析器は実装していません。本文試作時には語義・形態素・定型spanの照合が必要です。formsも活用例であり、網羅的な表層形許可リストではありません。

`python -B scripts/build_k1_data.py` は手選定シードからJSON・Schema・予定表を再生成します。人間が変更するときはシードも更新してください。Tier変更でIDを振り直さず、意味を入れ替えるときは旧IDを退役させて新IDを作ります。

Phase 1の17ファイルとPhase 1.1の22ファイルをSHA-256台帳付きで `reports/phase1_snapshot/` と `reports/phase1_1_snapshot/` に保存しています。旧レポート・旧validator・旧テストは保持。履歴監査は保存版validatorを保存版データに対して実行し、過去の結果を上書きしません。
