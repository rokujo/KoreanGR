# Phase 3.9a 結果要約

**D / STRUCTURAL_FAIL。66/100 commit、K1-067で停止。068以降は生成していない。**

今回のauthor contract retry修正と少数known-gap promptは実装・回帰テストを通過した。停止原因はcontract typoではなく、予定新出 `졸리다` の登録adjectiveと単文Kiwi VVの不整合である。production中に解析器を変更せず、067の候補をcreditしなかった。

| 指標 | 結果 |
|---|---:|
| commit | 66/100 |
| formal attempts | 80（commitした66本は79、停止067は1） |
| formal first-pass | 55/66 = 83.33% |
| mean attempts/committed text | 1.197 |
| author_contract_retry_count | 0 |
| production contract failures recovered | 0（fixtureでの回復検証とは別） |
| contract max3 exhaustion | なし |
| 初回返却済みdraftのfinding | 28/67 = 41.79% |
| 初回返却済みdraftのapparent future finding | 3/67 = 4.48% |
| committed future / unresolved | 0 / 0 |
| committed hard errors / planned mismatch / final canonical mismatch | 0 / 0 / 0 |
| selected review / incidental | 153 / 559 credit |
| actual introduced Expansion | 131語 |
| effective distinct Expansion credits | 843（初出を含む、同一教材同一語は1） |
| capped exposure progress | 554/3000 |
| required_future_credit_rate | 2446 / 234 = 10.453、GREEN（soft） |
| outstanding / near deadline / expired debt | 65 / 13 / 14 windows |
| recovered expired / ever expired | 35 / 49 windows |
| saved known-gap events | 2（027: 지우다、061: スープの汁を表す국물不足を省略） |
| production wall | 15460.65秒 = 約4.295時間 |
| committed sec/text mean / median / p90 | 223.42 / 188.69 / 328.05 |
| committed sec/text min / max | 104.09 / 607.16 |
| 300本serial推定 | 未算出：100本未完走 |
| performance正式色判定 | INCOMPLETE：100本未完走 |

正式validatorのfuture flagは失敗066に1件あったが、元のsurfaceは予定新出 `목마르다` の活用であり、`목 + 마르다` への分割に起因する。これはreport-onlyの作者確認で、意図した語彙の真の未導入使用とは区別する。validatorの結果を成功へ書き換えず、短い自然文へrepair後PASSした。001の그것、042の봉지も含め、apparent finding率を真のfuture使用率と同一視しない。

## contract・品質・履歴

pre/post full suiteは各331 PASS、failures/errors/skips=0。schemaのkeyは旧正式実装から移行し、controller/author template/testsが同じJSON Schemaを読む。missing/misspelling/extra/type/許可値/parse errorをstate-safeに回復する。本文・訳・titleのdigestを保持、contract-only failureをformal attemptへ数えず、最大3回を別管理する。実本番でtypoが回復した実績はないため、テスト成功と本番実績を分ける。

K1-027の1文と訳に、作者のUnicode転送ミスによる文字化けがcommit後に見つかった。明確なlanguage/content quality問題1 incident、translation問題1 incidentとして記録する。同じincidentにより、紙の交換のreferent明示も欠けた。mechanical coverageではpunctuationとして扱われ、当該spanに語彙creditはない。凍結本文とledgerは上書きせず、人間spot reviewへ含める。機械hard PASSだけでfinal corpus品質PASSとは言わない。

known-gap 2件は保存済みの観察イベント数であり、内部下書き全体の完全なgap監査ではない。wind/messageの新negativeはauthor支援のみ。語彙800・文法32・初出・windows・sense registryは変更していない。過去Phase 3.9その他のfreeze成果物を今回の成功へ書き換えていない。

## scheduler・diversity・速度

025→050→停止066の必要平均は10.211→10.408→10.453と上昇。expired回収35 windowsは実績だが、残り100本試験は未完了で長期成立を承認できない。065〜066で回収した一方、未消化65 windowsは依然保持する。75/100 checkpointは到達していないので作成しない。

genreは18種類。fingerprintの低い類似度だけで意味的重複なしとは断定しない。ホテル準備・写真の共有・家族の食事・忘れ物等の再利用は、人間spot reviewでgoal/problem/resolutionの違いを確認する。review quotaのための副次事件を避け、vetoをdeadlineより優先した。

最大計時stageはscene_planning（6049.80秒）。scene planning＋author draft＋naturalness reviewは約75.0%のproduction wallを占める。ただしscene_planningはbegin→plan受理であり、sceneと最初の本文案を同じauthor応答で作成した時間も一部含む。author_draftはplan受理後の時間。両者を純粋な独立LLM latencyへ分解したbenchmarkではない。

preflight repairはwallの約7.77%、formal retry repairは約1.43%。contract retry overheadは0。pre-run engineering/setup（pre full suiteを含む）とpost regression/replay/reportingはproduction wall外。partialの平均は3.8 full50の136.95秒より遅いが、標本・負荷・計測待機が違うため正式な100本速度改善とは判定しない。

## 次に進めるか

**101〜300 continuationには進めない。** 次の修正候補は `졸리다` の登録POSとKiwi POSとの限定互換の一点。新しい一般semantic parserや全800語の語義監査へ広げない。変更は今回のrunへ適用せず、別開発版でpositive/negative・planned identity・failed-state isolationを確認してから、別zero-state enduranceを検討する。027のartifact修正も別版で扱う。

数値の詳細・freeze/integrity・ledger replay結果はvalidation JSON、韓国語本文＋日本語訳はhuman spot review、contractと停止の根拠はそれぞれ専用レポートに保存する。


## Implementation and measurement details

# Phase 3.9a endurance trial

**D / STRUCTURAL_FAIL** — 66/100 committed. No K1-101 or later generated.

Mechanical evaluate and atomic commit are byte-identical to Phase 3.8. The new envelope changes only run range/paths/provenance. Prompt and scene presentation were frozen before production. Existing credit/payment rules remain authoritative. Semantic warnings never block production.

Effective credit includes introductions plus selected and incidental distinct Expansion appearances; previous-only credits are separately recorded per text. Capped progress counts each vocabulary ID at most six times. Repetition beyond six never reduces remaining required credits.

Timing is live local author/callback wall time, not isolated external API latency. Engineering, pre/post regression, reporting and replay are excluded. Author self-checks are not independent gold. Early review hints can be vetoed; no selection is credited without canonical body occurrence.

First pass 0.8333333333333334; mean attempts 1.196969696969697; contract-only retries 0 (recovered 0); initial findings 0.417910447761194; initial future 0.04477611940298507.
Capped progress 554/3000; future required rate 10.452991452991453; outstanding 65; expired 14; recovered expired 35.
Timing {'n': 66, 'mean': 223.4167436909091, 'median': 188.69299119999778, 'p90': 328.0494786000054, 'min': 104.08582539999043, 'max': 607.1556311999884}; wall 15460.646900200009; stages {'scene_planning': 6049.802819399949, 'lexical_preflight': 128.21828470003675, 'author_draft': 3614.90098510003, 'preflight_repair': 1200.9025361000095, 'morphology_vocab_analysis': 189.6765712993947, 'mechanical_validation': 478.62071090054815, 'naturalness_review': 1929.6008794999798, 'final_reanalysis': 159.51836620001995, 'commit': 900.2171601000591, 'controller_overhead': 72.23779549993924, 'retry_repair': 221.22110780004004}; performance INCOMPLETE.
300-text serial hours: mean None, median None. Later vocabulary load and human quality review are excluded.
No automatic continuation: user confirmation is required before K1-101..300.


## Full metrics

```json
{
  "phase": "3.9a",
  "committed_count": 66,
  "completed": false,
  "stop": {
    "type": "structural_lexical_pos_contract",
    "text": 67,
    "vocab_id": "ko_k1_0419",
    "registered_pos": "adjective",
    "observed_sentence_raw_pos": "VV",
    "reason": "All six independent basic-inflection probes yield VV for the planned sleepy lemma; frozen POS compatibility leaves registered identity unresolved. No unsafe alias, DB edit or planned introduction omission permitted during production.",
    "failed_candidate_credited": false,
    "max_attempt_exhaustion": false
  },
  "total_attempts": 80,
  "formal_first_pass_count": 55,
  "formal_first_pass_ratio": 0.8333333333333334,
  "mean_attempts": 1.196969696969697,
  "initial_draft_with_finding": 28,
  "initial_draft_with_future": 3,
  "initial_finding_ratio": 0.417910447761194,
  "initial_future_ratio": 0.04477611940298507,
  "preflight_completed_count": 67,
  "author_contract_retry_count": 0,
  "contract_failures_recovered": 0,
  "contract_max_exhaustion": false,
  "formal_future_findings": [
    {
      "text": 66,
      "attempt": 1,
      "vocab_id": "ko_k1_0670",
      "lemma": "목",
      "surface": "목",
      "start": 454,
      "reason": "future_expansion"
    }
  ],
  "retry_error_codes": {
    "unknown_or_unresolved": 6,
    "coverage_or_token_policy": 14,
    "candidate_format": 1,
    "unresolved_context_ambiguity": 3,
    "future_expansion": 1,
    "planned_new_not_present": 2
  },
  "hard_errors": 0,
  "committed_future": 0,
  "committed_unresolved": 0,
  "planned_mismatch": 0,
  "final_canonical_mismatch": 0,
  "integrity_errors": [],
  "restricted_false_accepts": [],
  "failed_state_isolation": true,
  "semantic_warning_count": 967,
  "naturalness_warning_categories": {
    "nat_reference_clarity": 44,
    "nat_restricted_sense": 27,
    "nat_verb_argument_frame": 8,
    "nat_filler_adverb": 11,
    "nat_genitive_overuse": 1
  },
  "confirmed_committed_issues": [
    {
      "text_number": 27,
      "category": "translation_and_language_quality",
      "confirmed": true,
      "type": "author_file_transport_encoding_failure",
      "cause": "A PowerShell-to-Python pipe used to insert one Korean/Japanese pair encoded the Unicode literals as question marks. The author reviewed the intended insertion instead of the serialized pair before commit.",
      "impact": "One added paper-exchange sentence and its translation are corrupted; the intended explicit exchange therefore is missing. Existing Korean sentences remain preserved.",
      "mechanical_interpretation": "The corrupted span is punctuation rather than an unknown content word under the existing lexical denominator, so its acceptance does not establish correct language quality. No intro/exposure credit arose from that span.",
      "resolution": "Committed historical text stays frozen. Later candidate files use Unicode-preserving apply_patch; post-mechanical author review reads serialized pairs. Propose future corpus repair in a separate authorized version, not during this frozen trial.",
      "human_review_required": true,
      "not_an_analyzer_or_scope_research_change": true
    }
  ],
  "author_repair_count": 7,
  "known_gap_occurrences": [
    {
      "phase": "3.9a",
      "text": 27,
      "intended_meaning": "erase the initial written answer before rewriting",
      "missing_natural_word": "지우다",
      "current_workaround": "omit erasing action; borrow the eraser and write the answer again without a substitute verb",
      "whether_omission_solved_it": true,
      "resolution": "omit_rewrite",
      "recurrence_count_in_this_run": 1,
      "historical_reference": "Existing known gap from Phase 3.8/3.9; no new restriction or vocabulary change."
    },
    {
      "phase": "3.9a",
      "text": 61,
      "intended_meaning": "friend consumes ramen broth with spoon",
      "missing_natural_word": "국물",
      "current_workaround": "omit broth description; state ordinary spoon use",
      "whether_omission_solved_it": true,
      "resolution": "omit",
      "recurrence_count_in_this_run": 1,
      "source": "Post-run compilation of saved live-author self-check note; not a new lexical restriction and not an exhaustive internal-gap count"
    }
  ],
  "selected_review": 153,
  "incidental": 559,
  "introduced_count": 131,
  "effective_review_credits": 843,
  "effective_credit_distribution": {
    "n": 66,
    "mean": 12.772727272727273,
    "median": 13.0,
    "p90": 19,
    "min": 2,
    "max": 29
  },
  "exposure_distribution": {
    "7": 12,
    "8": 8,
    "0": 369,
    "11": 3,
    "6": 9,
    "5": 13,
    "3": 14,
    "23": 1,
    "20": 2,
    "16": 2,
    "15": 3,
    "14": 3,
    "10": 3,
    "12": 1,
    "13": 3,
    "9": 5,
    "1": 17,
    "2": 18,
    "4": 10,
    "21": 1,
    "31": 1,
    "26": 1,
    "22": 1
  },
  "outstanding_debt": [
    {
      "vocab_id": "ko_k1_0301",
      "window_index": 2,
      "window": {
        "from": 33,
        "to": 73
      }
    },
    {
      "vocab_id": "ko_k1_0306",
      "window_index": 2,
      "window": {
        "from": 35,
        "to": 75
      }
    },
    {
      "vocab_id": "ko_k1_0310",
      "window_index": 2,
      "window": {
        "from": 37,
        "to": 77
      }
    },
    {
      "vocab_id": "ko_k1_0326",
      "window_index": 2,
      "window": {
        "from": 65,
        "to": 105
      }
    },
    {
      "vocab_id": "ko_k1_0340",
      "window_index": 2,
      "window": {
        "from": 52,
        "to": 92
      }
    },
    {
      "vocab_id": "ko_k1_0342",
      "window_index": 2,
      "window": {
        "from": 53,
        "to": 93
      }
    },
    {
      "vocab_id": "ko_k1_0343",
      "window_index": 0,
      "window": {
        "from": 31,
        "to": 34
      }
    },
    {
      "vocab_id": "ko_k1_0343",
      "window_index": 1,
      "window": {
        "from": 35,
        "to": 53
      }
    },
    {
      "vocab_id": "ko_k1_0343",
      "window_index": 2,
      "window": {
        "from": 54,
        "to": 94
      }
    },
    {
      "vocab_id": "ko_k1_0345",
      "window_index": 1,
      "window": {
        "from": 36,
        "to": 54
      }
    },
    {
      "vocab_id": "ko_k1_0345",
      "window_index": 2,
      "window": {
        "from": 55,
        "to": 95
      }
    },
    {
      "vocab_id": "ko_k1_0349",
      "window_index": 2,
      "window": {
        "from": 57,
        "to": 97
      }
    },
    {
      "vocab_id": "ko_k1_0350",
      "window_index": 2,
      "window": {
        "from": 57,
        "to": 97
      }
    },
    {
      "vocab_id": "ko_k1_0352",
      "window_index": 1,
      "window": {
        "from": 40,
        "to": 58
      }
    },
    {
      "vocab_id": "ko_k1_0352",
      "window_index": 2,
      "window": {
        "from": 59,
        "to": 99
      }
    },
    {
      "vocab_id": "ko_k1_0353",
      "window_index": 1,
      "window": {
        "from": 41,
        "to": 59
      }
    },
    {
      "vocab_id": "ko_k1_0353",
      "window_index": 2,
      "window": {
        "from": 60,
        "to": 100
      }
    },
    {
      "vocab_id": "ko_k1_0354",
      "window_index": 1,
      "window": {
        "from": 41,
        "to": 59
      }
    },
    {
      "vocab_id": "ko_k1_0354",
      "window_index": 2,
      "window": {
        "from": 60,
        "to": 100
      }
    },
    {
      "vocab_id": "ko_k1_0355",
      "window_index": 2,
      "window": {
        "from": 61,
        "to": 101
      }
    },
    {
      "vocab_id": "ko_k1_0356",
      "window_index": 2,
      "window": {
        "from": 61,
        "to": 101
      }
    },
    {
      "vocab_id": "ko_k1_0357",
      "window_index": 2,
      "window": {
        "from": 62,
        "to": 102
      }
    },
    {
      "vocab_id": "ko_k1_0358",
      "window_index": 2,
      "window": {
        "from": 62,
        "to": 102
      }
    },
    {
      "vocab_id": "ko_k1_0359",
      "window_index": 2,
      "window": {
        "from": 63,
        "to": 103
      }
    },
    {
      "vocab_id": "ko_k1_0361",
      "window_index": 2,
      "window": {
        "from": 64,
        "to": 104
      }
    },
    {
      "vocab_id": "ko_k1_0366",
      "window_index": 0,
      "window": {
        "from": 43,
        "to": 46
      }
    },
    {
      "vocab_id": "ko_k1_0366",
      "window_index": 1,
      "window": {
        "from": 47,
        "to": 65
      }
    },
    {
      "vocab_id": "ko_k1_0366",
      "window_index": 2,
      "window": {
        "from": 66,
        "to": 106
      }
    },
    {
      "vocab_id": "ko_k1_0367",
      "window_index": 0,
      "window": {
        "from": 44,
        "to": 47
      }
    },
    {
      "vocab_id": "ko_k1_0367",
      "window_index": 1,
      "window": {
        "from": 48,
        "to": 66
      }
    },
    {
      "vocab_id": "ko_k1_0368",
      "window_index": 1,
      "window": {
        "from": 48,
        "to": 66
      }
    },
    {
      "vocab_id": "ko_k1_0369",
      "window_index": 1,
      "window": {
        "from": 49,
        "to": 67
      }
    },
    {
      "vocab_id": "ko_k1_0370",
      "window_index": 1,
      "window": {
        "from": 49,
        "to": 67
      }
    },
    {
      "vocab_id": "ko_k1_0371",
      "window_index": 1,
      "window": {
        "from": 50,
        "to": 68
      }
    },
    {
      "vocab_id": "ko_k1_0374",
      "window_index": 0,
      "window": {
        "from": 47,
        "to": 50
      }
    },
    {
      "vocab_id": "ko_k1_0374",
      "window_index": 1,
      "window": {
        "from": 51,
        "to": 69
      }
    },
    {
      "vocab_id": "ko_k1_0380",
      "window_index": 1,
      "window": {
        "from": 54,
        "to": 72
      }
    },
    {
      "vocab_id": "ko_k1_0386",
      "window_index": 1,
      "window": {
        "from": 57,
        "to": 75
      }
    },
    {
      "vocab_id": "ko_k1_0388",
      "window_index": 1,
      "window": {
        "from": 58,
        "to": 76
      }
    },
    {
      "vocab_id": "ko_k1_0390",
      "window_index": 1,
      "window": {
        "from": 59,
        "to": 77
      }
    },
    {
      "vocab_id": "ko_k1_0392",
      "window_index": 0,
      "window": {
        "from": 56,
        "to": 59
      }
    },
    {
      "vocab_id": "ko_k1_0392",
      "window_index": 1,
      "window": {
        "from": 60,
        "to": 78
      }
    },
    {
      "vocab_id": "ko_k1_0394",
      "window_index": 1,
      "window": {
        "from": 61,
        "to": 79
      }
    },
    {
      "vocab_id": "ko_k1_0395",
      "window_index": 1,
      "window": {
        "from": 61,
        "to": 79
      }
    },
    {
      "vocab_id": "ko_k1_0396",
      "window_index": 1,
      "window": {
        "from": 62,
        "to": 80
      }
    },
    {
      "vocab_id": "ko_k1_0397",
      "window_index": 1,
      "window": {
        "from": 62,
        "to": 80
      }
    },
    {
      "vocab_id": "ko_k1_0399",
      "window_index": 0,
      "window": {
        "from": 59,
        "to": 62
      }
    },
    {
      "vocab_id": "ko_k1_0399",
      "window_index": 1,
      "window": {
        "from": 63,
        "to": 81
      }
    },
    {
      "vocab_id": "ko_k1_0400",
      "window_index": 1,
      "window": {
        "from": 64,
        "to": 82
      }
    },
    {
      "vocab_id": "ko_k1_0401",
      "window_index": 1,
      "window": {
        "from": 64,
        "to": 82
      }
    },
    {
      "vocab_id": "ko_k1_0402",
      "window_index": 0,
      "window": {
        "from": 61,
        "to": 64
      }
    },
    {
      "vocab_id": "ko_k1_0402",
      "window_index": 1,
      "window": {
        "from": 65,
        "to": 83
      }
    },
    {
      "vocab_id": "ko_k1_0403",
      "window_index": 1,
      "window": {
        "from": 65,
        "to": 83
      }
    },
    {
      "vocab_id": "ko_k1_0404",
      "window_index": 0,
      "window": {
        "from": 62,
        "to": 65
      }
    },
    {
      "vocab_id": "ko_k1_0404",
      "window_index": 1,
      "window": {
        "from": 66,
        "to": 84
      }
    },
    {
      "vocab_id": "ko_k1_0405",
      "window_index": 1,
      "window": {
        "from": 66,
        "to": 84
      }
    },
    {
      "vocab_id": "ko_k1_0406",
      "window_index": 0,
      "window": {
        "from": 63,
        "to": 66
      }
    },
    {
      "vocab_id": "ko_k1_0407",
      "window_index": 0,
      "window": {
        "from": 63,
        "to": 66
      }
    },
    {
      "vocab_id": "ko_k1_0408",
      "window_index": 0,
      "window": {
        "from": 64,
        "to": 67
      }
    },
    {
      "vocab_id": "ko_k1_0409",
      "window_index": 0,
      "window": {
        "from": 64,
        "to": 67
      }
    },
    {
      "vocab_id": "ko_k1_0411",
      "window_index": 0,
      "window": {
        "from": 65,
        "to": 68
      }
    },
    {
      "vocab_id": "ko_k1_0412",
      "window_index": 0,
      "window": {
        "from": 66,
        "to": 69
      }
    },
    {
      "vocab_id": "ko_k1_0414",
      "window_index": 0,
      "window": {
        "from": 66,
        "to": 69
      }
    },
    {
      "vocab_id": "ko_k1_0770",
      "window_index": 2,
      "window": {
        "from": 58,
        "to": 98
      }
    },
    {
      "vocab_id": "ko_k1_0778",
      "window_index": 2,
      "window": {
        "from": 66,
        "to": 106
      }
    }
  ],
  "expired_debt": [
    {
      "vocab_id": "ko_k1_0343",
      "window_index": 0,
      "window": {
        "from": 31,
        "to": 34
      }
    },
    {
      "vocab_id": "ko_k1_0343",
      "window_index": 1,
      "window": {
        "from": 35,
        "to": 53
      }
    },
    {
      "vocab_id": "ko_k1_0345",
      "window_index": 1,
      "window": {
        "from": 36,
        "to": 54
      }
    },
    {
      "vocab_id": "ko_k1_0352",
      "window_index": 1,
      "window": {
        "from": 40,
        "to": 58
      }
    },
    {
      "vocab_id": "ko_k1_0353",
      "window_index": 1,
      "window": {
        "from": 41,
        "to": 59
      }
    },
    {
      "vocab_id": "ko_k1_0354",
      "window_index": 1,
      "window": {
        "from": 41,
        "to": 59
      }
    },
    {
      "vocab_id": "ko_k1_0366",
      "window_index": 0,
      "window": {
        "from": 43,
        "to": 46
      }
    },
    {
      "vocab_id": "ko_k1_0366",
      "window_index": 1,
      "window": {
        "from": 47,
        "to": 65
      }
    },
    {
      "vocab_id": "ko_k1_0367",
      "window_index": 0,
      "window": {
        "from": 44,
        "to": 47
      }
    },
    {
      "vocab_id": "ko_k1_0374",
      "window_index": 0,
      "window": {
        "from": 47,
        "to": 50
      }
    },
    {
      "vocab_id": "ko_k1_0392",
      "window_index": 0,
      "window": {
        "from": 56,
        "to": 59
      }
    },
    {
      "vocab_id": "ko_k1_0399",
      "window_index": 0,
      "window": {
        "from": 59,
        "to": 62
      }
    },
    {
      "vocab_id": "ko_k1_0402",
      "window_index": 0,
      "window": {
        "from": 61,
        "to": 64
      }
    },
    {
      "vocab_id": "ko_k1_0404",
      "window_index": 0,
      "window": {
        "from": 62,
        "to": 65
      }
    }
  ],
  "recovered_expired_count": 35,
  "ever_expired_count": 49,
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
    ],
    [
      "ko_k1_0332",
      0
    ],
    [
      "ko_k1_0338",
      0
    ],
    [
      "ko_k1_0340",
      0
    ],
    [
      "ko_k1_0341",
      0
    ],
    [
      "ko_k1_0342",
      0
    ],
    [
      "ko_k1_0345",
      0
    ],
    [
      "ko_k1_0347",
      0
    ],
    [
      "ko_k1_0348",
      0
    ],
    [
      "ko_k1_0349",
      0
    ],
    [
      "ko_k1_0350",
      0
    ],
    [
      "ko_k1_0351",
      1
    ],
    [
      "ko_k1_0354",
      0
    ],
    [
      "ko_k1_0358",
      1
    ],
    [
      "ko_k1_0360",
      0
    ],
    [
      "ko_k1_0368",
      0
    ],
    [
      "ko_k1_0369",
      0
    ],
    [
      "ko_k1_0370",
      0
    ],
    [
      "ko_k1_0371",
      0
    ],
    [
      "ko_k1_0372",
      0
    ],
    [
      "ko_k1_0376",
      0
    ],
    [
      "ko_k1_0380",
      0
    ],
    [
      "ko_k1_0382",
      0
    ],
    [
      "ko_k1_0384",
      0
    ],
    [
      "ko_k1_0385",
      0
    ],
    [
      "ko_k1_0388",
      0
    ],
    [
      "ko_k1_0391",
      0
    ],
    [
      "ko_k1_0394",
      0
    ],
    [
      "ko_k1_0395",
      0
    ],
    [
      "ko_k1_0396",
      0
    ],
    [
      "ko_k1_0397",
      0
    ],
    [
      "ko_k1_0810",
      0
    ]
  ],
  "near_deadline_debt": [
    {
      "vocab_id": "ko_k1_0367",
      "window_index": 1,
      "window": {
        "from": 48,
        "to": 66
      }
    },
    {
      "vocab_id": "ko_k1_0368",
      "window_index": 1,
      "window": {
        "from": 48,
        "to": 66
      }
    },
    {
      "vocab_id": "ko_k1_0369",
      "window_index": 1,
      "window": {
        "from": 49,
        "to": 67
      }
    },
    {
      "vocab_id": "ko_k1_0370",
      "window_index": 1,
      "window": {
        "from": 49,
        "to": 67
      }
    },
    {
      "vocab_id": "ko_k1_0371",
      "window_index": 1,
      "window": {
        "from": 50,
        "to": 68
      }
    },
    {
      "vocab_id": "ko_k1_0374",
      "window_index": 1,
      "window": {
        "from": 51,
        "to": 69
      }
    },
    {
      "vocab_id": "ko_k1_0406",
      "window_index": 0,
      "window": {
        "from": 63,
        "to": 66
      }
    },
    {
      "vocab_id": "ko_k1_0407",
      "window_index": 0,
      "window": {
        "from": 63,
        "to": 66
      }
    },
    {
      "vocab_id": "ko_k1_0408",
      "window_index": 0,
      "window": {
        "from": 64,
        "to": 67
      }
    },
    {
      "vocab_id": "ko_k1_0409",
      "window_index": 0,
      "window": {
        "from": 64,
        "to": 67
      }
    },
    {
      "vocab_id": "ko_k1_0411",
      "window_index": 0,
      "window": {
        "from": 65,
        "to": 68
      }
    },
    {
      "vocab_id": "ko_k1_0412",
      "window_index": 0,
      "window": {
        "from": 66,
        "to": 69
      }
    },
    {
      "vocab_id": "ko_k1_0414",
      "window_index": 0,
      "window": {
        "from": 66,
        "to": 69
      }
    }
  ],
  "genre_distribution": {
    "school": 7,
    "friends": 5,
    "home": 3,
    "outdoor": 1,
    "short_dialogue": 2,
    "shopping": 6,
    "family": 6,
    "travel": 5,
    "simple_outing": 4,
    "objects": 2,
    "health": 2,
    "daily_life": 4,
    "simple_hobby": 3,
    "food": 4,
    "small_problem": 5,
    "transport": 3,
    "weather": 1,
    "work": 3
  },
  "max_scene_similarity": 0.16666666666666666,
  "eojeol": {
    "n": 66,
    "mean": 140.62121212121212,
    "median": 139.0,
    "p90": 150,
    "min": 125,
    "max": 170
  },
  "sentence_length_distribution": {
    "4": 1087,
    "5": 799,
    "3": 130,
    "1": 19,
    "6": 80,
    "2": 16,
    "7": 2,
    "8": 1
  },
  "production_wall_seconds": 15460.646900200009,
  "per_text_seconds": {
    "n": 66,
    "mean": 223.4167436909091,
    "median": 188.69299119999778,
    "p90": 328.0494786000054,
    "min": 104.08582539999043,
    "max": 607.1556311999884
  },
  "stage_seconds": {
    "scene_planning": 6049.802819399949,
    "lexical_preflight": 128.21828470003675,
    "author_draft": 3614.90098510003,
    "preflight_repair": 1200.9025361000095,
    "morphology_vocab_analysis": 189.6765712993947,
    "mechanical_validation": 478.62071090054815,
    "naturalness_review": 1929.6008794999798,
    "final_reanalysis": 159.51836620001995,
    "commit": 900.2171601000591,
    "controller_overhead": 72.23779549993924,
    "retry_repair": 221.22110780004004
  },
  "preflight_repair_fraction": 0.07767479225493946,
  "formal_retry_fraction": 0.014308657925379447,
  "largest_stage": "scene_planning",
  "capped_exposure_progress": 554,
  "required_total": 3000,
  "remaining_required_capped_credits": 2446,
  "remaining_texts_to_300": 234,
  "required_future_credit_rate": 10.452991452991453,
  "planning_color": "GREEN",
  "outstanding_windows": 65,
  "expired_windows": 14,
  "ledger_replay_errors": [],
  "pre_regression": {
    "tests": 331,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 310.9647130999947,
    "success": true
  },
  "post_regression": {
    "tests": 331,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "seconds": 168.4196854000038,
    "success": true
  },
  "performance": "INCOMPLETE",
  "checkpoint_trajectory": [
    {
      "text": 25,
      "rate": 10.210909090909091,
      "trajectory": "initial"
    },
    {
      "text": 50,
      "rate": 10.408,
      "trajectory": "rising"
    }
  ],
  "verdict": "D",
  "status": "STRUCTURAL_FAIL",
  "estimated_300_mean_hours": null,
  "estimated_300_median_hours": null,
  "corpus_candidate_reusable": false,
  "continuation_requires_user_confirmation": true,
  "automatic_committed_pattern_findings": [],
  "confirmed_language_quality_incident_count": 1,
  "translation_issue_incident_count": 1,
  "quality_review_limit": "Author screening and selected spot review, not independent human gold or exhaustive semantic audit.",
  "committed_registered_gap_events": [
    {
      "text": 27,
      "intended_meaning": "erase the initial written answer before rewriting",
      "missing_natural_word": "지우다",
      "current_workaround": "omit erasing action; borrow the eraser and write the answer again without a substitute verb",
      "whether_omission_solved_it": true,
      "resolution": "omit_rewrite",
      "recurrence_count_in_this_run": 1,
      "historical_reference": "Existing known gap from Phase 3.8/3.9; no new restriction or vocabulary change."
    }
  ],
  "known_gap_event_count": 2,
  "known_gap_count_limit": "Saved observed events only; internal draft corrections were not exhaustively archived.",
  "formal_future_flag_count": 1,
  "formal_future_assessment": [
    {
      "text": 66,
      "attempt": 1,
      "vocab_id": "ko_k1_0670",
      "lemma": "목",
      "surface": "목",
      "start": 454,
      "reason": "future_expansion",
      "assessment": "parser_split_of_planned_compound",
      "original_compound_vocab_id": "ko_k1_0418",
      "evidence": "Failed 066 source contains inflected planned thirsty word, not an independent neck noun. Simple first-person sentence in attempt02 resolves planned identity. Failed attempt remains rejected."
    }
  ],
  "true_formal_future_violation_count_report_only": 0,
  "formal_future_assessment_origin": "Post-run author audit of original surface and current planned ID; hard results are not rewritten.",
  "initial_finding_metric_definition": "First returned self-checked draft scanned once per text, not raw first internal writing. Includes stopped text067; 67 scans.",
  "raw_internal_draft_finding_rate": null,
  "raw_internal_draft_metric_limit": "Some internal self-check repairs saved in notes; no complete raw internal draft archive. Do not infer raw compliance from callback preflight rates.",
  "benchmark_is_partial": true,
  "pre_run_engineering_setup_wall_seconds_including_pre_suite": 508.588251,
  "stage_boundary_limit": "Scene planning is begin-to-plan receipt and sometimes includes first prose draft written with scene metadata. Author draft is later interval. Live author wall includes reasoning, tool transport and context pauses, not pure external API latency.",
  "generator_planning_draft_review_fraction": 0.7499236454232693,
  "unattributed_production_wall_seconds": 515.7296836000023,
  "unattributed_wall_description": "Inter-text initialization and callback/control time outside per-text stage timers; not silently removed.",
  "genre_count": 18,
  "exposure_distribution_compact": {
    "0": 369,
    "1": 17,
    "2": 18,
    "3": 14,
    "4": 10,
    "5": 13,
    "6_plus": 59
  },
  "partial_scheduler_trajectory": [
    {
      "text": 25,
      "rate": 10.210909090909091,
      "trajectory": "initial"
    },
    {
      "text": 50,
      "rate": 10.408,
      "trajectory": "rising"
    },
    {
      "text": 66,
      "rate": 10.452991452991453,
      "trajectory": "rising_since_050",
      "checkpoint": false
    }
  ],
  "scheduler_endurance_proven": false,
  "contract_recovery_tested_in_regression": true,
  "contract_recovery_observed_in_production": false,
  "missing_checkpoints": [
    75,
    100
  ],
  "current_corpus_needs_quality_repair_in_separate_version": [
    27
  ],
  "spot_review_text_numbers": [
    1,
    4,
    5,
    7,
    10,
    11,
    12,
    19,
    21,
    24,
    25,
    27,
    28,
    34,
    39,
    41,
    45,
    50,
    51,
    61
  ]
}
```
