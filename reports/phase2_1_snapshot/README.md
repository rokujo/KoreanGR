# Korean K1 vocabulary design — Phase 1.2

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
