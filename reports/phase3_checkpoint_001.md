# Phase 3 checkpoint K1-001

逐次確定本文 0 本。停止状態: stopped。

過去実績はこのrunの本文だけ。未導入400語等の0回を失敗と扱わない。99% target missはhard failureではない。

| 指標 | 結果 |
|---|---|
| generated_texts | 0 |
| hard_errors | 0 |
| controlled_violations | 0 |
| previous_below_98 | 0 |
| grammar_violations | 0 |
| unresolved_content_words | 0 |
| introduction_conflicts | 0 |
| semantic_schedule_conflicts | 0 |
| new_vocabulary_introduced | 0 |
| planned_introductions | 0 |
| actual_selected_review_exposures | 0 |
| incidental_exposures | 0 |
| actual_exposure_distribution | {0: 500} |
| introduced_exposure_distribution | {} |
| total_outstanding_debt | 0 |
| debt_approaching_deadline | 0 |
| expired_debt | 0 |
| defer_events | 0 |
| naturalness_warning_categories | {} |
| semantic_review_flags | 0 |
| natural_expression_gaps | [] |
| genre_distribution | {} |
| scene_similarity_max | 0 |
| scene_extreme_similarity_pairs | [] |
| mean_eojeol | None |
| min_eojeol | 0 |
| max_eojeol | 0 |
| sentence_length_distribution | {} |
| preferred_sentence_compliance | None |
| hard_max_violations | 0 |
| previous_coverage_min | None |
| previous_coverage_mean | None |
| target_99_misses | 0 |
| new_review_debt_events_last_10 | 0 |

## 停止した本文試行

確定実績のhard errors 0は本文PASSを意味しない。001の失敗試行は8エラーメッセージ、controlled違反1・previous<98違反1・未解決内容語1・119어절。実ledgerにcreditなし。002以降は生成していない。詳細はk1_phase3_sequential_50_report.md。
