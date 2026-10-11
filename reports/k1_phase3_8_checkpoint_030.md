# Phase 3.8 checkpoint 030

{
  "phase": "3.8",
  "completed": false,
  "committed_count": 30,
  "state_epoch": 30,
  "stop": null,
  "hard_errors": 0,
  "integrity_errors": [],
  "total_attempts": 42,
  "first_pass_count": 20,
  "first_pass_ratio": 0.6666666666666666,
  "mean_attempts": 1.4,
  "attempts": [
    2,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    3,
    2,
    2,
    2,
    1,
    2,
    1,
    1,
    3,
    1,
    2,
    1,
    1,
    1,
    1,
    1,
    2,
    1,
    1,
    2,
    1,
    1
  ],
  "retry_error_codes": {
    "future_expansion": 3,
    "coverage_or_token_policy": 20,
    "unresolved_context_ambiguity": 3,
    "unknown_or_unresolved": 4,
    "title_permission": 2
  },
  "rejected_attempts": 10,
  "future_contaminated_candidates": 3,
  "future_in_committed": 0,
  "unresolved_in_committed": 0,
  "planned_mismatch": 0,
  "structural_scope_mismatches": 0,
  "resolved_scope_mismatches": 0,
  "failed_state_isolation": true,
  "semantic_warning_count": 360,
  "semantic_warning_distribution": {
    "REVIEW": 355,
    "FAIL": 5
  },
  "naturalness_warning_count": 70,
  "naturalness_categories": {
    "nat_restricted_sense": 22,
    "nat_reference_clarity": 46,
    "nat_verb_argument_frame": 1,
    "nat_filler_adverb": 1
  },
  "author_confirmed_draft_issues": [
    {
      "text": 1,
      "attempt": 1,
      "evidence": {
        "naturalness": "REPAIR",
        "translation_fidelity": "REPAIR",
        "review_word_integration": "PASS",
        "reason": "先生が弟へ名前を言う文は誰の名前か曖昧で、訳だけ『自分の名前』と補っていた。学校の説明へ簡略化し、韓国語と訳のreferentを一致させる。機械warning数の削減を目的とする修正ではない。"
      }
    },
    {
      "text": 12,
      "attempt": 1,
      "evidence": {
        "naturalness": "REPAIR",
        "translation_fidelity": "PASS",
        "review_word_integration": "PASS",
        "reason": "『병원에는 아픈 사람이 있어요』の直後の그 사람は病人へ参照が移る可能性がある。勤務主体を의사と再提示し、終盤の勉強話は語り手の自分の学習へ絞って人物を不必要に切り替えない。warning数の削減ではなく、referentの具体的な修正。"
      }
    }
  ],
  "confirmed_committed_issues": [],
  "recurring_patterns": {},
  "selected_review": 62,
  "incidental": 87,
  "introduced_count": 60,
  "exposure_distribution": {
    "4": 12,
    "3": 13,
    "0": 440,
    "5": 2,
    "2": 18,
    "6": 2,
    "8": 1,
    "1": 8,
    "7": 1,
    "14": 1,
    "16": 1,
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
      "vocab_id": "ko_k1_0327",
      "window_index": 1,
      "window": {
        "from": 27,
        "to": 45
      }
    },
    {
      "vocab_id": "ko_k1_0328",
      "window_index": 1,
      "window": {
        "from": 27,
        "to": 45
      }
    },
    {
      "vocab_id": "ko_k1_0329",
      "window_index": 0,
      "window": {
        "from": 24,
        "to": 27
      }
    },
    {
      "vocab_id": "ko_k1_0329",
      "window_index": 1,
      "window": {
        "from": 28,
        "to": 46
      }
    },
    {
      "vocab_id": "ko_k1_0331",
      "window_index": 1,
      "window": {
        "from": 29,
        "to": 47
      }
    },
    {
      "vocab_id": "ko_k1_0332",
      "window_index": 0,
      "window": {
        "from": 25,
        "to": 28
      }
    },
    {
      "vocab_id": "ko_k1_0332",
      "window_index": 1,
      "window": {
        "from": 29,
        "to": 47
      }
    },
    {
      "vocab_id": "ko_k1_0333",
      "window_index": 1,
      "window": {
        "from": 30,
        "to": 48
      }
    },
    {
      "vocab_id": "ko_k1_0334",
      "window_index": 1,
      "window": {
        "from": 30,
        "to": 48
      }
    },
    {
      "vocab_id": "ko_k1_0336",
      "window_index": 0,
      "window": {
        "from": 27,
        "to": 30
      }
    },
    {
      "vocab_id": "ko_k1_0338",
      "window_index": 0,
      "window": {
        "from": 28,
        "to": 31
      }
    },
    {
      "vocab_id": "ko_k1_0340",
      "window_index": 0,
      "window": {
        "from": 29,
        "to": 32
      }
    },
    {
      "vocab_id": "ko_k1_0342",
      "window_index": 0,
      "window": {
        "from": 30,
        "to": 33
      }
    },
    {
      "vocab_id": "ko_k1_0808",
      "window_index": 1,
      "window": {
        "from": 26,
        "to": 44
      }
    },
    {
      "vocab_id": "ko_k1_0373",
      "window_index": 2,
      "window": {
        "from": 26,
        "to": 66
      }
    },
    {
      "vocab_id": "ko_k1_0443",
      "window_index": 2,
      "window": {
        "from": 27,
        "to": 67
      }
    },
    {
      "vocab_id": "ko_k1_0448",
      "window_index": 2,
      "window": {
        "from": 30,
        "to": 70
      }
    },
    {
      "vocab_id": "ko_k1_0449",
      "window_index": 2,
      "window": {
        "from": 30,
        "to": 70
      }
    }
  ],
  "expired_debt": [
    {
      "vocab_id": "ko_k1_0329",
      "window_index": 0,
      "window": {
        "from": 24,
        "to": 27
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
  "near_deadline_debt": [
    {
      "vocab_id": "ko_k1_0329",
      "window_index": 0,
      "window": {
        "from": 24,
        "to": 27
      }
    },
    {
      "vocab_id": "ko_k1_0332",
      "window_index": 0,
      "window": {
        "from": 25,
        "to": 28
      }
    },
    {
      "vocab_id": "ko_k1_0336",
      "window_index": 0,
      "window": {
        "from": 27,
        "to": 30
      }
    },
    {
      "vocab_id": "ko_k1_0338",
      "window_index": 0,
      "window": {
        "from": 28,
        "to": 31
      }
    },
    {
      "vocab_id": "ko_k1_0340",
      "window_index": 0,
      "window": {
        "from": 29,
        "to": 32
      }
    }
  ],
  "mathematically_unrecoverable": [],
  "genre_distribution": {
    "family": 2,
    "short_dialogue": 1,
    "objects": 2,
    "transport": 1,
    "food": 2,
    "weather": 2,
    "school": 3,
    "shopping": 4,
    "simple_hobby": 1,
    "simple_outing": 2,
    "home": 2,
    "work": 2,
    "small_problem": 2,
    "health": 1,
    "travel": 1,
    "friends": 2
  },
  "max_scene_similarity": 0.16666666666666666,
  "scene_similarities": [
    {
      "a": 2,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 3,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 3,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 4,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 4,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 4,
      "b": 3,
      "score": 0.0
    },
    {
      "a": 5,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 5,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 5,
      "b": 3,
      "score": 0.0
    },
    {
      "a": 5,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 6,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 6,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 6,
      "b": 3,
      "score": 0.0
    },
    {
      "a": 6,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 6,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 7,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 7,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 7,
      "b": 3,
      "score": 0.0
    },
    {
      "a": 7,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 7,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 7,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 8,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 8,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 8,
      "b": 3,
      "score": 0.0
    },
    {
      "a": 8,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 8,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 8,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 8,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 9,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 9,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 9,
      "b": 3,
      "score": 0.0
    },
    {
      "a": 9,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 9,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 9,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 9,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 9,
      "b": 8,
      "score": 0.0
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
      "score": 0.0
    },
    {
      "a": 10,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 10,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 10,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 10,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 10,
      "b": 8,
      "score": 0.0
    },
    {
      "a": 10,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 1,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 3,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 8,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 11,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 2,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 3,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 8,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 12,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 3,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 8,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 13,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 4,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 8,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 14,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 5,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 8,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 15,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 6,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 8,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 16,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 7,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 8,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 17,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 8,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 18,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 9,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 19,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 10,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 20,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 11,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 21,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 12,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 22,
      "b": 21,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 13,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 21,
      "score": 0.0
    },
    {
      "a": 23,
      "b": 22,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 14,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 21,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 22,
      "score": 0.0
    },
    {
      "a": 24,
      "b": 23,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 15,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 21,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 22,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 23,
      "score": 0.0
    },
    {
      "a": 25,
      "b": 24,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 16,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 21,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 22,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 23,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 24,
      "score": 0.0
    },
    {
      "a": 26,
      "b": 25,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 17,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 21,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 22,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 23,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 24,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 25,
      "score": 0.0
    },
    {
      "a": 27,
      "b": 26,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 18,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 21,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 22,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 23,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 24,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 25,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 26,
      "score": 0.0
    },
    {
      "a": 28,
      "b": 27,
      "score": 0.0
    },
    {
      "a": 29,
      "b": 19,
      "score": 0.0
    },
    {
      "a": 29,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 29,
      "b": 21,
      "score": 0.0
    },
    {
      "a": 29,
      "b": 22,
      "score": 0.0
    },
    {
      "a": 29,
      "b": 23,
      "score": 0.0
    },
    {
      "a": 29,
      "b": 24,
      "score": 0.023809523809523808
    },
    {
      "a": 29,
      "b": 25,
      "score": 0.0
    },
    {
      "a": 29,
      "b": 26,
      "score": 0.0
    },
    {
      "a": 29,
      "b": 27,
      "score": 0.0
    },
    {
      "a": 29,
      "b": 28,
      "score": 0.16666666666666666
    },
    {
      "a": 30,
      "b": 20,
      "score": 0.0
    },
    {
      "a": 30,
      "b": 21,
      "score": 0.0
    },
    {
      "a": 30,
      "b": 22,
      "score": 0.0
    },
    {
      "a": 30,
      "b": 23,
      "score": 0.0
    },
    {
      "a": 30,
      "b": 24,
      "score": 0.0
    },
    {
      "a": 30,
      "b": 25,
      "score": 0.0
    },
    {
      "a": 30,
      "b": 26,
      "score": 0.0
    },
    {
      "a": 30,
      "b": 27,
      "score": 0.0
    },
    {
      "a": 30,
      "b": 28,
      "score": 0.0
    },
    {
      "a": 30,
      "b": 29,
      "score": 0.0
    }
  ],
  "eojeol": {
    "n": 30,
    "min": 132,
    "max": 165,
    "mean": 143.46666666666667,
    "median": 141.5,
    "p90": 156
  },
  "sentence_lengths": {
    "4": 603,
    "5": 268,
    "3": 150,
    "1": 5,
    "2": 6,
    "6": 13,
    "7": 1
  },
  "preferred_sentence_ratio": 0.9894837476099426,
  "production_wall_seconds": 4031.451559299996,
  "per_text_seconds": {
    "n": 30,
    "min": 60.5486086000019,
    "max": 277.67050089999975,
    "mean": 128.9107440133334,
    "median": 98.7784020500003,
    "p90": 226.1390376000054
  },
  "stage_seconds": {
    "scene_planning": 1093.5497132000019,
    "lexical_preflight": 46.15647360000003,
    "author_draft": 1277.678530299956,
    "morphology_vocab_analysis": 76.41566299975966,
    "mechanical_validation": 109.8440934002283,
    "naturalness_review": 783.200170999975,
    "retry_repair": 206.29734790001385,
    "final_reanalysis": 58.01753860003373,
    "commit": 190.51384469992627,
    "controller_overhead": 25.648944700107677
  },
  "estimated_300_mean_hours": null,
  "estimated_300_median_hours": null,
  "baseline": {
    "mean": 128.3,
    "median": 114.9,
    "p90": 163.63,
    "first_pass": 0.3,
    "mean_attempts": 1.9
  },
  "largest_stage": "author_draft",
  "engineering_setup_seconds": 266.063808,
  "pre_regression": {
    "tests": 317,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 134.43668190000608,
    "success": true
  },
  "surface_recovery_count": 13,
  "surface_recovery_count_all_candidates": 19,
  "surface_recovery_distribution": {
    "오늘": 9,
    "내일": 3,
    "어제": 1
  },
  "preflight_future_findings": 62,
  "preflight_drafts_with_future": 25,
  "preflight_state_isolation": true,
  "recovery_fixture_result": {
    "rows": [
      {
        "historical_phase": "3_6",
        "text": 2,
        "source": "pilot\\ko\\k1\\phase3_6\\candidates\\K1-002-attempt-01.json",
        "hard_pass": true,
        "hard_errors": [],
        "coverage": {
          "denominator_N": 145,
          "new_tokens_U": 2,
          "controlled_vocab_coverage": 1.0,
          "previous_vocab_coverage": 0.9862068965517241,
          "target_99_met": false
        },
        "canonical_lexical_map": [
          {
            "sentence_index": 1,
            "start": 0,
            "end": 2,
            "surface": "오늘",
            "canonical_vocab_id": "ko_k1_0068",
            "lemma": "오늘",
            "pos": "noun",
            "sense": "today",
            "sentence_raw": [
              {
                "form": "오늘",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 2,
            "end": 3,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 4,
            "end": 7,
            "surface": "금요일",
            "canonical_vocab_id": "ko_k1_0089",
            "lemma": "금요일",
            "pos": "noun",
            "sense": "friday",
            "sentence_raw": [
              {
                "form": "금요일",
                "tag": "NNG",
                "start": 4,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 7,
            "end": 8,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 8,
            "end": 9,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 10,
            "end": 11,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 11,
            "end": 12,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 13,
            "end": 14,
            "surface": "집",
            "canonical_vocab_id": "ko_k1_0042",
            "lemma": "집",
            "pos": "noun",
            "sense": "home",
            "sentence_raw": [
              {
                "form": "집",
                "tag": "NNG",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 14,
            "end": 15,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 16,
            "end": 17,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 16,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 17,
            "end": 19,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 17,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 21,
            "end": 23,
            "surface": "내일",
            "canonical_vocab_id": "ko_k1_0070",
            "lemma": "내일",
            "pos": "noun",
            "sense": "tomorrow",
            "sentence_raw": [
              {
                "form": "내일",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 23,
            "end": 24,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 25,
            "end": 27,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 27,
            "end": 28,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 29,
            "end": 31,
            "surface": "만나",
            "canonical_vocab_id": "ko_k1_0188",
            "lemma": "만나다",
            "pos": "verb",
            "sense": "meet",
            "sentence_raw": [
              {
                "form": "만나",
                "tag": "VV",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 31,
            "end": 32,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 33,
            "end": 34,
            "surface": "싶",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "싶",
                "tag": "VX",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 34,
            "end": 36,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 38,
            "end": 40,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 40,
            "end": 41,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 42,
            "end": 44,
            "surface": "내일",
            "canonical_vocab_id": "ko_k1_0070",
            "lemma": "내일",
            "pos": "noun",
            "sense": "tomorrow",
            "sentence_raw": [
              {
                "form": "내일",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 45,
            "end": 47,
            "surface": "시간",
            "canonical_vocab_id": "ko_k1_0076",
            "lemma": "시간",
            "pos": "noun",
            "sense": "time",
            "sentence_raw": [
              {
                "form": "시간",
                "tag": "NNG",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 47,
            "end": 48,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 49,
            "end": 50,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 50,
            "end": 52,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 54,
            "end": 55,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 55,
            "end": 56,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 57,
            "end": 59,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 59,
            "end": 61,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 62,
            "end": 65,
            "surface": "전화해",
            "canonical_vocab_id": "ko_k1_0220",
            "lemma": "전화하다",
            "pos": "verb",
            "sense": "phone",
            "sentence_raw": [
              {
                "form": "전화",
                "tag": "NNG",
                "start": 8,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 64,
            "end": 66,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 68,
            "end": 70,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 70,
            "end": 71,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 72,
            "end": 74,
            "surface": "전화",
            "canonical_vocab_id": "ko_k1_0105",
            "lemma": "전화",
            "pos": "noun",
            "sense": "telephone",
            "sentence_raw": [
              {
                "form": "전화",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 74,
            "end": 75,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 76,
            "end": 77,
            "surface": "받",
            "canonical_vocab_id": "ko_k1_0193",
            "lemma": "받다",
            "pos": "verb",
            "sense": "receive",
            "sentence_raw": [
              {
                "form": "받",
                "tag": "VV-R",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 77,
            "end": 78,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 79,
            "end": 81,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 11,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 80,
            "end": 82,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 85,
            "end": 87,
            "surface": "내일",
            "canonical_vocab_id": "ko_k1_0070",
            "lemma": "내일",
            "pos": "noun",
            "sense": "tomorrow",
            "sentence_raw": [
              {
                "form": "내일",
                "tag": "NNG",
                "start": 1,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 88,
            "end": 90,
            "surface": "아침",
            "canonical_vocab_id": "ko_k1_0072",
            "lemma": "아침",
            "pos": "noun",
            "sense": "morning",
            "sentence_raw": [
              {
                "form": "아침",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 90,
            "end": 91,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 92,
            "end": 94,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 94,
            "end": 95,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 96,
            "end": 97,
            "surface": "가",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 96,
            "end": 98,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 103,
            "end": 106,
            "surface": "아니요",
            "canonical_vocab_id": "ko_k1_0443",
            "lemma": "아니요",
            "pos": "interjection",
            "sense": "no_polite",
            "sentence_raw": [
              {
                "form": "아니",
                "tag": "VCN",
                "start": 1,
                "length": 2
              },
              {
                "form": "요",
                "tag": "EC",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 108,
            "end": 110,
            "surface": "아침",
            "canonical_vocab_id": "ko_k1_0072",
            "lemma": "아침",
            "pos": "noun",
            "sense": "morning",
            "sentence_raw": [
              {
                "form": "아침",
                "tag": "NNG",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 110,
            "end": 111,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 111,
            "end": 112,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 113,
            "end": 115,
            "surface": "숙제",
            "canonical_vocab_id": "ko_k1_0137",
            "lemma": "숙제",
            "pos": "noun",
            "sense": "homework",
            "sentence_raw": [
              {
                "form": "숙제",
                "tag": "NNG",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 115,
            "end": 116,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 117,
            "end": 118,
            "surface": "해",
            "canonical_vocab_id": "ko_k1_0179",
            "lemma": "하다",
            "pos": "verb",
            "sense": "do",
            "sentence_raw": [
              {
                "form": "하",
                "tag": "VV",
                "start": 15,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 117,
            "end": 119,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 122,
            "end": 123,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 123,
            "end": 124,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 125,
            "end": 127,
            "surface": "공책",
            "canonical_vocab_id": "ko_k1_0102",
            "lemma": "공책",
            "pos": "noun",
            "sense": "notebook",
            "sentence_raw": [
              {
                "form": "공책",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 127,
            "end": 128,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 129,
            "end": 130,
            "surface": "보",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 130,
            "end": 131,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 132,
            "end": 134,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 10,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 133,
            "end": 135,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 138,
            "end": 139,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 139,
            "end": 140,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 141,
            "end": 143,
            "surface": "아침",
            "canonical_vocab_id": "ko_k1_0072",
            "lemma": "아침",
            "pos": "noun",
            "sense": "morning",
            "sentence_raw": [
              {
                "form": "아침",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 143,
            "end": 144,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 144,
            "end": 145,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 146,
            "end": 148,
            "surface": "공부",
            "canonical_vocab_id": "ko_k1_0136",
            "lemma": "공부",
            "pos": "noun",
            "sense": "study",
            "sentence_raw": [
              {
                "form": "공부",
                "tag": "NNG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 148,
            "end": 149,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 150,
            "end": 151,
            "surface": "해",
            "canonical_vocab_id": "ko_k1_0179",
            "lemma": "하다",
            "pos": "verb",
            "sense": "do",
            "sentence_raw": [
              {
                "form": "하",
                "tag": "VV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 150,
            "end": 152,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 155,
            "end": 157,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 157,
            "end": 158,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 159,
            "end": 161,
            "surface": "저녁",
            "canonical_vocab_id": "ko_k1_0074",
            "lemma": "저녁",
            "pos": "noun",
            "sense": "evening",
            "sentence_raw": [
              {
                "form": "저녁",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 161,
            "end": 162,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 163,
            "end": 165,
            "surface": "시간",
            "canonical_vocab_id": "ko_k1_0076",
            "lemma": "시간",
            "pos": "noun",
            "sense": "time",
            "sentence_raw": [
              {
                "form": "시간",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 165,
            "end": 166,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 167,
            "end": 168,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 168,
            "end": 170,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 172,
            "end": 173,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 173,
            "end": 174,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 175,
            "end": 177,
            "surface": "저녁",
            "canonical_vocab_id": "ko_k1_0074",
            "lemma": "저녁",
            "pos": "noun",
            "sense": "evening",
            "sentence_raw": [
              {
                "form": "저녁",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 177,
            "end": 178,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 178,
            "end": 179,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 180,
            "end": 182,
            "surface": "시간",
            "canonical_vocab_id": "ko_k1_0076",
            "lemma": "시간",
            "pos": "noun",
            "sense": "time",
            "sentence_raw": [
              {
                "form": "시간",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 182,
            "end": 183,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 184,
            "end": 185,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 185,
            "end": 187,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 190,
            "end": 192,
            "surface": "저녁",
            "canonical_vocab_id": "ko_k1_0074",
            "lemma": "저녁",
            "pos": "noun",
            "sense": "evening",
            "sentence_raw": [
              {
                "form": "저녁",
                "tag": "NNG",
                "start": 1,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 192,
            "end": 193,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 194,
            "end": 196,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 196,
            "end": 198,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 199,
            "end": 201,
            "surface": "만나",
            "canonical_vocab_id": "ko_k1_0188",
            "lemma": "만나다",
            "pos": "verb",
            "sense": "meet",
            "sentence_raw": [
              {
                "form": "만나",
                "tag": "VV",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 200,
            "end": 202,
            "surface": "나요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 207,
            "end": 208,
            "surface": "네",
            "canonical_vocab_id": "ko_k1_0442",
            "lemma": "네",
            "pos": "interjection",
            "sense": "yes",
            "sentence_raw": [
              {
                "form": "네",
                "tag": "IC",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 210,
            "end": 212,
            "surface": "저녁",
            "canonical_vocab_id": "ko_k1_0074",
            "lemma": "저녁",
            "pos": "noun",
            "sense": "evening",
            "sentence_raw": [
              {
                "form": "저녁",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 212,
            "end": 213,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 214,
            "end": 216,
            "surface": "만나",
            "canonical_vocab_id": "ko_k1_0188",
            "lemma": "만나다",
            "pos": "verb",
            "sense": "meet",
            "sentence_raw": [
              {
                "form": "만나",
                "tag": "VV",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 215,
            "end": 217,
            "surface": "나요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 220,
            "end": 222,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 222,
            "end": 223,
            "surface": "가",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "가",
                "tag": "JKS",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 224,
            "end": 225,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 225,
            "end": 227,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 228,
            "end": 230,
            "surface": "다시",
            "canonical_vocab_id": "ko_k1_0274",
            "lemma": "다시",
            "pos": "adverb",
            "sense": "again",
            "sentence_raw": [
              {
                "form": "다시",
                "tag": "MAG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 231,
            "end": 233,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 11,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 232,
            "end": 234,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 237,
            "end": 239,
            "surface": "어디",
            "canonical_vocab_id": "ko_k1_0014",
            "lemma": "어디",
            "pos": "pronoun",
            "sense": "where",
            "sentence_raw": [
              {
                "form": "어디",
                "tag": "NP",
                "start": 1,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 239,
            "end": 241,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 242,
            "end": 245,
            "surface": "기다려",
            "canonical_vocab_id": "ko_k1_0189",
            "lemma": "기다리다",
            "pos": "verb",
            "sense": "wait",
            "sentence_raw": [
              {
                "form": "기다리",
                "tag": "VV",
                "start": 6,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 244,
            "end": 246,
            "surface": "려요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 250,
            "end": 252,
            "surface": "학교",
            "canonical_vocab_id": "ko_k1_0043",
            "lemma": "학교",
            "pos": "noun",
            "sense": "school",
            "sentence_raw": [
              {
                "form": "학교",
                "tag": "NNG",
                "start": 1,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 253,
            "end": 254,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 255,
            "end": 257,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 258,
            "end": 259,
            "surface": "앞",
            "canonical_vocab_id": "ko_k1_0061",
            "lemma": "앞",
            "pos": "noun",
            "sense": "front",
            "sentence_raw": [
              {
                "form": "앞",
                "tag": "NNG",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 259,
            "end": 261,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 262,
            "end": 265,
            "surface": "기다려",
            "canonical_vocab_id": "ko_k1_0189",
            "lemma": "기다리다",
            "pos": "verb",
            "sense": "wait",
            "sentence_raw": [
              {
                "form": "기다리",
                "tag": "VV",
                "start": 13,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 264,
            "end": 266,
            "surface": "려요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 269,
            "end": 271,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 271,
            "end": 272,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 273,
            "end": 275,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 275,
            "end": 276,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 277,
            "end": 278,
            "surface": "잘",
            "canonical_vocab_id": "ko_k1_0266",
            "lemma": "잘",
            "pos": "adverb",
            "sense": "well",
            "sentence_raw": [
              {
                "form": "잘",
                "tag": "MAG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 279,
            "end": 280,
            "surface": "알",
            "canonical_vocab_id": "ko_k1_0207",
            "lemma": "알다",
            "pos": "verb",
            "sense": "know",
            "sentence_raw": [
              {
                "form": "알",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 280,
            "end": 282,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 284,
            "end": 286,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 286,
            "end": 287,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 287,
            "end": 288,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 289,
            "end": 290,
            "surface": "꽃",
            "canonical_vocab_id": "ko_k1_0159",
            "lemma": "꽃",
            "pos": "noun",
            "sense": "flower",
            "sentence_raw": [
              {
                "form": "꽃",
                "tag": "NNG",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 290,
            "end": 291,
            "surface": "하",
            "canonical_vocab_id": "ko_k1_0179",
            "lemma": "하다",
            "pos": "verb",
            "sense": "do",
            "sentence_raw": [
              {
                "form": "하",
                "tag": "VV",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 291,
            "end": 292,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 293,
            "end": 295,
            "surface": "나무",
            "canonical_vocab_id": "ko_k1_0160",
            "lemma": "나무",
            "pos": "noun",
            "sense": "tree",
            "sentence_raw": [
              {
                "form": "나무",
                "tag": "NNG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 295,
            "end": 296,
            "surface": "가",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "가",
                "tag": "JKS",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 297,
            "end": 298,
            "surface": "많",
            "canonical_vocab_id": "ko_k1_0236",
            "lemma": "많다",
            "pos": "adjective",
            "sense": "many",
            "sentence_raw": [
              {
                "form": "많",
                "tag": "VA",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 298,
            "end": 300,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 303,
            "end": 304,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 304,
            "end": 305,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 306,
            "end": 308,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 308,
            "end": 310,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 311,
            "end": 313,
            "surface": "사진",
            "canonical_vocab_id": "ko_k1_0104",
            "lemma": "사진",
            "pos": "noun",
            "sense": "photo",
            "sentence_raw": [
              {
                "form": "사진",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 313,
            "end": 314,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 315,
            "end": 316,
            "surface": "찍",
            "canonical_vocab_id": "ko_k1_0229",
            "lemma": "찍다",
            "pos": "verb",
            "sense": "take_photo",
            "sentence_raw": [
              {
                "form": "찍",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 316,
            "end": 317,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 318,
            "end": 319,
            "surface": "싶",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "싶",
                "tag": "VX",
                "start": 15,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 319,
            "end": 321,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 16,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 323,
            "end": 325,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 325,
            "end": 326,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 327,
            "end": 328,
            "surface": "꽃",
            "canonical_vocab_id": "ko_k1_0159",
            "lemma": "꽃",
            "pos": "noun",
            "sense": "flower",
            "sentence_raw": [
              {
                "form": "꽃",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 329,
            "end": 331,
            "surface": "사진",
            "canonical_vocab_id": "ko_k1_0104",
            "lemma": "사진",
            "pos": "noun",
            "sense": "photo",
            "sentence_raw": [
              {
                "form": "사진",
                "tag": "NNG",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 331,
            "end": 332,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 333,
            "end": 334,
            "surface": "찍",
            "canonical_vocab_id": "ko_k1_0229",
            "lemma": "찍다",
            "pos": "verb",
            "sense": "take_photo",
            "sentence_raw": [
              {
                "form": "찍",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 334,
            "end": 335,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 336,
            "end": 337,
            "surface": "싶",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "싶",
                "tag": "VX",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 337,
            "end": 339,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 341,
            "end": 344,
            "surface": "토요일",
            "canonical_vocab_id": "ko_k1_0090",
            "lemma": "토요일",
            "pos": "noun",
            "sense": "saturday",
            "sentence_raw": [
              {
                "form": "토요일",
                "tag": "NNG",
                "start": 0,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 345,
            "end": 347,
            "surface": "아침",
            "canonical_vocab_id": "ko_k1_0072",
            "lemma": "아침",
            "pos": "noun",
            "sense": "morning",
            "sentence_raw": [
              {
                "form": "아침",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 347,
            "end": 348,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 348,
            "end": 349,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 350,
            "end": 351,
            "surface": "집",
            "canonical_vocab_id": "ko_k1_0042",
            "lemma": "집",
            "pos": "noun",
            "sense": "home",
            "sentence_raw": [
              {
                "form": "집",
                "tag": "NNG",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 351,
            "end": 353,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 354,
            "end": 357,
            "surface": "공부해",
            "canonical_vocab_id": "ko_k1_0202",
            "lemma": "공부하다",
            "pos": "verb",
            "sense": "study",
            "sentence_raw": [
              {
                "form": "공부",
                "tag": "NNG",
                "start": 13,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 15,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 356,
            "end": 358,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 360,
            "end": 361,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 361,
            "end": 362,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 363,
            "end": 364,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 364,
            "end": 365,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 366,
            "end": 367,
            "surface": "읽",
            "canonical_vocab_id": "ko_k1_0177",
            "lemma": "읽다",
            "pos": "verb",
            "sense": "read",
            "sentence_raw": [
              {
                "form": "읽",
                "tag": "VV",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 367,
            "end": 368,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 369,
            "end": 371,
            "surface": "숙제",
            "canonical_vocab_id": "ko_k1_0137",
            "lemma": "숙제",
            "pos": "noun",
            "sense": "homework",
            "sentence_raw": [
              {
                "form": "숙제",
                "tag": "NNG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 371,
            "end": 372,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 373,
            "end": 374,
            "surface": "해",
            "canonical_vocab_id": "ko_k1_0179",
            "lemma": "하다",
            "pos": "verb",
            "sense": "do",
            "sentence_raw": [
              {
                "form": "하",
                "tag": "VV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 373,
            "end": 375,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 377,
            "end": 379,
            "surface": "숙제",
            "canonical_vocab_id": "ko_k1_0137",
            "lemma": "숙제",
            "pos": "noun",
            "sense": "homework",
            "sentence_raw": [
              {
                "form": "숙제",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 379,
            "end": 380,
            "surface": "가",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "가",
                "tag": "JKS",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 381,
            "end": 383,
            "surface": "끝나",
            "canonical_vocab_id": "ko_k1_0201",
            "lemma": "끝나다",
            "pos": "verb",
            "sense": "end_intransitive",
            "sentence_raw": [
              {
                "form": "끝나",
                "tag": "VV",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 383,
            "end": 384,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 385,
            "end": 386,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 386,
            "end": 387,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 388,
            "end": 389,
            "surface": "쉬",
            "canonical_vocab_id": "ko_k1_0224",
            "lemma": "쉬다",
            "pos": "verb",
            "sense": "rest",
            "sentence_raw": [
              {
                "form": "쉬",
                "tag": "VV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 389,
            "end": 391,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 393,
            "end": 395,
            "surface": "저녁",
            "canonical_vocab_id": "ko_k1_0074",
            "lemma": "저녁",
            "pos": "noun",
            "sense": "evening",
            "sentence_raw": [
              {
                "form": "저녁",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 395,
            "end": 396,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 396,
            "end": 397,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 398,
            "end": 399,
            "surface": "옷",
            "canonical_vocab_id": "ko_k1_0115",
            "lemma": "옷",
            "pos": "noun",
            "sense": "clothes",
            "sentence_raw": [
              {
                "form": "옷",
                "tag": "NNG",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 399,
            "end": 400,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 401,
            "end": 402,
            "surface": "입",
            "canonical_vocab_id": "ko_k1_0196",
            "lemma": "입다",
            "pos": "verb",
            "sense": "wear_clothes",
            "sentence_raw": [
              {
                "form": "입",
                "tag": "VV-R",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 402,
            "end": 403,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 404,
            "end": 405,
            "surface": "집",
            "canonical_vocab_id": "ko_k1_0042",
            "lemma": "집",
            "pos": "noun",
            "sense": "home",
            "sentence_raw": [
              {
                "form": "집",
                "tag": "NNG",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 405,
            "end": 407,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 408,
            "end": 410,
            "surface": "나가",
            "canonical_vocab_id": "ko_k1_0216",
            "lemma": "나가다",
            "pos": "verb",
            "sense": "go_out",
            "sentence_raw": [
              {
                "form": "나가",
                "tag": "VV",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 409,
            "end": 411,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 16,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 414,
            "end": 415,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 415,
            "end": 416,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 417,
            "end": 419,
            "surface": "버스",
            "canonical_vocab_id": "ko_k1_0144",
            "lemma": "버스",
            "pos": "noun",
            "sense": "bus",
            "sentence_raw": [
              {
                "form": "버스",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 419,
            "end": 420,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 421,
            "end": 422,
            "surface": "타",
            "canonical_vocab_id": "ko_k1_0198",
            "lemma": "타다",
            "pos": "verb",
            "sense": "ride",
            "sentence_raw": [
              {
                "form": "타",
                "tag": "VV",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 422,
            "end": 423,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 424,
            "end": 426,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 426,
            "end": 428,
            "surface": "으로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "으로",
                "tag": "JKB",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 429,
            "end": 430,
            "surface": "가",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 15,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 429,
            "end": 431,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 433,
            "end": 435,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 435,
            "end": 436,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 437,
            "end": 439,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 440,
            "end": 441,
            "surface": "앞",
            "canonical_vocab_id": "ko_k1_0061",
            "lemma": "앞",
            "pos": "noun",
            "sense": "front",
            "sentence_raw": [
              {
                "form": "앞",
                "tag": "NNG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 441,
            "end": 443,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 444,
            "end": 447,
            "surface": "기다려",
            "canonical_vocab_id": "ko_k1_0189",
            "lemma": "기다리다",
            "pos": "verb",
            "sense": "wait",
            "sentence_raw": [
              {
                "form": "기다리",
                "tag": "VV",
                "start": 11,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 446,
            "end": 448,
            "surface": "려요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 450,
            "end": 452,
            "surface": "만나",
            "canonical_vocab_id": "ko_k1_0188",
            "lemma": "만나다",
            "pos": "verb",
            "sense": "meet",
            "sentence_raw": [
              {
                "form": "만나",
                "tag": "VV",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 452,
            "end": 453,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "ETM",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 454,
            "end": 456,
            "surface": "시간",
            "canonical_vocab_id": "ko_k1_0076",
            "lemma": "시간",
            "pos": "noun",
            "sense": "time",
            "sentence_raw": [
              {
                "form": "시간",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 456,
            "end": 457,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKC",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 458,
            "end": 459,
            "surface": "돼",
            "canonical_vocab_id": "ko_k1_0373",
            "lemma": "되다",
            "pos": "verb",
            "sense": "become",
            "sentence_raw": [
              {
                "form": "되",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 458,
            "end": 460,
            "surface": "돼요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 462,
            "end": 463,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 463,
            "end": 464,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 465,
            "end": 467,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 467,
            "end": 468,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 469,
            "end": 470,
            "surface": "보",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 470,
            "end": 471,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 472,
            "end": 473,
            "surface": "웃",
            "canonical_vocab_id": "ko_k1_0227",
            "lemma": "웃다",
            "pos": "verb",
            "sense": "laugh_smile",
            "sentence_raw": [
              {
                "form": "웃",
                "tag": "VV-R",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 473,
            "end": 475,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 477,
            "end": 479,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 479,
            "end": 481,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 2,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 482,
            "end": 484,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 485,
            "end": 486,
            "surface": "안",
            "canonical_vocab_id": "ko_k1_0060",
            "lemma": "안",
            "pos": "noun",
            "sense": "inside",
            "sentence_raw": [
              {
                "form": "안",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 486,
            "end": 488,
            "surface": "으로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "으로",
                "tag": "JKB",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 489,
            "end": 492,
            "surface": "들어가",
            "canonical_vocab_id": "ko_k1_0215",
            "lemma": "들어가다",
            "pos": "verb",
            "sense": "go_in",
            "sentence_raw": [
              {
                "form": "들어가",
                "tag": "VV",
                "start": 12,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 491,
            "end": 493,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 495,
            "end": 497,
            "surface": "오늘",
            "canonical_vocab_id": "ko_k1_0068",
            "lemma": "오늘",
            "pos": "noun",
            "sense": "today",
            "sentence_raw": [
              {
                "form": "오늘",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 497,
            "end": 498,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 499,
            "end": 501,
            "surface": "바람",
            "canonical_vocab_id": "ko_k1_0154",
            "lemma": "바람",
            "pos": "noun",
            "sense": "wind",
            "sentence_raw": [
              {
                "form": "바람",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 501,
            "end": 502,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 503,
            "end": 506,
            "surface": "시원해",
            "canonical_vocab_id": "ko_k1_0254",
            "lemma": "시원하다",
            "pos": "adjective",
            "sense": "cool_refreshing",
            "sentence_raw": [
              {
                "form": "시원",
                "tag": "XR",
                "start": 8,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSA",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 505,
            "end": 507,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 510,
            "end": 512,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 512,
            "end": 513,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 514,
            "end": 516,
            "surface": "나무",
            "canonical_vocab_id": "ko_k1_0160",
            "lemma": "나무",
            "pos": "noun",
            "sense": "tree",
            "sentence_raw": [
              {
                "form": "나무",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 517,
            "end": 518,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 518,
            "end": 519,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 520,
            "end": 521,
            "surface": "앉",
            "canonical_vocab_id": "ko_k1_0184",
            "lemma": "앉다",
            "pos": "verb",
            "sense": "sit",
            "sentence_raw": [
              {
                "form": "앉",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 521,
            "end": 523,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 525,
            "end": 527,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 527,
            "end": 528,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 529,
            "end": 532,
            "surface": "휴대폰",
            "canonical_vocab_id": "ko_k1_0106",
            "lemma": "휴대폰",
            "pos": "noun",
            "sense": "mobile_phone",
            "sentence_raw": [
              {
                "form": "휴대폰",
                "tag": "NNG",
                "start": 4,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 532,
            "end": 534,
            "surface": "으로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "으로",
                "tag": "JKB",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 535,
            "end": 536,
            "surface": "꽃",
            "canonical_vocab_id": "ko_k1_0159",
            "lemma": "꽃",
            "pos": "noun",
            "sense": "flower",
            "sentence_raw": [
              {
                "form": "꽃",
                "tag": "NNG",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 537,
            "end": 539,
            "surface": "사진",
            "canonical_vocab_id": "ko_k1_0104",
            "lemma": "사진",
            "pos": "noun",
            "sense": "photo",
            "sentence_raw": [
              {
                "form": "사진",
                "tag": "NNG",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 539,
            "end": 540,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 541,
            "end": 542,
            "surface": "찍",
            "canonical_vocab_id": "ko_k1_0229",
            "lemma": "찍다",
            "pos": "verb",
            "sense": "take_photo",
            "sentence_raw": [
              {
                "form": "찍",
                "tag": "VV",
                "start": 16,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 542,
            "end": 544,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 17,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 546,
            "end": 547,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 547,
            "end": 548,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 549,
            "end": 551,
            "surface": "나무",
            "canonical_vocab_id": "ko_k1_0160",
            "lemma": "나무",
            "pos": "noun",
            "sense": "tree",
            "sentence_raw": [
              {
                "form": "나무",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 552,
            "end": 554,
            "surface": "사진",
            "canonical_vocab_id": "ko_k1_0104",
            "lemma": "사진",
            "pos": "noun",
            "sense": "photo",
            "sentence_raw": [
              {
                "form": "사진",
                "tag": "NNG",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 554,
            "end": 555,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 556,
            "end": 557,
            "surface": "찍",
            "canonical_vocab_id": "ko_k1_0229",
            "lemma": "찍다",
            "pos": "verb",
            "sense": "take_photo",
            "sentence_raw": [
              {
                "form": "찍",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 557,
            "end": 559,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 561,
            "end": 563,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 563,
            "end": 564,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 565,
            "end": 567,
            "surface": "사진",
            "canonical_vocab_id": "ko_k1_0104",
            "lemma": "사진",
            "pos": "noun",
            "sense": "photo",
            "sentence_raw": [
              {
                "form": "사진",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 567,
            "end": 568,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 569,
            "end": 570,
            "surface": "보",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 570,
            "end": 571,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 572,
            "end": 575,
            "surface": "이야기",
            "canonical_vocab_id": "ko_k1_0134",
            "lemma": "이야기",
            "pos": "noun",
            "sense": "story_talk",
            "sentence_raw": [
              {
                "form": "이야기",
                "tag": "NNG",
                "start": 11,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 575,
            "end": 576,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 577,
            "end": 578,
            "surface": "해",
            "canonical_vocab_id": "ko_k1_0179",
            "lemma": "하다",
            "pos": "verb",
            "sense": "do",
            "sentence_raw": [
              {
                "form": "하",
                "tag": "VV",
                "start": 16,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 577,
            "end": 579,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 16,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 581,
            "end": 583,
            "surface": "사진",
            "canonical_vocab_id": "ko_k1_0104",
            "lemma": "사진",
            "pos": "noun",
            "sense": "photo",
            "sentence_raw": [
              {
                "form": "사진",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 583,
            "end": 584,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 584,
            "end": 585,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 586,
            "end": 587,
            "surface": "꽃",
            "canonical_vocab_id": "ko_k1_0159",
            "lemma": "꽃",
            "pos": "noun",
            "sense": "flower",
            "sentence_raw": [
              {
                "form": "꽃",
                "tag": "NNG",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 587,
            "end": 588,
            "surface": "하",
            "canonical_vocab_id": "ko_k1_0179",
            "lemma": "하다",
            "pos": "verb",
            "sense": "do",
            "sentence_raw": [
              {
                "form": "하",
                "tag": "VV",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 588,
            "end": 589,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 590,
            "end": 592,
            "surface": "나무",
            "canonical_vocab_id": "ko_k1_0160",
            "lemma": "나무",
            "pos": "noun",
            "sense": "tree",
            "sentence_raw": [
              {
                "form": "나무",
                "tag": "NNG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 592,
            "end": 593,
            "surface": "가",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "가",
                "tag": "JKS",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 594,
            "end": 595,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 595,
            "end": 597,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 36,
            "start": 599,
            "end": 600,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 36,
            "start": 600,
            "end": 601,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 36,
            "start": 602,
            "end": 604,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 36,
            "start": 604,
            "end": 606,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 36,
            "start": 607,
            "end": 608,
            "surface": "집",
            "canonical_vocab_id": "ko_k1_0042",
            "lemma": "집",
            "pos": "noun",
            "sense": "home",
            "sentence_raw": [
              {
                "form": "집",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 36,
            "start": 608,
            "end": 610,
            "surface": "으로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "으로",
                "tag": "JKB",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 36,
            "start": 611,
            "end": 614,
            "surface": "돌아가",
            "canonical_vocab_id": "ko_k1_0214",
            "lemma": "돌아가다",
            "pos": "verb",
            "sense": "go_back",
            "sentence_raw": [
              {
                "form": "돌아가",
                "tag": "VV",
                "start": 12,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 36,
            "start": 613,
            "end": 615,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          }
        ],
        "scope_disagreements": [
          {
            "type": "scope_identity_disagreement_warning",
            "scope": "full_text",
            "start": 207,
            "end": 208,
            "surface": "네",
            "sentence_identity": "ko_k1_0442",
            "diagnostic_identities": [
              "ko_k1_0442"
            ],
            "sentence_raw_pos": [
              "IC"
            ],
            "diagnostic_raw_pos": [
              "JKG",
              "NP"
            ],
            "id_disagreement": false,
            "pos_only_disagreement": true,
            "disagreement": true,
            "structural_defect": false,
            "decision": "WARNING_ONLY"
          }
        ],
        "credit": false
      },
      {
        "historical_phase": "3_6b",
        "text": 7,
        "source": "pilot\\ko\\k1\\phase3_6b\\candidates\\K1-007-attempt-01.json",
        "hard_pass": true,
        "hard_errors": [],
        "coverage": {
          "denominator_N": 129,
          "new_tokens_U": 2,
          "controlled_vocab_coverage": 1.0,
          "previous_vocab_coverage": 0.9844961240310077,
          "target_99_met": false
        },
        "canonical_lexical_map": [
          {
            "sentence_index": 1,
            "start": 0,
            "end": 1,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 1,
            "end": 2,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 3,
            "end": 5,
            "surface": "여덟",
            "canonical_vocab_id": "ko_k1_0288",
            "lemma": "여덟",
            "pos": "numeral",
            "sense": "eight_native",
            "sentence_raw": [
              {
                "form": "여덟",
                "tag": "NR",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 6,
            "end": 7,
            "surface": "살",
            "canonical_vocab_id": "ko_k1_0469",
            "lemma": "살",
            "pos": "counter",
            "sense": "age_year",
            "sentence_raw": [
              {
                "form": "살",
                "tag": "NNB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 7,
            "end": 8,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 8,
            "end": 10,
            "surface": "에요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에요",
                "tag": "EF",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 12,
            "end": 14,
            "surface": "학교",
            "canonical_vocab_id": "ko_k1_0043",
            "lemma": "학교",
            "pos": "noun",
            "sense": "school",
            "sentence_raw": [
              {
                "form": "학교",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 14,
            "end": 16,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 2,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 17,
            "end": 20,
            "surface": "한국어",
            "canonical_vocab_id": "ko_k1_0169",
            "lemma": "한국어",
            "pos": "noun",
            "sense": "korean_language",
            "sentence_raw": [
              {
                "form": "한국어",
                "tag": "NNP",
                "start": 5,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 20,
            "end": 21,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 22,
            "end": 24,
            "surface": "배울",
            "canonical_vocab_id": "ko_k1_0209",
            "lemma": "배우다",
            "pos": "verb",
            "sense": "learn",
            "sentence_raw": [
              {
                "form": "배우",
                "tag": "VV",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 23,
            "end": 24,
            "surface": "울",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆯ",
                "tag": "ETM",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 25,
            "end": 26,
            "surface": "거",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "거",
                "tag": "NNB",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 26,
            "end": 27,
            "surface": "예",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 14,
                "length": 0
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 26,
            "end": 28,
            "surface": "예요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "예요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 30,
            "end": 31,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 31,
            "end": 32,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 33,
            "end": 35,
            "surface": "아침",
            "canonical_vocab_id": "ko_k1_0072",
            "lemma": "아침",
            "pos": "noun",
            "sense": "morning",
            "sentence_raw": [
              {
                "form": "아침",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 35,
            "end": 36,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 37,
            "end": 39,
            "surface": "학교",
            "canonical_vocab_id": "ko_k1_0043",
            "lemma": "학교",
            "pos": "noun",
            "sense": "school",
            "sentence_raw": [
              {
                "form": "학교",
                "tag": "NNG",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 39,
            "end": 40,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 41,
            "end": 42,
            "surface": "가",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 41,
            "end": 43,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 45,
            "end": 47,
            "surface": "교실",
            "canonical_vocab_id": "ko_k1_0055",
            "lemma": "교실",
            "pos": "noun",
            "sense": "classroom",
            "sentence_raw": [
              {
                "form": "교실",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 47,
            "end": 48,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 49,
            "end": 51,
            "surface": "학교",
            "canonical_vocab_id": "ko_k1_0043",
            "lemma": "학교",
            "pos": "noun",
            "sense": "school",
            "sentence_raw": [
              {
                "form": "학교",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 52,
            "end": 53,
            "surface": "안",
            "canonical_vocab_id": "ko_k1_0060",
            "lemma": "안",
            "pos": "noun",
            "sense": "inside",
            "sentence_raw": [
              {
                "form": "안",
                "tag": "NNG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 53,
            "end": 54,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 55,
            "end": 56,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 56,
            "end": 58,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 60,
            "end": 62,
            "surface": "교실",
            "canonical_vocab_id": "ko_k1_0055",
            "lemma": "교실",
            "pos": "noun",
            "sense": "classroom",
            "sentence_raw": [
              {
                "form": "교실",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 62,
            "end": 63,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 63,
            "end": 64,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 65,
            "end": 67,
            "surface": "학생",
            "canonical_vocab_id": "ko_k1_0036",
            "lemma": "학생",
            "pos": "noun",
            "sense": "student",
            "sentence_raw": [
              {
                "form": "학생",
                "tag": "NNG",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 68,
            "end": 69,
            "surface": "세",
            "canonical_vocab_id": "ko_k1_0283",
            "lemma": "셋",
            "pos": "numeral",
            "sense": "three_native",
            "sentence_raw": [
              {
                "form": "세",
                "tag": "MM",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 70,
            "end": 71,
            "surface": "명",
            "canonical_vocab_id": "ko_k1_0468",
            "lemma": "명",
            "pos": "counter",
            "sense": "person_unit",
            "sentence_raw": [
              {
                "form": "명",
                "tag": "NNB",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 71,
            "end": 72,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 73,
            "end": 74,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 74,
            "end": 76,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 78,
            "end": 80,
            "surface": "교실",
            "canonical_vocab_id": "ko_k1_0055",
            "lemma": "교실",
            "pos": "noun",
            "sense": "classroom",
            "sentence_raw": [
              {
                "form": "교실",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 80,
            "end": 81,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 82,
            "end": 83,
            "surface": "작",
            "canonical_vocab_id": "ko_k1_0235",
            "lemma": "작다",
            "pos": "adjective",
            "sense": "small",
            "sentence_raw": [
              {
                "form": "작",
                "tag": "VA",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 83,
            "end": 85,
            "surface": "지만",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "지만",
                "tag": "EC",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 86,
            "end": 89,
            "surface": "깨끗해",
            "canonical_vocab_id": "ko_k1_0259",
            "lemma": "깨끗하다",
            "pos": "adjective",
            "sense": "clean",
            "sentence_raw": [
              {
                "form": "깨끗",
                "tag": "XR",
                "start": 8,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSA",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 88,
            "end": 90,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 93,
            "end": 94,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 94,
            "end": 95,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 96,
            "end": 97,
            "surface": "문",
            "canonical_vocab_id": "ko_k1_0109",
            "lemma": "문",
            "pos": "noun",
            "sense": "door",
            "sentence_raw": [
              {
                "form": "문",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 98,
            "end": 99,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 99,
            "end": 100,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 101,
            "end": 102,
            "surface": "앉",
            "canonical_vocab_id": "ko_k1_0184",
            "lemma": "앉다",
            "pos": "verb",
            "sense": "sit",
            "sentence_raw": [
              {
                "form": "앉",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 102,
            "end": 104,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 106,
            "end": 109,
            "surface": "선생님",
            "canonical_vocab_id": "ko_k1_0037",
            "lemma": "선생님",
            "pos": "noun",
            "sense": "teacher",
            "sentence_raw": [
              {
                "form": "선생",
                "tag": "NNG",
                "start": 0,
                "length": 2
              },
              {
                "form": "님",
                "tag": "XSN",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 109,
            "end": 110,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 111,
            "end": 112,
            "surface": "제",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 111,
            "end": 112,
            "surface": "제",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "의",
                "tag": "JKG",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 113,
            "end": 115,
            "surface": "이름",
            "canonical_vocab_id": "ko_k1_0039",
            "lemma": "이름",
            "pos": "noun",
            "sense": "name",
            "sentence_raw": [
              {
                "form": "이름",
                "tag": "NNG",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 115,
            "end": 116,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 117,
            "end": 118,
            "surface": "알",
            "canonical_vocab_id": "ko_k1_0207",
            "lemma": "알다",
            "pos": "verb",
            "sense": "know",
            "sentence_raw": [
              {
                "form": "알",
                "tag": "VV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 118,
            "end": 120,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 122,
            "end": 124,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 124,
            "end": 125,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 126,
            "end": 127,
            "surface": "제",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 126,
            "end": 127,
            "surface": "제",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "의",
                "tag": "JKG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 128,
            "end": 130,
            "surface": "이름",
            "canonical_vocab_id": "ko_k1_0039",
            "lemma": "이름",
            "pos": "noun",
            "sense": "name",
            "sentence_raw": [
              {
                "form": "이름",
                "tag": "NNG",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 130,
            "end": 131,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 132,
            "end": 133,
            "surface": "몰",
            "canonical_vocab_id": "ko_k1_0208",
            "lemma": "모르다",
            "pos": "verb",
            "sense": "not_know",
            "sentence_raw": [
              {
                "form": "모르",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 133,
            "end": 135,
            "surface": "라요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 137,
            "end": 138,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 138,
            "end": 139,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 140,
            "end": 142,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 142,
            "end": 144,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 145,
            "end": 147,
            "surface": "이름",
            "canonical_vocab_id": "ko_k1_0039",
            "lemma": "이름",
            "pos": "noun",
            "sense": "name",
            "sentence_raw": [
              {
                "form": "이름",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 147,
            "end": 148,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 149,
            "end": 151,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 12,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 150,
            "end": 152,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 154,
            "end": 156,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 156,
            "end": 157,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 158,
            "end": 159,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 159,
            "end": 161,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 162,
            "end": 164,
            "surface": "이름",
            "canonical_vocab_id": "ko_k1_0039",
            "lemma": "이름",
            "pos": "noun",
            "sense": "name",
            "sentence_raw": [
              {
                "form": "이름",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 164,
            "end": 165,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 166,
            "end": 168,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 12,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 167,
            "end": 169,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 171,
            "end": 173,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 173,
            "end": 174,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 175,
            "end": 176,
            "surface": "제",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 175,
            "end": 176,
            "surface": "제",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "의",
                "tag": "JKG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 177,
            "end": 178,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 178,
            "end": 179,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 180,
            "end": 181,
            "surface": "앉",
            "canonical_vocab_id": "ko_k1_0184",
            "lemma": "앉다",
            "pos": "verb",
            "sense": "sit",
            "sentence_raw": [
              {
                "form": "앉",
                "tag": "VV",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 181,
            "end": 183,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 186,
            "end": 189,
            "surface": "선생님",
            "canonical_vocab_id": "ko_k1_0037",
            "lemma": "선생님",
            "pos": "noun",
            "sense": "teacher",
            "sentence_raw": [
              {
                "form": "선생",
                "tag": "NNG",
                "start": 0,
                "length": 2
              },
              {
                "form": "님",
                "tag": "XSN",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 189,
            "end": 190,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 191,
            "end": 193,
            "surface": "수업",
            "canonical_vocab_id": "ko_k1_0142",
            "lemma": "수업",
            "pos": "noun",
            "sense": "class_lesson",
            "sentence_raw": [
              {
                "form": "수업",
                "tag": "NNG",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 193,
            "end": 194,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 195,
            "end": 198,
            "surface": "시작해",
            "canonical_vocab_id": "ko_k1_0200",
            "lemma": "시작하다",
            "pos": "verb",
            "sense": "start",
            "sentence_raw": [
              {
                "form": "시작",
                "tag": "NNG",
                "start": 9,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 197,
            "end": 199,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 201,
            "end": 202,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 202,
            "end": 203,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 204,
            "end": 207,
            "surface": "한국어",
            "canonical_vocab_id": "ko_k1_0169",
            "lemma": "한국어",
            "pos": "noun",
            "sense": "korean_language",
            "sentence_raw": [
              {
                "form": "한국어",
                "tag": "NNP",
                "start": 3,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 207,
            "end": 208,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 209,
            "end": 210,
            "surface": "잘",
            "canonical_vocab_id": "ko_k1_0266",
            "lemma": "잘",
            "pos": "adverb",
            "sense": "well",
            "sentence_raw": [
              {
                "form": "잘",
                "tag": "MAG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 211,
            "end": 212,
            "surface": "몰",
            "canonical_vocab_id": "ko_k1_0208",
            "lemma": "모르다",
            "pos": "verb",
            "sense": "not_know",
            "sentence_raw": [
              {
                "form": "모르",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 212,
            "end": 214,
            "surface": "라요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 216,
            "end": 219,
            "surface": "그래서",
            "canonical_vocab_id": "ko_k1_0279",
            "lemma": "그래서",
            "pos": "conjunction",
            "sense": "so",
            "sentence_raw": [
              {
                "form": "그래서",
                "tag": "MAJ",
                "start": 0,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 220,
            "end": 223,
            "surface": "선생님",
            "canonical_vocab_id": "ko_k1_0037",
            "lemma": "선생님",
            "pos": "noun",
            "sense": "teacher",
            "sentence_raw": [
              {
                "form": "선생",
                "tag": "NNG",
                "start": 4,
                "length": 2
              },
              {
                "form": "님",
                "tag": "XSN",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 224,
            "end": 225,
            "surface": "말",
            "canonical_vocab_id": "ko_k1_0133",
            "lemma": "말",
            "pos": "noun",
            "sense": "speech",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 225,
            "end": 226,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 227,
            "end": 228,
            "surface": "듣",
            "canonical_vocab_id": "ko_k1_0175",
            "lemma": "듣다",
            "pos": "verb",
            "sense": "hear_listen",
            "sentence_raw": [
              {
                "form": "듣",
                "tag": "VV-I",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 228,
            "end": 229,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 230,
            "end": 231,
            "surface": "있",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VX",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 231,
            "end": 233,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 235,
            "end": 238,
            "surface": "선생님",
            "canonical_vocab_id": "ko_k1_0037",
            "lemma": "선생님",
            "pos": "noun",
            "sense": "teacher",
            "sentence_raw": [
              {
                "form": "선생",
                "tag": "NNG",
                "start": 0,
                "length": 2
              },
              {
                "form": "님",
                "tag": "XSN",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 238,
            "end": 239,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 240,
            "end": 241,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 241,
            "end": 242,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 243,
            "end": 244,
            "surface": "보",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 244,
            "end": 245,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 246,
            "end": 248,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 11,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 247,
            "end": 249,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 252,
            "end": 254,
            "surface": "괜찮",
            "canonical_vocab_id": "ko_k1_0413",
            "lemma": "괜찮다",
            "pos": "adjective",
            "sense": "okay",
            "sentence_raw": [
              {
                "form": "괜찮",
                "tag": "VA",
                "start": 1,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 254,
            "end": 256,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 260,
            "end": 262,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 1,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 262,
            "end": 263,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 264,
            "end": 267,
            "surface": "한국어",
            "canonical_vocab_id": "ko_k1_0169",
            "lemma": "한국어",
            "pos": "noun",
            "sense": "korean_language",
            "sentence_raw": [
              {
                "form": "한국어",
                "tag": "NNP",
                "start": 5,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 267,
            "end": 268,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 269,
            "end": 271,
            "surface": "같이",
            "canonical_vocab_id": "ko_k1_0019",
            "lemma": "같이",
            "pos": "adverb",
            "sense": "together",
            "sentence_raw": [
              {
                "form": "같이",
                "tag": "MAG",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 272,
            "end": 274,
            "surface": "배울",
            "canonical_vocab_id": "ko_k1_0209",
            "lemma": "배우다",
            "pos": "verb",
            "sense": "learn",
            "sentence_raw": [
              {
                "form": "배우",
                "tag": "VV",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 273,
            "end": 274,
            "surface": "울",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆯ",
                "tag": "ETM",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 275,
            "end": 276,
            "surface": "거",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "거",
                "tag": "NNB",
                "start": 16,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 276,
            "end": 277,
            "surface": "예",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 17,
                "length": 0
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 276,
            "end": 278,
            "surface": "예요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "예요",
                "tag": "EF",
                "start": 17,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 282,
            "end": 285,
            "surface": "선생님",
            "canonical_vocab_id": "ko_k1_0037",
            "lemma": "선생님",
            "pos": "noun",
            "sense": "teacher",
            "sentence_raw": [
              {
                "form": "선생",
                "tag": "NNG",
                "start": 0,
                "length": 2
              },
              {
                "form": "님",
                "tag": "XSN",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 285,
            "end": 286,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 287,
            "end": 289,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 289,
            "end": 291,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 292,
            "end": 293,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 293,
            "end": 294,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 295,
            "end": 296,
            "surface": "줘",
            "canonical_vocab_id": "ko_k1_0192",
            "lemma": "주다",
            "pos": "verb",
            "sense": "give",
            "sentence_raw": [
              {
                "form": "주",
                "tag": "VV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 295,
            "end": 297,
            "surface": "줘요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 299,
            "end": 300,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 300,
            "end": 301,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 302,
            "end": 303,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 303,
            "end": 304,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 305,
            "end": 306,
            "surface": "보",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 306,
            "end": 307,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 308,
            "end": 310,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 9,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 309,
            "end": 311,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 314,
            "end": 315,
            "surface": "이",
            "canonical_vocab_id": "ko_k1_0444",
            "lemma": "이",
            "pos": "determiner",
            "sense": "this",
            "sentence_raw": [
              {
                "form": "이",
                "tag": "MM",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 316,
            "end": 317,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 317,
            "end": 318,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 319,
            "end": 320,
            "surface": "읽",
            "canonical_vocab_id": "ko_k1_0177",
            "lemma": "읽다",
            "pos": "verb",
            "sense": "read",
            "sentence_raw": [
              {
                "form": "읽",
                "tag": "VV",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 320,
            "end": 322,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 326,
            "end": 327,
            "surface": "네",
            "canonical_vocab_id": "ko_k1_0442",
            "lemma": "네",
            "pos": "interjection",
            "sense": "yes",
            "sentence_raw": [
              {
                "form": "네",
                "tag": "IC",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 331,
            "end": 332,
            "surface": "그",
            "canonical_vocab_id": "ko_k1_0445",
            "lemma": "그",
            "pos": "determiner",
            "sense": "that",
            "sentence_raw": [
              {
                "form": "그",
                "tag": "MM",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 333,
            "end": 334,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 334,
            "end": 335,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 336,
            "end": 339,
            "surface": "한국어",
            "canonical_vocab_id": "ko_k1_0169",
            "lemma": "한국어",
            "pos": "noun",
            "sense": "korean_language",
            "sentence_raw": [
              {
                "form": "한국어",
                "tag": "NNP",
                "start": 6,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 340,
            "end": 341,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 341,
            "end": 342,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 342,
            "end": 344,
            "surface": "에요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 347,
            "end": 348,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 348,
            "end": 349,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 350,
            "end": 351,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 351,
            "end": 352,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 353,
            "end": 354,
            "surface": "열",
            "canonical_vocab_id": "ko_k1_0194",
            "lemma": "열다",
            "pos": "verb",
            "sense": "open",
            "sentence_raw": [
              {
                "form": "열",
                "tag": "VV",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 354,
            "end": 355,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 356,
            "end": 357,
            "surface": "읽",
            "canonical_vocab_id": "ko_k1_0177",
            "lemma": "읽다",
            "pos": "verb",
            "sense": "read",
            "sentence_raw": [
              {
                "form": "읽",
                "tag": "VV",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 357,
            "end": 359,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 362,
            "end": 365,
            "surface": "선생님",
            "canonical_vocab_id": "ko_k1_0037",
            "lemma": "선생님",
            "pos": "noun",
            "sense": "teacher",
            "sentence_raw": [
              {
                "form": "선생",
                "tag": "NNG",
                "start": 0,
                "length": 2
              },
              {
                "form": "님",
                "tag": "XSN",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 365,
            "end": 366,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 367,
            "end": 368,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 368,
            "end": 369,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 370,
            "end": 371,
            "surface": "읽",
            "canonical_vocab_id": "ko_k1_0177",
            "lemma": "읽다",
            "pos": "verb",
            "sense": "read",
            "sentence_raw": [
              {
                "form": "읽",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 371,
            "end": 373,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 375,
            "end": 377,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 377,
            "end": 378,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 379,
            "end": 382,
            "surface": "선생님",
            "canonical_vocab_id": "ko_k1_0037",
            "lemma": "선생님",
            "pos": "noun",
            "sense": "teacher",
            "sentence_raw": [
              {
                "form": "선생",
                "tag": "NNG",
                "start": 4,
                "length": 2
              },
              {
                "form": "님",
                "tag": "XSN",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 383,
            "end": 384,
            "surface": "말",
            "canonical_vocab_id": "ko_k1_0133",
            "lemma": "말",
            "pos": "noun",
            "sense": "speech",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 384,
            "end": 385,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 386,
            "end": 387,
            "surface": "들",
            "canonical_vocab_id": "ko_k1_0175",
            "lemma": "듣다",
            "pos": "verb",
            "sense": "hear_listen",
            "sentence_raw": [
              {
                "form": "듣",
                "tag": "VV-I",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 387,
            "end": 389,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 391,
            "end": 394,
            "surface": "그리고",
            "canonical_vocab_id": "ko_k1_0276",
            "lemma": "그리고",
            "pos": "conjunction",
            "sense": "and_then",
            "sentence_raw": [
              {
                "form": "그리고",
                "tag": "MAJ",
                "start": 0,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 395,
            "end": 397,
            "surface": "공책",
            "canonical_vocab_id": "ko_k1_0102",
            "lemma": "공책",
            "pos": "noun",
            "sense": "notebook",
            "sentence_raw": [
              {
                "form": "공책",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 397,
            "end": 398,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 399,
            "end": 401,
            "surface": "이름",
            "canonical_vocab_id": "ko_k1_0039",
            "lemma": "이름",
            "pos": "noun",
            "sense": "name",
            "sentence_raw": [
              {
                "form": "이름",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 401,
            "end": 402,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 403,
            "end": 404,
            "surface": "써",
            "canonical_vocab_id": "ko_k1_0178",
            "lemma": "쓰다",
            "pos": "verb",
            "sense": "write",
            "sentence_raw": [
              {
                "form": "쓰",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 403,
            "end": 405,
            "surface": "써요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 407,
            "end": 409,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 409,
            "end": 410,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 411,
            "end": 413,
            "surface": "공책",
            "canonical_vocab_id": "ko_k1_0102",
            "lemma": "공책",
            "pos": "noun",
            "sense": "notebook",
            "sentence_raw": [
              {
                "form": "공책",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 413,
            "end": 414,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 415,
            "end": 417,
            "surface": "이름",
            "canonical_vocab_id": "ko_k1_0039",
            "lemma": "이름",
            "pos": "noun",
            "sense": "name",
            "sentence_raw": [
              {
                "form": "이름",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 417,
            "end": 418,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 419,
            "end": 420,
            "surface": "써",
            "canonical_vocab_id": "ko_k1_0178",
            "lemma": "쓰다",
            "pos": "verb",
            "sense": "write",
            "sentence_raw": [
              {
                "form": "쓰",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 419,
            "end": 421,
            "surface": "써요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 423,
            "end": 424,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 424,
            "end": 425,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 426,
            "end": 428,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 428,
            "end": 430,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 431,
            "end": 432,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 432,
            "end": 433,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 434,
            "end": 435,
            "surface": "봐",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 434,
            "end": 436,
            "surface": "봐요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 438,
            "end": 440,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 440,
            "end": 441,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 442,
            "end": 443,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 443,
            "end": 444,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 445,
            "end": 448,
            "surface": "도와줘",
            "canonical_vocab_id": "ko_k1_0225",
            "lemma": "도와주다",
            "pos": "verb",
            "sense": "help",
            "sentence_raw": [
              {
                "form": "도와주",
                "tag": "VV",
                "start": 7,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 447,
            "end": 449,
            "surface": "줘요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 452,
            "end": 454,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 454,
            "end": 455,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 456,
            "end": 458,
            "surface": "문제",
            "canonical_vocab_id": "ko_k1_0131",
            "lemma": "문제",
            "pos": "noun",
            "sense": "problem",
            "sentence_raw": [
              {
                "form": "문제",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 458,
            "end": 459,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 460,
            "end": 461,
            "surface": "읽",
            "canonical_vocab_id": "ko_k1_0177",
            "lemma": "읽다",
            "pos": "verb",
            "sense": "read",
            "sentence_raw": [
              {
                "form": "읽",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 461,
            "end": 462,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 463,
            "end": 464,
            "surface": "답",
            "canonical_vocab_id": "ko_k1_0132",
            "lemma": "답",
            "pos": "noun",
            "sense": "answer",
            "sentence_raw": [
              {
                "form": "답",
                "tag": "NNG",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 464,
            "end": 465,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 466,
            "end": 467,
            "surface": "찾",
            "canonical_vocab_id": "ko_k1_0211",
            "lemma": "찾다",
            "pos": "verb",
            "sense": "find_look_for",
            "sentence_raw": [
              {
                "form": "찾",
                "tag": "VV",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 467,
            "end": 469,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 471,
            "end": 473,
            "surface": "문제",
            "canonical_vocab_id": "ko_k1_0131",
            "lemma": "문제",
            "pos": "noun",
            "sense": "problem",
            "sentence_raw": [
              {
                "form": "문제",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 473,
            "end": 474,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 475,
            "end": 476,
            "surface": "쉽",
            "canonical_vocab_id": "ko_k1_0243",
            "lemma": "쉽다",
            "pos": "adjective",
            "sense": "easy",
            "sentence_raw": [
              {
                "form": "쉽",
                "tag": "VA-I",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 476,
            "end": 477,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 478,
            "end": 479,
            "surface": "답",
            "canonical_vocab_id": "ko_k1_0132",
            "lemma": "답",
            "pos": "noun",
            "sense": "answer",
            "sentence_raw": [
              {
                "form": "답",
                "tag": "NNG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 479,
            "end": 480,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 481,
            "end": 482,
            "surface": "알",
            "canonical_vocab_id": "ko_k1_0207",
            "lemma": "알다",
            "pos": "verb",
            "sense": "know",
            "sentence_raw": [
              {
                "form": "알",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 482,
            "end": 484,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 486,
            "end": 487,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 487,
            "end": 488,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 489,
            "end": 492,
            "surface": "한국어",
            "canonical_vocab_id": "ko_k1_0169",
            "lemma": "한국어",
            "pos": "noun",
            "sense": "korean_language",
            "sentence_raw": [
              {
                "form": "한국어",
                "tag": "NNP",
                "start": 3,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 492,
            "end": 493,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 494,
            "end": 495,
            "surface": "더",
            "canonical_vocab_id": "ko_k1_0449",
            "lemma": "더",
            "pos": "adverb",
            "sense": "more",
            "sentence_raw": [
              {
                "form": "더",
                "tag": "MAG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 496,
            "end": 498,
            "surface": "배우",
            "canonical_vocab_id": "ko_k1_0209",
            "lemma": "배우다",
            "pos": "verb",
            "sense": "learn",
            "sentence_raw": [
              {
                "form": "배우",
                "tag": "VV",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 498,
            "end": 499,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 500,
            "end": 501,
            "surface": "싶",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "싶",
                "tag": "VX",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 501,
            "end": 503,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 505,
            "end": 507,
            "surface": "수업",
            "canonical_vocab_id": "ko_k1_0142",
            "lemma": "수업",
            "pos": "noun",
            "sense": "class_lesson",
            "sentence_raw": [
              {
                "form": "수업",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 507,
            "end": 508,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 509,
            "end": 511,
            "surface": "끝나",
            "canonical_vocab_id": "ko_k1_0201",
            "lemma": "끝나다",
            "pos": "verb",
            "sense": "end_intransitive",
            "sentence_raw": [
              {
                "form": "끝나",
                "tag": "VV",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 511,
            "end": 512,
            "surface": "면",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "면",
                "tag": "EC",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 513,
            "end": 514,
            "surface": "책",
            "canonical_vocab_id": "ko_k1_0101",
            "lemma": "책",
            "pos": "noun",
            "sense": "book",
            "sentence_raw": [
              {
                "form": "책",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 514,
            "end": 515,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 516,
            "end": 518,
            "surface": "가방",
            "canonical_vocab_id": "ko_k1_0114",
            "lemma": "가방",
            "pos": "noun",
            "sense": "bag",
            "sentence_raw": [
              {
                "form": "가방",
                "tag": "NNG",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 518,
            "end": 519,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 520,
            "end": 521,
            "surface": "넣",
            "canonical_vocab_id": "ko_k1_0228",
            "lemma": "넣다",
            "pos": "verb",
            "sense": "put_in",
            "sentence_raw": [
              {
                "form": "넣",
                "tag": "VV",
                "start": 15,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 521,
            "end": 523,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 16,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 525,
            "end": 527,
            "surface": "내일",
            "canonical_vocab_id": "ko_k1_0070",
            "lemma": "내일",
            "pos": "noun",
            "sense": "tomorrow",
            "sentence_raw": [
              {
                "form": "내일",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 527,
            "end": 528,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 529,
            "end": 531,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 531,
            "end": 533,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 534,
            "end": 537,
            "surface": "공부할",
            "canonical_vocab_id": "ko_k1_0202",
            "lemma": "공부하다",
            "pos": "verb",
            "sense": "study",
            "sentence_raw": [
              {
                "form": "공부",
                "tag": "NNG",
                "start": 9,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 536,
            "end": 537,
            "surface": "할",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆯ",
                "tag": "ETM",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 538,
            "end": 539,
            "surface": "거",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "거",
                "tag": "NNB",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 539,
            "end": 540,
            "surface": "예",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 14,
                "length": 0
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 35,
            "start": 539,
            "end": 541,
            "surface": "예요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "예요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          }
        ],
        "scope_disagreements": [
          {
            "type": "scope_identity_disagreement_warning",
            "scope": "full_text",
            "start": 260,
            "end": 262,
            "surface": "우리",
            "sentence_identity": "ko_k1_0004",
            "diagnostic_identities": [
              "ko_k1_0004"
            ],
            "sentence_raw_pos": [
              "NP"
            ],
            "diagnostic_raw_pos": [
              "NNG"
            ],
            "id_disagreement": false,
            "pos_only_disagreement": true,
            "disagreement": true,
            "structural_defect": false,
            "decision": "WARNING_ONLY"
          },
          {
            "type": "scope_identity_disagreement_warning",
            "scope": "paragraph",
            "start": 260,
            "end": 262,
            "surface": "우리",
            "sentence_identity": "ko_k1_0004",
            "diagnostic_identities": [
              "ko_k1_0004"
            ],
            "sentence_raw_pos": [
              "NP"
            ],
            "diagnostic_raw_pos": [
              "NNG"
            ],
            "id_disagreement": false,
            "pos_only_disagreement": true,
            "disagreement": true,
            "structural_defect": false,
            "decision": "WARNING_ONLY"
          },
          {
            "type": "scope_identity_disagreement_warning",
            "scope": "full_text",
            "start": 326,
            "end": 327,
            "surface": "네",
            "sentence_identity": "ko_k1_0442",
            "diagnostic_identities": [
              "ko_k1_0442"
            ],
            "sentence_raw_pos": [
              "IC"
            ],
            "diagnostic_raw_pos": [
              "JKG",
              "NP"
            ],
            "id_disagreement": false,
            "pos_only_disagreement": true,
            "disagreement": true,
            "structural_defect": false,
            "decision": "WARNING_ONLY"
          },
          {
            "type": "scope_identity_disagreement_warning",
            "scope": "paragraph",
            "start": 326,
            "end": 327,
            "surface": "네",
            "sentence_identity": "ko_k1_0442",
            "diagnostic_identities": [
              "ko_k1_0442"
            ],
            "sentence_raw_pos": [
              "IC"
            ],
            "diagnostic_raw_pos": [
              "JKG",
              "NP"
            ],
            "id_disagreement": false,
            "pos_only_disagreement": true,
            "disagreement": true,
            "structural_defect": false,
            "decision": "WARNING_ONLY"
          }
        ],
        "credit": false
      },
      {
        "historical_phase": "3_6c",
        "text": 1,
        "source": "pilot\\ko\\k1\\phase3_6c\\candidates\\K1-001-attempt-01.json",
        "hard_pass": true,
        "hard_errors": [],
        "coverage": {
          "denominator_N": 133,
          "new_tokens_U": 2,
          "controlled_vocab_coverage": 1.0,
          "previous_vocab_coverage": 0.9849624060150376,
          "target_99_met": false
        },
        "canonical_lexical_map": [
          {
            "sentence_index": 1,
            "start": 0,
            "end": 1,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 1,
            "end": 2,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 3,
            "end": 5,
            "surface": "아침",
            "canonical_vocab_id": "ko_k1_0072",
            "lemma": "아침",
            "pos": "noun",
            "sense": "morning",
            "sentence_raw": [
              {
                "form": "아침",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 5,
            "end": 7,
            "surface": "부터",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "부터",
                "tag": "JX",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 8,
            "end": 10,
            "surface": "회사",
            "canonical_vocab_id": "ko_k1_0044",
            "lemma": "회사",
            "pos": "noun",
            "sense": "company",
            "sentence_raw": [
              {
                "form": "회사",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 10,
            "end": 12,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 13,
            "end": 15,
            "surface": "일해",
            "canonical_vocab_id": "ko_k1_0203",
            "lemma": "일하다",
            "pos": "verb",
            "sense": "work",
            "sentence_raw": [
              {
                "form": "일",
                "tag": "NNG",
                "start": 13,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 14,
            "end": 16,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 18,
            "end": 20,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 20,
            "end": 21,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 22,
            "end": 24,
            "surface": "회사",
            "canonical_vocab_id": "ko_k1_0044",
            "lemma": "회사",
            "pos": "noun",
            "sense": "company",
            "sentence_raw": [
              {
                "form": "회사",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 24,
            "end": 26,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 27,
            "end": 29,
            "surface": "일하",
            "canonical_vocab_id": "ko_k1_0203",
            "lemma": "일하다",
            "pos": "verb",
            "sense": "work",
            "sentence_raw": [
              {
                "form": "일",
                "tag": "NNG",
                "start": 9,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 29,
            "end": 30,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 31,
            "end": 32,
            "surface": "있",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VX",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 32,
            "end": 34,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 36,
            "end": 38,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 38,
            "end": 39,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 40,
            "end": 41,
            "surface": "제",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 40,
            "end": 41,
            "surface": "제",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "의",
                "tag": "JKG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 42,
            "end": 43,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 43,
            "end": 44,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 45,
            "end": 46,
            "surface": "앉",
            "canonical_vocab_id": "ko_k1_0184",
            "lemma": "앉다",
            "pos": "verb",
            "sense": "sit",
            "sentence_raw": [
              {
                "form": "앉",
                "tag": "VV",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 46,
            "end": 48,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 50,
            "end": 51,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 51,
            "end": 52,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 53,
            "end": 56,
            "surface": "컴퓨터",
            "canonical_vocab_id": "ko_k1_0107",
            "lemma": "컴퓨터",
            "pos": "noun",
            "sense": "computer",
            "sentence_raw": [
              {
                "form": "컴퓨터",
                "tag": "NNG",
                "start": 3,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 56,
            "end": 57,
            "surface": "로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "로",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 58,
            "end": 59,
            "surface": "일",
            "canonical_vocab_id": "ko_k1_0135",
            "lemma": "일",
            "pos": "noun",
            "sense": "work",
            "sentence_raw": [
              {
                "form": "일",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 59,
            "end": 60,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 61,
            "end": 62,
            "surface": "해",
            "canonical_vocab_id": "ko_k1_0179",
            "lemma": "하다",
            "pos": "verb",
            "sense": "do",
            "sentence_raw": [
              {
                "form": "하",
                "tag": "VV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 61,
            "end": 63,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 65,
            "end": 67,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 67,
            "end": 68,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 69,
            "end": 71,
            "surface": "종이",
            "canonical_vocab_id": "ko_k1_0103",
            "lemma": "종이",
            "pos": "noun",
            "sense": "paper",
            "sentence_raw": [
              {
                "form": "종이",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 71,
            "end": 72,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 73,
            "end": 75,
            "surface": "이름",
            "canonical_vocab_id": "ko_k1_0039",
            "lemma": "이름",
            "pos": "noun",
            "sense": "name",
            "sentence_raw": [
              {
                "form": "이름",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 75,
            "end": 76,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 77,
            "end": 78,
            "surface": "써",
            "canonical_vocab_id": "ko_k1_0178",
            "lemma": "쓰다",
            "pos": "verb",
            "sense": "write",
            "sentence_raw": [
              {
                "form": "쓰",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 77,
            "end": 79,
            "surface": "써요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 81,
            "end": 83,
            "surface": "점심",
            "canonical_vocab_id": "ko_k1_0073",
            "lemma": "점심",
            "pos": "noun",
            "sense": "lunch",
            "sentence_raw": [
              {
                "form": "점심",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 84,
            "end": 86,
            "surface": "시간",
            "canonical_vocab_id": "ko_k1_0076",
            "lemma": "시간",
            "pos": "noun",
            "sense": "time",
            "sentence_raw": [
              {
                "form": "시간",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 86,
            "end": 87,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKC",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 88,
            "end": 89,
            "surface": "됐",
            "canonical_vocab_id": "ko_k1_0373",
            "lemma": "되다",
            "pos": "verb",
            "sense": "become",
            "sentence_raw": [
              {
                "form": "되",
                "tag": "VV",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 88,
            "end": 89,
            "surface": "됐",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "었",
                "tag": "EP",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 89,
            "end": 91,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 94,
            "end": 95,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 95,
            "end": 96,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 97,
            "end": 100,
            "surface": "컴퓨터",
            "canonical_vocab_id": "ko_k1_0107",
            "lemma": "컴퓨터",
            "pos": "noun",
            "sense": "computer",
            "sentence_raw": [
              {
                "form": "컴퓨터",
                "tag": "NNG",
                "start": 3,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 101,
            "end": 102,
            "surface": "앞",
            "canonical_vocab_id": "ko_k1_0061",
            "lemma": "앞",
            "pos": "noun",
            "sense": "front",
            "sentence_raw": [
              {
                "form": "앞",
                "tag": "NNG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 102,
            "end": 104,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 105,
            "end": 108,
            "surface": "일어나",
            "canonical_vocab_id": "ko_k1_0183",
            "lemma": "일어나다",
            "pos": "verb",
            "sense": "get_up",
            "sentence_raw": [
              {
                "form": "일어나",
                "tag": "VV",
                "start": 11,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 107,
            "end": 109,
            "surface": "나요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 111,
            "end": 114,
            "surface": "그리고",
            "canonical_vocab_id": "ko_k1_0276",
            "lemma": "그리고",
            "pos": "conjunction",
            "sense": "and_then",
            "sentence_raw": [
              {
                "form": "그리고",
                "tag": "MAJ",
                "start": 0,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 115,
            "end": 117,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 117,
            "end": 119,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 120,
            "end": 122,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 9,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 121,
            "end": 123,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 10,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 126,
            "end": 128,
            "surface": "식당",
            "canonical_vocab_id": "ko_k1_0046",
            "lemma": "식당",
            "pos": "noun",
            "sense": "restaurant",
            "sentence_raw": [
              {
                "form": "식당",
                "tag": "NNG",
                "start": 1,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 128,
            "end": 130,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 131,
            "end": 132,
            "surface": "밥",
            "canonical_vocab_id": "ko_k1_0120",
            "lemma": "밥",
            "pos": "noun",
            "sense": "cooked_rice_meal",
            "sentence_raw": [
              {
                "form": "밥",
                "tag": "NNG",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 132,
            "end": 133,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 134,
            "end": 135,
            "surface": "먹",
            "canonical_vocab_id": "ko_k1_0172",
            "lemma": "먹다",
            "pos": "verb",
            "sense": "eat",
            "sentence_raw": [
              {
                "form": "먹",
                "tag": "VV",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 135,
            "end": 136,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "ETM",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 137,
            "end": 138,
            "surface": "거",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "거",
                "tag": "NNB",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 138,
            "end": 139,
            "surface": "예",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 13,
                "length": 0
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 138,
            "end": 140,
            "surface": "예요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "예요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 143,
            "end": 145,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 145,
            "end": 146,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 147,
            "end": 149,
            "surface": "종이",
            "canonical_vocab_id": "ko_k1_0103",
            "lemma": "종이",
            "pos": "noun",
            "sense": "paper",
            "sentence_raw": [
              {
                "form": "종이",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 149,
            "end": 150,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 151,
            "end": 152,
            "surface": "보",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 152,
            "end": 153,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 154,
            "end": 156,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 11,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 155,
            "end": 157,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 160,
            "end": 161,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 161,
            "end": 162,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 163,
            "end": 164,
            "surface": "일",
            "canonical_vocab_id": "ko_k1_0135",
            "lemma": "일",
            "pos": "noun",
            "sense": "work",
            "sentence_raw": [
              {
                "form": "일",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 164,
            "end": 165,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 166,
            "end": 168,
            "surface": "많이",
            "canonical_vocab_id": "ko_k1_0267",
            "lemma": "많이",
            "pos": "adverb",
            "sense": "a_lot",
            "sentence_raw": [
              {
                "form": "많이",
                "tag": "MAG",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 169,
            "end": 170,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 170,
            "end": 172,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 176,
            "end": 177,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 177,
            "end": 178,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 179,
            "end": 180,
            "surface": "일",
            "canonical_vocab_id": "ko_k1_0135",
            "lemma": "일",
            "pos": "noun",
            "sense": "work",
            "sentence_raw": [
              {
                "form": "일",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 180,
            "end": 181,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 182,
            "end": 183,
            "surface": "하",
            "canonical_vocab_id": "ko_k1_0179",
            "lemma": "하다",
            "pos": "verb",
            "sense": "do",
            "sentence_raw": [
              {
                "form": "하",
                "tag": "VV",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 183,
            "end": 184,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 185,
            "end": 186,
            "surface": "갈",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 185,
            "end": 186,
            "surface": "갈",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆯ",
                "tag": "ETM",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 187,
            "end": 188,
            "surface": "거",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "거",
                "tag": "NNB",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 188,
            "end": 189,
            "surface": "예",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 13,
                "length": 0
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 188,
            "end": 190,
            "surface": "예요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "예요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 194,
            "end": 195,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 195,
            "end": 196,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 197,
            "end": 199,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 199,
            "end": 201,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 202,
            "end": 204,
            "surface": "다시",
            "canonical_vocab_id": "ko_k1_0274",
            "lemma": "다시",
            "pos": "adverb",
            "sense": "again",
            "sentence_raw": [
              {
                "form": "다시",
                "tag": "MAG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 205,
            "end": 207,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 11,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 206,
            "end": 208,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 211,
            "end": 213,
            "surface": "괜찮",
            "canonical_vocab_id": "ko_k1_0413",
            "lemma": "괜찮다",
            "pos": "adjective",
            "sense": "okay",
            "sentence_raw": [
              {
                "form": "괜찮",
                "tag": "VA",
                "start": 1,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 213,
            "end": 215,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 219,
            "end": 220,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 220,
            "end": 221,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 222,
            "end": 224,
            "surface": "시간",
            "canonical_vocab_id": "ko_k1_0076",
            "lemma": "시간",
            "pos": "noun",
            "sense": "time",
            "sentence_raw": [
              {
                "form": "시간",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 224,
            "end": 225,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 226,
            "end": 227,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 227,
            "end": 229,
            "surface": "어서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어서",
                "tag": "EC",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 230,
            "end": 233,
            "surface": "기다릴",
            "canonical_vocab_id": "ko_k1_0189",
            "lemma": "기다리다",
            "pos": "verb",
            "sense": "wait",
            "sentence_raw": [
              {
                "form": "기다리",
                "tag": "VV",
                "start": 12,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 232,
            "end": 233,
            "surface": "릴",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆯ",
                "tag": "ETM",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 234,
            "end": 235,
            "surface": "거",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "거",
                "tag": "NNB",
                "start": 16,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 235,
            "end": 236,
            "surface": "예",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 17,
                "length": 0
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 235,
            "end": 237,
            "surface": "예요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "예요",
                "tag": "EF",
                "start": 17,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 240,
            "end": 241,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 241,
            "end": 242,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 243,
            "end": 245,
            "surface": "책상",
            "canonical_vocab_id": "ko_k1_0112",
            "lemma": "책상",
            "pos": "noun",
            "sense": "desk",
            "sentence_raw": [
              {
                "form": "책상",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 246,
            "end": 247,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 247,
            "end": 249,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 250,
            "end": 251,
            "surface": "물",
            "canonical_vocab_id": "ko_k1_0119",
            "lemma": "물",
            "pos": "noun",
            "sense": "water",
            "sentence_raw": [
              {
                "form": "물",
                "tag": "NNG",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 251,
            "end": 252,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 253,
            "end": 255,
            "surface": "마셔",
            "canonical_vocab_id": "ko_k1_0173",
            "lemma": "마시다",
            "pos": "verb",
            "sense": "drink",
            "sentence_raw": [
              {
                "form": "마시",
                "tag": "VV",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 254,
            "end": 256,
            "surface": "셔요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 258,
            "end": 260,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 260,
            "end": 261,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 262,
            "end": 264,
            "surface": "종이",
            "canonical_vocab_id": "ko_k1_0103",
            "lemma": "종이",
            "pos": "noun",
            "sense": "paper",
            "sentence_raw": [
              {
                "form": "종이",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 264,
            "end": 265,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 266,
            "end": 268,
            "surface": "이름",
            "canonical_vocab_id": "ko_k1_0039",
            "lemma": "이름",
            "pos": "noun",
            "sense": "name",
            "sentence_raw": [
              {
                "form": "이름",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 268,
            "end": 269,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 270,
            "end": 272,
            "surface": "다시",
            "canonical_vocab_id": "ko_k1_0274",
            "lemma": "다시",
            "pos": "adverb",
            "sense": "again",
            "sentence_raw": [
              {
                "form": "다시",
                "tag": "MAG",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 273,
            "end": 274,
            "surface": "써",
            "canonical_vocab_id": "ko_k1_0178",
            "lemma": "쓰다",
            "pos": "verb",
            "sense": "write",
            "sentence_raw": [
              {
                "form": "쓰",
                "tag": "VV",
                "start": 15,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 273,
            "end": 275,
            "surface": "써요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 277,
            "end": 279,
            "surface": "이름",
            "canonical_vocab_id": "ko_k1_0039",
            "lemma": "이름",
            "pos": "noun",
            "sense": "name",
            "sentence_raw": [
              {
                "form": "이름",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 279,
            "end": 280,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 281,
            "end": 282,
            "surface": "많",
            "canonical_vocab_id": "ko_k1_0236",
            "lemma": "많다",
            "pos": "adjective",
            "sense": "many",
            "sentence_raw": [
              {
                "form": "많",
                "tag": "VA",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 282,
            "end": 284,
            "surface": "아서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어서",
                "tag": "EC",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 285,
            "end": 287,
            "surface": "시간",
            "canonical_vocab_id": "ko_k1_0076",
            "lemma": "시간",
            "pos": "noun",
            "sense": "time",
            "sentence_raw": [
              {
                "form": "시간",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 287,
            "end": 288,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 289,
            "end": 292,
            "surface": "필요해",
            "canonical_vocab_id": "ko_k1_0222",
            "lemma": "필요하다",
            "pos": "adjective",
            "sense": "necessary",
            "sentence_raw": [
              {
                "form": "필요",
                "tag": "NNG",
                "start": 12,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSA",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 291,
            "end": 293,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 296,
            "end": 297,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 297,
            "end": 298,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 299,
            "end": 301,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 302,
            "end": 303,
            "surface": "일",
            "canonical_vocab_id": "ko_k1_0135",
            "lemma": "일",
            "pos": "noun",
            "sense": "work",
            "sentence_raw": [
              {
                "form": "일",
                "tag": "NNG",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 303,
            "end": 304,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 305,
            "end": 308,
            "surface": "도와줘",
            "canonical_vocab_id": "ko_k1_0225",
            "lemma": "도와주다",
            "pos": "verb",
            "sense": "help",
            "sentence_raw": [
              {
                "form": "돕",
                "tag": "VV-I",
                "start": 9,
                "length": 1
              },
              {
                "form": "어",
                "tag": "EC",
                "start": 10,
                "length": 1
              },
              {
                "form": "주",
                "tag": "VX",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 307,
            "end": 309,
            "surface": "줘요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 311,
            "end": 313,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 313,
            "end": 314,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 315,
            "end": 316,
            "surface": "제",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 315,
            "end": 316,
            "surface": "제",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "의",
                "tag": "JKG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 317,
            "end": 318,
            "surface": "말",
            "canonical_vocab_id": "ko_k1_0133",
            "lemma": "말",
            "pos": "noun",
            "sense": "speech",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 318,
            "end": 319,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 320,
            "end": 321,
            "surface": "듣",
            "canonical_vocab_id": "ko_k1_0175",
            "lemma": "듣다",
            "pos": "verb",
            "sense": "hear_listen",
            "sentence_raw": [
              {
                "form": "듣",
                "tag": "VV-I",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 321,
            "end": 322,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 323,
            "end": 324,
            "surface": "써",
            "canonical_vocab_id": "ko_k1_0178",
            "lemma": "쓰다",
            "pos": "verb",
            "sense": "write",
            "sentence_raw": [
              {
                "form": "쓰",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 323,
            "end": 325,
            "surface": "써요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 327,
            "end": 329,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 330,
            "end": 331,
            "surface": "일",
            "canonical_vocab_id": "ko_k1_0135",
            "lemma": "일",
            "pos": "noun",
            "sense": "work",
            "sentence_raw": [
              {
                "form": "일",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 331,
            "end": 332,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 333,
            "end": 335,
            "surface": "끝났",
            "canonical_vocab_id": "ko_k1_0201",
            "lemma": "끝나다",
            "pos": "verb",
            "sense": "end_intransitive",
            "sentence_raw": [
              {
                "form": "끝나",
                "tag": "VV",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 334,
            "end": 335,
            "surface": "났",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "었",
                "tag": "EP",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 335,
            "end": 337,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 339,
            "end": 341,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 341,
            "end": 342,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 343,
            "end": 345,
            "surface": "회사",
            "canonical_vocab_id": "ko_k1_0044",
            "lemma": "회사",
            "pos": "noun",
            "sense": "company",
            "sentence_raw": [
              {
                "form": "회사",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 346,
            "end": 347,
            "surface": "밖",
            "canonical_vocab_id": "ko_k1_0059",
            "lemma": "밖",
            "pos": "noun",
            "sense": "outside",
            "sentence_raw": [
              {
                "form": "밖",
                "tag": "NNG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 347,
            "end": 349,
            "surface": "으로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "으로",
                "tag": "JKB",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 350,
            "end": 352,
            "surface": "나가",
            "canonical_vocab_id": "ko_k1_0216",
            "lemma": "나가다",
            "pos": "verb",
            "sense": "go_out",
            "sentence_raw": [
              {
                "form": "나가",
                "tag": "VV",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 351,
            "end": 353,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 355,
            "end": 357,
            "surface": "회사",
            "canonical_vocab_id": "ko_k1_0044",
            "lemma": "회사",
            "pos": "noun",
            "sense": "company",
            "sentence_raw": [
              {
                "form": "회사",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 358,
            "end": 359,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 359,
            "end": 360,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 361,
            "end": 363,
            "surface": "식당",
            "canonical_vocab_id": "ko_k1_0046",
            "lemma": "식당",
            "pos": "noun",
            "sense": "restaurant",
            "sentence_raw": [
              {
                "form": "식당",
                "tag": "NNG",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 363,
            "end": 364,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 365,
            "end": 366,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 366,
            "end": 368,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 370,
            "end": 372,
            "surface": "식당",
            "canonical_vocab_id": "ko_k1_0046",
            "lemma": "식당",
            "pos": "noun",
            "sense": "restaurant",
            "sentence_raw": [
              {
                "form": "식당",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 372,
            "end": 373,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 373,
            "end": 374,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 375,
            "end": 377,
            "surface": "손님",
            "canonical_vocab_id": "ko_k1_0038",
            "lemma": "손님",
            "pos": "noun",
            "sense": "guest_customer",
            "sentence_raw": [
              {
                "form": "손",
                "tag": "NNG",
                "start": 5,
                "length": 1
              },
              {
                "form": "님",
                "tag": "XSN",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 377,
            "end": 378,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 379,
            "end": 381,
            "surface": "많이",
            "canonical_vocab_id": "ko_k1_0267",
            "lemma": "많이",
            "pos": "adverb",
            "sense": "a_lot",
            "sentence_raw": [
              {
                "form": "많이",
                "tag": "MAG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 382,
            "end": 383,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 383,
            "end": 385,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 388,
            "end": 390,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 390,
            "end": 391,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 392,
            "end": 394,
            "surface": "창문",
            "canonical_vocab_id": "ko_k1_0110",
            "lemma": "창문",
            "pos": "noun",
            "sense": "window",
            "sentence_raw": [
              {
                "form": "창문",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 395,
            "end": 396,
            "surface": "앞",
            "canonical_vocab_id": "ko_k1_0061",
            "lemma": "앞",
            "pos": "noun",
            "sense": "front",
            "sentence_raw": [
              {
                "form": "앞",
                "tag": "NNG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 396,
            "end": 397,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 398,
            "end": 399,
            "surface": "앉",
            "canonical_vocab_id": "ko_k1_0184",
            "lemma": "앉다",
            "pos": "verb",
            "sense": "sit",
            "sentence_raw": [
              {
                "form": "앉",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 399,
            "end": 401,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 403,
            "end": 404,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 404,
            "end": 405,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 406,
            "end": 407,
            "surface": "밥",
            "canonical_vocab_id": "ko_k1_0120",
            "lemma": "밥",
            "pos": "noun",
            "sense": "cooked_rice_meal",
            "sentence_raw": [
              {
                "form": "밥",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 407,
            "end": 409,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하",
                "tag": "XSV",
                "start": 4,
                "length": 1
              },
              {
                "form": "고",
                "tag": "EC",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 410,
            "end": 412,
            "surface": "채소",
            "canonical_vocab_id": "ko_k1_0125",
            "lemma": "채소",
            "pos": "noun",
            "sense": "vegetable",
            "sentence_raw": [
              {
                "form": "채소",
                "tag": "NNG",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 412,
            "end": 413,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 414,
            "end": 415,
            "surface": "먹",
            "canonical_vocab_id": "ko_k1_0172",
            "lemma": "먹다",
            "pos": "verb",
            "sense": "eat",
            "sentence_raw": [
              {
                "form": "먹",
                "tag": "VV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 415,
            "end": 417,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 419,
            "end": 421,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 421,
            "end": 422,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 423,
            "end": 424,
            "surface": "밥",
            "canonical_vocab_id": "ko_k1_0120",
            "lemma": "밥",
            "pos": "noun",
            "sense": "cooked_rice_meal",
            "sentence_raw": [
              {
                "form": "밥",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 424,
            "end": 426,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하",
                "tag": "XSV",
                "start": 5,
                "length": 1
              },
              {
                "form": "고",
                "tag": "EC",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 427,
            "end": 429,
            "surface": "고기",
            "canonical_vocab_id": "ko_k1_0124",
            "lemma": "고기",
            "pos": "noun",
            "sense": "meat",
            "sentence_raw": [
              {
                "form": "고기",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 429,
            "end": 430,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 431,
            "end": 432,
            "surface": "먹",
            "canonical_vocab_id": "ko_k1_0172",
            "lemma": "먹다",
            "pos": "verb",
            "sense": "eat",
            "sentence_raw": [
              {
                "form": "먹",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 432,
            "end": 434,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 436,
            "end": 437,
            "surface": "밥",
            "canonical_vocab_id": "ko_k1_0120",
            "lemma": "밥",
            "pos": "noun",
            "sense": "cooked_rice_meal",
            "sentence_raw": [
              {
                "form": "밥",
                "tag": "NNG",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 437,
            "end": 438,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 439,
            "end": 442,
            "surface": "따뜻하",
            "canonical_vocab_id": "ko_k1_0253",
            "lemma": "따뜻하다",
            "pos": "adjective",
            "sense": "warm",
            "sentence_raw": [
              {
                "form": "따뜻",
                "tag": "XR",
                "start": 3,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSA",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 442,
            "end": 443,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 444,
            "end": 446,
            "surface": "고기",
            "canonical_vocab_id": "ko_k1_0124",
            "lemma": "고기",
            "pos": "noun",
            "sense": "meat",
            "sentence_raw": [
              {
                "form": "고기",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 446,
            "end": 447,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 448,
            "end": 450,
            "surface": "맛있",
            "canonical_vocab_id": "ko_k1_0247",
            "lemma": "맛있다",
            "pos": "adjective",
            "sense": "tasty",
            "sentence_raw": [
              {
                "form": "맛있",
                "tag": "VA",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 450,
            "end": 452,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 454,
            "end": 456,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 456,
            "end": 457,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 458,
            "end": 459,
            "surface": "밥",
            "canonical_vocab_id": "ko_k1_0120",
            "lemma": "밥",
            "pos": "noun",
            "sense": "cooked_rice_meal",
            "sentence_raw": [
              {
                "form": "밥",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 459,
            "end": 460,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 461,
            "end": 462,
            "surface": "먹",
            "canonical_vocab_id": "ko_k1_0172",
            "lemma": "먹다",
            "pos": "verb",
            "sense": "eat",
            "sentence_raw": [
              {
                "form": "먹",
                "tag": "VV",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 462,
            "end": 463,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 464,
            "end": 465,
            "surface": "쉬",
            "canonical_vocab_id": "ko_k1_0224",
            "lemma": "쉬다",
            "pos": "verb",
            "sense": "rest",
            "sentence_raw": [
              {
                "form": "쉬",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 465,
            "end": 467,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 469,
            "end": 470,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 470,
            "end": 471,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 472,
            "end": 473,
            "surface": "물",
            "canonical_vocab_id": "ko_k1_0119",
            "lemma": "물",
            "pos": "noun",
            "sense": "water",
            "sentence_raw": [
              {
                "form": "물",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 473,
            "end": 474,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 475,
            "end": 477,
            "surface": "마시",
            "canonical_vocab_id": "ko_k1_0173",
            "lemma": "마시다",
            "pos": "verb",
            "sense": "drink",
            "sentence_raw": [
              {
                "form": "마시",
                "tag": "VV",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 477,
            "end": 478,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 479,
            "end": 480,
            "surface": "쉬",
            "canonical_vocab_id": "ko_k1_0224",
            "lemma": "쉬다",
            "pos": "verb",
            "sense": "rest",
            "sentence_raw": [
              {
                "form": "쉬",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 480,
            "end": 482,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 485,
            "end": 487,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 487,
            "end": 488,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 489,
            "end": 491,
            "surface": "회사",
            "canonical_vocab_id": "ko_k1_0044",
            "lemma": "회사",
            "pos": "noun",
            "sense": "company",
            "sentence_raw": [
              {
                "form": "회사",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 492,
            "end": 495,
            "surface": "이야기",
            "canonical_vocab_id": "ko_k1_0134",
            "lemma": "이야기",
            "pos": "noun",
            "sense": "story_talk",
            "sentence_raw": [
              {
                "form": "이야기",
                "tag": "NNG",
                "start": 7,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 495,
            "end": 496,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 497,
            "end": 498,
            "surface": "해",
            "canonical_vocab_id": "ko_k1_0179",
            "lemma": "하다",
            "pos": "verb",
            "sense": "do",
            "sentence_raw": [
              {
                "form": "하",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 497,
            "end": 499,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 501,
            "end": 503,
            "surface": "식당",
            "canonical_vocab_id": "ko_k1_0046",
            "lemma": "식당",
            "pos": "noun",
            "sense": "restaurant",
            "sentence_raw": [
              {
                "form": "식당",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 503,
            "end": 505,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 2,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 506,
            "end": 507,
            "surface": "쉬",
            "canonical_vocab_id": "ko_k1_0224",
            "lemma": "쉬다",
            "pos": "verb",
            "sense": "rest",
            "sentence_raw": [
              {
                "form": "쉬",
                "tag": "VV",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 507,
            "end": 509,
            "surface": "니까",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "니까",
                "tag": "EC",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 510,
            "end": 512,
            "surface": "다시",
            "canonical_vocab_id": "ko_k1_0274",
            "lemma": "다시",
            "pos": "adverb",
            "sense": "again",
            "sentence_raw": [
              {
                "form": "다시",
                "tag": "MAG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 513,
            "end": 515,
            "surface": "일할",
            "canonical_vocab_id": "ko_k1_0203",
            "lemma": "일하다",
            "pos": "verb",
            "sense": "work",
            "sentence_raw": [
              {
                "form": "일",
                "tag": "NNG",
                "start": 12,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 514,
            "end": 515,
            "surface": "할",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆯ",
                "tag": "ETM",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 516,
            "end": 517,
            "surface": "수",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "수",
                "tag": "NNB",
                "start": 15,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 518,
            "end": 519,
            "surface": "있",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 17,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 519,
            "end": 521,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 18,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 523,
            "end": 524,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 524,
            "end": 525,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 526,
            "end": 528,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 528,
            "end": 530,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 531,
            "end": 533,
            "surface": "회사",
            "canonical_vocab_id": "ko_k1_0044",
            "lemma": "회사",
            "pos": "noun",
            "sense": "company",
            "sentence_raw": [
              {
                "form": "회사",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 533,
            "end": 534,
            "surface": "로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "로",
                "tag": "JKB",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 535,
            "end": 538,
            "surface": "돌아가",
            "canonical_vocab_id": "ko_k1_0214",
            "lemma": "돌아가다",
            "pos": "verb",
            "sense": "go_back",
            "sentence_raw": [
              {
                "form": "돌아가",
                "tag": "VV",
                "start": 12,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 537,
            "end": 539,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 541,
            "end": 543,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 543,
            "end": 544,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 545,
            "end": 547,
            "surface": "책상",
            "canonical_vocab_id": "ko_k1_0112",
            "lemma": "책상",
            "pos": "noun",
            "sense": "desk",
            "sentence_raw": [
              {
                "form": "책상",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 547,
            "end": 548,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 549,
            "end": 550,
            "surface": "앉",
            "canonical_vocab_id": "ko_k1_0184",
            "lemma": "앉다",
            "pos": "verb",
            "sense": "sit",
            "sentence_raw": [
              {
                "form": "앉",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 550,
            "end": 551,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 552,
            "end": 553,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 553,
            "end": 554,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 555,
            "end": 558,
            "surface": "컴퓨터",
            "canonical_vocab_id": "ko_k1_0107",
            "lemma": "컴퓨터",
            "pos": "noun",
            "sense": "computer",
            "sentence_raw": [
              {
                "form": "컴퓨터",
                "tag": "NNG",
                "start": 14,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 558,
            "end": 559,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 17,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 560,
            "end": 561,
            "surface": "봐",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 19,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 560,
            "end": 562,
            "surface": "봐요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 19,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          }
        ],
        "scope_disagreements": [
          {
            "type": "scope_identity_disagreement_warning",
            "scope": "full_text",
            "start": 176,
            "end": 177,
            "surface": "저",
            "sentence_identity": "ko_k1_0002",
            "diagnostic_identities": [
              "ko_k1_0446"
            ],
            "sentence_raw_pos": [
              "NP"
            ],
            "diagnostic_raw_pos": [
              "MM"
            ],
            "id_disagreement": true,
            "pos_only_disagreement": false,
            "disagreement": true,
            "structural_defect": false,
            "decision": "WARNING_ONLY"
          },
          {
            "type": "scope_identity_disagreement_warning",
            "scope": "paragraph",
            "start": 176,
            "end": 177,
            "surface": "저",
            "sentence_identity": "ko_k1_0002",
            "diagnostic_identities": [
              "ko_k1_0446"
            ],
            "sentence_raw_pos": [
              "NP"
            ],
            "diagnostic_raw_pos": [
              "MM"
            ],
            "id_disagreement": true,
            "pos_only_disagreement": false,
            "disagreement": true,
            "structural_defect": false,
            "decision": "WARNING_ONLY"
          },
          {
            "type": "scope_identity_disagreement_warning",
            "scope": "full_text",
            "start": 219,
            "end": 220,
            "surface": "저",
            "sentence_identity": "ko_k1_0002",
            "diagnostic_identities": [
              "ko_k1_0446"
            ],
            "sentence_raw_pos": [
              "NP"
            ],
            "diagnostic_raw_pos": [
              "MM"
            ],
            "id_disagreement": true,
            "pos_only_disagreement": false,
            "disagreement": true,
            "structural_defect": false,
            "decision": "WARNING_ONLY"
          },
          {
            "type": "scope_identity_disagreement_warning",
            "scope": "paragraph",
            "start": 219,
            "end": 220,
            "surface": "저",
            "sentence_identity": "ko_k1_0002",
            "diagnostic_identities": [
              "ko_k1_0446"
            ],
            "sentence_raw_pos": [
              "NP"
            ],
            "diagnostic_raw_pos": [
              "MM"
            ],
            "id_disagreement": true,
            "pos_only_disagreement": false,
            "disagreement": true,
            "structural_defect": false,
            "decision": "WARNING_ONLY"
          }
        ],
        "credit": false
      },
      {
        "historical_phase": "3_7",
        "text": 5,
        "source": "pilot\\ko\\k1\\phase3_7\\candidates\\K1-005-attempt-01.json",
        "hard_pass": true,
        "hard_errors": [],
        "coverage": {
          "denominator_N": 142,
          "new_tokens_U": 2,
          "controlled_vocab_coverage": 1.0,
          "previous_vocab_coverage": 0.9859154929577465,
          "target_99_met": false
        },
        "canonical_lexical_map": [
          {
            "sentence_index": 1,
            "start": 0,
            "end": 2,
            "surface": "오늘",
            "canonical_vocab_id": "ko_k1_0068",
            "lemma": "오늘",
            "pos": "noun",
            "sense": "today",
            "sentence_raw": [
              {
                "form": "오늘",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 2,
            "end": 3,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 4,
            "end": 6,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 6,
            "end": 8,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 9,
            "end": 11,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 11,
            "end": 12,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 13,
            "end": 14,
            "surface": "가",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 1,
            "start": 13,
            "end": 15,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 17,
            "end": 19,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 19,
            "end": 21,
            "surface": "까지",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "까지",
                "tag": "JX",
                "start": 2,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 22,
            "end": 24,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 24,
            "end": 26,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 27,
            "end": 28,
            "surface": "걸",
            "canonical_vocab_id": "ko_k1_0186",
            "lemma": "걷다",
            "pos": "verb",
            "sense": "walk",
            "sentence_raw": [
              {
                "form": "걸",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 2,
            "start": 28,
            "end": 30,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 32,
            "end": 34,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 34,
            "end": 35,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 36,
            "end": 38,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 38,
            "end": 40,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 41,
            "end": 44,
            "surface": "운동하",
            "canonical_vocab_id": "ko_k1_0204",
            "lemma": "운동하다",
            "pos": "verb",
            "sense": "exercise",
            "sentence_raw": [
              {
                "form": "운동",
                "tag": "NNG",
                "start": 9,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 44,
            "end": 45,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 46,
            "end": 47,
            "surface": "싶",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "싶",
                "tag": "VX",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 3,
            "start": 47,
            "end": 49,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 51,
            "end": 52,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 52,
            "end": 53,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 54,
            "end": 56,
            "surface": "오늘",
            "canonical_vocab_id": "ko_k1_0068",
            "lemma": "오늘",
            "pos": "noun",
            "sense": "today",
            "sentence_raw": [
              {
                "form": "오늘",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 56,
            "end": 57,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 58,
            "end": 61,
            "surface": "운동하",
            "canonical_vocab_id": "ko_k1_0204",
            "lemma": "운동하다",
            "pos": "verb",
            "sense": "exercise",
            "sentence_raw": [
              {
                "form": "운동",
                "tag": "NNG",
                "start": 7,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 61,
            "end": 62,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 63,
            "end": 64,
            "surface": "싶",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "싶",
                "tag": "VX",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 4,
            "start": 64,
            "end": 66,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 68,
            "end": 70,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 71,
            "end": 72,
            "surface": "앞",
            "canonical_vocab_id": "ko_k1_0061",
            "lemma": "앞",
            "pos": "noun",
            "sense": "front",
            "sentence_raw": [
              {
                "form": "앞",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 72,
            "end": 74,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 75,
            "end": 76,
            "surface": "작",
            "canonical_vocab_id": "ko_k1_0235",
            "lemma": "작다",
            "pos": "adjective",
            "sense": "small",
            "sentence_raw": [
              {
                "form": "작",
                "tag": "VA",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 76,
            "end": 77,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "ETM",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 78,
            "end": 79,
            "surface": "길",
            "canonical_vocab_id": "ko_k1_0056",
            "lemma": "길",
            "pos": "noun",
            "sense": "road",
            "sentence_raw": [
              {
                "form": "길",
                "tag": "NNG",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 79,
            "end": 80,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 81,
            "end": 82,
            "surface": "봐",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 5,
            "start": 81,
            "end": 83,
            "surface": "봐요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 85,
            "end": 86,
            "surface": "길",
            "canonical_vocab_id": "ko_k1_0056",
            "lemma": "길",
            "pos": "noun",
            "sense": "road",
            "sentence_raw": [
              {
                "form": "길",
                "tag": "NNG",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 87,
            "end": 88,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 88,
            "end": 89,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 89,
            "end": 90,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 91,
            "end": 92,
            "surface": "꽃",
            "canonical_vocab_id": "ko_k1_0159",
            "lemma": "꽃",
            "pos": "noun",
            "sense": "flower",
            "sentence_raw": [
              {
                "form": "꽃",
                "tag": "NNG",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 92,
            "end": 93,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 94,
            "end": 96,
            "surface": "많이",
            "canonical_vocab_id": "ko_k1_0267",
            "lemma": "많이",
            "pos": "adverb",
            "sense": "a_lot",
            "sentence_raw": [
              {
                "form": "많이",
                "tag": "MAG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 97,
            "end": 98,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 6,
            "start": 98,
            "end": 100,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 103,
            "end": 105,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 105,
            "end": 106,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 107,
            "end": 108,
            "surface": "꽃",
            "canonical_vocab_id": "ko_k1_0159",
            "lemma": "꽃",
            "pos": "noun",
            "sense": "flower",
            "sentence_raw": [
              {
                "form": "꽃",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 108,
            "end": 109,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 110,
            "end": 111,
            "surface": "보",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 111,
            "end": 112,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 113,
            "end": 114,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 114,
            "end": 116,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 117,
            "end": 119,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 14,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 15,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 7,
            "start": 118,
            "end": 120,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 15,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 123,
            "end": 124,
            "surface": "이",
            "canonical_vocab_id": "ko_k1_0444",
            "lemma": "이",
            "pos": "determiner",
            "sense": "this",
            "sentence_raw": [
              {
                "form": "이",
                "tag": "MM",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 125,
            "end": 126,
            "surface": "길",
            "canonical_vocab_id": "ko_k1_0056",
            "lemma": "길",
            "pos": "noun",
            "sense": "road",
            "sentence_raw": [
              {
                "form": "길",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 126,
            "end": 127,
            "surface": "로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "로",
                "tag": "JKB",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 128,
            "end": 129,
            "surface": "갈",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 8,
            "start": 128,
            "end": 131,
            "surface": "갈까요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆯ까요",
                "tag": "EF",
                "start": 6,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 134,
            "end": 135,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 135,
            "end": 136,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 137,
            "end": 139,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 139,
            "end": 141,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 142,
            "end": 143,
            "surface": "꽃",
            "canonical_vocab_id": "ko_k1_0159",
            "lemma": "꽃",
            "pos": "noun",
            "sense": "flower",
            "sentence_raw": [
              {
                "form": "꽃",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 144,
            "end": 145,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 145,
            "end": 147,
            "surface": "으로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "으로",
                "tag": "JKB",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 148,
            "end": 149,
            "surface": "가",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 9,
            "start": 148,
            "end": 150,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 152,
            "end": 154,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 154,
            "end": 155,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 156,
            "end": 158,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 159,
            "end": 160,
            "surface": "안",
            "canonical_vocab_id": "ko_k1_0060",
            "lemma": "안",
            "pos": "noun",
            "sense": "inside",
            "sentence_raw": [
              {
                "form": "안",
                "tag": "NNG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 160,
            "end": 161,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 162,
            "end": 165,
            "surface": "들어가",
            "canonical_vocab_id": "ko_k1_0215",
            "lemma": "들어가다",
            "pos": "verb",
            "sense": "go_in",
            "sentence_raw": [
              {
                "form": "들어가",
                "tag": "VV",
                "start": 10,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 10,
            "start": 164,
            "end": 166,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 168,
            "end": 169,
            "surface": "안",
            "canonical_vocab_id": "ko_k1_0060",
            "lemma": "안",
            "pos": "noun",
            "sense": "inside",
            "sentence_raw": [
              {
                "form": "안",
                "tag": "NNG",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 169,
            "end": 170,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 170,
            "end": 171,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 172,
            "end": 173,
            "surface": "큰",
            "canonical_vocab_id": "ko_k1_0234",
            "lemma": "크다",
            "pos": "adjective",
            "sense": "big",
            "sentence_raw": [
              {
                "form": "크",
                "tag": "VA",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 172,
            "end": 173,
            "surface": "큰",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆫ",
                "tag": "ETM",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 174,
            "end": 176,
            "surface": "나무",
            "canonical_vocab_id": "ko_k1_0160",
            "lemma": "나무",
            "pos": "noun",
            "sense": "tree",
            "sentence_raw": [
              {
                "form": "나무",
                "tag": "NNG",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 176,
            "end": 177,
            "surface": "가",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "가",
                "tag": "JKS",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 178,
            "end": 179,
            "surface": "많",
            "canonical_vocab_id": "ko_k1_0236",
            "lemma": "많다",
            "pos": "adjective",
            "sense": "many",
            "sentence_raw": [
              {
                "form": "많",
                "tag": "VA",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 11,
            "start": 179,
            "end": 181,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 183,
            "end": 185,
            "surface": "나무",
            "canonical_vocab_id": "ko_k1_0160",
            "lemma": "나무",
            "pos": "noun",
            "sense": "tree",
            "sentence_raw": [
              {
                "form": "나무",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 186,
            "end": 187,
            "surface": "앞",
            "canonical_vocab_id": "ko_k1_0061",
            "lemma": "앞",
            "pos": "noun",
            "sense": "front",
            "sentence_raw": [
              {
                "form": "앞",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 187,
            "end": 188,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 188,
            "end": 189,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 190,
            "end": 191,
            "surface": "긴",
            "canonical_vocab_id": "ko_k1_0238",
            "lemma": "길다",
            "pos": "adjective",
            "sense": "long",
            "sentence_raw": [
              {
                "form": "길",
                "tag": "VA",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 190,
            "end": 191,
            "surface": "긴",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆫ",
                "tag": "ETM",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 192,
            "end": 193,
            "surface": "길",
            "canonical_vocab_id": "ko_k1_0056",
            "lemma": "길",
            "pos": "noun",
            "sense": "road",
            "sentence_raw": [
              {
                "form": "길",
                "tag": "NNG",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 193,
            "end": 194,
            "surface": "이",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "JKS",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 195,
            "end": 196,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 12,
            "start": 196,
            "end": 198,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 201,
            "end": 203,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 203,
            "end": 204,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 205,
            "end": 206,
            "surface": "긴",
            "canonical_vocab_id": "ko_k1_0238",
            "lemma": "길다",
            "pos": "adjective",
            "sense": "long",
            "sentence_raw": [
              {
                "form": "길",
                "tag": "VA",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 205,
            "end": 206,
            "surface": "긴",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "ᆫ",
                "tag": "ETM",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 207,
            "end": 208,
            "surface": "길",
            "canonical_vocab_id": "ko_k1_0056",
            "lemma": "길",
            "pos": "noun",
            "sense": "road",
            "sentence_raw": [
              {
                "form": "길",
                "tag": "NNG",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 208,
            "end": 210,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 211,
            "end": 212,
            "surface": "뛰",
            "canonical_vocab_id": "ko_k1_0187",
            "lemma": "뛰다",
            "pos": "verb",
            "sense": "run",
            "sentence_raw": [
              {
                "form": "뛰",
                "tag": "VV",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 212,
            "end": 213,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 214,
            "end": 215,
            "surface": "싶",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "싶",
                "tag": "VX",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 13,
            "start": 215,
            "end": 217,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 219,
            "end": 220,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 220,
            "end": 221,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 222,
            "end": 224,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 224,
            "end": 226,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 227,
            "end": 228,
            "surface": "길",
            "canonical_vocab_id": "ko_k1_0056",
            "lemma": "길",
            "pos": "noun",
            "sense": "road",
            "sentence_raw": [
              {
                "form": "길",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 228,
            "end": 230,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 231,
            "end": 232,
            "surface": "뛰",
            "canonical_vocab_id": "ko_k1_0187",
            "lemma": "뛰다",
            "pos": "verb",
            "sense": "run",
            "sentence_raw": [
              {
                "form": "뛰",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 14,
            "start": 232,
            "end": 234,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 236,
            "end": 238,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 238,
            "end": 239,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 240,
            "end": 242,
            "surface": "빠르",
            "canonical_vocab_id": "ko_k1_0241",
            "lemma": "빠르다",
            "pos": "adjective",
            "sense": "fast",
            "sentence_raw": [
              {
                "form": "빠르",
                "tag": "VA",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 242,
            "end": 243,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 244,
            "end": 245,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 245,
            "end": 246,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 247,
            "end": 249,
            "surface": "느려",
            "canonical_vocab_id": "ko_k1_0242",
            "lemma": "느리다",
            "pos": "adjective",
            "sense": "slow",
            "sentence_raw": [
              {
                "form": "느리",
                "tag": "VA",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 15,
            "start": 248,
            "end": 250,
            "surface": "려요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 252,
            "end": 253,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 253,
            "end": 254,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 255,
            "end": 257,
            "surface": "빨리",
            "canonical_vocab_id": "ko_k1_0269",
            "lemma": "빨리",
            "pos": "adverb",
            "sense": "quickly",
            "sentence_raw": [
              {
                "form": "빨리",
                "tag": "MAG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 258,
            "end": 259,
            "surface": "뛰",
            "canonical_vocab_id": "ko_k1_0187",
            "lemma": "뛰다",
            "pos": "verb",
            "sense": "run",
            "sentence_raw": [
              {
                "form": "뛰",
                "tag": "VV",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 259,
            "end": 260,
            "surface": "면",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "면",
                "tag": "EC",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 261,
            "end": 264,
            "surface": "피곤해",
            "canonical_vocab_id": "ko_k1_0256",
            "lemma": "피곤하다",
            "pos": "adjective",
            "sense": "tired",
            "sentence_raw": [
              {
                "form": "피곤",
                "tag": "NNG",
                "start": 9,
                "length": 2
              },
              {
                "form": "하",
                "tag": "XSA",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 16,
            "start": 263,
            "end": 265,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 267,
            "end": 269,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 269,
            "end": 270,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 271,
            "end": 273,
            "surface": "의자",
            "canonical_vocab_id": "ko_k1_0111",
            "lemma": "의자",
            "pos": "noun",
            "sense": "chair",
            "sentence_raw": [
              {
                "form": "의자",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 273,
            "end": 274,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 275,
            "end": 276,
            "surface": "앉",
            "canonical_vocab_id": "ko_k1_0184",
            "lemma": "앉다",
            "pos": "verb",
            "sense": "sit",
            "sentence_raw": [
              {
                "form": "앉",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 276,
            "end": 278,
            "surface": "아서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어서",
                "tag": "EC",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 279,
            "end": 280,
            "surface": "쉬",
            "canonical_vocab_id": "ko_k1_0224",
            "lemma": "쉬다",
            "pos": "verb",
            "sense": "rest",
            "sentence_raw": [
              {
                "form": "쉬",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 280,
            "end": 281,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 282,
            "end": 283,
            "surface": "싶",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "싶",
                "tag": "VX",
                "start": 15,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 17,
            "start": 283,
            "end": 285,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 16,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 287,
            "end": 289,
            "surface": "나무",
            "canonical_vocab_id": "ko_k1_0160",
            "lemma": "나무",
            "pos": "noun",
            "sense": "tree",
            "sentence_raw": [
              {
                "form": "나무",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 290,
            "end": 291,
            "surface": "옆",
            "canonical_vocab_id": "ko_k1_0063",
            "lemma": "옆",
            "pos": "noun",
            "sense": "side",
            "sentence_raw": [
              {
                "form": "옆",
                "tag": "NNG",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 291,
            "end": 292,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 293,
            "end": 294,
            "surface": "작",
            "canonical_vocab_id": "ko_k1_0235",
            "lemma": "작다",
            "pos": "adjective",
            "sense": "small",
            "sentence_raw": [
              {
                "form": "작",
                "tag": "VA",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 294,
            "end": 295,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "ETM",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 296,
            "end": 298,
            "surface": "의자",
            "canonical_vocab_id": "ko_k1_0111",
            "lemma": "의자",
            "pos": "noun",
            "sense": "chair",
            "sentence_raw": [
              {
                "form": "의자",
                "tag": "NNG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 298,
            "end": 299,
            "surface": "가",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "가",
                "tag": "JKS",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 300,
            "end": 301,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 18,
            "start": 301,
            "end": 303,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 306,
            "end": 308,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 308,
            "end": 309,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 310,
            "end": 312,
            "surface": "의자",
            "canonical_vocab_id": "ko_k1_0111",
            "lemma": "의자",
            "pos": "noun",
            "sense": "chair",
            "sentence_raw": [
              {
                "form": "의자",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 312,
            "end": 313,
            "surface": "를",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "를",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 314,
            "end": 315,
            "surface": "보",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 315,
            "end": 316,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 317,
            "end": 319,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 11,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 19,
            "start": 318,
            "end": 320,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 323,
            "end": 324,
            "surface": "그",
            "canonical_vocab_id": "ko_k1_0445",
            "lemma": "그",
            "pos": "determiner",
            "sense": "that",
            "sentence_raw": [
              {
                "form": "그",
                "tag": "MM",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 325,
            "end": 327,
            "surface": "의자",
            "canonical_vocab_id": "ko_k1_0111",
            "lemma": "의자",
            "pos": "noun",
            "sense": "chair",
            "sentence_raw": [
              {
                "form": "의자",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 327,
            "end": 328,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 329,
            "end": 330,
            "surface": "앉",
            "canonical_vocab_id": "ko_k1_0184",
            "lemma": "앉다",
            "pos": "verb",
            "sense": "sit",
            "sentence_raw": [
              {
                "form": "앉",
                "tag": "VV",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 20,
            "start": 330,
            "end": 333,
            "surface": "을까요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을까요",
                "tag": "EF",
                "start": 8,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 336,
            "end": 337,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 337,
            "end": 338,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 339,
            "end": 341,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 341,
            "end": 343,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 344,
            "end": 346,
            "surface": "의자",
            "canonical_vocab_id": "ko_k1_0111",
            "lemma": "의자",
            "pos": "noun",
            "sense": "chair",
            "sentence_raw": [
              {
                "form": "의자",
                "tag": "NNG",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 346,
            "end": 347,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 348,
            "end": 349,
            "surface": "앉",
            "canonical_vocab_id": "ko_k1_0184",
            "lemma": "앉다",
            "pos": "verb",
            "sense": "sit",
            "sentence_raw": [
              {
                "form": "앉",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 21,
            "start": 349,
            "end": 351,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 353,
            "end": 354,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 354,
            "end": 355,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 356,
            "end": 358,
            "surface": "가방",
            "canonical_vocab_id": "ko_k1_0114",
            "lemma": "가방",
            "pos": "noun",
            "sense": "bag",
            "sentence_raw": [
              {
                "form": "가방",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 358,
            "end": 360,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 361,
            "end": 362,
            "surface": "물",
            "canonical_vocab_id": "ko_k1_0119",
            "lemma": "물",
            "pos": "noun",
            "sense": "water",
            "sentence_raw": [
              {
                "form": "물",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 362,
            "end": 363,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 364,
            "end": 365,
            "surface": "찾",
            "canonical_vocab_id": "ko_k1_0211",
            "lemma": "찾다",
            "pos": "verb",
            "sense": "find_look_for",
            "sentence_raw": [
              {
                "form": "찾",
                "tag": "VV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 22,
            "start": 365,
            "end": 367,
            "surface": "아요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 369,
            "end": 371,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 371,
            "end": 372,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 373,
            "end": 374,
            "surface": "물",
            "canonical_vocab_id": "ko_k1_0119",
            "lemma": "물",
            "pos": "noun",
            "sense": "water",
            "sentence_raw": [
              {
                "form": "물",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 374,
            "end": 375,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 376,
            "end": 378,
            "surface": "마시",
            "canonical_vocab_id": "ko_k1_0173",
            "lemma": "마시다",
            "pos": "verb",
            "sense": "drink",
            "sentence_raw": [
              {
                "form": "마시",
                "tag": "VV",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 378,
            "end": 379,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 380,
            "end": 381,
            "surface": "쉬",
            "canonical_vocab_id": "ko_k1_0224",
            "lemma": "쉬다",
            "pos": "verb",
            "sense": "rest",
            "sentence_raw": [
              {
                "form": "쉬",
                "tag": "VV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 23,
            "start": 381,
            "end": 383,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 385,
            "end": 387,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 387,
            "end": 388,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 389,
            "end": 390,
            "surface": "물",
            "canonical_vocab_id": "ko_k1_0119",
            "lemma": "물",
            "pos": "noun",
            "sense": "water",
            "sentence_raw": [
              {
                "form": "물",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 390,
            "end": 391,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 392,
            "end": 393,
            "surface": "더",
            "canonical_vocab_id": "ko_k1_0449",
            "lemma": "더",
            "pos": "adverb",
            "sense": "more",
            "sentence_raw": [
              {
                "form": "더",
                "tag": "MAG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 394,
            "end": 396,
            "surface": "마시",
            "canonical_vocab_id": "ko_k1_0173",
            "lemma": "마시다",
            "pos": "verb",
            "sense": "drink",
            "sentence_raw": [
              {
                "form": "마시",
                "tag": "VV",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 396,
            "end": 397,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 398,
            "end": 399,
            "surface": "싶",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "싶",
                "tag": "VX",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 24,
            "start": 399,
            "end": 401,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 404,
            "end": 405,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 405,
            "end": 406,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 407,
            "end": 409,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 409,
            "end": 411,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 5,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 412,
            "end": 413,
            "surface": "물",
            "canonical_vocab_id": "ko_k1_0119",
            "lemma": "물",
            "pos": "noun",
            "sense": "water",
            "sentence_raw": [
              {
                "form": "물",
                "tag": "NNG",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 413,
            "end": 414,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 415,
            "end": 416,
            "surface": "줘",
            "canonical_vocab_id": "ko_k1_0192",
            "lemma": "주다",
            "pos": "verb",
            "sense": "give",
            "sentence_raw": [
              {
                "form": "주",
                "tag": "VV",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 25,
            "start": 415,
            "end": 417,
            "surface": "줘요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 419,
            "end": 421,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 421,
            "end": 422,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 423,
            "end": 424,
            "surface": "물",
            "canonical_vocab_id": "ko_k1_0119",
            "lemma": "물",
            "pos": "noun",
            "sense": "water",
            "sentence_raw": [
              {
                "form": "물",
                "tag": "NNG",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 424,
            "end": 425,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 5,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 426,
            "end": 428,
            "surface": "마시",
            "canonical_vocab_id": "ko_k1_0173",
            "lemma": "마시다",
            "pos": "verb",
            "sense": "drink",
            "sentence_raw": [
              {
                "form": "마시",
                "tag": "VV",
                "start": 7,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 428,
            "end": 429,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 430,
            "end": 431,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 431,
            "end": 433,
            "surface": "에게",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에게",
                "tag": "JKB",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 434,
            "end": 436,
            "surface": "말해",
            "canonical_vocab_id": "ko_k1_0176",
            "lemma": "말하다",
            "pos": "verb",
            "sense": "speak",
            "sentence_raw": [
              {
                "form": "말",
                "tag": "NNG",
                "start": 15,
                "length": 1
              },
              {
                "form": "하",
                "tag": "XSV",
                "start": 16,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 26,
            "start": 435,
            "end": 437,
            "surface": "해요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 16,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 440,
            "end": 441,
            "surface": "몇",
            "canonical_vocab_id": "ko_k1_0448",
            "lemma": "몇",
            "pos": "determiner",
            "sense": "how_many",
            "sentence_raw": [
              {
                "form": "몇",
                "tag": "MM",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 442,
            "end": 443,
            "surface": "시",
            "canonical_vocab_id": "ko_k1_0077",
            "lemma": "시",
            "pos": "counter",
            "sense": "clock_hour",
            "sentence_raw": [
              {
                "form": "시",
                "tag": "NNB",
                "start": 3,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 443,
            "end": 444,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 4,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 445,
            "end": 446,
            "surface": "집",
            "canonical_vocab_id": "ko_k1_0042",
            "lemma": "집",
            "pos": "noun",
            "sense": "home",
            "sentence_raw": [
              {
                "form": "집",
                "tag": "NNG",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 446,
            "end": 447,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 448,
            "end": 449,
            "surface": "가",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 27,
            "start": 448,
            "end": 450,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 453,
            "end": 454,
            "surface": "저",
            "canonical_vocab_id": "ko_k1_0002",
            "lemma": "저",
            "pos": "pronoun",
            "sense": "i_humble",
            "sentence_raw": [
              {
                "form": "저",
                "tag": "NP",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 454,
            "end": 455,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 456,
            "end": 458,
            "surface": "다섯",
            "canonical_vocab_id": "ko_k1_0285",
            "lemma": "다섯",
            "pos": "numeral",
            "sense": "five_native",
            "sentence_raw": [
              {
                "form": "다섯",
                "tag": "NR",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 459,
            "end": 460,
            "surface": "시",
            "canonical_vocab_id": "ko_k1_0077",
            "lemma": "시",
            "pos": "counter",
            "sense": "clock_hour",
            "sentence_raw": [
              {
                "form": "시",
                "tag": "NNB",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 460,
            "end": 461,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 462,
            "end": 463,
            "surface": "집",
            "canonical_vocab_id": "ko_k1_0042",
            "lemma": "집",
            "pos": "noun",
            "sense": "home",
            "sentence_raw": [
              {
                "form": "집",
                "tag": "NNG",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 463,
            "end": 464,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 465,
            "end": 466,
            "surface": "가",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 28,
            "start": 465,
            "end": 467,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 469,
            "end": 470,
            "surface": "집",
            "canonical_vocab_id": "ko_k1_0042",
            "lemma": "집",
            "pos": "noun",
            "sense": "home",
            "sentence_raw": [
              {
                "form": "집",
                "tag": "NNG",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 470,
            "end": 472,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 1,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 473,
            "end": 475,
            "surface": "가족",
            "canonical_vocab_id": "ko_k1_0023",
            "lemma": "가족",
            "pos": "noun",
            "sense": "family",
            "sentence_raw": [
              {
                "form": "가족",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 475,
            "end": 477,
            "surface": "하고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "하고",
                "tag": "JKB",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 478,
            "end": 480,
            "surface": "저녁",
            "canonical_vocab_id": "ko_k1_0074",
            "lemma": "저녁",
            "pos": "noun",
            "sense": "evening",
            "sentence_raw": [
              {
                "form": "저녁",
                "tag": "NNG",
                "start": 9,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 480,
            "end": 481,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 482,
            "end": 483,
            "surface": "먹",
            "canonical_vocab_id": "ko_k1_0172",
            "lemma": "먹다",
            "pos": "verb",
            "sense": "eat",
            "sentence_raw": [
              {
                "form": "먹",
                "tag": "VV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 483,
            "end": 484,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "ETM",
                "start": 14,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 485,
            "end": 486,
            "surface": "거",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "거",
                "tag": "NNB",
                "start": 16,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 486,
            "end": 487,
            "surface": "예",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "이",
                "tag": "VCP",
                "start": 17,
                "length": 0
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 29,
            "start": 486,
            "end": 488,
            "surface": "예요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "예요",
                "tag": "EF",
                "start": 17,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 490,
            "end": 492,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 492,
            "end": 493,
            "surface": "도",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "도",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 494,
            "end": 496,
            "surface": "다섯",
            "canonical_vocab_id": "ko_k1_0285",
            "lemma": "다섯",
            "pos": "numeral",
            "sense": "five_native",
            "sentence_raw": [
              {
                "form": "다섯",
                "tag": "NR",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 497,
            "end": 498,
            "surface": "시",
            "canonical_vocab_id": "ko_k1_0077",
            "lemma": "시",
            "pos": "counter",
            "sense": "clock_hour",
            "sentence_raw": [
              {
                "form": "시",
                "tag": "NNB",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 498,
            "end": 499,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 500,
            "end": 501,
            "surface": "집",
            "canonical_vocab_id": "ko_k1_0042",
            "lemma": "집",
            "pos": "noun",
            "sense": "home",
            "sentence_raw": [
              {
                "form": "집",
                "tag": "NNG",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 501,
            "end": 502,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 503,
            "end": 504,
            "surface": "가",
            "canonical_vocab_id": "ko_k1_0170",
            "lemma": "가다",
            "pos": "verb",
            "sense": "go",
            "sentence_raw": [
              {
                "form": "가",
                "tag": "VV",
                "start": 13,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 30,
            "start": 503,
            "end": 505,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 508,
            "end": 510,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 510,
            "end": 511,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 512,
            "end": 514,
            "surface": "의자",
            "canonical_vocab_id": "ko_k1_0111",
            "lemma": "의자",
            "pos": "noun",
            "sense": "chair",
            "sentence_raw": [
              {
                "form": "의자",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 514,
            "end": 516,
            "surface": "에서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에서",
                "tag": "JKB",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 517,
            "end": 520,
            "surface": "일어나",
            "canonical_vocab_id": "ko_k1_0183",
            "lemma": "일어나다",
            "pos": "verb",
            "sense": "get_up",
            "sentence_raw": [
              {
                "form": "일어나",
                "tag": "VV",
                "start": 9,
                "length": 3
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 519,
            "end": 521,
            "surface": "나서",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어서",
                "tag": "EC",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 522,
            "end": 524,
            "surface": "가방",
            "canonical_vocab_id": "ko_k1_0114",
            "lemma": "가방",
            "pos": "noun",
            "sense": "bag",
            "sentence_raw": [
              {
                "form": "가방",
                "tag": "NNG",
                "start": 14,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 524,
            "end": 525,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 16,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 526,
            "end": 527,
            "surface": "봐",
            "canonical_vocab_id": "ko_k1_0174",
            "lemma": "보다",
            "pos": "verb",
            "sense": "see_watch",
            "sentence_raw": [
              {
                "form": "보",
                "tag": "VV",
                "start": 18,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 31,
            "start": 526,
            "end": 528,
            "surface": "봐요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 18,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 530,
            "end": 531,
            "surface": "물",
            "canonical_vocab_id": "ko_k1_0119",
            "lemma": "물",
            "pos": "noun",
            "sense": "water",
            "sentence_raw": [
              {
                "form": "물",
                "tag": "NNG",
                "start": 0,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 531,
            "end": 532,
            "surface": "은",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "은",
                "tag": "JX",
                "start": 1,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 533,
            "end": 535,
            "surface": "모두",
            "canonical_vocab_id": "ko_k1_0020",
            "lemma": "모두",
            "pos": "adverb",
            "sense": "all_together",
            "sentence_raw": [
              {
                "form": "모두",
                "tag": "MAG",
                "start": 3,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 536,
            "end": 538,
            "surface": "가방",
            "canonical_vocab_id": "ko_k1_0114",
            "lemma": "가방",
            "pos": "noun",
            "sense": "bag",
            "sentence_raw": [
              {
                "form": "가방",
                "tag": "NNG",
                "start": 6,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 539,
            "end": 540,
            "surface": "안",
            "canonical_vocab_id": "ko_k1_0060",
            "lemma": "안",
            "pos": "noun",
            "sense": "inside",
            "sentence_raw": [
              {
                "form": "안",
                "tag": "NNG",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 540,
            "end": 541,
            "surface": "에",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "에",
                "tag": "JKB",
                "start": 10,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 542,
            "end": 543,
            "surface": "있",
            "canonical_vocab_id": "ko_k1_0180",
            "lemma": "있다",
            "pos": "adjective",
            "sense": "exist",
            "sentence_raw": [
              {
                "form": "있",
                "tag": "VA",
                "start": 12,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 32,
            "start": 543,
            "end": 545,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 13,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 547,
            "end": 549,
            "surface": "친구",
            "canonical_vocab_id": "ko_k1_0022",
            "lemma": "친구",
            "pos": "noun",
            "sense": "friend",
            "sentence_raw": [
              {
                "form": "친구",
                "tag": "NNG",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 549,
            "end": 550,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 551,
            "end": 553,
            "surface": "가방",
            "canonical_vocab_id": "ko_k1_0114",
            "lemma": "가방",
            "pos": "noun",
            "sense": "bag",
            "sentence_raw": [
              {
                "form": "가방",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 553,
            "end": 554,
            "surface": "을",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "을",
                "tag": "JKO",
                "start": 6,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 555,
            "end": 556,
            "surface": "닫",
            "canonical_vocab_id": "ko_k1_0195",
            "lemma": "닫다",
            "pos": "verb",
            "sense": "close",
            "sentence_raw": [
              {
                "form": "닫",
                "tag": "VV-R",
                "start": 8,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 556,
            "end": 557,
            "surface": "고",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "고",
                "tag": "EC",
                "start": 9,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 558,
            "end": 559,
            "surface": "웃",
            "canonical_vocab_id": "ko_k1_0227",
            "lemma": "웃다",
            "pos": "verb",
            "sense": "laugh_smile",
            "sentence_raw": [
              {
                "form": "웃",
                "tag": "VV-R",
                "start": 11,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 33,
            "start": 559,
            "end": 561,
            "surface": "어요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 563,
            "end": 565,
            "surface": "우리",
            "canonical_vocab_id": "ko_k1_0004",
            "lemma": "우리",
            "pos": "pronoun",
            "sense": "we",
            "sentence_raw": [
              {
                "form": "우리",
                "tag": "NP",
                "start": 0,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 565,
            "end": 566,
            "surface": "는",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "는",
                "tag": "JX",
                "start": 2,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 567,
            "end": 569,
            "surface": "공원",
            "canonical_vocab_id": "ko_k1_0051",
            "lemma": "공원",
            "pos": "noun",
            "sense": "park",
            "sentence_raw": [
              {
                "form": "공원",
                "tag": "NNG",
                "start": 4,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 570,
            "end": 571,
            "surface": "밖",
            "canonical_vocab_id": "ko_k1_0059",
            "lemma": "밖",
            "pos": "noun",
            "sense": "outside",
            "sentence_raw": [
              {
                "form": "밖",
                "tag": "NNG",
                "start": 7,
                "length": 1
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 571,
            "end": 573,
            "surface": "으로",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "으로",
                "tag": "JKB",
                "start": 8,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 574,
            "end": 576,
            "surface": "나가",
            "canonical_vocab_id": "ko_k1_0216",
            "lemma": "나가다",
            "pos": "verb",
            "sense": "go_out",
            "sentence_raw": [
              {
                "form": "나가",
                "tag": "VV",
                "start": 11,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          },
          {
            "sentence_index": 34,
            "start": 575,
            "end": 577,
            "surface": "가요",
            "canonical_vocab_id": null,
            "lemma": null,
            "pos": null,
            "sense": null,
            "sentence_raw": [
              {
                "form": "어요",
                "tag": "EF",
                "start": 12,
                "length": 2
              }
            ],
            "canonical_reason": "Existing sentence-local morphology/POS/context resolvers; actual permission checked separately. No broad-scope override."
          }
        ],
        "scope_disagreements": [],
        "credit": false
      }
    ],
    "report_only": true
  },
  "partial_3_6b_baseline": {
    "mean": 77.02,
    "median": 70.13,
    "p90": 119.98,
    "committed": 6,
    "not_a_completed_benchmark": true
  },
  "restricted_sense_rejects": 0,
  "restricted_sense_usage_count": 59,
  "basic_sense_family_usage_counts": {
    "breakfast_meal": 4,
    "morning_time": 7,
    "dinner_meal": 3,
    "evening_time": 5
  },
  "lexical_policy_violations_committed": 0,
  "translation_issue_repairs": 1,
  "baseline_phase3_7": {
    "mean": 104.79,
    "median": 95.19,
    "p90": 150.46,
    "first_pass": 0.8,
    "mean_attempts": 1.2,
    "partial": true
  },
  "scope_disagreement_count": 4,
  "scope_disagreement_distribution": {
    "full_text": 2,
    "paragraph": 2
  },
  "registered_id_disagreements": 2,
  "pos_only_disagreements": 2,
  "scope_disagreement_examples": [
    {
      "type": "scope_identity_disagreement_warning",
      "scope": "full_text",
      "start": 434,
      "end": 435,
      "surface": "네",
      "sentence_identity": "ko_k1_0442",
      "diagnostic_identities": [
        "ko_k1_0442"
      ],
      "sentence_raw_pos": [
        "IC"
      ],
      "diagnostic_raw_pos": [
        "JKG",
        "NP"
      ],
      "id_disagreement": false,
      "pos_only_disagreement": true,
      "disagreement": true,
      "structural_defect": false,
      "decision": "WARNING_ONLY"
    },
    {
      "type": "scope_identity_disagreement_warning",
      "scope": "paragraph",
      "start": 434,
      "end": 435,
      "surface": "네",
      "sentence_identity": "ko_k1_0442",
      "diagnostic_identities": [
        "ko_k1_0442"
      ],
      "sentence_raw_pos": [
        "IC"
      ],
      "diagnostic_raw_pos": [
        "JKG",
        "NP"
      ],
      "id_disagreement": false,
      "pos_only_disagreement": true,
      "disagreement": true,
      "structural_defect": false,
      "decision": "WARNING_ONLY"
    },
    {
      "type": "scope_identity_disagreement_warning",
      "scope": "full_text",
      "start": 348,
      "end": 350,
      "surface": "우리",
      "sentence_identity": "ko_k1_0004",
      "diagnostic_identities": [],
      "sentence_raw_pos": [
        "NP"
      ],
      "diagnostic_raw_pos": [],
      "id_disagreement": true,
      "pos_only_disagreement": false,
      "disagreement": true,
      "structural_defect": false,
      "decision": "WARNING_ONLY"
    },
    {
      "type": "scope_identity_disagreement_warning",
      "scope": "paragraph",
      "start": 348,
      "end": 350,
      "surface": "우리",
      "sentence_identity": "ko_k1_0004",
      "diagnostic_identities": [],
      "sentence_raw_pos": [
        "NP"
      ],
      "diagnostic_raw_pos": [],
      "id_disagreement": true,
      "pos_only_disagreement": false,
      "disagreement": true,
      "structural_defect": false,
      "decision": "WARNING_ONLY"
    }
  ],
  "restricted_sense_false_accepts": []
}
