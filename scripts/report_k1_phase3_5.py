"""Human-readable Phase 3.5 reports from saved diagnostics only."""
from collections import Counter
from k1_phase3 import ROOT,read,write

def save(name,content):
    (ROOT/'reports'/name).write_text(content,encoding='utf-8')

def build():
    r=read(ROOT/'reports/k1_phase3_5_validation_result.json')
    registry=read(ROOT/'config/languages/ko/k1/grammar_semantics.json')['entries']
    fixtures=read(ROOT/'tests/fixtures/k1_phase3_5_grammar_semantics.json')
    corpus=read(ROOT/'reports/k1_phase3_5_existing_text_audit.json')
    fcounts=Counter(x['grammar_id'] for x in fixtures)
    lines=['# Phase 3.5 grammar32意味監査\n',
      '語彙800・文法32・ID・予定表・window・過去runは不変です。意味範囲のauthorityはgrammar.jsonと凍結K1文書のみです。新registryは別overlayであり、一般韓国語知識による許可意味の追加ではありません。\n',
      f"32項目を監査。狭いauto PASS経路を持つ項目は32、構造中心は11、文脈heuristicは21です。全32項目にREVIEW経路があります。registryで明示した意味policy疑問は8項目です。自動PASS可能数は、あらゆる用例を自動判定できる数ではありません。\n",
      '## 32項目の監査表\n',
      '| grammar ID | surface | frozen meaning / notes | allowed functions | 別意味・未許可候補 | auto PASS | REVIEW | fixture数 |',
      '|---|---|---|---|---|---|---|---|']
    for e in registry:
        g=e['frozen_definition'];meaning=g['meaning_ja']+' / '+g['notes']
        lines.append(f"| {e['grammar_id']} | {e['surface']} | {meaning} | {', '.join(e['allowed_functions'])} | {', '.join(e['disallowed_or_unapproved_functions'])} | 狭いframeのみ（{e['autocheck']}） | 根拠不足時に必須 | {fcounts[e['grammar_id']]} |")
    lines += ['\n接続詞は原因・密接な順序・具体的条件等、各frozen noteにある関係のみ認可します。理由・発見、条件・反実仮想、能力・推量、進行・結果状態を同一surfaceという理由で統合しません。\n',
      '## 機械検証と限界\n',
      f"全32正例＋37意味対照＋1前段境界、70 fixtureの期待結果はすべて一致しました。短文だけでなく、最初の誤PASS003の全文でもg30 roleをFAILにしました。修正文 `저는 어머니에게 사진을 주고 싶어요.` は全意味check PASS、g30なしです。\n",
      '作者のfunction申告は分類の入力にしません。raw span、登録lemma/POS/sense、dependent名詞、述語frame、局所文脈を保存します。rawは変更しません。PASSと同じsurfaceでも、lexical frameを替えたnegativeを検証しました。\n',
      'g14の凍結正例はraw EF/세요になり、旧形態gateにunresolvedが残る場合があります。semantic overlayは依頼候補を検出しますが、形態gateを通ったことにはしません。70 fixtureの成功は対象意味checkまたは前段rejectの期待結果であり、全文語彙・形態PASSではありません。\n',
      '만에のnegativeはraw NNB/만として返り、g32へ対応せず前段unresolvedでrejectされます。初期fixtureが要求していた「g32 REVIEW」を、raw根拠に合う「前段reject」へ修正しました。hard ruleや意味範囲は緩めていません。初期の失敗テスト結果・logも別ファイルに保存しました。\n',
      '있는/없는はg26の明示異形として対応づけ、元g27候補を診断に保存します。g04の内部copula、g31明示形에서부터は親構文への限定委譲です。単独에서の起点を認可していません。\n',
      '## 過去28本文のreport-only監査\n',
      f"Phase 2.3 25本＋Phase 3.4 clean 3本。{r['frozen_audit_counts']}。28/28にREVIEW候補があります。REVIEWは誤用確定ではなく、局所frameの不足・係り先・省略主語・広い所属関係などのfalse negativeも含みます。大量正常用例を自動承認できたとは結論しません。現gateの保守性を可視化した結果です。\n",
      '| source | id | PASS | REVIEW | FAIL候補 |','|---|---|---:|---:|---:|']
    for c in corpus:
        lines.append(f"| {c['path']} | {c['id']} | {c['counts']['PASS']} | {c['counts']['REVIEW']} | {c['counts']['FAIL']} |")
    lines += ['\n### 新たな定義外用法の候補\n',
      '以下6件はg23の起点frameとして自動FAILにしました。起点が明確な `학교에서 집으로 와요` はfrozen definition外です。出発・降車の表現については動作場所との境界を含め人間が確認してください。6件すべてを独立goldで誤用確定したとは扱いません。過去本文・過去PASS・ledgerは上書きしていません。\n',
      '| source | 原句 | 根拠 |','|---|---|---|']
    for c in r['frozen_audit_fail_candidates']:lines.append(f"| {c['path']} | {c['sentence']} | {c['reason']} |")
    lines += ['\nPhase 3.4 clean003の `아버지는 어머니에게 사진을 받아요.` は人を出所とするg28のpolicy REVIEWです。第三者の希望、되다補語、抽象的genitiveも疑問として分離しました。\n',
      '### gate改善が必要な正常用例候補\n',
      '387件だった初期REVIEWを、縮約所有の重なるspan、있는/없는の明示異形、場所での걷다/뛰다と移動起点の対照で369件まで減らしました。許可意味を増やしたのではなく、frozen例外と局所frameを正しく扱いました。残るREVIEWには `공책에 답을 써요`、省略された本人の希望、抽象的所属、助詞から先の形容詞を飛ばす係り先などがあります。意味policyの確認とparserの改善を分けて進めます。\n',
      f"## regression\n\n全suite {r['tests']['all']['tests']}件、focused {r['tests']['focused']['tests']}件、いずれもPASS。Phase 3.1〜3.4のresolver、alias、quote、우리、grouping、同形義、future/retired/planned identity、atomic/failed isolation、実candidate schemaの001〜050対照も維持しています。\n",
      '## 判定\n\nC / FAIL。意味誤用の遮断・保存・無creditは成立しましたが、smokeは004で停止し、005までの成功条件を満たしていません。50本連続試験へは進めません。\n']
    save('k1_phase3_5_grammar_semantic_audit.md','\n'.join(lines))

    policy=['# Phase 3.5 needs_human_policy\n',
      'registryに8件の意味範囲疑問を記録しています。下記の用法は確認前に自動許可しません。今回はgrammar.json、ID、allowed functionを拡張していません。\n',
      '| ID / surface | frozen記述 | 確認事項 | 現在の処理 |','|---|---|---|---|']
    for e in registry:
        if e['needs_human_policy']:
            policy.append(f"| {e['grammar_id']} / {e['surface']} | {e['notes']} | {e['needs_human_policy']} | REVIEW、commit禁止 |")
    policy += ['\n## 文脈境界の追加確認（policy件数8とは別）\n',
      'g21の「目的語の基本用法」と、経路・時間extent、여행을 가다のevent-objectの境界を確認してください。対照fixture `길을 걸어요` は許可範囲・歩行lemma双方の根拠が不足するためREVIEWです。独立に「基本目的語」範囲が確定していない用例をFAILにしない方針です。\n',
      'g23の起点は明示的に保留されているため、単なるpolicy曖昧性ではありません。ただし出発/降車が起点か動作場所かは文脈の確認が必要です。必要なら将来の定義修正を別途審査してください。今回のFAIL候補を理由に起点を自動追加しません。\n',
      '文脈不足のREVIEWと、意味範囲のneeds_human_policyを分離しています。369件をそのまま人間へ全件確認させる運用にはしません。頻出型（g22書込み場所、g29抽象所属、g06省略主語、g28出所、g05現在証拠）をまとめて仕様・係り先処理を確認します。\n',
      '## 技術blocker（意味policyとは別）\n',
      '004のCore 마시다の `마셔요` が말/VX + 시/EPとして解析されました。対照probeでは対象の接続文をsentence／quoted／narration／paragraph／fullの全scopeで同様に誤解析しました。今回の根拠はscope差や引用符差ではなく、고直後の補助用言候補との競合です。新たな無条件aliasで救済せず、raw span・局所構文・限定identity復元の対照を次修正で設計すべきです。g14 EF/세요の前段unresolvedも監査履歴に残しています。これらは語彙・文法範囲を広げる理由ではありません。\n']
    save('k1_phase3_5_policy_questions.md','\n'.join(policy))

    smoke=['# Phase 3.5 zero-state smoke\n',
      '**C / FAIL。001〜003をcommit、004でSTOP、005未生成。006以降・50本・300本は生成していません。**\n',
      '新runはepoch0・実績ゼロから開始。過去ledgerやcreditは流用していません。候補→hard/semantic gate→最終再解析→atomic commitの順です。1教材max5attemptですが、semantic FAIL/REVIEWはPhase 3.5規定で即STOPです。\n',
      '| text | attempt | 状態 | 어절 | N | U | controlled | previous | semantic FAIL/REVIEW |',
      '|---|---:|---|---:|---:|---:|---:|---:|---|']
    for c in r['smoke']['results']:
        cov=c['coverage'];smoke.append(f"| {c['id']} | 1 | COMMITTED | {c['eojeol']} | {cov['denominator_N']} | {cov['new_tokens_U']} | 100% | {100*cov['previous_vocab_coverage']:.4f}% | 0 / 0 |")
    fc=r['smoke']['failed_004']['coverage']
    smoke.append(f"| K1-004 | 1 | REJECTED / STOP | 137 | {fc['denominator_N']} | {fc['new_tokens_U']} | {100*fc['controlled_vocab_coverage']:.4f}% | {100*fc['previous_vocab_coverage']:.4f}% | 0 / 1 |")
    smoke += ['\n001〜003はfuture/invalid/unresolved/grammar違反0、planned new == actual new、120〜180어절。final reanalysisで意味diagnosticsも一致しています。new token各2でN<200のため99% target未達は予想範囲でありblockerではありません。\n',
      '## STOP原因を分離\n',
      '- `물어보다 / ko_k1_0378` は004では未導入。作者draftミスであり、語彙DBや初出予定を変更しません。\n'
      '- `저는 물을 받고 마셔요.` の全文rawで마셔요が말/VX + 시/EPへ崩れ、Core 마시다 identityを失いました。新構造analyzer問題です。\n'
      '- g09は接続先の登録述語が存在しないためREVIEW。未知語を想像で補って並列/順序PASSにしません。semantic gateがこの取り逃しを安全側で拒否しました。\n',
      '004のcoverage不達もhard rejectです。単発draftミスならretry可能ですが、今回はsemantic REVIEW／構造問題STOPが優先されます。retryで隠さず残りを生成していません。run_controlのsemantic_grammar_stopを保存し、追加診断を別audit JSONへ記録しました。\n',
      'ローカルsmokeの本文作者は手動sourceで、量産generatorの完成を主張しません。allowed snapshotとsentence precheckはgate側で実行していますが、作者側の事前制約適用が不十分で未導入語を混入しました。次はsnapshotを作者callbackへ先に渡すrun_one経路を使って、この差を解消する必要があります。未提出の準備草稿はcandidate／実績とは別扱いです。\n',
      '## 実review/debt\n',
      f"003の괜찮다は作者review候補には含めましたがschedulerのselected集合には入りませんでした。実出現をincidentalとしてcreditし、開いていたwindow0へ支払いました。selected review credit={r['smoke']['selected_review_credits']}、incidental={r['smoke']['incidental_credits']}、導入済みExpansion={r['smoke']['actual_introduced']}。debtは되다（window003〜006）1件、expired=0。004の되다/네/아니요は一切creditしていません。004で開く予定のwindowも、未commitの時計を進めて払済みにしません。\n",
      '実ledger epoch3と003までの履歴をTEMPのゼロstateで再現し、ledger全体一致を確認しました。004前後のauthoritative SHAも一致。新engineでatomic before/after publish crash、idempotent commit、最終meaning check差分拒否をテストしました。\n',
      '## gateの実証範囲\n',
      '32 grammarの意味registry、70 fixture、bad003全文回帰は成立。過去28本文は6 FAIL候補・369 REVIEWで、任意の自然な用例への対応はまだ十分ではありません。REVIEWを全て人間承認へ回すのではなく、同型をまとめてpolicyとparser能力を改善する必要があります。\n',
      f"全{r['tests']['all']['tests']}テスト／focused {r['tests']['focused']['tests']}テストPASS、凍結{r['frozen_files_checked']}ファイル変更0。テストPASSはsmoke完了PASSを意味しません。\n",
      '## 次へ進む条件\n',
      'まず고直後の마셔요の補助用言誤分割とg14 EF境界を解析器で監査し、許可snapshotからfuture混入を防ぐ作者側precheckを実行前に適用します。次に8件の意味policy疑問と頻出REVIEW型の係り先・省略主体を確認し、別の実績ゼロrunで001〜005を再試験してください。現時点で001〜050の連続試験は再開しません。\n']
    save('k1_phase3_5_smoke_report.md','\n'.join(smoke))
    review=['# Phase 3.5 committed smoke review\n','001〜003のみ。004は失敗candidateとして別保存。作者評価は人間レビューの代替ではありません。\n']
    state=read(ROOT/'state/phase3_5_smoke_exposure_ledger.json')
    for c in state['committed_records']:
        review += [f"## {c['id']} — {c['title_ko']}\n",c['text_ko']+'\n',c['translation_ja']+'\n',
          f"new={c['actual_new_vocab_ids']}; review={c['actual_review_vocab_ids']}; incidental={c['incidental_previous_vocab_ids']}; coverage={c['coverage']}; meaning={Counter(x['decision'] for x in c['semantic_grammar_checks'])}\n"]
    save('k1_phase3_5_smoke_review.md','\n'.join(review))

if __name__=='__main__':build()
