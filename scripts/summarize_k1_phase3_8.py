"""Post-run reporting only. Does not modify engines, inputs, texts or ledger."""
from collections import Counter
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'reports'
P = ROOT / 'pilot/ko/k1/phase3_8'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    r = read(R / 'k1_phase3_8_validation_result.json')
    if not r['completed'] or r['ledger_replay_errors'] or r['integrity_errors']:
        raise RuntimeError('Post-run summary requires completed, integrity-checked replay')
    rows = [read(p) for p in sorted((P / 'texts').glob('*.json'))]
    attempts = [read(p) for p in sorted((P / 'candidates').glob('*.json'))]
    timing = read(R / 'k1_phase3_8_timing.json')
    ledger = read(ROOT / 'state/phase3_8_production_exposure_ledger.json')
    cfg = ROOT / 'config/languages/ko/k1'
    vocab = {e['id']: e for name in ('core_vocab.json', 'expansion_vocab.json') for e in read(cfg / name)}
    registry = read(cfg / 'explicit_restricted_senses.json')['entries']
    # These three formal findings were Core inflection / compound false rejects,
    # not genuinely authored future Expansion lemmas. Preserve original results.
    false_future = {'K1-009-attempt-01', 'K1-009-attempt-02', 'K1-014-attempt-01'}
    body_future = [a for a in attempts if any(e['code'] == 'future_expansion' for e in a['hard_errors'])]
    primary = Counter()
    for a in attempts:
        if a['hard_pass']:
            continue
        codes = [e['code'] for e in a['hard_errors']]
        key = next((k for k in ('title_permission', 'future_expansion', 'unresolved_context_ambiguity',
                              'unknown_or_unresolved', 'length', 'coverage_or_token_policy') if k in codes), codes[0])
        primary[key] += 1
    committed_issue = dict(text='K1-048', category='naturalness_issue',
        surface='저는 의자에 앉고 책을 열어요.',
        reason='紙の本を開く標準的な表現は펴다。追跡中の不足を열다で代用した表現が残った。restricted registry外の自然さ問題であり、語義ゲートのfalse acceptanceと混同しない。',
        suggested_revision='저는 의자에 앉고 책을 읽어요.', action='report_only; committed text unchanged')
    draft_issues = [dict(text='K1-039', categories=['verb_argument_frame', 'scene_plausibility'],
        evidence_file='pilot/ko/k1/phase3_8/drafts/K1-039-review.json',
        before='자전거를 닫아요 / 持参の果物をカフェ店内で食べる',
        resolution='自転車を降りる。持参食は公園で食べる。'),
        dict(text='K1-047', categories=['unnatural_substitution'],
        evidence_file='pilot/ko/k1/phase3_8/drafts/K1-047-review.json',
        before='친구도 자기 집에서 가방을 만들어요.',
        resolution='친구도 자기 옷을 가방에 넣어요.')]
    gaps = [dict(lemma='펴다', texts=[7, 48], status='tracked_existing_gap',
                 resolution='007は行為省略、048には代用が残りreport-only修正候補。'),
            dict(lemma='입히다', texts=[11], status='omitted', resolution='着せる行為を省略。입다へ代用しない。'),
            dict(lemma='지우다', texts=[27], status='omitted', resolution='消去動作を省略し、書き直す。닦다へ代用しない。')]
    r['automated_pre_quality_verdict'] = {'verdict': r['verdict'], 'status': r['status']}
    r.update(verdict='B', status='GENERATOR_TUNING',
        final_recommendation_reason='50本hard/integrity PASS。048の自然さ問題1件、初稿49/50にpreflight finding、formal first-pass72%・mean attempts1.34。pipelineを巨大化せずgeneratorの許可語彙遵守と既知bad-pattern運用を改善する。',
        confirmed_committed_issues=[committed_issue], confirmed_preformal_quality_issues=draft_issues,
        natural_expression_gaps=gaps,
        initial_preflight_drafts_with_findings=sum(bool(t['lexical_preflight']['findings']) for t in timing['texts']),
        formal_primary_retry_causes=dict(primary),
        formal_true_future_body_candidates=len([a for a in body_future if f"{a['id']}-attempt-{a['attempt_number']:02d}" not in false_future]),
        formal_core_morphology_false_future_candidates=sorted(false_future),
        quality_categories=dict(A='mechanical lexical/form error', B='explicit restricted-sense violation',
                                C='naturalness issue', D='translation issue', E='diagnostic-only warning'),
        naturalness_review_independent_gold=False,
        future_in_committed=0,
        words_with_at_least_six_exposures=sum(e['actual_exposure_count'] >= 6 for e in ledger['entries']),
        capped_six_exposure_progress=sum(min(6, e['actual_exposure_count']) for e in ledger['entries']),
        remaining_six_exposure_credits_needed=sum(max(0, 6-e['actual_exposure_count']) for e in ledger['entries']))
    write(R / 'k1_phase3_8_validation_result.json', r)
    write(R / 'k1_phase3_8_quality_audit.json', dict(committed_issues=[committed_issue],
         preformal_issues=draft_issues, formal_author_repairs=r['author_confirmed_draft_issues'],
         gaps=gaps, exhaustive_corpus_gold_review=False))
    # Preserve the six checkpoint samples even if the optional union exceeds 14.
    fixed = {1, 10, 20, 30, 40, 50}
    ranked = []
    for key in (lambda x: x['attempt_number'], lambda x: len(x['restricted_sense_checks']),
                lambda x: len(x['naturalness']['lint_warnings'])):
        ranked.extend(x['text_number'] for x in sorted(rows, key=key, reverse=True)[:4])
    chosen = set(fixed)
    for n in [48] + ranked:
        if len(chosen) < 14:
            chosen.add(n)
    r['human_spot_review_texts'] = sorted(chosen)
    write(R / 'k1_phase3_8_validation_result.json', r)
    def names(ids):
        return ' / '.join(vocab[i]['lemma'] for i in ids) or '—'
    human = ['# Phase 3.8 人間抜き取りレビュー', '',
             '固定6本を含む最大14本。作者自己評価は独立goldではない。048は既知の自然さ問題として本文を保存したまま提示する。', '']
    for x in rows:
        if x['text_number'] not in chosen:
            continue
        human += [f"## {x['id']} — {x['title_ko']}", '',
                  f"{x['eojeol_count']} 어절 / attempts {x['attempt_number']} / 新出: {names(x['actual_new_vocab_ids'])} / review: {names(x['actual_review_vocab_ids'])}",
                  f"自然さwarnings {len(x['naturalness']['lint_warnings'])} / semantic warnings {len(x['semantic_grammar_warnings'])}",
                  ('**report-only自然さ問題:** 책을 열어요 → 行為を省略して책을 읽어요を候補とする。' if x['text_number'] == 48 else ''),
                  '', x['text_ko'], '', x['translation_ja'], '']
    (R / 'k1_phase3_8_human_spot_review.md').write_text('\n'.join(human) + '\n', encoding='utf-8')
    old_report = R / 'k1_phase3_8_production_001_050_report.md'
    old_report.replace(R / 'k1_phase3_8_automated_run_metrics.md')
    p = r['per_text_seconds']
    doc = ['# K1 Phase 3.8 最終レポート', '', '**判定 B / GENERATOR_TUNING。50/50完走、hard条件とstate integrityはPASS。**', '',
       '初稿とformal candidateを区別する。formal first-passは72%だが、初稿49/50にはpreflight findingがあり、39/50でfuture findingが出た。機械ゲートを緩めず本文repairで吸収できた。300本へは進まず、generatorの許可リスト遵守と既知の不自然な代用を改善する。', '',
       '| 指標 | 結果 |', '|---|---|',
       f"| committed / attempts | 50/50 / {r['total_attempts']} |",
       f"| first-pass / mean attempts | {r['first_pass_ratio']:.0%} / {r['mean_attempts']:.2f} |",
       '| committed controlled / previous | 全100% / 全98%以上 |',
       '| committed future / unresolved / planned mismatch / final canonical mismatch / integrity | 全0 |',
       f"| restricted rejects / checkpoint false accepts検出 | {r['restricted_sense_rejects']} / {len(r['restricted_sense_false_accepts'])} |",
       f"| basic family counts | {r['basic_sense_family_usage_counts']} |",
       f"| scope warnings | {r['scope_disagreement_count']}（paragraph 2 / full 2、coverage不変更） |",
       f"| semantic / naturalness warnings | {r['semantic_warning_count']} / {r['naturalness_warning_count']} |",
       '| confirmed language issues | formal修正2教材、preformal確認2教材、commit後report-only1教材（048） |',
       f"| translation repair | formal {r['translation_issue_repairs']}件。048の訳は原文通りで、訳だけ補正しない |",
       f"| selected / incidental / introduced | {r['selected_review']} / {r['incidental']} / {r['introduced_count']} |",
       f"| outstanding / expired / near-deadline debt | {len(r['outstanding_debt'])} / {len(r['expired_debt'])} / {len(r['near_deadline_debt'])} window（word数とは異なる） |",
       f"| mathematically unrecoverable | {len(r['mathematically_unrecoverable'])}（各語の残り教材数判定。共同scene容量の保証ではない） |",
       f"| production wall | {r['production_wall_seconds']:.2f}秒（{r['production_wall_seconds']/3600:.2f}時間） |",
       f"| mean / median / p90 | {p['mean']:.2f} / {p['median']:.2f} / {p['p90']:.2f}秒 |",
       f"| min / max | {p['min']:.2f} / {p['max']:.2f}秒 |",
       f"| 300本 serial mean / median | {r['estimated_300_mean_hours']:.2f} / {r['estimated_300_median_hours']:.2f}時間 |",
       f"| performance / 最大stage | {r['performance']} / {r['largest_stage']} |", '',
       f"3.7の10本partial baseline（104.79/95.19/150.46秒）比: mean {p['mean']/104.79-1:+.1%}、median {p['median']/95.19-1:+.1%}。50本と10本の部分runなので参考比較。時刻はlive authorの思考・ファイル受け渡し・操作時間を含む実測で、純粋なAPIモデルlatencyではない。setup {r['engineering_setup_seconds']:.2f}秒、pre/post full tests・最終replay・レポートはproduction wall外。", '',
       '## 語義ポリシーと限定範囲', '',
       'basic_sense_families.jsonに人間承認済みの朝/朝食、夕方/夕食をoverlayとして保存。元DBのlemma/POS/sense/IDを保持し、旧meal除外notesのこの2件だけを明示的に上書きする。同一IDなのでnew lemmaや800予算を増やさない。', '',
       'explicit_restricted_senses.jsonは既存notesに明示された18件のみ。各source file・notes・canonical tripleを照合する。狭い禁止contextに明確に該当すればcandidate hard reject、それ以外はNO_CLEAR_VIOLATIONであり完全WSDの証明ではない。全800語の意味棚卸しは実施しない。', '',
       '本runの18語対象usage86件を再確認し、明示違反を検出しなかった。未導入のregistry語は使用していない。語義negative fixturesはcanonical IDに対する狭いcontextルールの対照試験であり、未知の全語義を解決した試験ではない。', '',
       '## 語彙・retry', '',
       f"formal retry一次原因（複数errorを一次原因にまとめる）: {dict(primary)}。機械reject15attempt、作者がmechanical PASS後にrepairした2attempt。元の機械error全件内訳はvalidation_result.jsonを参照。", '',
       f"formal body future findings4candidateのうち3件はCore 듣다/공책の誤解決を保守的にrejectしたもの。確認できる真のbody futureは043の이제 1candidate。title policyのfindingも別に保存する。preflight future finding89は初稿での検出件数で、全件を独立WSD goldとして真の混入と認定しない。commit済みfutureは0。", '',
       '## review / debt', '',
       f"実distinct-text exposure合計 {sum(e['actual_exposure_count'] for e in ledger['entries'])} = introduction99 + selected108 + incidental211。6本以上達成は{r['words_with_at_least_six_exposures']}語。分布: {r['exposure_distribution']}。0回401語は主にまだ導入予定が先の語である。", '',
       f"6回を超えた重複を進捗からcapすると {r['capped_six_exposure_progress']}/3000 credits。残り{r['remaining_six_exposure_credits_needed']} creditsを次の250教材で実現する必要がある（平均 {r['remaining_six_exposure_credits_needed']/250:.2f} distinct Expansion/text）。この50本だけで500語×6回の成立を認定しない。", '',
       '69 outstanding windowsのうち23は期限を過ぎた未消化window。繰越は仕様上許可される。衣類・眼鏡等に未消化があるが、違和感のある挿入やsilent creditはしなかった。次の連続runではdebtに合う自然なscene候補を早めに出すgenerator支援が必要。', '',
       '## 自然さ・translation・diversity', '',
       'formal author repairは001の名前のreferent/訳の補完、012の病人と医師の指示混同。preformal確認例は039の自転車を閉める代用と店内で持参食を食べる場面、047の旅行かばんを作る代用。修正済み。これはlexical policyやsemantic grammar warningと別に扱う。', '',
       '048の紙の本に책을 열어요が残った。これは펴다不足への不自然な代用の再発で、report-onlyの修正案は動作を省略して책을 읽어요とする。元commitは改変しない。입히다（011）・지우다（027）は行為を省略して解決。新語をDBへ追加していない。', '',
       f"genre distribution: {r['genre_distribution']}。直近10本との最大fingerprint similarity {r['max_scene_similarity']:.3f}。fingerprintの具体的な文字列比較は意味的な似た展開を過小検出し得る。学校/家庭/食事への偏りや終盤の会話型を人間spotで確認する。", '',
       f"N에게 웃어요 / habitual progressiveの機械recurrence検索: {r['recurring_patterns']}。検出0をあらゆる自然さ問題0の証明にしない。sentence preferred compliance {r['preferred_sentence_ratio']:.1%}、hard max違反0。", '',
       '## 検証とfreeze', '',
       f"full regression: pre {r['pre_regression']['tests']} PASS、post {r['post_regression']['tests']} PASS（各1回）。ledger zero-state replay errors {r['ledger_replay_errors']}。歴史成果物とproductionコードfreeze一致。過去本文・ledgerのcreditを流用していない。050を超える本文は生成していない。", '',
       'historical 3.7/005、3.6/002、3.6b/007、3.6c/001はreport-onlyで全hard PASS。夕食はbasic family、scope-only identity差は診断扱い。真のfuture negative fixturesは引き続きreject。比較対象の元ファイルは変更していない。', '',
       '## 次の判断', '',
       '**B: GENERATOR_TUNING。** validatorを一般的なsemantic parserへ拡張せず、初稿の許可リスト遵守と既知bad-pattern（펴다不足時の省略を含む）を作者側で強化する。抜き取りレビューで品質を確認し、debtの繰越を次のrunでも測る。今回の完走を300本の自動生成許可とは扱わない。', '',
       '詳細: k1_phase3_8_validation_result.json、k1_phase3_8_timing.json、k1_phase3_8_human_spot_review.md、k1_phase3_8_automated_run_metrics.md。']
    old_report.write_text('\n'.join(doc)+'\n', encoding='utf-8')
    table=['# Phase 3.8 Sense policy source audit', '', '| ID | lemma / allowed sense | frozen source | notes |', '|---|---|---|---|']
    for e in registry:
        table.append(f"| {e['vocab_id']} | {e['lemma']} / {e['allowed_sense']} | {e['source']['file']} | {e['source']['notes']} |")
    table += ['', '全18件で元canonical tripleとnotesが一致。新しいpolysemy推測による制限は加えない。朝食/夕食の2件は人間承認のbasic familyとして別overlay。',
              '', '本runで明確なrestriction違反0、NO_CLEAR_VIOLATIONは全意味の自動承認ではない。言語品質・訳・diagnosticは別に報告する。']
    (R/'k1_phase3_8_sense_policy_audit.md').write_text('\n'.join(table)+'\n', encoding='utf-8')
    print(json.dumps(dict(verdict=r['verdict'], spot_texts=sorted(chosen), committed=50,
         mean=p['mean'], median=p['median'], p90=p['p90']), ensure_ascii=False))


if __name__=='__main__':
    main()
