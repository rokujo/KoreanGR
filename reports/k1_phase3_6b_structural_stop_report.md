# Phase 3.6b STOP at K1-007

D / STRUCTURAL_FAIL. Committed 001..006 only. Failed 007 has no exposure credit. No 008+ generation or engine change.

{
  "phase": "3.6b",
  "completed": false,
  "committed_count": 6,
  "state_epoch": 6,
  "stop": {
    "type": "structural_analyzer_defect",
    "text": 7,
    "errors": [
      {
        "code": "unknown_or_unresolved",
        "detail": {
          "vocab_id": null,
          "lemma": "우리",
          "surface": "우리",
          "start": 260,
          "reason": "unknown_or_unresolved"
        }
      },
      {
        "code": "scope_identity_mismatch",
        "detail": {
          "type": "SCOPE_IDENTITY_MISMATCH",
          "start": 260,
          "end": 262,
          "surface": "우리",
          "views": [
            {
              "scope": "sentence",
              "original_offset": 259,
              "before_recovery_ids": [
                "ko_k1_0004"
              ],
              "resolved_ids": [
                "ko_k1_0004"
              ],
              "ne_recovery_decisions": []
            },
            {
              "scope": "paragraph",
              "original_offset": 186,
              "before_recovery_ids": [],
              "resolved_ids": [],
              "ne_recovery_decisions": []
            },
            {
              "scope": "full_text",
              "original_offset": 0,
              "before_recovery_ids": [],
              "resolved_ids": [],
              "ne_recovery_decisions": []
            }
          ],
          "decision": "UNRESOLVED",
          "structural_defect": true,
          "author_intent_not_authority": true
        }
      },
      {
        "code": "structural_analyzer_defect",
        "detail": {
          "usage": {
            "vocab_id": null,
            "lemma": "우리",
            "surface": "우리",
            "start": 260,
            "reason": "unknown_or_unresolved"
          },
          "sentence": "\"우리는 한국어를 같이 배울 거예요.\"",
          "isolated_pass": true
        }
      },
      {
        "code": "unresolved_context_ambiguity",
        "detail": {
          "type": "identity_boundary",
          "surface": "우리",
          "lemma": "우리",
          "start": 260,
          "raw_pos": "NNG",
          "registered_candidates": [
            {
              "id": "ko_k1_0004",
              "pos": "pronoun",
              "sense": "we"
            }
          ],
          "alias_reason": null,
          "status": "REVIEW",
          "requires_candidate_review": true
        }
      },
      {
        "code": "unresolved_context_ambiguity",
        "detail": {
          "type": "uri_pronoun_context",
          "surface": "우리",
          "raw_pos": "NNG",
          "raw_parts": [
            {
              "form": "우리",
              "tag": "NNG",
              "start": 260,
              "length": 2
            }
          ],
          "raw_indices": [
            152
          ],
          "start": 260,
          "end": 262,
          "scope": "full_candidate",
          "preceding_tokens": [
            {
              "form": "어요",
              "tag": "EF",
              "start": 254,
              "length": 2
            },
            {
              "form": ".",
              "tag": "SF",
              "start": 256,
              "length": 1
            },
            {
              "form": "\"",
              "tag": "SSC",
              "start": 257,
              "length": 1
            },
            {
              "form": "\"",
              "tag": "SSO",
              "start": 259,
              "length": 1
            }
          ],
          "following_tokens": [
            {
              "form": "는",
              "tag": "JX",
              "start": 262,
              "length": 1
            },
            {
              "form": "한국어",
              "tag": "NNP",
              "start": 264,
              "length": 3
            },
            {
              "form": "를",
              "tag": "JKO",
              "start": 267,
              "length": 1
            },
            {
              "form": "같이",
              "tag": "MAG",
              "start": 269,
              "length": 2
            }
          ],
          "following_noun": null,
          "registered_id": "ko_k1_0004",
          "registered_pos": "pronoun",
          "registered_sense": "we",
          "context_evidence": {
            "exact_original_surface": true,
            "unique_registered_identity": true,
            "single_exact_raw_span": true,
            "raw_np_or_nng": true,
            "left_word_boundary": true,
            "no_particle_on_uri": false,
            "whitespace_before_head": false,
            "limited_registered_nominal_head": false,
            "following_head_exact": false,
            "speaker_group_raw_anchor": true,
            "no_spatial_noun_contrast": true,
            "balanced_or_independent": true,
            "annotation_group_exclusive": true,
            "raw_span_accounted_once": true
          },
          "speaker_anchors": [
            {
              "form": "저",
              "raw_pos": "NP",
              "start": 0,
              "particle": "는"
            },
            {
              "form": "저",
              "raw_pos": "NP",
              "start": 30,
              "particle": "는"
            },
            {
              "form": "저",
              "raw_pos": "NP",
              "start": 93,
              "particle": "는"
            },
            {
              "form": "저",
              "raw_pos": "NP",
              "start": 137,
              "particle": "는"
            },
            {
              "form": "저",
              "raw_pos": "NP",
              "start": 201,
              "particle": "는"
            }
          ],
          "quotation_context": {
            "inside_balanced": true,
            "open_offset": 259,
            "close_offset": 279,
            "opening": "\"",
            "closing": "\"",
            "inside_unmatched": false
          },
          "decision": "REVIEW",
          "original_annotation": [
            {
              "surface": "우리",
              "lemma": "우리",
              "pos": null,
              "sense": null,
              "vocab_id": null,
              "role": "unresolved",
              "start": 260,
              "end": 262,
              "morph_indices": [
                152
              ],
              "grammar_id": null
            }
          ],
          "permission_granted": false,
          "status": "REVIEW",
          "requires_candidate_review": true
        }
      },
      {
        "code": "coverage_or_token_policy",
        "detail": "Token 123: uncontrolled vocabulary or future introduction"
      },
      {
        "code": "coverage_or_token_policy",
        "detail": "controlled_vocab_coverage below hard 100%"
      },
      {
        "code": "coverage_or_token_policy",
        "detail": "previous_vocab_coverage below hard 98%"
      }
    ]
  },
  "hard_errors": 0,
  "integrity_errors": [],
  "total_attempts": 11,
  "first_pass_count": 2,
  "first_pass_ratio": 0.3333333333333333,
  "mean_attempts": 1.6666666666666667,
  "attempts": [
    2,
    2,
    2,
    1,
    2,
    1
  ],
  "retry_error_codes": {
    "future_expansion": 4,
    "unknown_or_unresolved": 8,
    "coverage_or_token_policy": 22,
    "unresolved_context_ambiguity": 5,
    "planned_new_not_present": 1,
    "scope_identity_mismatch": 1,
    "structural_analyzer_defect": 1
  },
  "rejected_attempts": 5,
  "future_contaminated_candidates": 2,
  "future_in_committed": 0,
  "unresolved_in_committed": 0,
  "planned_mismatch": 0,
  "structural_scope_mismatches": 1,
  "resolved_scope_mismatches": 5,
  "failed_state_isolation": true,
  "semantic_warning_count": 55,
  "semantic_warning_distribution": {
    "REVIEW": 54,
    "FAIL": 1
  },
  "naturalness_warning_count": 1,
  "naturalness_categories": {
    "nat_restricted_sense": 1
  },
  "author_confirmed_draft_issues": [],
  "confirmed_committed_issues": [],
  "recurring_patterns": {},
  "selected_review": 8,
  "incidental": 2,
  "introduced_count": 12,
  "exposure_distribution": {
    "0": 488,
    "2": 6,
    "3": 2,
    "1": 4
  },
  "outstanding_debt": [],
  "expired_debt": [],
  "near_deadline_debt": [],
  "mathematically_unrecoverable": [],
  "genre_distribution": {
    "simple_outing": 1,
    "short_dialogue": 1,
    "objects": 1,
    "transport": 1,
    "food": 1,
    "shopping": 1
  },
  "max_scene_similarity": 0.16666666666666666,
  "scene_similarities": [
    {
      "a": 2,
      "b": 1,
      "score": 0.05555555555555555
    },
    {
      "a": 3,
      "b": 1,
      "score": 0.1111111111111111
    },
    {
      "a": 3,
      "b": 2,
      "score": 0.041666666666666664
    },
    {
      "a": 4,
      "b": 1,
      "score": 0.05555555555555555
    },
    {
      "a": 4,
      "b": 2,
      "score": 0.16666666666666666
    },
    {
      "a": 4,
      "b": 3,
      "score": 0.041666666666666664
    },
    {
      "a": 5,
      "b": 1,
      "score": 0.1111111111111111
    },
    {
      "a": 5,
      "b": 2,
      "score": 0.041666666666666664
    },
    {
      "a": 5,
      "b": 3,
      "score": 0.16666666666666666
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
      "score": 0.03333333333333333
    },
    {
      "a": 6,
      "b": 4,
      "score": 0.041666666666666664
    },
    {
      "a": 6,
      "b": 5,
      "score": 0.03333333333333333
    }
  ],
  "eojeol": {
    "n": 6,
    "min": 135,
    "max": 144,
    "mean": 138.83333333333334,
    "median": 137.5,
    "p90": 144
  },
  "sentence_lengths": {
    "2": 3,
    "4": 153,
    "3": 24,
    "5": 26,
    "1": 7,
    "6": 1
  },
  "preferred_sentence_ratio": 0.9532710280373832,
  "production_wall_seconds": 530.9835020000028,
  "per_text_seconds": {
    "n": 6,
    "min": 62.84094109999569,
    "max": 119.97917779999989,
    "mean": 77.0184484666667,
    "median": 70.12529649999851,
    "p90": 119.97917779999989
  },
  "stage_seconds": {
    "scene_planning": 254.98220280000533,
    "author_draft": 76.43984180000552,
    "morphology_vocab_analysis": 15.490475699880335,
    "mechanical_validation": 2.2709526001199265,
    "retry_repair": 91.04871159998584,
    "naturalness_review": 64.09094429999823,
    "final_reanalysis": 8.663925499997276,
    "commit": 3.674923700004001,
    "controller_overhead": 4.5193739000023925
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
  "largest_stage": "scene_planning",
  "engineering_setup_seconds": 215.854142,
  "pre_regression": {
    "tests": 286,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 123.29430850000062,
    "success": true
  },
  "ledger_replay_errors": [],
  "post_regression": {
    "tests": 286,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 126.14243580000038,
    "success": true
  },
  "verdict": "D",
  "status": "STRUCTURAL_FAIL",
  "performance": "INCOMPLETE",
  "speed_optimization_target": "generator",
  "candidate_primary_cause_distribution": {
    "future_vocabulary": 2,
    "unregistered_compound": 1,
    "pos_boundary": 1,
    "structural_scope_identity_mismatch": 1
  },
  "normal_retry_primary_cause_distribution": {
    "future_vocabulary": 2,
    "unregistered_compound": 1,
    "pos_boundary": 1
  },
  "author_confirmed_candidate_issue_groups": [
    {
      "text": 1,
      "attempt": 1,
      "category": "verb_argument_frame",
      "surface": "어머니에게 꽃을 말해요",
      "resolution": "어머니에게 말해요 followed by direct speech; repaired in attempt 2"
    },
    {
      "text": 1,
      "attempt": 1,
      "category": "third_person_desire",
      "surface": "어머니도 꽃을 보고 싶어요",
      "resolution": "Changed to narrator's own desire in attempt 2"
    },
    {
      "text": 2,
      "attempt": 1,
      "category": "third_person_desire",
      "surface": "친구는 커피를 마시고 싶어요 / 친구도 빵을 먹고 싶어요",
      "resolution": "Changed to literal food preferences in attempt 2"
    },
    {
      "text": 3,
      "attempt": 1,
      "category": "unnatural_substitution",
      "surface": "사진을 책상 위에 넣어요",
      "resolution": "Changed to a location/state sentence in attempt 2; did not use 넣다 as 놓다"
    }
  ],
  "author_confirmed_candidate_issue_group_count": 4,
  "timing_limitations": {
    "production_total": "Monotonic measured wall time; unchanged actual total, no stored-text replay used as generation timing",
    "stage_boundary": "For texts 002 through 007, the plan command and prose file authoring were submitted in the same LLM tool-call payload. Planning timing therefore includes much of prose composition before the command ran; author_draft timing mostly covers file transport. For 001, plan and prose were separate calls. No stage durations are retrospectively reassigned or invented.",
    "interpretation": "Use combined scene_planning + author_draft + retry_repair as the generator cost. Individual planning/draft stage ranking is an instrumentation limitation, not evidence that planning itself is slower than writing. Six committed initial texts and a STOP are insufficient to demonstrate 50-text production throughput or give an official 300-text forecast."
  },
  "recurrence_warning_count": 0,
  "controlled_min": 1.0,
  "previous_min": 0.9844961240310077,
  "committed_grammar_form_errors": 0,
  "sentence_hard_max": 6,
  "final_reanalysis_mismatches": [],
  "partial_speed_comparison": {
    "mean_ratio_to_baseline": 0.6002996762795533,
    "median_ratio_to_baseline": 0.6103158964316667,
    "p90_ratio_to_baseline": 0.7332346012344918,
    "not_a_completed_50_text_benchmark": true
  },
  "generator_combined_seconds": 422.4707561999967,
  "scope_mismatch_stop_count": 1,
  "checkpoint_status": "Stopped at 007 before checkpoint 010; no 010/020/030/040/050 checkpoint was fabricated",
  "credit_to_failed_007": false,
  "unintroduced_planned_007_ids": [
    "ko_k1_0468",
    "ko_k1_0469"
  ],
  "generation_upper_bound_observed": 7,
  "next_step": "Separate targeted investigation of particle-bearing quoted uri identity; no engine change applied in this run",
  "fresh_generation_verified": true
}
