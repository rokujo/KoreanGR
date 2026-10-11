# Phase 3.9a checkpoint

{
  "phase": "3.9a",
  "committed_count": 25,
  "completed": false,
  "stop": null,
  "total_attempts": 30,
  "formal_first_pass_count": 20,
  "formal_first_pass_ratio": 0.8,
  "mean_attempts": 1.2,
  "initial_draft_with_finding": 11,
  "initial_draft_with_future": 1,
  "initial_finding_ratio": 0.44,
  "initial_future_ratio": 0.04,
  "preflight_completed_count": 25,
  "author_contract_retry_count": 0,
  "contract_failures_recovered": 0,
  "contract_max_exhaustion": false,
  "formal_future_findings": [],
  "retry_error_codes": {
    "unknown_or_unresolved": 3,
    "coverage_or_token_policy": 6
  },
  "hard_errors": 0,
  "committed_future": 0,
  "committed_unresolved": 0,
  "planned_mismatch": 0,
  "final_canonical_mismatch": 0,
  "integrity_errors": [],
  "restricted_false_accepts": [],
  "failed_state_isolation": true,
  "semantic_warning_count": 327,
  "naturalness_warning_categories": {
    "nat_reference_clarity": 30,
    "nat_restricted_sense": 6,
    "nat_verb_argument_frame": 3,
    "nat_filler_adverb": 5
  },
  "confirmed_committed_issues": [],
  "author_repair_count": 3,
  "known_gap_occurrences": [],
  "selected_review": 60,
  "incidental": 113,
  "introduced_count": 50,
  "effective_review_credits": 223,
  "effective_credit_distribution": {
    "n": 25,
    "mean": 8.92,
    "median": 9,
    "p90": 14,
    "min": 2,
    "max": 18
  },
  "exposure_distribution": {
    "7": 4,
    "5": 5,
    "0": 450,
    "6": 5,
    "3": 12,
    "2": 9,
    "4": 3,
    "8": 2,
    "1": 5,
    "9": 2,
    "12": 2,
    "11": 1
  },
  "outstanding_debt": [
    {
      "vocab_id": "ko_k1_0310",
      "window_index": 1,
      "window": {
        "from": 18,
        "to": 36
      }
    },
    {
      "vocab_id": "ko_k1_0319",
      "window_index": 1,
      "window": {
        "from": 23,
        "to": 41
      }
    },
    {
      "vocab_id": "ko_k1_0320",
      "window_index": 1,
      "window": {
        "from": 23,
        "to": 41
      }
    },
    {
      "vocab_id": "ko_k1_0321",
      "window_index": 1,
      "window": {
        "from": 24,
        "to": 42
      }
    },
    {
      "vocab_id": "ko_k1_0322",
      "window_index": 1,
      "window": {
        "from": 24,
        "to": 42
      }
    },
    {
      "vocab_id": "ko_k1_0323",
      "window_index": 1,
      "window": {
        "from": 25,
        "to": 43
      }
    },
    {
      "vocab_id": "ko_k1_0324",
      "window_index": 1,
      "window": {
        "from": 25,
        "to": 43
      }
    },
    {
      "vocab_id": "ko_k1_0332",
      "window_index": 0,
      "window": {
        "from": 25,
        "to": 28
      }
    }
  ],
  "expired_debt": [],
  "recovered_expired_count": 4,
  "ever_expired_count": 4,
  "recovered_expired_windows": [
    [
      "ko_k1_0310",
      0
    ],
    [
      "ko_k1_0311",
      0
    ],
    [
      "ko_k1_0321",
      0
    ],
    [
      "ko_k1_0322",
      0
    ]
  ],
  "near_deadline_debt": [
    {
      "vocab_id": "ko_k1_0332",
      "window_index": 0,
      "window": {
        "from": 25,
        "to": 28
      }
    }
  ],
  "genre_distribution": {
    "school": 2,
    "friends": 1,
    "home": 1,
    "outdoor": 1,
    "short_dialogue": 1,
    "shopping": 3,
    "family": 4,
    "travel": 2,
    "simple_outing": 1,
    "objects": 2,
    "health": 1,
    "daily_life": 2,
    "simple_hobby": 1,
    "food": 2,
    "small_problem": 1
  },
  "max_scene_similarity": 0.16666666666666666,
  "eojeol": {
    "n": 25,
    "mean": 140.36,
    "median": 138,
    "p90": 150,
    "min": 128,
    "max": 165
  },
  "sentence_length_distribution": {
    "4": 456,
    "5": 274,
    "3": 37,
    "1": 11,
    "6": 30,
    "2": 3,
    "7": 1
  },
  "production_wall_seconds": 4801.105424499998,
  "per_text_seconds": {
    "n": 25,
    "mean": 186.64706772000005,
    "median": 174.35749029999715,
    "p90": 277.74850040000456,
    "min": 104.08582539999043,
    "max": 382.3849918000051
  },
  "stage_seconds": {
    "scene_planning": 1630.7405056000134,
    "lexical_preflight": 57.48404280001705,
    "author_draft": 1293.4280293999764,
    "preflight_repair": 332.11528849999013,
    "morphology_vocab_analysis": 83.74055819964269,
    "mechanical_validation": 82.87557210038358,
    "naturalness_review": 868.7332612000464,
    "final_reanalysis": 71.91528889998153,
    "commit": 158.3025925000693,
    "controller_overhead": 33.17138359985256,
    "retry_repair": 53.670170200028224
  },
  "preflight_repair_fraction": 0.06917475438160738,
  "formal_retry_fraction": 0.011178711037285252,
  "largest_stage": "scene_planning",
  "capped_exposure_progress": 192,
  "required_total": 3000,
  "remaining_required_capped_credits": 2808,
  "remaining_texts_to_300": 275,
  "required_future_credit_rate": 10.210909090909091,
  "planning_color": "GREEN",
  "outstanding_windows": 8,
  "expired_windows": 0,
  "trajectory": "initial",
  "newly_expired_since_checkpoint": 4,
  "recovered_expired_since_checkpoint": 4,
  "scheduler_risk": false
}
