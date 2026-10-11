"""Build new Phase 2.1 design artifacts only; never modify frozen inputs/texts."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from k1_review_scheduler import SCENES, ReviewScheduler, affinity, capacity_dry_run, make_windows
from k1_annotation_triage import triage
from k1_schedule import distribution

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'config/languages/ko/k1'
REPORTS = ROOT / 'reports'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load():
    expansion = read(DATA / 'expansion_vocab.json')
    core = read(DATA / 'core_vocab.json')
    intro = read(DATA / 'introduction_schedule.json')['rows']
    old = read(DATA / 'vocab_exposure_schedule.json')
    records = [read(p) for p in sorted((ROOT / 'pilot/ko/k1/texts').glob('K1-*.json'))]
    return core, expansion, intro, old, records


def window_data(expansion, intro):
    first = {vid: r['text'] for r in intro for vid in r['entry_ids']}
    return {'language': 'ko', 'level': 'K1', 'phase': '2.1',
        'status': 'window_policy_dry_run_not_observed',
        'source': {name: digest(ROOT / name) for name in (
            'config/languages/ko/k1/introduction_schedule.json',
            'config/languages/ko/k1/vocab_exposure_schedule.json',
            'reports/k1_phase2_input_freeze.json',
            'reports/k1_phase2_pilot_artifact_manifest.json')},
        'policy': {'historical_exact_reviews_binding': False, 'target_distinct_actual_texts': 6,
            'review_goal_min': 5, 'review_goal_max': 8, 'extra_reviews_allowed_if_coherent': True,
            'window_miss_is_immediate_failure': False, 'final_deadline': 300,
            'minimum_gap_preferred': 3, 'selection_counts_as_exposure': False,
            'controlled_vocab_coverage_hard_min': 1.0, 'previous_vocab_coverage_hard_min': .98,
            'previous_vocab_coverage_target': .99, 'new_lemma_max': 2,
            'new_token_soft_max': 3, 'coverage_target_miss_is_blocker': False},
        'scene_catalog': list(SCENES),
        'entries': [{'vocab_id': e['id'], 'first_introduction_text': first[e['id']],
            'review_windows': make_windows(first[e['id']]), 'scene_affinity': affinity(e),
            'semantic_domain': affinity(e)[0], 'affinity_status': 'heuristic_requires_realization_review'}
            for e in expansion]}


# These are scene goals, not generated Korean texts or fixed destination numbers.
# Helper lemmas are positive lexical checks; missing helpers cannot pass the gate.
REPLAY_SCENES = {
    '물고기': ('nature', '川で生きた魚を観察する', ['강', '보다'], []),
    '계산하다': ('shopping', '必要な品を買って代金を払う', ['돈', '사다'], []),
    '찍다': ('school', '学校の受付で紙に判を押す', ['종이', '이름'], ['도장']),
    '새롭다': ('school', '初めての授業を受けて新しい経験を話す', ['수업', '처음'], []),
    '급하다': ('transport', '出発まで時間がなく移動を急ぐ', ['시간', '출발하다'], []),
    '이불': ('home', '泊まる友達の寝具を準備する', ['친구', '준비하다'], []),
    '맵다': ('food', '辛い食事を注文して味を確かめる', ['음식', '주문하다'], []),
    '테이프': ('shopping', '学校で必要なテープを買い、友達にも渡す', ['학교', '사다', '주다'], []),
    '버리다': ('home', '掃除して不要な紙を捨てる', ['종이', '청소하다'], []),
    '쓰다': ('food', '茶を飲んで苦い味を確かめる', ['차', '마시다'], []),
    '수영장': ('outdoor', 'プールへ行って泳ぐ予定を相談する', ['수영하다', '가다'], []),
    '미술관': ('travel', '美術館へ行く道と入館を相談する', ['길', '가다'], []),
    '목': ('health', '喉が痛く病院へ行く', ['아프다', '병원'], []),
    '감': ('food', '家族のために柿を選んで食べる', ['가족', '먹다'], []),
    '나뭇잎': ('nature', '落ちた葉を観察し季節の変化を話す', ['가을', '보다'], []),
    '회의': ('work', '会議の開始時間と準備を確認する', ['시간', '준비하다'], []),
    '벽': ('home', '部屋の壁の色を見て写真を飾る場所を相談する', ['색', '사진', '보다'], []),
    '돌': ('nature', '散歩中の道の石を見て歩く場所を選ぶ', ['길', '걷다'], []),
    '풀': ('nature', '草が多い場所で座る場所を選ぶ', ['곳', '앉다'], []),
    '이': ('health', '歯が痛いという問題を中心に病院へ行く', ['아프다', '병원'], []),
    '던지다': ('outdoor', '海へ小さい石を投げ、届く場所を比べず観察する', ['돌', '바다', '작다'], []),
}


def replay(windows, core, expansion, intro, old, records):
    by_id = {e['id']: e for e in expansion}
    entries = {e['vocab_id']: e for e in windows['entries']}
    old_entries = {e['vocab_id']: e for e in old['entries']}
    new = {r['text']: r['entry_ids'] for r in intro}
    pilot = {r['text_number']: r for r in records}
    known = core + expansion
    actual = {vid: set() for vid in by_id}
    for r in records:
        for a in r['annotations']:
            if a.get('vocab_id') in actual:
                actual[a['vocab_id']].add(r['text_number'])
    # Reserve simulated destinations cumulatively. Original historical reservations
    # are merely a conservative load estimate and are not an eligibility rule.
    loads = Counter({r['text']: r['review_vocab_count'] for r in old['texts']})
    conflict_keys = {(r['text_number'], c['vocab_id']) for r in records
                     for c in r['semantic_schedule_conflicts']}
    reservations = {}
    reserved_texts = set()
    rows = []
    for record in records:
        for conflict in record['semantic_schedule_conflicts']:
            vid, source = conflict['vocab_id'], record['text_number']
            e = by_id[vid]; plan = entries[vid]
            stage = old_entries[vid]['review_texts'].index(source)
            scene, goal, helpers, missing_helpers = REPLAY_SCENES[e['lemma']]
            # Hypothetical historical events plus prior replay reservations.
            # Never turn a previous omitted conflict into a ghost exposure.
            def probe(text, positive, veto=()):
                scheduler = ReviewScheduler(windows)
                first = plan['first_introduction_text']
                scheduler.record(first, [vid])
                events = []
                for t in old_entries[vid]['review_texts'][:stage]:
                    if (t, vid) in conflict_keys:
                        t = reservations.get((t, vid))
                    if t is not None and t < text:
                        events.append(t)
                for t in sorted(set(events)):
                    scheduler.record(t, [vid])
                return scheduler.select(text, [scene], positive, veto, desired=1)
            original = probe(source, [vid], [vid])
            assert not original['selected_reviews']
            candidates = []
            for next_stage in range(stage, 5):
                w = plan['review_windows'][next_stage]
                for t in range(max(source + 1, w['from']), w['to'] + 1):
                    if t in actual[vid] or t in old_entries[vid]['review_texts'] or t in pilot or t in reserved_texts:
                        continue  # frozen prose isn't redesigned; duplicates give no new exposure
                    if any(not any(x['lemma'] == lemma and (
                        x['tier'] == 'core' or entries[x['id']]['first_introduction_text'] < t)
                        for x in known) for lemma in helpers):
                        continue
                    # New words anchor the scene first; every current introduction
                    # must have that coarse scene option. Realization still needs QA.
                    if any(scene not in entries[n]['scene_affinity'] for n in new[t]):
                        continue
                    result = probe(t, [] if missing_helpers else [vid])
                    if not missing_helpers and not result['selected_reviews']:
                        continue
                    candidates.append((next_stage, loads[t], len(new[t]), t, result))
                if candidates:
                    break
            if candidates:
                next_stage, load, new_count, destination, result = min(candidates, key=lambda c: c[:4])
                loads[destination] += 1
                reserved_texts.add(destination)  # do not merge unrelated proposed scene goals
                actual[vid].add(destination)  # simulated reservation only; local variable not persistent actual ledger
                if not missing_helpers:
                    reservations[(source, vid)] = destination
                outcome = 'same_window_other_text' if next_stage == stage else 'carry_to_next_window'
                status = 'conditional_scene_fit' if not missing_helpers else 'placement_only_lexical_gap'
            else:
                destination = None; next_stage = None; result = None
                outcome = 'carry_to_next_window'; status = 'needs_scene_redesign_before_300'
            rows.append({'source_text': source, 'vocab_id': vid, 'lemma': e['lemma'],
                'sense': e['sense'], 'reason': conflict['reason'], 'original_window_index': stage,
                'original_window': plan['review_windows'][stage], 'outcome': outcome,
                'candidate_text': destination, 'candidate_window_index': next_stage,
                'scene': scene, 'scene_goal_ja': goal, 'registered_helpers': helpers,
                'unregistered_helper_risk': missing_helpers,
                'original_semantic_gate': 'rejected', 'new_intro_ids': new.get(destination, []),
                'scheduler_selected': bool(result and result['selected_reviews']),
                'status': status, 'actual_exposure_confirmed': False,
                'candidate_scene_provisional': True})
    return rows


def dry_run(windows, core, expansion, intro, old, records):
    numerical = capacity_dry_run(windows)
    by_id = {e['id']: e for e in expansion}
    new_by_text = {r['text']: r['entry_ids'] for r in intro}
    for row in numerical['rows']:
        ids = [r['vocab_id'] for r in row['reviews']]
        row['review_count'] = len(ids)
        row['new_count'] = len(new_by_text[row['text']])
        row['total_expansion_count'] = len(ids) + row['new_count']
        row['tier_review_counts'] = dict(Counter(by_id[v]['tier'] for v in ids))
    numerical['review_statistics'] = distribution([r['review_count'] for r in numerical['rows']])
    numerical['total_statistics'] = distribution([r['total_expansion_count'] for r in numerical['rows']])
    numerical['fast_zone_review_statistics'] = distribution([r['review_count'] for r in numerical['rows'][275:]])
    numerical['above_eight_texts'] = sum(r['review_count'] > 8 for r in numerical['rows'])
    numerical['fast_zone_recent_E3_count'] = sum(
        by_id[r['vocab_id']]['tier'] == 'E3' and row['text'] - next(
            e['first_introduction_text'] for e in windows['entries'] if e['vocab_id'] == r['vocab_id']) <= 20
        for row in numerical['rows'][275:] for r in row['reviews'])
    vocab = {e['id']: e for e in core + expansion}
    return {'status': 'design_dry_run_no_new_prose', 'numeric_capacity': numerical,
            'conflict_replay': replay(windows, core, expansion, intro, old, records),
            'annotation_triage': triage(records, vocab, {e['id'] for e in read(DATA / 'grammar.json')})}


def reports(dry, validation, core, expansion, records):
    numeric, replay_rows, annotation = dry['numeric_capacity'], dry['conflict_replay'], dry['annotation_triage']
    def table(headers, rows):
        return '\n'.join(['|' + '|'.join(headers) + '|', '|' + '|'.join(['---'] * len(headers)) + '|'] +
                         ['|' + '|'.join(str(v).replace('|', '/') for v in row) + '|' for row in rows])
    stats = numeric['review_statistics']
    lines = ['# K1 Phase 2.1 review scheduler設計・dry-run', '',
        '本文は生成・再生成していない。Phase 1.2の800語・32文法・導入予定とPhase 2の20本文・レポート・検証結果はSHA-256照合で保存した。語彙交換も未適用。', '',
        '## 判定範囲', '',
        'windowデータ・期限債務処理・件数容量は成立。23件を全件replayし、場面適合と日付予約を分けて評価した。移動先は未生成教材の仮の場面カードであり、本文の自然さ・実出現・coverageの実測を保証しない。', '',
        'Phase 2の旧overall FAIL 12件は履歴として維持する。言語hard違反は0件、20本すべてcontrolled100%、previous98%以上、文法・長さ・一文上限を満たした。新方式では固定review欠落を言語hard failureとみなさない。', '',
        '## 方式と適用優先順位', '',
        '`vocab_review_windows.json`をPhase 2.1以降のreview用overlayとして使用する。初出は従来のintroduction_schedule.jsonを唯一の正式入力とし、vocab_exposure_schedule.jsonのreview_textsは歴史・比較用に限る。旧validatorと旧pilotのschedule_passは書き換えない。profileのcoverage・初出・文法・長さ仕様はそのまま使用し、固定review割当だけ新overlayを優先する。', '',
        '残り150本以上：+2〜5、+6〜24、+25〜65、+66〜119、+120〜300末尾。残り90〜149本：+2〜5、+6〜19、+20〜39、+40〜69、+70〜末尾。残り45〜89本：+2〜5、+6〜15、+16〜23、+24〜L−1、+L〜末尾（L=max(35,min(60,floor(残り×.75)))）。すべて初出より後、5窓、重なりなし、最終窓の終点300。初出255の場合も5つの異なる後続教材を確保する。', '',
        '1. 当該教材の新出IDを取得し、新出語の意味を中心に場面候補を作る。新出0ならreview候補の共通目的から場面を選ぶ。',
        '2. 初出が実出現として確認された語だけを候補プールに入れる。scene affinityで粗く絞り、場面内の使い方の肯定的確認とvetoを受ける。タグ一致だけで採用しない。',
        '3. 意味適合100×一致率、期限接近20/残り日数、期限超過債務、実出現不足4×不足本数、直近との距離で順位付け。同じscene領域（affinityの第一候補）の採用が増すと12ずつ減点、距離3未満は30減点。品詞やカテゴリが同じだけで類義語扱いにしない。係数・domainは設計初版で、自然さの証明ではない。',
        '4. 5〜8語をsoft目標とする。scene側が同じ目的で統合できると確認した場合だけextra capacityを渡す。API上0語も許容し、語数未達のための一文追加をしない。10語超または新出含む12語超は負荷警告を返す。',
        '5. 本文・sense・coverage検証後のconfirmed IDsだけrecordする。選択だけでは出現扱いにしない。実台帳は教材順に記録し、同教材内の複数tokenは1本。未来語・旧ID・未確認初出のreviewを拒否する。', '',
        '## 未消化と最終期限', '',
        'windowの期限切れは即FAILでなく債務として残し、同窓後半または後の窓で消化する。1出現は最古の未消化窓1つにしか充当しない。未開窓へ前払いしない。先行する任意の再出現も実際の異なる教材数には計上するが、分散窓の代用にはしない。3本の距離はsoftで期限を優先できる。', '',
        'auditは期限まで3本の語・期限切れ債務・残り教材数では6本に到達できない語を警告する。300終了時は初出の実確認と6本以上の実出現がhard条件。分散窓未達は別途警告して、近距離だけで6本を埋めた語も点検する。301への繰越は許可しない。終盤は締切在庫からsceneを設計し、適合できない語が残れば語彙・導入期・場面設計の修正候補を報告する。deadlineは意味vetoを解除しない。', '',
        '## 容量と負荷', '',
        '500語×5review=2,500回、平均8.333回/300本。全ての実再遭遇をscheduled reviewだけで満たし、全教材8語上限とする場合は2,400回で100回不足し、序盤はさらに候補が少ない。一方、scheduled以外の自然なprevious Expansionの実出現も6本の条件へ数えられるため、scheduled 5〜8という目標自体は矛盾しない。runtime recordにはscheduled以外も含め、既に6本を満たした語を追加要求しない。', '',
        f'意味を制約しないinterval EDFで、1教材10reviewの仮容量にて{sum(r["review_count"] for r in numeric["rows"])}回を配置。未配置{len(numeric["misses"])}回。これは数的可能性の証明のみであり、実行用の固定割当ではない。', '',
        table(['対象', 'min', 'max', 'mean', 'median', 'p90'], [
            [name, *[values[k] for k in ('min', 'max', 'mean', 'median', 'p90')]] for name, values in (
                ('全300本review', stats), ('新出含むExpansion', numeric['total_statistics']),
                ('276〜300 review', numeric['fast_zone_review_statistics']))]), '',
        f'8review超は{numeric["above_eight_texts"]}本。最終25本の最近20本以内導入E3は{numeric["fast_zone_recent_E3_count"]}件。このEDFは全2,500回を予約扱いにした容量証明で、5〜8語に均した自然な運用のサンプルではない。自然なextra previous語の確認で実際のscheduled必要数を減らし、余剰候補・債務の分散をPhase 2.2で実測する。', '',
        '## 23 conflict replay（元本文は保存）', '',
        '元の場面は全件semantic vetoでreject。以下の日付は固定要求ではなく、候補探索が得た仮予約である。既存20本文は移動先として再編集せず、同語の既存出現日や同日予約を避けた。仮予約は1教材1つの場面目的にし、互いに無関係な移動案を同じ教材へ統合しない。移動先の新出語にscene affinityが合う場合だけ候補にする。helpersはその時点の導入済み登録語へ照合する。', '',
        table(['元教材', '語 / sense', '元窓', '結果', '窓index移動（0始まり）', '仮候補', '場面目的', '判定'], [
            [f'K1-{r["source_text"]:03}', r['lemma'] + ' / ' + r['sense'],
             f'{r["original_window"]["from"]}〜{r["original_window"]["to"]}', r['outcome'],
             f'{r["original_window_index"]}→{r["candidate_window_index"]}',
             f'K1-{r["candidate_text"]:03}' if r['candidate_text'] else '要scene再設計',
             r['scene_goal_ja'], r['status']] for r in replay_rows]), '',
        'carryは次以降の窓への繰越を表す。複数窓を越えても最古の未消化債務を1回だけ充当する。元教材で使う0件、結果内訳：' + str(dict(Counter(r['outcome'] for r in replay_rows))) + '。場面仮適合：' +
            str(sum(r['scheduler_selected'] for r in replay_rows)) + '/23件。日付だけの候補は自然な本文成立とは数えない。', '',
        '찍다(stamp)は道具語도장の不足候補があり、仮予約してもpositive gateを通さない。語彙微修正または別の自然な実現が確認されるまで未解決として残す。테이프は貼る動作を要しない「買って渡す」、이は元本文に歯痛を追加せず別教材の歯痛を主目的とする、던지다は導入済み돌を投げる別の場面に逃がす。これらは一般的な貼付・歯磨き・球遊びの語彙不足を解消したことにはならない。', '',
        '## coverage policy（変更なし）', '',
        'controlled coverage hard100%、previous hard98%、target99%、新出lemma最大2、新出token soft合計3。N/Uの定義はprofile.countingに従う。(N-U)/N>=.98をhardとする。U=2かつN<200なら99%target未達は計算上予想され、mass-generation blockerにはしない。controlled違反や他のhard条件は引き続きblocker。', '',
        '## annotationの分類と集約', '',
        f'269件を{annotation["total_groups"]}の型×語義×形態パターンに集約。分類は承認ではなく優先順位付け。', '',
        table(['区分', '出現件数', 'テンプレート群数'], [[c, n, annotation['group_counts'].get(c, 0)]
              for c, n in annotation['occurrence_counts'].items()]), '',
        '저のNP/MM・登録NNG+XSV/XSA/XSN複合・数詞直後の登録counterは期待される構造型。ただし一度は型の確認を行う。눈・일・쓰다等の同POS多義、茶の써(VV解析)、흘리다の涙義はsense確認群。안/수/거や다른の文法境界は許可構文テンプレートを確認する。未知の型・span不一致・DB不一致はtrue_unresolvedとして個別確認。', '',
        '代表文脈1件＋全発生位置を新dry_run.jsonに保存し、型承認後の同条件例は一括処理する。自動生成annotationを独立した正解とはみなさない。語彙・文法・解析器・規則の版が変われば承認cacheを無効化する。269件を個別に無条件確認する運用へは戻さない。', '',
        '## validator・履歴・次の判断', '',
        f'Phase 2.1 validator: {"PASS" if validation["ok"] else "FAIL"}、errors {len(validation["errors"])}。既存800語validatorと全テストも維持する。詳細はk1_phase2_1_validation_result.json。旧pilot validatorの12 schedule FAILは旧履歴として正常に残る。', '',
        '再現コマンド：`python -B scripts/build_k1_phase2_1.py`（新成果物だけ再作成）、`python -B scripts/validate_k1_phase2_1.py --json`（設計検証）、`python -B -m unittest discover -s tests -v`（既存＋追加テスト）。', '',
        '実台帳の形式は`[{"text": 1, "confirmed_ids": ["ko_k1_0373", "ko_k1_0413"]}, ...]`。各教材の実出現したExpansion全IDを渡す。`python -B scripts/validate_k1_phase2_1.py --actual-ledger <path> --through-text 150 --json`で途中の債務を点検し、300終了後だけ`--through-text 300 --final`を指定する。本文検証済みという出所は呼び出し側が保証する。パイロット20本だけの台帳で全300本の達成を推定しない。', '',
        'A「800語の微修正」を先に人間レビューすることを推奨する。少なくとも닦다・붙이다・공・그림・들다は基本場面の表現幅に直接効く。採否後、IDを新規採番しbudget/tier/migration/初出の整合を別Phaseで確定してからB「Phase 2.2で20本再生成」へ進む。交換は本Phaseで適用していない。大量生成はまだ進めない。', '',
        '残る人間判断：交換5組の採否、찍다(stamp)維持の必要性、scene affinityの狭さと使い方、9〜10語超を許容する場面、window繰越で失われる近距離再遭遇、annotationテンプレートの初回承認。外部依存は追加していない。', '']
    lines += ['## 作成ファイルとテスト記録', '',
        '- config/languages/ko/k1/vocab_review_windows.json / vocab_review_windows.schema.json',
        '- scripts/k1_review_scheduler.py / k1_annotation_triage.py / build_k1_phase2_1.py / validate_k1_phase2_1.py',
        '- tests/test_k1_review_scheduler.py',
        '- reports/k1_phase2_1_scheduler_report.md / k1_phase2_1_lexical_gap_report.md',
        '- reports/k1_phase2_1_dry_run.json / k1_phase2_1_validation_result.json / k1_phase2_1_test_result.json', '',
        '変更した既存ファイル：なし。dry_run.jsonの300行は本文でなく容量確認用のID割当。これを生成用の固定scheduleへ戻さない。', '']
    for run in validation.get('test_runs', []):
        lines.append(f'- `{run["command"]}`：{run["status"]}、{run["tests"]} tests。{run["scope"]}')
    lines.append('')
    (REPORTS / 'k1_phase2_1_scheduler_report.md').write_text('\n'.join(lines), encoding='utf-8')
    lexical_report(core, expansion, table)


def lexical_report(core, expansion, table):
    by_lemma = {}
    for e in core + expansion:
        by_lemma.setdefault(e['lemma'], []).append(e)
    candidates = [
        ['닦다', 'verb', '磨く・拭く（清掃動作）', '極めて基本／高・非実測', '歯磨き、机や手を拭く', '276:이; 193清掃の自然な具体化', 'E1（Core昇格も候補）', 'high', 'report60/104、276 author omit'],
        ['붙이다', 'verb', '貼る', '基本／高・非実測', 'テープ・工作・箱の修理', '189/284:테이프（189は移動も必要）', 'E2最小交換案／E1優先候補', 'high', '284 author omit、report60/104'],
        ['공', 'noun', 'ボール', '基本／高・非実測', '公園の遊び、投げる・拾う', '284:던지다（別教材の球遊び）', 'E1', 'high', '284 author omit、report60/104'],
        ['그림', 'noun', '絵', '基本／高・非実測', '描画・展示・好きな作品', '193:미술관の移動後; 189/190展示、170工作', 'E2最小交換案／E1優先候補', 'high', 'report76/104、170/190写真偏重'],
        ['들다', 'verb', '手で持ち上げる', '極めて基本／高・非実測', '鞄を持ち上げる、本を水から離す', '直接23件の解決ではない; 252こぼした本、284荷造り', 'E2最小交換案／E1優先候補', 'high', 'report104、252/284目的を担う動作'],
        ['도장', 'noun', '判・スタンプの道具', '一般日常／中・非実測', '受付、学校の確認印', '170:찍다(stamp)を別場面で具体化', 'E3候補／追加よりstamp義送り優先', 'medium', '170印を押す理由欠落を再監査'],
        ['배터리', 'noun', '電池・バッテリー', '日常／高見込み・非実測', '携帯が使えず充電する', '23件の直接解決なし; 234/255/284充電の理由', 'E2候補・今回は保留', 'medium', '新충전하다/충전기の原因説明から推定'],
        ['요즘', 'noun', 'このごろ', '日常／高見込み・非実測', '現在の習慣と以前の習慣', '直接解決なし; 252趣味を語る幅', 'E2候補・保留', 'low', '本文の趣味・反復説明から追加推定、明示的欠落記録なし'],
        ['동안', 'noun', '〜の間（期間）', '基本／高見込み・非実測', '待ち時間・旅行の長さ', '直接解決なし; 246早着・待機', 'E2候補・文法境界を併せてレビュー', 'low', '246待ち時間から推定、正式不足報告ではない'],
        ['묻다', 'verb', '尋ねる', '基本／高見込み・非実測', '道や予定を尋ねる', '直接解決なし; Core/Expansion代替可能', '追加しない（물어보다で足りる）', 'low', '既存물어보다の許可義を確認'],
        ['걸어가다', 'verb', '歩いて行く', '日常／高見込み・非実測', '移動', '直接解決なし; 걷다と가다の簡単な文で足りる', '追加しない', 'low', '移動本文に自然な代替があり必須不足ではない'],
        ['이야기하다', 'verb', '話をする', '日常／高見込み・非実測', '相談・会話', '直接解決なし; 이야기를 하다で足りる', '追加しない', 'low', '登録名詞+하다の分離表現で対応、複合語自動許可はしない'],
    ]
    assert all(row[0] not in by_lemma for row in candidates), 'Gap candidates must really be absent'
    swaps = [
        ('닦다', '오렌지', 'E1', '果物はCoreの과일/사과と多数Expansionで表せる。品種1語より清掃・歯磨き動作が多場面で必要。'),
        ('붙이다', '찍다', 'E2', 'stamp義ko_k1_0603だけを送り、Coreの사진を撮る義は維持。判の場面よりテープ・工作・修理に広く再利用。'),
        ('공', '포도', 'E1', '果物品種の追加価値より、既存던지다/줍다/놀다の具体的な対象が必要。'),
        ('그림', '오르다', 'E2', '移動の올라가다/올라오다等が既存。登る単純動作の語義重複より、그리다・미술관の対象名詞を補う。'),
        ('들다', '가져다주다', 'E2', '既存가져오다/가져가다と주다を別の簡単な文で使える。持ち上げる動作は別義の가지다で置き換えない。'),
    ]
    proposal_rows = []
    for add, remove, tier, reason in swaps:
        old = next(e for e in by_lemma[remove] if e['tier'] == tier)
        assert remove != '찍다' or old['sense'] == 'stamp'
        proposal_rows.append([add + ' ↔ ' + remove, old['id'], old['sense'], tier, reason])
    source = 'https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=14753'
    lines = ['# K1 Phase 2.1 lexical gap監査（交換未適用）', '',
        '現在Core300 / Expansion500 / Total800、E1/E2/E3=200/200/100、カテゴリ配分は全て維持。12教材23 conflict、20本文のauthor notes、Phase 2レポートを根拠に監査した。新語追加・K2語彙DB作成・ID更新・本文再生成はしていない。', '',
        '## 不足候補と根拠', '',
        '頻度・基本度は本パイロットの場面再利用性と初級上の具体性からの編集判断であり、コーパス頻度順位やTOPIK指定級の実測ではない。5つの明示報告語、追加監査の道具語、推定候補をconfidenceと証拠欄で区別する。どの候補も現行800内にはないことを機械照合した。', '',
        table(['lemma', 'POS', 'gloss_ja（限定義）', '頻度・基本度の推定', '必要な場面', '対応conflict/本文', 'tier候補', 'confidence', '証拠'], candidates), '',
        '追加語は単に元の23件の穴を埋めるものではない。例えば189の食事語や寝具語は、語彙を追加しても行き先相談に自然になるわけではなく、window側で分散する必要がある。닦다/붙이다/공は最終期の自然な標準場面を作る制約に直結し、그림/들다は展示の写真偏重や対象操作の不自然な省略を減らす。', '',
        f'道具語도장は[国立国語院 韓国語基礎辞典の「도장」]({source})で意味と찍다との組合せを確認した。ただし「この名詞なしではどの場面でもstampを使えない」とは断定しない。本dry-runで提示した受付場面では必要とみなし、別実現が確認されるまで承認保留とした。', '',
        '배터리は充電語を活かす原因説明に有用だが、原20本文の明示不足として報告された語ではない。요즘/동안も推定段階に留め、現時点で5語と同じ優先度へ上げない。물어보다/가지다/가져오다は既に登録済みで不足語へ重複追加しない。', '',
        '## 追加候補 ↔ 削除候補（人間レビュー待ち）', '',
        table(['交換案', '削除候補の恒久ID', '削除するsense', '交換tier', '理由'], proposal_rows), '',
        'これは5組の独立した案で、採用指示ではない。元語はいずれも日常語であり、単語そのものが難しい・無価値という評価ではなく、800枠内の優先順位の比較である。とくにオレンジ・ぶどうは具体的で使いやすいが、果物領域の品種数が相対的に多い。벽/목/돌/나뭇잎は衝突しただけで低価値と扱わず、windowを変えて再利用する。正式採用7語も維持する。', '',
        'この最小案のまま採用すればCoreは変更せず、E1の2語とE2の3語を同tierで交換するため300/500/800と200/200/100を保てる。붙이다/그림/들다はE1優先も検討したいが、昇格するなら同数の既存E1をE2へ送る別のTier差分案を先に承認する。800枠維持のためだけにCoreを勝手に移動しない。', '',
        'カテゴリは食べ物・自然−2、場所・生活用品+2、動詞の増減0となる案（공/그림は生活物品、닦다/붙이다/들다は動詞）。現行カテゴリ目標を厳密維持する場合は別の対応表の再設計が必要。現データのカテゴリ総数は変更していない。', '',
        '採用後の恒久IDは現行next_sequence=808以降を使用し、retired IDを再利用しない。rankは別の提示順として更新し、旧ID→新IDの関連をmigrationに明示する。初出予定・review窓・既存本文のfreeze版との対応も新バージョンに保存する。本Phaseでは採番していない。', '',
        '## 文法不足と語彙不足を分離', '',
        '-게の副詞化、動詞過去連体、-으면서、-지 않다、名詞化は語彙交換では解決しない。32項目の範囲で文を分ける方針を維持する。동안の名詞用法も時点副詞と混同せず、格助詞・期間構文の境界を確認する。語彙allow_inflectionを生産的な派生語の許可に読み替えない。', '',
        '## 次の判断', '',
        '推奨はA「800語の微修正」の人間レビューを先に行い、その後B「Phase 2.2で20本再生成」。特に5つの明示不足語の最小交換案とstamp義の必要性を決める。windowの設計・容量検証は成立するが、全23件の自然な本文成立は未証明である。99%target未達は単独で停止理由にしない。大量生成へは進まない。', '']
    (REPORTS / 'k1_phase2_1_lexical_gap_report.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    core, expansion, intro, old, records = load()
    windows = window_data(expansion, intro)
    write(DATA / 'vocab_review_windows.json', windows)
    dry = dry_run(windows, core, expansion, intro, old, records)
    write(REPORTS / 'k1_phase2_1_dry_run.json', dry)
    from validate_k1_phase2_1 import validate
    validation = validate()
    write(REPORTS / 'k1_phase2_1_validation_result.json', validation)
    reports(dry, validation, core, expansion, records)
    print(json.dumps({'ok': validation['ok'], 'errors': validation['errors'],
        'replay': dict(Counter(r['status'] for r in dry['conflict_replay'])),
        'numeric_complete': dry['numeric_capacity']['complete'],
        'annotation': {k: v for k, v in dry['annotation_triage'].items() if k != 'groups'}}, ensure_ascii=False))
    return 0 if validation['ok'] else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
