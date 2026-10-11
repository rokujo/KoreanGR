"""Apply the authorized five exchanges from the frozen pre-revision baseline."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import sys

from k1_review_scheduler import make_windows

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'config/languages/ko/k1'
REPORTS = ROOT / 'reports'
SNAPSHOT = REPORTS / 'phase2_1_snapshot'
BASE = SNAPSHOT / 'config/languages/ko/k1'

# Permanent IDs and display ranks are independent of introduction ordering.
EXCHANGES = [
    ('ko_k1_0363', 'ko_k1_0808', '닦다', 'verb', 'wipe_clean', '磨く・拭く', 'E1', 'verbs', '비누',
     ['daily_life', 'action', 'health', 'object', 'body'], ['home', 'health', 'object_problem', 'kitchen'],
     '清掃のために磨く・拭く動作のみ。歯磨き、机や物を拭く場面。抽象的な腕前を磨く義は許可しない。'),
    ('ko_k1_0603', 'ko_k1_0809', '붙이다', 'verb', 'attach_stick', '貼る', 'E2', 'verbs', '가위',
     ['daily_life', 'action', 'school', 'object', 'problem'], ['school', 'object_problem', 'home'],
     '紙・テープなどを対象へ貼り付ける物理的動作のみ。火をつける等の別義は許可しない。'),
    ('ko_k1_0365', 'ko_k1_0810', '공', 'noun', 'ball', 'ボール', 'E1', 'places_objects', '잠깐',
     ['daily_life', 'object', 'outdoor', 'action'], ['outdoor', 'friendship', 'school'],
     '遊び・運動に使うボールのみ。同音の抽象義や漢字語の構成要素は許可しない。'),
    ('ko_k1_0577', 'ko_k1_0811', '그림', 'noun', 'drawing_picture', '絵', 'E2', 'places_objects', '건물',
     ['daily_life', 'object', 'school', 'description'], ['school', 'home', 'travel'],
     '描かれた絵・図の中心義。写真はCore 사진で扱う。'),
    ('ko_k1_0571', 'ko_k1_0812', '들다', 'verb', 'hold_lift_by_hand', '手に持つ・持ち上げる', 'E2', 'verbs', '엘리베이터',
     ['daily_life', 'action', 'object', 'transport'], ['object_problem', 'home', 'transport'],
     '手に持つ・持ち上げる物理的動作だけを許可する。가방을 들어요 / 책을 들어요。'
     '費用がかかる・気に入る・年を取る・中へ入る系・その他の辞書上の別義は自動許可しない。'
     'lemmaが同じでも別senseは未許可。全用例で対象物と手による保持・持ち上げの文脈を確認する。'),
]


def read(path):
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def reject(value):
        raise ValueError('Non-JSON numeric constant: ' + value)
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=pairs, parse_constant=reject)


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def history_errors():
    errors = []
    manifest = read(SNAPSHOT / 'manifest.json')
    for name, checksum in manifest['files'].items():
        path = SNAPSHOT / name
        if not path.is_file() or digest(path) != checksum:
            errors.append('Historical snapshot changed: ' + name)
        # Old reports and pilot artifacts remain at their original locations too.
        if name.startswith('pilot/') or name.startswith('reports/'):
            current = ROOT / name
            if not current.is_file() or digest(current) != checksum:
                errors.append('Historical report/pilot changed: ' + name)
    return errors


def build():
    errors = history_errors()
    if errors:
        raise RuntimeError('\n'.join(errors))
    expansion = read(BASE / 'expansion_vocab.json')
    before = {e['id']: copy.deepcopy(e) for e in expansion}
    migration = read(BASE / 'id_migration.json')
    ledger = read(BASE / 'k2_candidates.json')
    proposals = read(BASE / 'expansion_replacement_proposals.json')
    introduction = read(BASE / 'introduction_schedule.json')
    old_first = {vid: r['text'] for r in introduction['rows'] for vid in r['entry_ids']}
    movements = []
    replacements = {}
    for old_id, new_id, lemma, pos, sense, gloss, tier, category, companion, tags, scenes, notes in EXCHANGES:
        old = before[old_id]
        assert old['tier'] == tier
        entry = {**old, 'id': new_id, 'lemma': lemma, 'pos': pos, 'sense': sense,
                 'gloss_ja': gloss, 'tier': tier, 'category': category, 'tags': tags,
                 'allow_inflection': pos == 'verb', 'introduced_from': 1 if tier == 'E1' else 61,
                 'introduced_to': 70 if tier == 'E1' else 170, 'target_exposures': 6,
                 'forms': [], 'notes': notes, 'confidence': 'high'}
        expansion[expansion.index(next(e for e in expansion if e['id'] == old_id))] = entry
        replacements[old_id] = new_id
        for row in introduction['rows']:
            row['entry_ids'] = [new_id if vid == old_id else vid for vid in row['entry_ids']]
        anchor = next(e for e in before.values() if e['lemma'] == companion and e['tier'] == tier)
        # A same-tier permutation anchored to a meaningful scene companion, not
        # copying the retired word's date or arbitrarily reassigning all 500 words.
        for row in introduction['rows']:
            row['entry_ids'] = [anchor['id'] if vid == new_id else new_id if vid == anchor['id'] else vid
                                for vid in row['entry_ids']]
        first = {vid: r['text'] for r in introduction['rows'] for vid in r['entry_ids']}
        movements.append({'new_id': new_id, 'new_lemma': lemma, 'tier': tier,
            'former_slot_text': old_first[old_id], 'new_first_text': first[new_id],
            'displaced_id': anchor['id'], 'displaced_lemma': companion,
            'displaced_from': old_first[anchor['id']], 'displaced_to': first[anchor['id']]})
        migration['mappings'].append({'phase': '2.1A', 'old_id': old_id, 'old_lemma': old['lemma'],
            'old_pos': old['pos'], 'old_sense': old['sense'], 'new_id': new_id, 'new_lemma': lemma,
            'new_pos': pos, 'new_sense': sense, 'rank': entry['rank'], 'tier': tier,
            'category': category, 'old_rank': old['rank'], 'old_tier': old['tier'],
            'old_category': old['category'], 'old_first_introduction_text': old_first[old_id],
            'new_first_introduction_text': first[new_id]})
        reason = {'닦다': '果物品種より歯磨き・清掃の基本動作を優先。',
                  '붙이다': '判の義より貼付・工作・修理の基本動作を優先。Core写真義は維持。',
                  '공': '果物品種より投げる・受ける・遊ぶ対象を優先。',
                  '그림': '上る移動語の重複を減らして描画・展示の対象名詞を補う。',
                  '들다': '既存の移動・授受語の組合せより物を保持・持ち上げる動作を補う。'}[lemma]
        ledger['entries'].append({'former_id': old_id, 'lemma': old['lemma'], 'pos': old['pos'],
            'sense': old['sense'], 'gloss_ja': old['gloss_ja'], 'status': 'K2_candidate_only',
            'reason': reason, 'replacement_id': new_id, 'former_rank': old['rank'],
            'former_tier': tier, 'former_category': old['category'], 'retired_in_phase': '2.1A'})
        proposals['entries'].append({'source_id': old_id, 'source_lemma': old['lemma'],
            'source_pos': old['pos'], 'source_sense': old['sense'], 'action': 'retire_and_replace',
            'removal_reason': reason, 'candidate': {k: entry[k] for k in (
                'lemma', 'pos', 'sense', 'gloss_ja', 'category', 'tier', 'notes')},
            'replacement_reason': 'Phase 2.1A人間レビューで正式採用。', 'status': 'accepted', 'adopted_id': new_id})
    expansion.sort(key=lambda e: e['rank'])
    migration['phase'] = '2.1A'
    migration['id_policy'].update(next_id_sequence=813, old_id_aliases_enabled=False,
        rank_policy='rankは1〜800の表示スロット。5新語は旧スロットを維持し、恒久ID0808〜0812を新規採番。初出順はrankと独立に再査定。')
    migration['retired_ids'] = sorted(m['old_id'] for m in migration['mappings'])
    migration['aliases'] = []
    ledger['notes'] = '退役12エントリのK2候補台帳のみ。K2の語彙・Tier・教材計画は設計しない。'
    proposals.update(phase='2.1A', notes='Phase 1.2の7交換とPhase 2.1Aの5交換の採用履歴。DBへ重ねて結合しない。')
    introduction['notes'] = 'Phase 2.1A：同tier内の5交換・5位置入替。最終初出255、256〜300は新出0。全500エントリの初出。'
    profile = read(BASE / 'profile.json')
    profile.update(version='0.2.1A', status='vocabulary_revised_flexible_windows_ready_for_phase2_2')
    profile['expansion_decision']['notes'] = 'Phase 1.2の7交換とPhase 2.1Aの5交換を正式採用。Tier件数維持。'
    profile['introduction'].update(last_text=255, consolidation_from=256)
    profile['feasibility'].update(introduction_slots=510, slack_slots=10,
        warning='255本×2枠=510枠。500語の初出後10枠の余裕。新出0/1教材も維持。',
        generation_gate='Phase 2.1Aは短い検証例のみ。PASS後に同じ20教材番号でPhase 2.2比較へ進める。大量生成は未承認。')
    profile['category_policy'] = {'hard_exact': False, 'baseline_targets': {
        'people_social': 40, 'places_objects': 90, 'food_nature': 50, 'verbs': 100,
        'adjectives': 65, 'adverbs_connectors': 50, 'time_counters_units': 35,
        'abstract_body_emotion': 40, 'school_work_transport_info': 30},
        'warning_absolute_difference': 15, 'warning_relative_difference': .25}
    profile['review_source'] = {'mode': 'flexible_windows', 'file': 'vocab_review_windows.json',
                              'historical_exact_reviews_binding': False}
    profile['lexical_sense_policy'] = {'identity_unit': ['lemma', 'pos', 'sense'],
        'lemma_only_approval': False, 'context_review_required_ids': ['ko_k1_0812'],
        'restricted_entries': {'ko_k1_0812': {'allowed_sense': 'hold_lift_by_hand',
            'allowed_gloss_ja': '手に持つ・持ち上げる', 'not_allowed_senses': [
                'cost', 'like', 'grow_old', 'enter', 'other_dictionary_senses']}}}
    for name, value in [('expansion_vocab.json', expansion), ('id_migration.json', migration),
                        ('k2_candidates.json', ledger), ('expansion_replacement_proposals.json', proposals),
                        ('introduction_schedule.json', introduction), ('profile.json', profile)]:
        write(DATA / name, value)
    write(DATA / 'vocab_exposure_schedule.json', {'language': 'ko', 'level': 'K1', 'phase': '2.1A',
        'status': 'historical_exact_reviews_not_active', 'historical_file':
        'reports/phase2_1_snapshot/config/languages/ko/k1/vocab_exposure_schedule.json',
        'introduction_source': 'introduction_schedule.json', 'active_review_source': 'vocab_review_windows.json',
        'historical_reviews_binding': False})
    schemas(profile)
    old_windows = {e['vocab_id']: e for e in read(BASE / 'vocab_review_windows.json')['entries']}
    first = {vid: r['text'] for r in introduction['rows'] for vid in r['entry_ids']}
    new_scenes = {row[1]: row[10] for row in EXCHANGES}
    window = copy.deepcopy(read(BASE / 'vocab_review_windows.json'))
    window.update(phase='2.1A', status='window_policy_active_not_observed')
    window['entries'] = []
    for e in expansion:
        scenes = new_scenes.get(e['id'], old_windows.get(e['id'], {}).get('scene_affinity'))
        window['entries'].append({'vocab_id': e['id'], 'first_introduction_text': first[e['id']],
            'review_windows': make_windows(first[e['id']]), 'scene_affinity': scenes,
            'semantic_domain': scenes[0], 'affinity_status': 'heuristic_requires_realization_review'})
    window['source'] = {path: digest(ROOT / path) for path in (
        'config/languages/ko/k1/introduction_schedule.json', 'config/languages/ko/k1/expansion_vocab.json',
        'config/languages/ko/k1/id_migration.json', 'config/languages/ko/k1/profile.json',
        'reports/phase2_1_snapshot/manifest.json')}
    write(DATA / 'vocab_review_windows.json', window)
    write(REPORTS / 'k1_phase2_1A_changes.json', {'phase': '2.1A', 'status': 'applied',
        'migration_mappings_added': migration['mappings'][7:], 'introduction_movements': movements,
        'changed_existing_vocab_entries': [], 'category_before': dict(Counter(e['category'] for e in before.values())),
        'category_after': dict(Counter(e['category'] for e in expansion)),
        'historical_snapshot': 'reports/phase2_1_snapshot', 'texts_generated': 0})
    gap_examples()


def schemas(profile):
    support = read(BASE / 'support.schema.json')
    properties = support['$defs']['profile']['properties']
    for name in ('expansion_decision', 'introduction', 'category_policy', 'review_source', 'lexical_sense_policy'):
        properties[name] = {'const': profile[name]}
        if name not in support['$defs']['profile']['required']:
            support['$defs']['profile']['required'].append(name)
    proposals = support['$defs']['replacement_proposals']['properties']
    proposals['phase'] = {'const': '2.1A'}
    proposals['entries'].update(minItems=12, maxItems=12)
    migration = support['$defs']['id_migration']
    migration['properties']['phase'] = {'const': '2.1A'}
    migration['required'] += ['retired_ids', 'aliases']
    migration['properties']['retired_ids'] = {'type': 'array', 'uniqueItems': True, 'minItems': 12,
        'maxItems': 12, 'items': {'type': 'string', 'pattern': '^ko_k1_[0-9]{4}$'}}
    migration['properties']['aliases'] = {'type': 'array', 'maxItems': 0}
    migration['properties']['id_policy']['properties']['old_id_aliases_enabled'] = {'const': False}
    migration['properties']['id_policy']['required'].append('old_id_aliases_enabled')
    mapping = migration['properties']['mappings']['items']['properties']
    for name in ('phase', 'old_category', 'old_tier'):
        mapping[name] = {'type': 'string', 'minLength': 1}
    for name in ('old_rank', 'old_first_introduction_text', 'new_first_introduction_text'):
        mapping[name] = {'type': 'integer', 'minimum': 1, 'maximum': 800 if name == 'old_rank' else 255}
    migration['properties']['mappings']['items']['allOf'] = [{'if': {'properties': {
        'old_id': {'enum': [e[0] for e in EXCHANGES]}}}, 'then': {'required': [
        'phase', 'old_rank', 'old_tier', 'old_category', 'old_first_introduction_text', 'new_first_introduction_text'],
        'properties': {'phase': {'const': '2.1A'}}}}]
    candidate = support['$defs']['k2_candidates']['properties']['entries']['items']['properties']
    candidate.update(former_rank={'type': 'integer', 'minimum': 301, 'maximum': 800},
        former_tier={'enum': ['E1', 'E2', 'E3']}, former_category={'type': 'string'},
        retired_in_phase={'const': '2.1A'})
    support['$defs']['k2_candidates']['properties']['entries']['items']['allOf'] = [{'if': {
        'properties': {'former_id': {'enum': [e[0] for e in EXCHANGES]}}}, 'then': {'required': [
            'former_rank', 'former_tier', 'former_category', 'retired_in_phase']}}]
    write(DATA / 'support.schema.json', support)
    window_schema = read(BASE / 'vocab_review_windows.schema.json')
    window_schema['properties']['phase'] = {'const': '2.1A'}
    window_schema['properties']['status'] = {'const': 'window_policy_active_not_observed'}
    window_schema['properties']['entries']['items']['properties']['first_introduction_text']['maximum'] = 255
    source_names = ['config/languages/ko/k1/introduction_schedule.json', 'config/languages/ko/k1/expansion_vocab.json',
        'config/languages/ko/k1/id_migration.json', 'config/languages/ko/k1/profile.json', 'reports/phase2_1_snapshot/manifest.json']
    window_schema['properties']['source'] = {'type': 'object', 'additionalProperties': False,
        'required': source_names, 'properties': {name: {'type': 'string', 'pattern': '^[a-f0-9]{64}$'} for name in source_names}}
    write(DATA / 'vocab_review_windows.schema.json', window_schema)
    exposure = read(DATA / 'vocab_exposure_schedule.json')
    write(DATA / 'vocab_exposure_schedule.schema.json', {'$schema': 'https://json-schema.org/draft/2020-12/schema',
        'title': 'Historical exact reviews reference; not an active schedule', 'const': exposure})
    vocab_schema = read(BASE / 'vocab.schema.json')
    for name in ('introduced_from', 'introduced_to'):
        vocab_schema['items']['properties'][name]['maximum'] = 255
        vocab_schema['items']['allOf'][0]['else']['properties'][name]['maximum'] = 255
    write(DATA / 'vocab.schema.json', vocab_schema)


def gap_examples():
    write(DATA / 'lexical_gap_checks.schema.json', {
        '$schema': 'https://json-schema.org/draft/2020-12/schema', 'type': 'object', 'additionalProperties': False,
        'required': ['phase', 'scope', 'annotation_is_independent_gold', 'groups'],
        'properties': {'phase': {'const': '2.1A'}, 'scope': {'const': 'isolated_examples_not_readers'},
            'annotation_is_independent_gold': {'const': False}, 'groups': {'type': 'array', 'minItems': 5, 'maxItems': 5,
                'items': {'type': 'object', 'additionalProperties': False, 'required': ['key', 'required', 'sentences'],
                    'properties': {'key': {'enum': ['tooth_cleaning', 'tape_attachment', 'ball_play', 'drawing_art', 'holding_lifting']},
                        'required': {'type': 'array', 'minItems': 2, 'maxItems': 3, 'uniqueItems': True,
                                     'items': {'type': 'string', 'minLength': 1}},
                        'sentences': {'type': 'array', 'minItems': 2, 'maxItems': 3,
                                      'items': {'type': 'string', 'minLength': 1, 'maxLength': 80}},
                        'declared_sense': {'const': 'hold_lift_by_hand'}, 'context_review_required': {'const': True},
                        'sense_overrides': {'type': 'object', 'additionalProperties': {'const': 'tooth'}}}}}}})
    write(DATA / 'lexical_gap_checks.json', {'phase': '2.1A', 'scope': 'isolated_examples_not_readers',
        'annotation_is_independent_gold': False, 'groups': [
            {'key': 'tooth_cleaning', 'required': ['이', '닦다'], 'sentences': [
                '아침에 이를 닦아요.', '저는 칫솔로 이를 닦아요.', '수건으로 책상을 닦아요.'],
             'sense_overrides': {'아침에 이를 닦아요.::이': 'tooth', '저는 칫솔로 이를 닦아요.::이': 'tooth'}},
            {'key': 'tape_attachment', 'required': ['테이프', '붙이다'], 'sentences': [
                '종이에 테이프를 붙여요.', '친구도 테이프를 붙여요.', '테이프로 종이를 책에 붙여요.']},
            {'key': 'ball_play', 'required': ['던지다', '공'], 'sentences': [
                '친구에게 공을 던져요.', '친구가 공을 받아요.']},
            {'key': 'drawing_art', 'required': ['미술관', '그리다', '그림'], 'sentences': [
                '미술관에서 그림을 봐요.', '집에서 그림을 그려요.', '그림은 책상 위에 있어요.']},
            {'key': 'holding_lifting', 'required': ['가방', '책', '들다'], 'sentences': [
                '가방을 들어요.', '저는 한 손으로 책을 들어요.'],
             'declared_sense': 'hold_lift_by_hand', 'context_review_required': True}
        ]})


def main():
    build()
    from validate_k1_phase2_1A import validate
    result = validate(DATA, check_examples=True)
    write(REPORTS / 'k1_phase2_1A_validation_result.json', result)
    from report_k1_phase2_1A import render
    render(result)
    print(json.dumps({'ok': result['ok'], 'errors': result['errors'], 'summary': {
        k: v for k, v in result['summary'].items() if k != 'lexical_gap_examples'},
        'example_groups': [{'key': e['key'], 'ok': e['ok']} for e in result['summary'].get('lexical_gap_examples', [])]}, ensure_ascii=False))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
