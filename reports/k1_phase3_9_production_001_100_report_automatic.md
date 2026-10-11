# Phase 3.9 endurance trial

**D / STRUCTURAL_FAIL** — 12/100 committed. No K1-101 or later generated.

Mechanical evaluate and atomic commit are byte-identical to Phase 3.8. The new envelope changes only run range/paths/provenance. Prompt and scene presentation were frozen before production. Existing credit/payment rules remain authoritative. Semantic warnings never block production.

Effective credit includes introductions plus selected and incidental distinct Expansion appearances; previous-only credits are separately recorded per text. Capped progress counts each vocabulary ID at most six times. Repetition beyond six never reduces remaining required credits.

Timing is live local author/callback wall time, not isolated external API latency. Engineering, pre/post regression, reporting and replay are excluded. Author self-checks are not independent gold. Early review hints can be vetoed; no selection is credited without canonical body occurrence.

First pass 0.8333333333333334; mean attempts 1.1666666666666667; initial findings 0.46153846153846156; initial future 0.0.
Capped progress 72/3000; future required rate 10.166666666666666; outstanding 5; expired 0; recovered expired 0.
Timing {'n': 12, 'mean': 278.813771883335, 'median': 215.17075430000114, 'p90': 487.30098010000074, 'min': 110.62739020001027, 'max': 688.9574667000124}; wall 3628.0080683000124; stages {'scene_planning': 932.342924600016, 'lexical_preflight': 25.335103999997955, 'author_draft': 1311.1937331000227, 'preflight_repair': 153.8207887999888, 'morphology_vocab_analysis': 34.9146462000208, 'mechanical_validation': 18.67590439999185, 'naturalness_review': 664.9825095000269, 'final_reanalysis': 31.342230099980952, 'commit': 36.79561470002227, 'controller_overhead': 13.193076699972153, 'retry_repair': 209.5410031999927}; performance INCOMPLETE.
300-text serial hours: mean None, median None. Later vocabulary load and human quality review are excluded.
No automatic continuation: user confirmation is required before K1-101..300.

## Full metrics

```json
{
  "phase": "3.9",
  "committed_count": 12,
  "completed": false,
  "stop": {
    "type": "author_input_contract_error",
    "text_number": 13,
    "reason": "Author self-check missing required keys; controller stopped before candidate submission."
  },
  "total_attempts": 14,
  "formal_first_pass_count": 10,
  "formal_first_pass_ratio": 0.8333333333333334,
  "mean_attempts": 1.1666666666666667,
  "initial_draft_with_finding": 6,
  "initial_draft_with_future": 0,
  "initial_finding_ratio": 0.46153846153846156,
  "initial_future_ratio": 0.0,
  "formal_future_findings": [],
  "retry_error_codes": {
    "coverage_or_token_policy": 1
  },
  "hard_errors": 0,
  "committed_future": 0,
  "committed_unresolved": 0,
  "planned_mismatch": 0,
  "final_canonical_mismatch": 0,
  "integrity_errors": [],
  "restricted_false_accepts": [],
  "failed_state_isolation": true,
  "semantic_warning_count": 142,
  "naturalness_warning_categories": {
    "nat_restricted_sense": 6,
    "nat_reference_clarity": 3
  },
  "confirmed_committed_issues": [],
  "author_repair_count": 1,
  "known_gap_occurrences": [
    {
      "text": 7,
      "intended_meaning": "open a paper book before the group lesson",
      "missing_natural_word": "펴다",
      "current_workaround": "omit opening and directly read the book",
      "whether_omission_solved_it": true,
      "resolution": "omit",
      "recurrence_count_in_this_run": 1,
      "historical_reference": "Known Phase 3.8 gap; no vocabulary or sense expansion."
    },
    {
      "text": 11,
      "intended_meaning": "dress the baby before resting",
      "missing_natural_word": "입히다",
      "current_workaround": "omit the dressing step and begin with the family already at home",
      "whether_omission_solved_it": true,
      "resolution": "omit",
      "recurrence_count_in_this_run": 1,
      "historical_reference": "Known Phase 3.8 gap; never use 입다 as causative dress."
    }
  ],
  "selected_review": 23,
  "incidental": 25,
  "introduced_count": 24,
  "effective_review_credits": 72,
  "effective_credit_distribution": {
    "n": 12,
    "mean": 6,
    "median": 6.5,
    "p90": 8,
    "min": 2,
    "max": 9
  },
  "exposure_distribution": {
    "3": 7,
    "2": 5,
    "0": 476,
    "1": 5,
    "4": 1,
    "6": 2,
    "5": 4
  },
  "outstanding_debt": [
    {
      "vocab_id": "ko_k1_0306",
      "window_index": 0,
      "window": {
        "from": 12,
        "to": 15
      }
    },
    {
      "vocab_id": "ko_k1_0446",
      "window_index": 1,
      "window": {
        "from": 10,
        "to": 28
      }
    },
    {
      "vocab_id": "ko_k1_0447",
      "window_index": 1,
      "window": {
        "from": 10,
        "to": 28
      }
    },
    {
      "vocab_id": "ko_k1_0448",
      "window_index": 1,
      "window": {
        "from": 11,
        "to": 29
      }
    },
    {
      "vocab_id": "ko_k1_0467",
      "window_index": 1,
      "window": {
        "from": 12,
        "to": 30
      }
    }
  ],
  "expired_debt": [],
  "recovered_expired_count": 0,
  "ever_expired_count": 0,
  "recovered_expired_windows": [],
  "near_deadline_debt": [
    {
      "vocab_id": "ko_k1_0306",
      "window_index": 0,
      "window": {
        "from": 12,
        "to": 15
      }
    }
  ],
  "genre_distribution": {
    "friends": 1,
    "short_dialogue": 1,
    "family": 1,
    "simple_outing": 1,
    "transport": 1,
    "food": 1,
    "school": 1,
    "objects": 1,
    "weather": 1,
    "work": 1,
    "home": 1,
    "health": 1
  },
  "max_scene_similarity": 0.016666666666666666,
  "eojeol": {
    "n": 12,
    "mean": 140.08333333333334,
    "median": 135.5,
    "p90": 157,
    "min": 124,
    "max": 179
  },
  "sentence_length_distribution": {
    "5": 110,
    "4": 242,
    "1": 8,
    "3": 31,
    "6": 10,
    "2": 1
  },
  "production_wall_seconds": 3628.0080683000124,
  "per_text_seconds": {
    "n": 12,
    "mean": 278.813771883335,
    "median": 215.17075430000114,
    "p90": 487.30098010000074,
    "min": 110.62739020001027,
    "max": 688.9574667000124
  },
  "stage_seconds": {
    "scene_planning": 932.342924600016,
    "lexical_preflight": 25.335103999997955,
    "author_draft": 1311.1937331000227,
    "preflight_repair": 153.8207887999888,
    "morphology_vocab_analysis": 34.9146462000208,
    "mechanical_validation": 18.67590439999185,
    "naturalness_review": 664.9825095000269,
    "final_reanalysis": 31.342230099980952,
    "commit": 36.79561470002227,
    "controller_overhead": 13.193076699972153,
    "retry_repair": 209.5410031999927
  },
  "preflight_repair_fraction": 0.042398138566451735,
  "formal_retry_fraction": 0.05775648765251452,
  "largest_stage": "author_draft",
  "capped_exposure_progress": 72,
  "required_total": 3000,
  "remaining_required_capped_credits": 2928,
  "remaining_texts_to_300": 288,
  "required_future_credit_rate": 10.166666666666666,
  "planning_color": "GREEN",
  "outstanding_windows": 5,
  "expired_windows": 0,
  "ledger_replay_errors": [],
  "pre_regression": {
    "tests": 323,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 290.3407193000021,
    "success": true
  },
  "post_regression": {
    "tests": 323,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 219.77888579999853,
    "success": true
  },
  "performance": "INCOMPLETE",
  "checkpoint_trajectory": [],
  "verdict": "D",
  "status": "STRUCTURAL_FAIL",
  "estimated_300_mean_hours": null,
  "estimated_300_median_hours": null,
  "corpus_candidate_reusable": false,
  "continuation_requires_user_confirmation": true
}
```
