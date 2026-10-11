# Phase 2 pilot

確定入力は `config/languages/ko/k1/` を読み取り専用として扱います。freeze台帳は `reports/k1_phase2_input_freeze.json`。既存のPhase 1.2成果物・スクリプト・テストは変更していません。

20本の本文・訳・annotationは `texts/K1-xxx.json`、手書きシードは `authored_scenes.json`、データから選んだ番号と理由は `selection.json`。全300本を生成する実装ではありません。

```powershell
python -m pip install -r requirements-phase2.txt
python -B scripts/select_k1_pilot.py
python -B scripts/build_k1_pilot.py
python -B scripts/validate_k1_pilot.py --save
python -B scripts/report_k1_pilot.py
python -B -m unittest discover -s tests -v
```

validatorは予定語の省略をFAILとして終了コード1を返します。23件の移動案は提案のみで、元scheduleは維持しています。語彙・文法・長さのhard検査はannotation仮説を前提にしており、自然さ・語義・訳には人間レビューが必要です。
