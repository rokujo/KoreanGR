# Korean K1 vocabulary design — Phase 1

韓国語K1の語彙・文法データの初版です。教材本文は生成していません。
採用判断前の案であり、構造検証の成功は言語品質・学習者の既知率の保証ではありません。

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate_k1_vocab.py
python scripts/validate_k1_vocab.py --json
python -m unittest discover -s tests -v
```

- データ: `config/languages/ko/k1/`
- 設計・変更差分・境界語・要確認点: `reports/k1_vocab_design_report.md`
- 機械検証結果: `reports/k1_vocab_validation_result.json`
- `core_vocab.source.json`: ユーザー原案の語・順序・カテゴリを保存した300エントリ。共通POSと中心義はこのPhaseで付与。
- `core_vocab.json`: 한국を固有名詞台帳へ移し、아니다に置き換えた最小修正候補300語。
- `expansion_vocab.json`: 500語。`category`は配分用、`tags`は教材利用用。両者は別の役割。
- `forms`は活用・異形の例示です。網羅的な形態素解析器や語形許可リストではありません。

再現用の手選定シードは `scripts/build_k1_data.py` にあります。
`python scripts/build_k1_data.py` はJSONとSchemaを再生成して上書きします。
人間レビュー後の修正はシードにも反映してから再生成してください。
`rank`は安定した配列順であり、コーパス頻度順位ではありません。

500語を250本までに2語ずつ導入すると余裕は0枠です。
新出語を本文だけで習得させる場合は99%既知率にも制約があります。
レポートのFを確認し、導入・測定方針を確定してから次Phaseへ進みます。
