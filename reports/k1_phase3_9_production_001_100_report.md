# Phase 3.9 — 停止runの結果

**D / STRUCTURAL_FAIL（author callback入力契約違反による制御STOP）**。K1-001〜012の12本をcommitし、K1-013で停止した。100本endurance trialは未完了である。K1-014以降を生成しておらず、300本continuationへ進めない。

停止原因は、私が自己点検JSONの既定キーを誤って別名で記載したこと。解析器の誤解析、validatorの矛盾、schedulerの数学的不成立は確認されていない。controllerはcandidate提出前に停止し、K1-013へのcreditは0件だった。入力ミスと制御STOPを、Korean analyzer defectと混同しない。

## 実績

| 指標 | 結果 |
|---|---:|
| committed | 12 / 100 |
| 正式attempt総数 | 14 |
| 正式first-pass commit | 10 / 12 = 83.33% |
| mean attempts | 1.17 |
| 初回preflight findingあり | 6 / 12 = 50% |
| 初回preflight future findingあり | 0 / 12 = 0% |
| true formal future | 0 |
| committed future / unresolved / planned mismatch | 各0 |
| committed hard error / final canonical mismatch | 各0 |
| restricted-sense false acceptance | 機械再監査上0 |
| author naturalness repair | 1回（K1-008の借り物referent） |
| mechanical reject | 1回（K1-012のprevious coverage不足） |
| post-commit言語品質指摘 | 1件（K1-009、作者再読。独立goldではない） |
| post-commit追加レビュー候補 | 1件（K1-003の「종이에 말을 써요」） |
| 確認済みtranslation issue | 作者再読上0 |
| semantic grammar diagnostics | 142件。hard blockerにしていない |
| naturalness lint warnings | 9件（restricted_sense 6、reference_clarity 3） |

初回preflight率は、作者自己点検**後**に返されたdraftを測る。内部自己点検では未導入語などを修正しているため、rawの最初の文案にfutureがなかったとは主張しない。K1-013は自己点検契約が通らずpreflight未実施なので、分母から除外する。監査前collectorの13行分母値は別途保存する。

K1-012の初回正式candidateはN=146、U=3、previous=97.945%でrejectした。同じ通院・帰宅場面に沿う行動を加え、再candidateはN=151、U=3、previous=98.013%、157어절でPASSした。閾値を緩めず、失敗candidateへcreditしていない。

## Exposure / scheduler

| 指標 | 結果 |
|---|---:|
| 実際に導入済みExpansion | 24語 |
| selected review credits | 23 |
| incidental credits | 25 |
| current introduction credits | 24 |
| effective distinct Expansion credits | 72 |
| capped exposure progress | 72 / 3000 = 2.4% |
| remaining credits | 2928 |
| remaining texts to 300 | 288 |
| required_future_credit_rate | 10.1667 / text（soft GREEN） |
| outstanding windows | 5 |
| expired / recovered expired | 0 / 0 |
| near-deadline debt | 1 window（남편、期限015） |

同一本文内の複数tokenは1credit。effective creditには初出も含める。previous-only creditは48、effective平均は6/text。露出分布は0回476語、1回5語、2回5語、3回7語、4回1語、5回4語、6回2語。未導入476語の0回を欠落creditとして補完しない。

025 / 050 / 075 / 100には到達していないため、checkpoint trajectoryや100本時点のprojectionは未検証。12本時点のsoft GREENから長期scheduler成立を結論しない。

## Natural-expression gaps / diversity

生成中に記録したgapは2件：007の펴다、011の입히다。いずれもその動作を省略し、近い動詞へ無理に置換しなかった。commit後の009再読では、風を自然に描写する불다の不足を追加で記録した。`밖에는 비하고 바람이 있어요` のinventory風表現はreport-onlyで指摘し、次回は風の描写を省略する案を出す。既存本文や語彙DBは変更しない。

genreはfriends / short_dialogue / family / simple_outing / transport / food / school / objects / weather / work / home / healthが各1本。最大fingerprint similarityは0.0167。ただしlabel文字列の違いがスコアを小さくするため、これを意味的多様性の証明と扱わない。初期本文では本・家族・待機・着席会話の背景が複数回使われる。目的は変わるが、100本での展開反復は未検証。

平均140.08어절、範囲124〜179。sentence長分布は1어절8文、2어절1文、3어절31文、4어절242文、5어절110文、6어절10文。preferred 3〜7への適合は393/402=97.76%。自然な短い応答へ不要語を足していない。

## Timing

| 指標 | 秒 |
|---|---:|
| production wall（停止した013の作業も含む） | 3628.01（約1.01時間） |
| committed 12本 mean | 278.81 |
| median | 215.17 |
| p90（nearest-rank） | 487.30 |
| min / max | 110.63 / 688.96 |
| author_draft合計 | 1311.19 |
| scene_planning合計 | 932.34 |
| naturalness_review合計 | 664.98 |
| preflight repair合計 | 153.82（wallの4.24%） |
| formal retry repair合計 | 209.54（wallの5.78%） |

最大stageはauthor_draft。次の速度最適化対象はgenerator / author運用であり、validatorのhard条件を緩めることではない。Phase 3.8のmean136.95 / median124.89 / p90 219.31秒より、今回の部分実測は遅かった。自己点検後のfinding率が下がったことだけで速度改善を主張できない。

engineering/setupはproduction前の約533.76秒、pre full regressionを含む。post regression・ledger replay・report作成はproductionから除外した。時間はlive authorの推論・ツール往復・ファイル操作等を含む実測で、純粋な外部LLM API時間ではない。100本完走条件を満たさないため、300本mean/median estimateは**未算出**、正式performance判定もINCOMPLETEとする。

## Integrity / 判定

pre / post full regressionは各323件PASS。機械的hard・freeze・projection・zero-state ledger replayの確定結果は [validation result](k1_phase3_9_validation_result.json) を参照する。停止時のledger SHAはadministrative finalization前後一致。過去Phaseのfreeze成果物と今回のmechanical evaluate / atomic commitを変更していない。

今回のDはauthor callback契約作成ミスによる未完了runの判定であり、解析器研究やgrammar意味分類hard化を提案するものではない。次回は既定自己点検JSONテンプレートをそのまま使用し、同じproduction-lite pipelineで**新しいzero-state trial**を行うのが狭い修正となる。このrunを100本成功扱いにせず、final K1 corpus候補にも認定しない。

詳細：[停止監査](k1_phase3_9_stop_analysis.md)、[author契約事故](k1_phase3_9_author_contract_stop.json)、[review監査](k1_phase3_9_review_audit.json)、[本文spot review](k1_phase3_9_human_spot_review.md)。

## Audited machine-readable result

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
  "initial_finding_ratio": 0.5,
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
  "confirmed_committed_issues": [
    {
      "text": 9,
      "category": "C_naturalness",
      "surface": "밖에는 비하고 바람이 있어요.",
      "reason": "Weather is described with an inventory-like existential relation. In this context, 비가 와요 is the simpler idiomatic rain expression; a wind-action verb is not available in the current snapshot.",
      "preferred_strategy": "Omit the wind statement and use 밖에는 비가 많이 와요. No change applied to committed text.",
      "systematic_recurrence_established": false,
      "status": "report_only"
    }
  ],
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
  "continuation_requires_user_confirmation": true,
  "automatic_collector_initial_finding_ratio": 0.46153846153846156,
  "automatic_collector_initial_future_ratio": 0.0,
  "preflight_completed_texts": 12,
  "preflight_not_completed_texts": [
    13
  ],
  "preflight_rate_definition": "After author self-check, before official candidate; only completed preflights in denominator. Internal author repairs may precede this measurement.",
  "true_formal_future": 0,
  "confirmed_quality_issue_count": 1,
  "human_review_flags": [
    {
      "text": 3,
      "category": "C_naturalness",
      "surface": "언니는 종이에 말을 써요.",
      "reason": "Check whether 말 is a natural noun for the written birthday message here. Do not silently broaden the vocabulary policy or declare a new hard restriction.",
      "preferred_strategy": "The immediately following quotation can identify the message; an object-omitting sentence such as 언니가 종이에 써요 may suffice. Report only.",
      "status": "REVIEW"
    }
  ],
  "confirmed_translation_issue_count": 0,
  "quality_audit_origin": "Post-commit author reread; model screening, not independent human gold",
  "post_commit_gap_occurrences": [
    {
      "phase": "3.9",
      "text": 9,
      "intended_meaning": "wind blowing outside together with rain",
      "missing_natural_word": "불다",
      "current_workaround": "Committed text used an inventory-like 비하고 바람이 있어요; post-commit review flags it as unnatural.",
      "whether_omission_solved_it": false,
      "resolution": "report_only; future rewrite should omit wind rather than force an approximate predicate",
      "recurrence_count_in_this_run": 1,
      "origin": "post_commit_author_audit_not_human_gold"
    }
  ],
  "engineering_setup_seconds": 533.760428,
  "endurance_trial_validated": false,
  "checkpoint_numbers_reached": [],
  "stop_classification": "operator_author_callback_contract_error; no lexical analyzer defect established",
  "partial_performance_comparison": {
    "phase3_8_mean": 136.95,
    "phase3_8_median": 124.89,
    "phase3_8_p90": 219.31,
    "mean_ratio": 2.03588004295973,
    "median_ratio": 1.722882170710234,
    "formal_performance_rating": "INCOMPLETE"
  }
}
```
