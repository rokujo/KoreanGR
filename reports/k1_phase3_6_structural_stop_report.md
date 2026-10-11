# Phase 3.6 structural STOP report

K1-001 committed once. K1-002 attempt 1 rejected; K1-003..010 not generated.

Actual yes response identity: single / quoted sentence = ko_k1_0442; full text = ko_k1_0003 + g29. Planned-ID gate rejected the candidate. No parser or validator edits during production.

Next action: fix this bounded response/possessive collision in a separate version/run. Do not resume this failed benchmark or credit the rejected candidate.

Completed text times are n=1. The 10-text throughput and 300-text estimate are not established.

{
  "phase": "3.6",
  "verdict": "C",
  "status": "STRUCTURAL_FAIL",
  "completed": false,
  "committed_count": 1,
  "stop": {
    "type": "structural_analyzer_defect",
    "text": 2,
    "surface": "네",
    "expected_vocab_id": "ko_k1_0442",
    "actual_vocab_id": "ko_k1_0003",
    "raw_parts": [
      "너/NP",
      "의/JKG"
    ],
    "diagnostic": "reports/k1_phase3_6_ne_identity_structural_diagnostic.json",
    "code_changed": false
  },
  "artifact_integrity_errors": [],
  "ledger_replay_errors": [],
  "state_epoch": 1,
  "committed_hard_errors": 0,
  "rejected_attempt_count": 2,
  "candidate_hard_error_distribution": {
    "unknown_or_unresolved": 1,
    "unresolved_context_ambiguity": 1,
    "coverage_or_token_policy": 3,
    "planned_new_not_present": 1
  },
  "first_attempt_pass_count": 0,
  "first_attempt_pass_ratio": 0.0,
  "attempts_per_committed_text": [
    2
  ],
  "mean_attempts": 2,
  "total_candidate_attempts": 3,
  "future_contaminated_candidate_count": 0,
  "future_usage_occurrences": 0,
  "future_in_committed": 0,
  "unknown_unresolved_in_committed": 0,
  "planned_identity_mismatch_in_committed": 0,
  "semantic_grammar_warnings": 11,
  "semantic_warning_distribution": {
    "REVIEW": 11
  },
  "naturalness_warnings": 0,
  "naturalness_warning_distribution": {},
  "confirmed_language_quality_issues": 0,
  "translation_fidelity_flags": 0,
  "review_debt": [],
  "expired_review_debt": [],
  "near_deadline_debt": [],
  "selected_review_exposures": 0,
  "incidental_exposures": 0,
  "actual_new_introduced": 2,
  "actual_exposure_distribution": {
    "0": 498,
    "1": 2
  },
  "genre_distribution": {
    "food": 1
  },
  "scene_similarities": [],
  "max_scene_similarity": 0,
  "eojeol_distribution": {
    "n": 1,
    "min": 133,
    "max": 133,
    "mean": 133,
    "median": 133,
    "p90": 133
  },
  "sentence_length_distribution": {
    "4": 22,
    "5": 6,
    "1": 1,
    "3": 4,
    "2": 1
  },
  "preferred_sentence_ratio": 0.9411764705882353,
  "production_wall_seconds": 290.2286604000037,
  "per_text_seconds": {
    "n": 1,
    "min": 132.43497869999555,
    "max": 132.43497869999555,
    "mean": 132.43497869999555,
    "median": 132.43497869999555,
    "p90": 132.43497869999555
  },
  "stage_seconds": {
    "scene_planning": 35.04942049999954,
    "author_draft": 127.65834609999729,
    "morphology_vocab_analysis": 4.587038699988625,
    "mechanical_validation": 0.3796579000118072,
    "retry_repair": 46.36255450000317,
    "naturalness_review": 20.258823800002574,
    "final_reanalysis": 1.2678595000033965,
    "commit": 0.18497029999707593,
    "controller_overhead": 0.6986354999899049,
    "structural_diagnostics": 52.258329800002684
  },
  "unassigned_between_text_seconds": 1.5230238000076497,
  "estimated_300_serial_hours": null,
  "performance": "INCOMPLETE",
  "pre_run_regression": {
    "tests": 274,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 148.4429992000005,
    "success": true
  },
  "post_run_regression": null,
  "attempted_text_count": 2,
  "attempts_per_attempted_text": [
    2,
    1
  ],
  "mean_attempts_per_attempted_text": 1.5,
  "first_attempt_pass_ratio_attempted": 0.0,
  "semantic_warnings_all_candidates": 30,
  "resolver_review_occurrences_all_candidates": 1,
  "all_failed_attempt_ledger_hashes_unchanged": true,
  "benchmark_sample_size": 1,
  "throughput_estimate_valid": false,
  "estimated_300_serial_hours_reason": "Stopped at structural analyzer defect in 002. One committed text does not establish serial throughput for 300.",
  "post_run_regression_not_run_reason": "Run stopped at 002; required after-010 full suite was not reached. Post-stop committed-ledger raw replay and frozen-hash checks passed.",
  "stop_diagnostics_file": "reports/k1_phase3_6_ne_identity_structural_diagnostic.json",
  "code_changed_during_production": false,
  "frozen_file_count": 742,
  "confirmed_language_quality_issue_scope": "Committed 001 author review only; failed 002 did not reach author approval.",
  "actual_introduction_ids": [
    "ko_k1_0373",
    "ko_k1_0413"
  ],
  "skipped_text_numbers": [
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
  ],
  "naturalness_warning_interpretation": "Warnings are not independent correctness judgments."
}
