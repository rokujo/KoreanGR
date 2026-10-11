# Phase 3 retry 停止checkpoint K1-002

生成・commit: 001のみ1本。002のcandidateはreject、停止理由はanalyzer構造的障害（네/ICを너へalias）。

- hard errors（commit済み）0、controlled違反0、previous<98違反0、grammar違反0、unresolved0。
- candidate: 3attempt、reject2。新出実導入2語、actual distinct exposure各1教材、未導入498語。
- review debt0、新規debt0、期限間近0、期限切れ0、selected review0、incidental0。
- naturalness warning1（本人紹介の名前を言う）、semantic確定問題0、natural_expression_gap0。
- genre family1、scene重複の判断はサンプル不足。
- 平均129어절、sentence length distribution {4: 24, 3: 2, 5: 5, 2: 1}。
- 10/20/30/40/50未到達。停止条件発動により次教材は生成しない。

詳細: [最終レポート](k1_phase3_retry_sequential_50_report.md)、[validation JSON](k1_phase3_retry_validation_result.json)。
