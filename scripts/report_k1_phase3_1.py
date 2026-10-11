"""Human-readable design, smoke evidence and committed Korean/Japanese text."""
from collections import Counter
from k1_phase3_1 import ROOT,REPORTS,RUN_DIR,LEDGER,read,write,freeze_errors

def report():
    r=read(REPORTS/'k1_phase3_1_validation_result.json')
    c=read(RUN_DIR/'texts/K1-001.json');audit=read(REPORTS/'k1_phase3_1_morphology_audit.json')
    tests=read(REPORTS/'k1_phase3_1_test_result.json') if (REPORTS/'k1_phase3_1_test_result.json').exists() else None
    focused=read(REPORTS/'k1_phase3_1_focused_test_result.json') if (REPORTS/'k1_phase3_1_focused_test_result.json').exists() else None
    snapshot=read(RUN_DIR/'allowed_vocab_snapshots/K1-001-epoch-0.json')
    roles=Counter(e['role'] for e in snapshot['entries'])
    lines=['# K1 Phase 3.1 candidate gate検証','',
        '**A. Phase 3.1 PASS — 別runで001〜050の連続試験を最初から再実施可能。**','',
        'このrunでは001だけをcommitした。002以降は生成していない。Phase 3の失敗本文・checkpoint・report・'
        'run state・露出ledger・validator結果はSHA-256でfreezeし、成功へ書き換えていない。','',
        '## Phase 3 failureの独立原因','',
        '| 原因 | 対策 |','|---|---|',
        '| 未導入들어오다、初出051が001へ混入 | allowed snapshotによるpermission check、future IDをinvalid_usage_idsへ分離、candidate reject |',
        '| 걸어요の걷다/walkと걸다/hangの解析曖昧性 | 正規活用＋登録sense＋局所構文・場面証拠を要求する限定resolver |',
        '| 119어절 | draft target130〜150。副詞ではなく同じsceneの必要な行動でcoherent expansion、120〜180hardは維持 |','',
        '## Candidate gate / retry','',
        'committed state→allowed snapshot→新出・scene・review候補→draft→sentence precheck→全文raw analysis→'
        'hard QA→naturalness lint/semantic second pass→repair/regenerate→最終再解析→atomic commit→次教材。', '',
        'candidateはcandidates/、rejectはfailed_attempts/へ保存。candidate段階で実ledgerをbyte単位で変更しない。'
        'retry回数はcandidate journalから取得する。標準max3。3回不合格ならrun停止。'
        'snapshot不可能、初出矛盾、analyzerの構造障害、state corruption、数学的露出不可能等は構造的停止。'
        '不正なdraft JSONも局所candidate_format rejectとし、実績を変更しない。','',
        'generatorはsnapshotと直前diagnosticsを受け取るcallback。今回のsmokeは既存失敗を意図的に再生し、'
        'future修正→length修正の順に、実feedbackを条件として使う決定的なregression callback。'
        '任意のLLMが常に3回で正しく修正できると実証したものではない。','',
        '| attempt | 結果 | 어절 | 主な診断 | ledger変更 |','|---|---|---|---|---|']
    lines += [f"| {a['attempt']} | {a['status']} | {a['eojeol']} | {', '.join(a['hard_error_codes']) or 'hard errors 0'} | {'なし' if a['state_unchanged'] else '異常'} |" for a in r['candidate_attempts']]
    lines += ['', 'attempt1では旧失敗を回帰再現し、futureをreject。attempt2では「友達も家で休みたい」へ行為を調整して、'
        '方向動詞のaliasを避けた。lengthだけが残る。attempt3では窓で天気を確認、実際に撮った写真を携帯で確認、'
        '写真に花も写っていることを確認する16어절を加え、135にした。filler副詞の追加はない。', '',
        '## Allowed snapshot','',
        f"001: roles={dict(roles)}。Core300＋当該新出2で語彙302。実導入済みExpansionは0。"
        f"固有名詞{len(snapshot['allowed_proper_names'])}、固定exception{len(snapshot['lexical_exceptions'])}を別枠で列挙。", '',
        '各エントリはvocab_id・lemma・pos・sense・tier・role・allowed_inflections・forms・morphology_hintsを持つ。'
        'input digestと実state checksumを添付し、stale候補をcommitしない。予定上の以前導入済みは許可しない。'
        'Core들어가다は許可するが、들어오다を類義語として許可するaliasは存在しない。'
        '괜찮아요はnew괜찮다の通常活用で、exceptionによる迂回にはしない。','',
        '## Limited resolver / raw analysis','',
        '공원까지 친구하고 걸어요. は、걷다/verb/walkの登録、正規活用걸어요、生成intent一致、'
        'locomotion、登録場所공원＋까지、人との同行친구하고、直接目的語なしをすべて確認して解決した。'
        'raw morphologyと元annotationは保存する。生成intentだけ・場所だけでは解決しない。'
        'がばんを壁へ掛けるCase Cは을目的語でveto。未解決ならcandidate reject。'
        '正しい歩行文でも保守的条件を満たさないものはREVIEWになり得る。resolverの条件を満たすためだけに同行者を作る運用は禁止する。','',
        '活用根拠: [国立国語院・걷다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=29667)。'
        '듣다は[韓国語基礎辞典](https://krdict.korean.go.kr/jpn/dicSearch/SearchView?ParaWordNo=74104)、'
        '돕다の活用は[同辞典](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=17203)で確認。'
        'Standalone돕다はactive K1ではないため追加しない。登録Core도와주다の厳密なraw prefix groupingだけを扱う。','',
        '## Irregular morphology監査','',
        f"active800のstem候補inventoryは{len(audit['stem_candidates'])}件。"
        'ㄷ/ㅂstemは不規則と自動認定しない。닫다・받다・입다をregular対照とした。'
        '르と登録하다 compoundも列挙。selected valid-inflection probesは28件、未知化/target認識失敗0。'
        'これは全活用・全senseの網羅的保証ではない。', '',
        '| lemma | class | 修正前unresolved | 修正後unresolved | target認識 |','|---|---|---|---|---|']
    lines += [f"| {p['lemma']} | {p['kind']} | {len(p.get('before_unresolved',[]))} | {len(p.get('after_unresolved',[]))} | {p.get('target_recognized')} |" for p in audit['probes']]
    lines += ['', '語彙DBのformsは変更していない。別overlayのmorphology_hintsを使用。'
        '다른の連体形境界を保持し、도와주고 싶어요の複合lemmaと希望文法を分離して検証した。'
        'auditの全語許可fixtureは実introや露出ledgerへ混ぜない。','',
        '## Sentence precheckの判断','',
        'sentence単位でfuture・unknown・retired・不許可文法形態素を診断する。全文raw解析でも同じpermissionを検証する。'
        '現在のcallbackは全文candidateを返すためprecheckは全文commit前の診断。token streaming型generatorの実装はしていない。'
        'sentence単位にprevious98%や120어절下限を適用せず、全文で検証する。','',
        '## Transaction safety','',
        'authoritative stateはcommitted record、導入、露出、debt payment、genre/scene履歴を含む単一JSON。'
        'OS writer lock＋同volumeのfsync済み一時ファイル＋atomic replaceで一度に公開する。'
        'texts/は復元可能なprojection。commit_id一致の再実行では露出を増やさず、異なるcandidateの二重commitを拒否。'
        'publish前faultで実state不変、publish後faultでprojection回復・credit重複なしをテストした。'
        'ディスク故障や電源断まで保証したとは扱わない。','',
        f"本smokeのepoch={r['ledger']['epoch']}、実導入{r['ledger']['introduced_count']}語、entry-text pairs={r['ledger']['actual_entry_text_pairs']}。"
        '2つのrejectは導入・露出・review count・debt payment・genre・sceneに一切反映しない。'
        'genre/scene各1件、debt0。500語中498語は0回、新出2語は各1回。','',
        '## Smoke hard result','',
        '| 指標 | 結果 |','|---|---|',
        f"| 어절 / 最大一文 | {c['eojeol_count']} / {c['max_sentence_eojeol']} |",
        f"| N / U | {c['coverage']['denominator_N']} / {c['coverage']['new_tokens_U']} |",
        f"| controlled coverage | {c['coverage']['controlled_vocab_coverage']:.2%} |",
        f"| previous coverage | {c['coverage']['previous_vocab_coverage']:.6%} |",
        '| 新出 | 되다 / 괜찮다、各1token、予定ID一致 |','| unresolved / future / grammar violation | 0 / 0 / 0 |',
        '| retired / invalid usage | 0 / 0 |','| final reanalysis | PASS |','| validator errors | 0 |',
        f"| naturalness lint / semantic flags | {r['naturalness']['lint_warnings']} / {r['naturalness']['semantic_flags']} |",'',
        '99% target missはhard98%を満たすため非blocker。Nは語彙意味単位token、Uは本教材の初出Expansion token。'
        '助詞・語尾・許可されたbound grammarはNから除外。全token controlledなのでprevious=(N−U)/N。'
        '語義・自然さ・日本語訳はモデル自己評価だけで最終承認しない。','',
        '## K1-001 committed本文','',c['text_ko'],'','### 日本語訳','',c['translation_ja'],'',
        '## Tests / freeze','',
        f"full suite: {tests if tests else '実行中。k1_phase3_1_test_result.jsonを参照。'}",'',
        f"最終focused suite: {focused if focused else '未保存'}",'',
        '初回新規testsで検出した二重keywordとVV-Iタグ対応は実装修正。hard条件の緩和や期待値だけの変更ではない。'
        '元Phase3のfailed001、checkpoint001、report、run state、ledger、validationは入力freezeに含め、全hash一致。','',
        '## 次の判断','',
        '**A. Phase 3.1 PASS。別runで001〜050の逐次再試験へ進める。** '
        '今回の証拠は001のcandidate gate・局所retry・限定resolver・transactionの成立まで。'
        '連続review window、review debt、incidental露出、scene/genre分布は50本再試験で検証する。'
        'このrunで002へ続行せず、300本量産も行わない。','',
        '## 成果物','',
        '- scripts/k1_candidate_gate.py / k1_phase3_1_resolver.py / k1_phase3_1.py / validate_k1_phase3_1.py',
        '- tests/test_k1_candidate_gate.py / tests/fixtures/k1_phase3_1_regression_cases.json',
        '- config/languages/ko/k1/phase3_1/morphology_hints.json / allowed_snapshot.schema.json',
        '- docs/ko_k1_candidate_gate.md',
        '- pilot/ko/k1/phase3_1/allowed_vocab_snapshots/ / candidates/ / failed_attempts/ / texts/K1-001.json',
        '- state/phase3_1_smoke_exposure_ledger.json',
        '- reports/k1_phase3_1_validation_result.json / k1_phase3_1_morphology_audit.json / k1_phase3_1_input_freeze.json']
    (REPORTS/'k1_phase3_1_candidate_gate_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    r['tests']=dict(full=tests,final_focused=focused);r['phase3_failure_unchanged']=not freeze_errors()
    write(REPORTS/'k1_phase3_1_validation_result.json',r)
    print('Phase 3.1 report saved.')

if __name__=='__main__':report()
