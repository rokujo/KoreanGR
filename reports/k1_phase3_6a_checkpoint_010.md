# Phase 3.6a checkpoint K1-010

commit 10, status PRODUCTION_READY_FOR_50


```json
{
  "phase": "3.6a",
  "verdict": "A",
  "status": "PRODUCTION_READY_FOR_50",
  "completed": true,
  "committed_count": 10,
  "stop": null,
  "artifact_integrity_errors": [],
  "ledger_replay_errors": [],
  "state_epoch": 10,
  "committed_hard_errors": 0,
  "rejected_attempt_count": 8,
  "candidate_hard_error_distribution": {
    "unknown_or_unresolved": 10,
    "unresolved_context_ambiguity": 4,
    "coverage_or_token_policy": 24
  },
  "first_attempt_pass_count": 3,
  "structural_scope_mismatch_count": 0,
  "resolved_scope_mismatch_count": 2,
  "ne_recovery_count": 2,
  "first_attempt_pass_ratio": 0.3,
  "attempts_per_committed_text": [
    2,
    3,
    2,
    1,
    3,
    1,
    1,
    2,
    2,
    2
  ],
  "mean_attempts": 1.9,
  "total_candidate_attempts": 19,
  "future_contaminated_candidate_count": 0,
  "future_usage_occurrences": 0,
  "future_in_committed": 0,
  "unknown_unresolved_in_committed": 0,
  "planned_identity_mismatch_in_committed": 0,
  "semantic_grammar_warnings": 111,
  "semantic_warning_distribution": {
    "REVIEW": 106,
    "FAIL": 5
  },
  "naturalness_warnings": 4,
  "naturalness_warning_distribution": {
    "nat_reference_clarity": 2,
    "nat_restricted_sense": 2
  },
  "confirmed_language_quality_issues": 0,
  "translation_fidelity_flags": 0,
  "review_debt": [
    {
      "vocab_id": "ko_k1_0446",
      "window_index": 1,
      "window": {
        "from": 10,
        "to": 28
      }
    },
    {
      "vocab_id": "ko_k1_0476",
      "window_index": 0,
      "window": {
        "from": 10,
        "to": 13
      }
    }
  ],
  "expired_review_debt": [],
  "near_deadline_debt": [],
  "selected_review_exposures": 20,
  "incidental_exposures": 5,
  "actual_new_introduced": 20,
  "actual_exposure_distribution": {
    "2": 8,
    "1": 4,
    "0": 480,
    "3": 7,
    "4": 1
  },
  "genre_distribution": {
    "weather": 1,
    "short_dialogue": 1,
    "shopping": 1,
    "transport": 1,
    "food": 1,
    "home": 1,
    "school": 1,
    "small_problem": 1,
    "family": 1,
    "simple_hobby": 1
  },
  "scene_similarities": [
    {
      "a": 2,
      "b": 1,
      "score": 0.16666666666666666
    },
    {
      "a": 3,
      "b": 1,
      "score": 0.05555555555555555
    },
    {
      "a": 3,
      "b": 2,
      "score": 0.05555555555555555
    },
    {
      "a": 4,
      "b": 1,
      "score": 0.16666666666666666
    },
    {
      "a": 4,
      "b": 2,
      "score": 0.16666666666666666
    },
    {
      "a": 4,
      "b": 3,
      "score": 0.05555555555555555
    },
    {
      "a": 5,
      "b": 1,
      "score": 0.041666666666666664
    },
    {
      "a": 5,
      "b": 2,
      "score": 0.041666666666666664
    },
    {
      "a": 5,
      "b": 3,
      "score": 0.1111111111111111
    },
    {
      "a": 5,
      "b": 4,
      "score": 0.041666666666666664
    },
    {
      "a": 6,
      "b": 1,
      "score": 0.041666666666666664
    },
    {
      "a": 6,
      "b": 2,
      "score": 0.041666666666666664
    },
    {
      "a": 6,
      "b": 3,
      "score": 0.041666666666666664
    },
    {
      "a": 6,
      "b": 4,
      "score": 0.041666666666666664
    },
    {
      "a": 6,
      "b": 5,
      "score": 0.08333333333333333
    },
    {
      "a": 7,
      "b": 1,
      "score": 0.041666666666666664
    },
    {
      "a": 7,
      "b": 2,
      "score": 0.041666666666666664
    },
    {
      "a": 7,
      "b": 3,
      "score": 0.041666666666666664
    },
    {
      "a": 7,
      "b": 4,
      "score": 0.041666666666666664
    },
    {
      "a": 7,
      "b": 5,
      "score": 0.03333333333333333
    },
    {
      "a": 7,
      "b": 6,
      "score": 0.03333333333333333
    },
    {
      "a": 8,
      "b": 1,
      "score": 0.05555555555555555
    },
    {
      "a": 8,
      "b": 2,
      "score": 0.05555555555555555
    },
    {
      "a": 8,
      "b": 3,
      "score": 0.16666666666666666
    },
    {
      "a": 8,
      "b": 4,
      "score": 0.05555555555555555
    },
    {
      "a": 8,
      "b": 5,
      "score": 0.1111111111111111
    },
    {
      "a": 8,
      "b": 6,
      "score": 0.041666666666666664
    },
    {
      "a": 8,
      "b": 7,
      "score": 0.041666666666666664
    },
    {
      "a": 9,
      "b": 1,
      "score": 0.041666666666666664
    },
    {
      "a": 9,
      "b": 2,
      "score": 0.041666666666666664
    },
    {
      "a": 9,
      "b": 3,
      "score": 0.041666666666666664
    },
    {
      "a": 9,
      "b": 4,
      "score": 0.041666666666666664
    },
    {
      "a": 9,
      "b": 5,
      "score": 0.08333333333333333
    },
    {
      "a": 9,
      "b": 6,
      "score": 0.08333333333333333
    },
    {
      "a": 9,
      "b": 7,
      "score": 0.03333333333333333
    },
    {
      "a": 9,
      "b": 8,
      "score": 0.041666666666666664
    },
    {
      "a": 10,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 10,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 10,
      "b": 3,
      "score": 0.03333333333333333
    },
    {
      "a": 10,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 10,
      "b": 5,
      "score": 0.06666666666666667
    },
    {
      "a": 10,
      "b": 6,
      "score": 0.027777777777777776
    },
    {
      "a": 10,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 10,
      "b": 8,
      "score": 0.03333333333333333
    },
    {
      "a": 10,
      "b": 9,
      "score": 0.027777777777777776
    }
  ],
  "max_scene_similarity": 0.16666666666666666,
  "eojeol_distribution": {
    "n": 10,
    "min": 125,
    "max": 170,
    "mean": 137.1,
    "median": 130.5,
    "p90": 157
  },
  "sentence_length_distribution": {
    "4": 212,
    "1": 5,
    "3": 55,
    "5": 58,
    "2": 7,
    "6": 7,
    "7": 1
  },
  "preferred_sentence_ratio": 0.9652173913043478,
  "production_wall_seconds": 1294.9310841000042,
  "per_text_seconds": {
    "n": 10,
    "min": 86.58579620000091,
    "max": 214.56055500000366,
    "mean": 128.30100954000082,
    "median": 114.90289805000066,
    "p90": 163.62730820000434
  },
  "stage_seconds": {
    "scene_planning": 470.1223413000189,
    "author_draft": 408.5818893000178,
    "morphology_vocab_analysis": 21.41865870001493,
    "mechanical_validation": 3.726353999969433,
    "retry_repair": 171.6247485000058,
    "naturalness_review": 181.36642089999077,
    "final_reanalysis": 11.639623900002334,
    "commit": 7.461881399991398,
    "controller_overhead": 7.0681773999967845
  },
  "estimated_300_mean_hours": 10.691750795000068,
  "estimated_300_median_hours": 9.575241504166721,
  "attempted_text_count": 10,
  "attempts_per_attempted_text": [
    2,
    3,
    2,
    1,
    3,
    1,
    1,
    2,
    2,
    2
  ],
  "semantic_warnings_all_candidates": 215,
  "failed_attempt_state_unchanged": true,
  "unassigned_between_text_seconds": 11.920988699996087,
  "estimated_300_serial_hours": {
    "estimated_300_mean_hours": 10.691750795000068,
    "estimated_300_median_hours": 9.575241504166721
  },
  "performance": "GREEN",
  "pre_run_regression": {
    "tests": 286,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 126.77304819999699,
    "success": true
  },
  "post_run_regression": {
    "tests": 286,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 115.15888239999913,
    "success": true
  },
  "largest_pipeline_stage": "scene_planning",
  "speed_optimization_target": "generator/author: scene planning, constrained draft and localized repair; validator is not the primary cost",
  "total_attempts": 19,
  "frozen_history_changes": [],
  "benchmark_code_changes": [],
  "retry_event_distribution": {
    "lexical_or_morphosyntactic_candidate_rejection": 7,
    "ne_short_scope_evidence_insufficient": 1,
    "author_translation_repair_after_mechanical_pass": 1
  },
  "author_confirmed_draft_language_issues": 1,
  "author_confirmed_translation_repairs": 1,
  "confirmed_language_quality_issues_scope": "Committed final prose; draft repairs are separately reported in author_confirmed_draft_language_issues and author_confirmed_translation_repairs.",
  "timing_caveats": [
    "Counters measure live local LLM author/file-callback elapsed time, including reasoning, file transport, tool wait and orchestration. Pure model inference cannot be isolated by these timers.",
    "K1-001 scene_planning includes context-resumption and controller inspection elapsed time. It remains in the production wall and per-text totals; it was not silently excluded as setup.",
    "K1-002 initial plan and initial draft were written together before the plan-stage boundary. Its measured scene_planning 38.392 seconds therefore includes initial drafting; stage totals are operational phase timings rather than a clean separation of planning and prose generation.",
    "Setup, resolver development, pre-run full regression and post-run tests/replay are outside the production wall. No code/config changes occurred during generation."
  ],
  "generator_side_total_seconds": 1050.3289791000425,
  "human_spot_review_pending": true
}
```
