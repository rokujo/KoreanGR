# Phase 3.6b Production Trial

## 停止結果と判断

**D / STRUCTURAL_FAIL**。K1-001〜006の6本をcommitし、007の初候補で構造STOP。008以降は生成していない。010に達していないため、10本刻みのcheckpointは作成していない。50本完走・300本量産への進行は認められる結果ではない。

問題文は `"우리는 한국어를 같이 배울 거예요."`。우리の単文rawはNP、段落・全文rawはNNG。既存の限定resolverは「우리＋許可名詞」の修飾関係を根拠にするもので、今回は우리に는が直接付く主語用法なので安全に復元できない。rawを上書きせず、scope identity mismatchとstructural analyzer defectで停止した。これはsemantic grammar warningによる停止ではない。

007は未commit。명・살の初出、review候補、incidental候補のいずれにもcreditしていない。failed candidateの評価前後ledger hashは一致し、epochは6のまま。候補・全文raw・診断は別run内に保存した。既存pipeline/configと過去成果物のhash差分は0件。途中でpromptやコードを修正していない。

| 指標 | 停止時の実績 |
|---|---|
| commit | 6/50 |
| 全candidate | 11件：成功6、reject5（うち最後の1件が構造STOP） |
| 一発PASS | committed教材では2/6 = 33.33%。停止007を含む着手全教材では2/7 = 28.57% |
| 平均attempt | 1.667 / committed text。各本 `[2,2,2,1,2,1]`、停止007は1attempt |
| retry一次原因 | future vocabulary 2、未登録compound 1、POS境界1。別途scope mismatch STOP 1 |
| future混入 | candidate 2/11、commit済み0 |
| 構造scope mismatch | 1件 |
| committed hard / unresolved / planned ID mismatch / replay差分 | すべて0 |
| coverage | controlled全件100%、previous最小98.45% |
| 文長・本文長 | sentence max 6、本文135〜144어절 |
| semantic / naturalness warning | committed本文55 / 1。semantic warningはhard gateに戻していない |
| 確認された言語問題 | committed本文0（作者自己評価）。初候補で確認し修正した問題4群をobservations JSONへ記録 |
| recurring pattern | committed本文のN에게 웃어요とhabit-progressive反復は0。3本以上の再発warningなし |
| 新出 / selected review / incidental | 12語 / 8 credit / 2 credit |
| outstanding / near-deadline / expired / 数学的回収不能debt | すべて0。50本連続での成立を証明するものではない |
| 実露出分布（500語全体） | 0回488語、1回4語、2回6語、3回2語 |
| genre | simple_outing / short_dialogue / objects / transport / food / shopping 各1 |
| 直近10本fingerprint最大類似 | 0.1667（簡易指標であり完全な意味類似判定ではない） |
| production wall | 530.98秒（8分50.98秒、未commit007と教材間時間を含む） |
| committed textのmean / median / p90 | 77.02 / 70.13 / 119.98秒。min 62.84、max 119.98秒 |
| 300本換算 | 正式算出なし。6本で構造停止したため、50本完走の速度・後半負荷を外挿しない |
| Phase 3.6aとの参考比較 | mean約40.0%、median約39.0%、p90約26.7%短い。ただし6本と10本の未対応小標本で、改善の証明ではない |
| 最大計測stage | scene_planning 254.98秒。planning＋draft＋repairは422.47秒で、次の速度改善対象はgenerator側 |
| pre / post regression | 各286 tests PASS。終了後zero-state raw replayは6本すべて一致 |

### timingの計数上の限界

001ではplan確定と本文作成を別tool callで行った。002〜007ではplanコマンドと本文ファイル作成を同じLLM tool-call payloadに含めたため、コマンド実行前に行われた本文の構成時間がscene_planningへ入っている。したがって個別planning/draft stageの厳密な分離はできていない。総wall timeは実測値を維持し、後からstage秒数を捏造・再配分していない。generatorの合計時間を解釈し、planning単独がボトルネックと断定しない。engineering/setupは215.85秒、pre/post tests・最終report・replayはproduction計測外。

### 次の提案（report-only）

まず、引用中で助詞を直接取る우리のscope identity instabilityを対象に、別Phaseで限定修正と否定対照fixtureを検討する。今回のrun内では修正も再開もしていない。既存286件がPASSしてもこの未収録ケースを解消したことにはならない。修正後の新zero-state trialで初めて50本運用を再評価する。語彙・文法意味範囲の拡張やsemantic gateの再厳格化は提案しない。

詳細補足は `k1_phase3_6b_run_observations.json`、機械結果の最終値は `k1_phase3_6b_validation_result.json` を参照。

Verdict **D: STRUCTURAL_FAIL**. Committed 6/50. No text beyond K1-050 was generated.

Frozen Phase 3.6a gate, analyzer, resolver, scheduler and policy are reused unchanged. Only the author overlay changes guidance. The new runner changes output paths, runtime max_text to 50 and timing/checkpoint reporting. Semantic role REVIEW/heuristic FAIL remain warnings.

Timing measures the live local LLM author and file callback, including reasoning and tool transport. It is not a prerecorded replay or isolated external API latency. Setup, pre-tests, post-tests and report/replay time are outside production wall time. Projections and atomic ledger are checked; final zero-state raw replay is separate.

Stop: {'type': 'structural_analyzer_defect', 'text': 7, 'errors': [{'code': 'unknown_or_unresolved', 'detail': {'vocab_id': None, 'lemma': '우리', 'surface': '우리', 'start': 260, 'reason': 'unknown_or_unresolved'}}, {'code': 'scope_identity_mismatch', 'detail': {'type': 'SCOPE_IDENTITY_MISMATCH', 'start': 260, 'end': 262, 'surface': '우리', 'views': [{'scope': 'sentence', 'original_offset': 259, 'before_recovery_ids': ['ko_k1_0004'], 'resolved_ids': ['ko_k1_0004'], 'ne_recovery_decisions': []}, {'scope': 'paragraph', 'original_offset': 186, 'before_recovery_ids': [], 'resolved_ids': [], 'ne_recovery_decisions': []}, {'scope': 'full_text', 'original_offset': 0, 'before_recovery_ids': [], 'resolved_ids': [], 'ne_recovery_decisions': []}], 'decision': 'UNRESOLVED', 'structural_defect': True, 'author_intent_not_authority': True}}, {'code': 'structural_analyzer_defect', 'detail': {'usage': {'vocab_id': None, 'lemma': '우리', 'surface': '우리', 'start': 260, 'reason': 'unknown_or_unresolved'}, 'sentence': '"우리는 한국어를 같이 배울 거예요."', 'isolated_pass': True}}, {'code': 'unresolved_context_ambiguity', 'detail': {'type': 'identity_boundary', 'surface': '우리', 'lemma': '우리', 'start': 260, 'raw_pos': 'NNG', 'registered_candidates': [{'id': 'ko_k1_0004', 'pos': 'pronoun', 'sense': 'we'}], 'alias_reason': None, 'status': 'REVIEW', 'requires_candidate_review': True}}, {'code': 'unresolved_context_ambiguity', 'detail': {'type': 'uri_pronoun_context', 'surface': '우리', 'raw_pos': 'NNG', 'raw_parts': [{'form': '우리', 'tag': 'NNG', 'start': 260, 'length': 2}], 'raw_indices': [152], 'start': 260, 'end': 262, 'scope': 'full_candidate', 'preceding_tokens': [{'form': '어요', 'tag': 'EF', 'start': 254, 'length': 2}, {'form': '.', 'tag': 'SF', 'start': 256, 'length': 1}, {'form': '"', 'tag': 'SSC', 'start': 257, 'length': 1}, {'form': '"', 'tag': 'SSO', 'start': 259, 'length': 1}], 'following_tokens': [{'form': '는', 'tag': 'JX', 'start': 262, 'length': 1}, {'form': '한국어', 'tag': 'NNP', 'start': 264, 'length': 3}, {'form': '를', 'tag': 'JKO', 'start': 267, 'length': 1}, {'form': '같이', 'tag': 'MAG', 'start': 269, 'length': 2}], 'following_noun': None, 'registered_id': 'ko_k1_0004', 'registered_pos': 'pronoun', 'registered_sense': 'we', 'context_evidence': {'exact_original_surface': True, 'unique_registered_identity': True, 'single_exact_raw_span': True, 'raw_np_or_nng': True, 'left_word_boundary': True, 'no_particle_on_uri': False, 'whitespace_before_head': False, 'limited_registered_nominal_head': False, 'following_head_exact': False, 'speaker_group_raw_anchor': True, 'no_spatial_noun_contrast': True, 'balanced_or_independent': True, 'annotation_group_exclusive': True, 'raw_span_accounted_once': True}, 'speaker_anchors': [{'form': '저', 'raw_pos': 'NP', 'start': 0, 'particle': '는'}, {'form': '저', 'raw_pos': 'NP', 'start': 30, 'particle': '는'}, {'form': '저', 'raw_pos': 'NP', 'start': 93, 'particle': '는'}, {'form': '저', 'raw_pos': 'NP', 'start': 137, 'particle': '는'}, {'form': '저', 'raw_pos': 'NP', 'start': 201, 'particle': '는'}], 'quotation_context': {'inside_balanced': True, 'open_offset': 259, 'close_offset': 279, 'opening': '"', 'closing': '"', 'inside_unmatched': False}, 'decision': 'REVIEW', 'original_annotation': [{'surface': '우리', 'lemma': '우리', 'pos': None, 'sense': None, 'vocab_id': None, 'role': 'unresolved', 'start': 260, 'end': 262, 'morph_indices': [152], 'grammar_id': None}], 'permission_granted': False, 'status': 'REVIEW', 'requires_candidate_review': True}}, {'code': 'coverage_or_token_policy', 'detail': 'Token 123: uncontrolled vocabulary or future introduction'}, {'code': 'coverage_or_token_policy', 'detail': 'controlled_vocab_coverage below hard 100%'}, {'code': 'coverage_or_token_policy', 'detail': 'previous_vocab_coverage below hard 98%'}]}. First-pass 2/6; mean attempts 1.6666666666666667; total attempts 11.
Production wall 530.98s. Per-text statistics: {'n': 6, 'min': 62.84094109999569, 'max': 119.97917779999989, 'mean': 77.0184484666667, 'median': 70.12529649999851, 'p90': 119.97917779999989}. Stages: {'scene_planning': 254.98220280000533, 'author_draft': 76.43984180000552, 'morphology_vocab_analysis': 15.490475699880335, 'mechanical_validation': 2.2709526001199265, 'retry_repair': 91.04871159998584, 'naturalness_review': 64.09094429999823, 'final_reanalysis': 8.663925499997276, 'commit': 3.674923700004001, 'controller_overhead': 4.5193739000023925}.
300 serial estimates: mean Noneh, median Noneh. Estimates are produced only on completion and do not include final human review or later vocabulary burden.
Baseline: {'mean': 128.3, 'median': 114.9, 'p90': 163.63, 'first_pass': 0.3, 'mean_attempts': 1.9}. Optimization target: generator.

Selected review 8; incidental 2; introduced 12; outstanding debt 0; expired 0; unrecoverable 0.
Exposure distribution: {0: 488, 2: 6, 3: 2, 1: 4}. Genre distribution: {'simple_outing': 1, 'short_dialogue': 1, 'objects': 1, 'transport': 1, 'food': 1, 'shopping': 1}. Max recent-ten fingerprint similarity 0.16666666666666666.
Semantic warnings 55; naturalness warnings 1; author-confirmed draft problems 0; committed problems 0. Self review is not independent gold.
Recurring patterns (heuristic, not hard errors): {}.

## Per-text results

| ID | attempts | eojeol | N/U | previous | selected/incidental | seconds |
|---|---:|---:|---|---:|---|---:|
| K1-001 | 2 | 142 | 140/2 | 98.57% | 0/0 | 62.84 |
| K1-002 | 2 | 138 | 133/2 | 98.50% | 0/0 | 69.41 |
| K1-003 | 2 | 137 | 135/2 | 98.52% | 2/0 | 70.84 |
| K1-004 | 1 | 135 | 129/2 | 98.45% | 2/0 | 65.41 |
| K1-005 | 2 | 144 | 138/2 | 98.55% | 2/1 | 119.98 |
| K1-006 | 1 | 137 | 130/2 | 98.46% | 2/1 | 73.63 |

## Full diagnostics

```json
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
  "speed_optimization_target": "generator"
}
```
