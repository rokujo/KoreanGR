# GitHub軽量版の保存範囲

リポジトリ: https://github.com/rokujo/KoreanGR

## Git管理するもの

- `config/`: 確定語彙800、文法32、初出予定、review windows、各Schema。
- `scripts/`: generator/controller、解析器、validator、scheduler、レポート処理。
- `tests/`: テストコードと既存の小さなfixture。
- `docs/`: 生成方針・自然さ・各Phase設計。
- `reports/`: 検証結果・レポート・歴史snapshot。レポート内の相対リンクが除外履歴を参照する場合がある。
- README、requirements、Git設定ファイル。

## ローカルにだけ残すもの

`pilot/`（約813MiB）と`state/`（約348MiB）は、今回の初回pushから除外した。生成候補、本文と訳、形態素診断、実ledgerを削除・移動・改変したわけではない。`.gitignore`でGit追跡対象から外しただけである。Git LFSも今回の軽量版では使用しない。

`reports/`内の過去snapshotは小さな歴史DB・コード・fixtureを含むため保存する。ルートの大型pilot/state run履歴とは区別する。

## 再現できる範囲

configの閲覧・Schemaによるデータ検査や、履歴pilotを読まない独立テストを実行できる。ただし既存の`validate_k1_vocab.py`は過去pilotのfreeze照合まで含むため、除外された履歴がないとFAILする。`tests/`を置いていても、全331件の回帰テストやfreeze監査・過去本文の再解析・ledger replayには、Git管理外のpilot/state履歴が必要である。軽量cloneで全suiteや完全なvalidatorが通ると主張しない。テストを無条件skipに変えたり、失敗を成功へ書き換えたりしていない。

完全な再現が必要な場合は、元workspaceの同じ版の`pilot/`と`state/`を別のバックアップから復元する。snapshot/freezeのSHA-256照合を保つため、ファイルのbyte列と相対パスを維持する。今後の小さな独立regression fixtureへの切り出しは別作業として検討する。

## 初回clone

```powershell
git clone https://github.com/rokujo/KoreanGR.git
cd KoreanGR
python -m pip install -r requirements-phase2.txt
python -B -X utf8 -m unittest discover -s tests -p test_lexical_coverage.py -v
```

`.gitattributes`の`* -text`により、Windows/LinuxのcloneでもGitが改行を自動変換しない。これは既存freezeのhash保護のためであり、既存DB・文法・run成果物を変更していない。

## 現状

Phase 3.9aは66/100 commit後、067の`졸리다`登録POSと単文解析POSの不整合で停止。過去runは保存したまま。新しい本生成や300本continuationの承認を、このGitHub公開作業で追加するものではない。
