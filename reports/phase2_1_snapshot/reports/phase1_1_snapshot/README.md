# Korean K1 vocabulary design — Phase 1.1

韓国語K1の語彙・文法データへPhase 1.1の人間レビューを反映しました。
Coreの한국予算外移動と아니다採用は確定です。Expansionの入替7組は提案段階で、現行500語を保持しています。
構造検証の成功は言語品質・学習者の既知率の保証ではありません。教材本文は生成していません。

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate_k1_vocab.py
python scripts/validate_k1_vocab.py --json
python -m unittest discover -s tests -v
python scripts/audit_phase1_1_changes.py
```

- データ: `config/languages/ko/k1/`
- 現行設計・全差分・入替案・要確認点: `reports/k1_vocab_design_report_phase1_1.md`
- 現行機械検証結果: `reports/k1_vocab_validation_result_phase1_1.json`
- JSONフィールド差分・ファイルハッシュ: `reports/k1_vocab_changes_phase1_1.json`
- 全変更ファイルのテキスト差分: `reports/k1_vocab_changes_phase1_1.patch`
- Phase 1の17ファイルとSHA-256台帳: `reports/phase1_snapshot/`。旧validator・旧テストも保存し、旧仕様で実行可能。
- 旧設計レポートと検証結果は元の`reports/k1_vocab_design_report.md` / `reports/k1_vocab_validation_result.json`にも保持。
- `core_vocab.source.json`: ユーザー原案の語・順序・カテゴリを保存した300エントリ。共通POSと中心義はこのPhaseで付与。
- `core_vocab.json`: 한국を固有名詞台帳へ移し、아니다を正式採用した300語。
- `expansion_vocab.json`: 500語。`category`は配分用、`tags`は教材利用用。両者は別の役割。
- `forms`は活用・異形の例示です。網羅的な形態素解析器や語形許可リストではありません。
- `expansion_replacement_proposals.json`: 現行予算外の7組の入替提案。未採用。語彙DBへ結合しない。
- `introduction_schedule.json`: 全300本分の初出配置可能性の証拠。本文・再遭遇計画・確定カリキュラムではありません。

再現用の手選定シードは `scripts/build_k1_data.py` にあります。
`python scripts/build_k1_data.py` はJSONとSchemaを再生成して上書きします。
人間レビュー後の修正はシードにも反映してから再生成してください。
既存のID・rank・lemma+POS+senseはすべて維持しました。
Tierを変更してもID・rankを振り直しません。優先度はtierを使用します。rankは頻度順位や現行Tier順位ではありません。

001〜275は500語に対して550枠、余裕50枠です。
配置例は期間内に新出0語10本・1語30本・2語235本を分散し、276〜300は新出0です。
既知率はhard 98%、target 99%。初出教材の新出語token総数は原則3以下（各語3回ではありません）。
新出語の大量反復は初出回で行わず、後続の最低5つの別教材で再遭遇させます。
比率とtoken方針は今回データ設計までを検証しており、実際の本文や学習者の知識を測定したものではありません。
