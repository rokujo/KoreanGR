"""Validate active Phase 2.1A IDs, meanings, introductions and flexible windows."""
import argparse
from collections import Counter
from pathlib import Path
import sys
import json
from jsonschema import Draft202012Validator

from build_k1_phase2_1A import BASE, DATA, EXCHANGES, ROOT, SNAPSHOT, digest, history_errors, read
from k1_review_scheduler import SCENES, ReviewScheduler, capacity_dry_run, make_windows
from lexical_coverage import evaluate_lexical_tokens
from k1_schedule import distribution


def resolve_vocab(lemma, pos, sense, files):
    """An exact sense lookup; never a lemma-only or retired-ID alias resolution."""
    matches = [e for e in files['core_vocab.json'] + files['expansion_vocab.json']
               if (e['lemma'], e['pos'], e['sense']) == (lemma, pos, sense)]
    if len(matches) != 1:
        raise ValueError('Unregistered or ambiguous lemma/POS/sense')
    return matches[0]['id']


def example_checks(files):
    # The installed Phase 2 Kiwi supplies morphology evidence. Its sense labels
    # remain hypotheses; physical 들다 is declared and context-reviewed here.
    from k1_pilot_analysis import analyze, make_kiwi
    kiwi = make_kiwi()
    first = {vid: r['text'] for r in files['introduction_schedule.json']['rows'] for vid in r['entry_ids']}
    vocab = {e['id']: e for e in files['core_vocab.json'] + files['expansion_vocab.json']}
    rows = []
    for group in files['lexical_gap_checks.json']['groups']:
        candidates = [e for e in vocab.values() if e['lemma'] in group['required']]
        # Tooth, not numeral/determiner 이; these examples specify that meaning.
        required_ids = [e['id'] for e in candidates if e['lemma'] != '이' or e['sense'] == 'tooth']
        text_number = max([first.get(vid, 0) for vid in required_ids] + [
            first[e['id']] for e in vocab.values() if e['lemma'] in ('칫솔', '수건', '손')]) + 1
        text = ' '.join(group['sentences'])
        analysis = analyze(text, files, text_number, [], group.get('sense_overrides'), kiwi=kiwi)
        used = {a['vocab_id'] for a in analysis['annotations'] if a['vocab_id']}
        tokens = []
        for a in analysis['annotations']:
            if a['role'] == 'grammar_function':
                tokens.append({'kind': 'grammar', 'id': a['grammar_id']})
            elif a['vocab_id']:
                tokens.append({'kind': 'vocab', 'id': a['vocab_id']})
            elif a['role'] == 'proper_name':
                tokens.append({'kind': 'proper_name', 'id': a['lemma']})
            elif a['role'] == 'frozen_exception':
                tokens.append({'kind': 'exception', 'id': a['exception_id']})
            else:
                tokens.append({'kind': 'unknown', 'id': a['lemma']})
        coverage = evaluate_lexical_tokens(tokens, text_number, files)
        unapproved_grammar = [i for i in analysis['annotation_review_required'] if i['type'] in (
            'unapproved_or_unresolved_grammar', 'unaccounted_morpheme')]
        row_errors = list(coverage['errors'])
        if not set(required_ids) <= used:
            row_errors.append('Required lexical pair missing')
        if analysis['unresolved_tokens'] or unapproved_grammar:
            row_errors.append('Unresolved morphology/grammar in short example')
        rows.append({'key': group['key'], 'scope': 'isolated_examples_not_readers',
            'sentences': group['sentences'], 'validation_text_number': text_number,
            'required_vocab_ids': sorted(required_ids), 'used_vocab_ids': sorted(used),
            'grammar_used': sorted(analysis['grammar_used']), 'coverage': coverage,
            'generated_annotations': analysis['annotations'], 'raw_morphology': analysis['raw_morphology'],
            'annotation_review_required': analysis['annotation_review_required'], 'errors': row_errors,
            'declared_sense_overrides': group.get('sense_overrides', {}),
            'ok': not row_errors, 'sense_truth_independently_verified': False})
    return rows


def validate(data_dir=DATA, check_examples=False):
    data_dir = Path(data_dir)
    errors, warnings, summary = [], [], {}
    def result():
        return {'ok': not errors, 'errors': errors, 'warnings': warnings, 'summary': summary,
                'scope': 'phase2_1A_vocabulary_revision_no_reader_generation'}
    names = ['core_vocab.json', 'core_vocab.source.json', 'expansion_vocab.json', 'grammar.json',
        'proper_names.json', 'lexical_exceptions.json', 'profile.json', 'id_migration.json',
        'k2_candidates.json', 'expansion_replacement_proposals.json', 'introduction_schedule.json',
        'vocab_review_windows.json', 'vocab_exposure_schedule.json', 'vocab.schema.json',
        'support.schema.json', 'grammar.schema.json', 'vocab_review_windows.schema.json',
        'vocab_exposure_schedule.schema.json', 'lexical_gap_checks.json', 'lexical_gap_checks.schema.json']
    files = {}
    for name in names:
        try:
            files[name] = read(data_dir / name)
        except (OSError, ValueError) as exc:
            errors.append(name + ': ' + str(exc))
    if errors:
        return result()
    for name, schema in [('core_vocab.json', 'vocab.schema.json'), ('expansion_vocab.json', 'vocab.schema.json'),
                          ('grammar.json', 'grammar.schema.json'), ('vocab_review_windows.json', 'vocab_review_windows.schema.json'),
                          ('vocab_exposure_schedule.json', 'vocab_exposure_schedule.schema.json'),
                          ('lexical_gap_checks.json', 'lexical_gap_checks.schema.json')]:
        try:
            Draft202012Validator.check_schema(files[schema])
            for issue in Draft202012Validator(files[schema]).iter_errors(files[name]):
                errors.append(f'{name}: {issue.message}')
        except Exception as exc:
            errors.append(f'{schema}: {exc}')
    support = files['support.schema.json']
    for name, definition in [('profile.json', 'profile'), ('id_migration.json', 'id_migration'),
        ('k2_candidates.json', 'k2_candidates'), ('expansion_replacement_proposals.json', 'replacement_proposals'),
        ('introduction_schedule.json', 'introduction_schedule'), ('proper_names.json', 'proper_names'),
        ('lexical_exceptions.json', 'exceptions')]:
        for issue in Draft202012Validator({**support, '$ref': '#/$defs/' + definition}).iter_errors(files[name]):
            errors.append(f'{name}: {issue.message}')
    if errors:
        return result()
    expected_pairs = {'tooth_cleaning': ['이', '닦다'], 'tape_attachment': ['테이프', '붙이다'],
        'ball_play': ['던지다', '공'], 'drawing_art': ['미술관', '그리다', '그림'], 'holding_lifting': ['가방', '책', '들다']}
    groups = files['lexical_gap_checks.json']['groups']
    if {g['key'] for g in groups} != set(expected_pairs) or any(g['required'] != expected_pairs[g['key']] for g in groups):
        errors.append('Lexical gap checks must cover all five required pairs')
    if any(len(s.split()) > 10 for g in groups for s in g['sentences']):
        errors.append('Short validation examples must stay within ten eojeol')
    core, expansion = files['core_vocab.json'], files['expansion_vocab.json']
    vocab = core + expansion
    active = {e['id']: e for e in vocab}
    expansion_ids = {e['id'] for e in expansion}
    profile = files['profile.json']
    categories = Counter(e['category'] for e in expansion)
    summary.update(core=len(core), expansion=len(expansion), total=len(vocab),
        tiers=dict(Counter(e['tier'] for e in expansion)), grammar=len(files['grammar.json']),
        categories=dict(categories), new_texts_generated=0)
    if (len(core), len(expansion), len(vocab)) != (300, 500, 800):
        errors.append('Core/Expansion/Total must be 300/500/800')
    if Counter(e['tier'] for e in expansion) != Counter(E1=200, E2=200, E3=100):
        errors.append('Tier counts must be 200/200/100')
    for label, values in [('ID', [e['id'] for e in vocab]), ('rank', [e['rank'] for e in vocab]),
                          ('lemma+POS+sense', [(e['lemma'], e['pos'], e['sense']) for e in vocab])]:
        if len(set(values)) != len(values):
            errors.append('Duplicate ' + label)
    if [e['rank'] for e in core] != list(range(1, 301)) or [e['rank'] for e in expansion] != list(range(301, 801)):
        errors.append('Display ranks must be ordered 1..800')
    baseline = read(BASE / 'expansion_vocab.json')
    baseline_by_id = {e['id']: e for e in baseline}
    new_ids = {x[1] for x in EXCHANGES}
    newly_retired = {x[0] for x in EXCHANGES}
    initial_migration = read(BASE / 'id_migration.json')
    initial_retired = {m['old_id'] for m in initial_migration['mappings']}
    retired = initial_retired | newly_retired
    if set(active) != {e['id'] for e in read(BASE / 'core_vocab.json') + baseline} - newly_retired | new_ids:
        errors.append('Active permanent ID set differs from authorized migration')
    if set(active) & retired:
        errors.append('Retired ID reused in active vocabulary')
    for e in expansion:
        if e['allow_inflection'] != (e['pos'] in ('verb', 'adjective')):
            errors.append(e['id'] + ': inflection/POS mismatch')
        low, high = profile['introduction']['ranges'][e['tier']]
        if not low <= e['introduced_from'] <= e['introduced_to'] <= high:
            errors.append(e['id'] + ': invalid introduction interval')
        if e['target_exposures'] != 6:
            errors.append(e['id'] + ': six distinct exposures required')
        if e['id'] in baseline_by_id and e['id'] not in newly_retired:
            previous = baseline_by_id[e['id']]
            if any(e[k] != previous[k] for k in ('lemma', 'pos', 'sense', 'rank', 'tier')):
                errors.append(e['id'] + ': unrelated identity/rank/tier changed')
    for old_id, new_id, lemma, pos, sense, gloss, tier, category, *_ in EXCHANGES:
        e = active.get(new_id)
        if not e or (e['lemma'], e['pos'], e['sense'], e['gloss_ja'], e['tier'], e['rank']) != (
            lemma, pos, sense, gloss, tier, baseline_by_id[old_id]['rank']):
            errors.append(lemma + ': adopted entry mismatch')
    if not any(e['lemma'] == '찍다' and e['sense'] == 'take_photo' and e['tier'] == 'core' for e in core):
        errors.append('Core 찍다/take_photo missing')
    if any(e['lemma'] == '찍다' and e['sense'] == 'stamp' for e in vocab):
        errors.append('Retired 찍다/stamp remains active')
    if any(e['lemma'] == '들다' and e['sense'] != 'hold_lift_by_hand' for e in vocab):
        errors.append('Unapproved 들다 sense active')
    if any(e['lemma'] in ('도장', '배터리', '요즘', '동안', '묻다', '걸어가다', '이야기하다') for e in vocab):
        errors.append('Unapproved deferred lexical candidate active')
    for name in ('core_vocab.json', 'core_vocab.source.json', 'grammar.json', 'grammar.schema.json',
                 'proper_names.json', 'lexical_exceptions.json'):
        if (data_dir / name).read_bytes() != (BASE / name).read_bytes():
            errors.append(name + ': protected baseline changed')
    before_profile = read(BASE / 'profile.json')
    for name in ('controlled_vocab_coverage_hard_min', 'previous_vocab_coverage_hard_min',
        'previous_vocab_coverage_target', 'coverage_policy', 'counting', 'new_vocab', 'grammar_policy',
        'length', 'sentence_length', 'repetition', 'style'):
        if profile[name] != before_profile[name]:
            errors.append(name + ': frozen language/coverage policy changed')
    if len(files['grammar.json']) != 32:
        errors.append('Grammar must remain 32')
    for name, actual, expected in [('last_text', profile['introduction']['last_text'], 255),
        ('consolidation_from', profile['introduction']['consolidation_from'], 256),
        ('introduction_slots', profile['feasibility']['introduction_slots'], 510),
        ('required_new_entries', profile['feasibility']['required_new_entries'], 500),
        ('slack_slots', profile['feasibility']['slack_slots'], 10)]:
        if actual != expected:
            errors.append(name + ': introduction capacity metadata mismatch')
    migration = files['id_migration.json']
    mappings = migration['mappings']
    if mappings[:7] != initial_migration['mappings'] or len(mappings) != 12:
        errors.append('Historical seven migrations must remain intact; total twelve')
    if migration['id_policy']['next_id_sequence'] != 813 or migration['aliases'] or migration['id_policy']['old_id_aliases_enabled']:
        errors.append('ID sequence/alias policy invalid')
    if not migration['id_policy']['immutable'] or migration['id_policy']['reuse_retired_ids'] or not migration['id_policy']['id_rank_independent']:
        errors.append('Immutable nonreuse ID policy invalid')
    if set(migration['retired_ids']) != retired or {m['old_id'] for m in mappings} != retired or len({m['new_id'] for m in mappings}) != 12:
        errors.append('Retired/new ID ledger mismatch')
    for m in mappings:
        e = active.get(m['new_id'])
        if not e or any(e[k] != m['new_' + k] for k in ('lemma', 'pos', 'sense')) or any(
            e[k] != m[k] for k in ('rank', 'tier', 'category')):
            errors.append('Migration identity mismatch: ' + m['old_id'])
        if m['old_id'] in newly_retired:
            previous = baseline_by_id[m['old_id']]
            expected = next(row for row in EXCHANGES if row[0] == m['old_id'])
            if m['new_id'] != expected[1] or m['rank'] != previous['rank']:
                errors.append('Authorized old/new ID correspondence or rank mismatch')
            if any(previous[k] != m['old_' + k] for k in ('lemma', 'pos', 'sense', 'rank', 'tier', 'category')):
                errors.append('Migration old identity mismatch')
    ledger = files['k2_candidates.json']
    if ledger['counted_in_K1_budget'] or len(ledger['entries']) != 12 or {e['former_id'] for e in ledger['entries']} != retired:
        errors.append('K2 candidate ledger must contain twelve retired entries only')
    if ledger['entries'][:7] != read(BASE / 'k2_candidates.json')['entries']:
        errors.append('Historical candidate ledger changed')
    for candidate in ledger['entries']:
        m = next((m for m in mappings if m['old_id'] == candidate['former_id']), None)
        if not m or any(candidate[k] != m['old_' + k] for k in ('lemma', 'pos', 'sense')) or candidate['replacement_id'] != m['new_id']:
            errors.append('Candidate ledger identity mismatch')
        if m and candidate['former_id'] in newly_retired and any(
            candidate['former_' + k] != m['old_' + k] for k in ('rank', 'tier', 'category')):
            errors.append('Candidate ledger former rank/tier/category mismatch')
    adoption = files['expansion_replacement_proposals.json']
    if {e['adopted_id'] for e in adoption['entries']} != {m['new_id'] for m in mappings}:
        errors.append('Adoption ledger mismatch')
    if adoption['entries'][:7] != read(BASE / 'expansion_replacement_proposals.json')['entries']:
        errors.append('Historical adoption records changed')
    for decision in adoption['entries']:
        m = next((m for m in mappings if m['old_id'] == decision['source_id']), None)
        e = active.get(decision['adopted_id'])
        if not m or not e or any(decision['source_' + k] != m['old_' + k] for k in ('lemma', 'pos', 'sense')) or decision['status'] != 'accepted' or any(
            decision['candidate'][k] != e[k] for k in ('lemma', 'pos', 'sense', 'gloss_ja', 'tier', 'category')):
            errors.append('Adoption decision identity mismatch')
    policy = profile['category_policy']
    if policy['hard_exact']:
        errors.append('Category distribution must be soft')
    for name in set(categories) | set(policy['baseline_targets']):
        target = policy['baseline_targets'].get(name, 0)
        delta = categories[name] - target
        if not target or abs(delta) > policy['warning_absolute_difference'] or abs(delta) / target > policy['warning_relative_difference']:
            warnings.append(f'CATEGORY: {name}: actual={categories[name]}, target={target}, delta={delta}')
    if errors:
        return result()
    rows = files['introduction_schedule.json']['rows']
    ids = [vid for r in rows for vid in r['entry_ids']]
    first = {vid: r['text'] for r in rows for vid in r['entry_ids']}
    if [r['text'] for r in rows] != list(range(1, 301)):
        errors.append('Introduction rows must be ordered 1..300')
    if len(ids) != 500 or len(set(ids)) != 500 or set(ids) != expansion_ids:
        errors.append('Introduction schedule must cover each active Expansion once')
    if any(len(r['entry_ids']) > 2 or (r['text'] >= 256 and r['entry_ids']) for r in rows):
        errors.append('New maximum two; new zero after 255')
    for e in expansion:
        if e['id'] not in first or not e['introduced_from'] <= first[e['id']] <= e['introduced_to']:
            errors.append(e['id'] + ': actual first introduction outside permitted interval')
    old_first = {vid: r['text'] for r in read(BASE / 'introduction_schedule.json')['rows'] for vid in r['entry_ids']}
    for m in mappings[7:]:
        if m['new_first_introduction_text'] != first.get(m['new_id']) or m['old_first_introduction_text'] != old_first[m['old_id']]:
            errors.append('Migration introduction mismatch')
        if first.get(m['new_id'], 301) >= old_first[m['old_id']]:
            errors.append('New basic word must be reassessed earlier than retired slot')
    window = files['vocab_review_windows.json']
    plans = {e['vocab_id']: e for e in window['entries']}
    if len(plans) != 500 or set(plans) != expansion_ids or set(plans) & retired:
        errors.append('Five windows required for all 500 active words; none for retired words')
    for vid, entry in plans.items():
        if entry['first_introduction_text'] != first.get(vid):
            errors.append(vid + ': window/introduction mismatch')
        if entry['review_windows'] != make_windows(entry['first_introduction_text']):
            errors.append(vid + ': five dispersed flexible windows mismatch')
        if not set(entry['scene_affinity']) <= set(SCENES):
            errors.append(vid + ': unknown scene affinity')
    for key in ('controlled_vocab_coverage_hard_min', 'previous_vocab_coverage_hard_min', 'previous_vocab_coverage_target'):
        if window['policy'][key] != profile[key]:
            errors.append('Review/coverage policy mismatch')
    for name, checksum in window['source'].items():
        source = data_dir / Path(name).name if name.startswith('config/languages/ko/k1/') else ROOT / name
        if not source.is_file() or digest(source) != checksum:
            errors.append('Review-window source checksum mismatch: ' + name)
    errors.extend(history_errors())
    if errors:
        return result()
    numerical = capacity_dry_run(window, 10)
    ledger_check = ReviewScheduler(window)
    for row in numerical['rows']:
        ledger_check.record(row['text'], rows[row['text'] - 1]['entry_ids'] + [e['vocab_id'] for e in row['reviews']])
    if not numerical['complete'] or not ledger_check.audit(300, final=True)['ok']:
        errors.append('Flexible-window numeric capacity proof failed')
    summary.update(introduction_capacity={'assigned': len(ids), 'slots': 510, 'slack': 10,
        'period_counts': dict(sorted((str(k), v) for k, v in Counter(len(r['entry_ids']) for r in rows[:255]).items())),
        'last_introduction': max(first.values()), 'new_entries_256_to_300': 0},
        replacements={'adopted_total': 12, 'adopted_this_phase': 5, 'pending': 0},
        id_migration={'retired': 12, 'new_this_phase': sorted(new_ids), 'next_sequence': 813, 'aliases': 0},
        review_windows={'active_entries': 500, 'window_count': 2500, 'retired_entries': 0,
            'numeric_review_capacity': 10, 'numeric_complete': numerical['complete'],
            'minimum_simulated_distinct_texts': 6, 'actual_exposure_verified': False,
            'review_load': distribution([len(r['reviews']) for r in numerical['rows']])},
        history_integrity='PASS', category_hard_exact=False,
        coverage_policy={'controlled_hard': 1.0, 'previous_hard': .98, 'previous_target': .99, 'target_miss_is_blocker': False},
        phase2_2_can_proceed=not errors, mass_generation_approved=False)
    if check_examples:
        try:
            checks = example_checks(files)
            summary['lexical_gap_examples'] = checks
            errors.extend('EXAMPLE: ' + e for row in checks for e in row['errors'])
            summary['phase2_2_can_proceed'] = not errors
        except Exception as exc:
            errors.append('Example verification failed: ' + str(exc))
            summary['phase2_2_can_proceed'] = False
    warnings += ['Flexible windows and numeric matching are plans, not actual exposure evidence.',
                 'Short-example morphology/sense annotations require human review; lemma alone never licenses a meaning.']
    return result()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=DATA)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--check-examples', action='store_true')
    args = parser.parse_args()
    output = validate(args.data_dir, args.check_examples)
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print('PASS' if output['ok'] else 'FAIL')
        print('errors:', len(output['errors']), 'warnings:', len(output['warnings']))
        print({k: output['summary'].get(k) for k in ('core', 'expansion', 'total', 'tiers', 'grammar')})
        for error in output['errors']:
            print('ERROR:', error)
    return 0 if output['ok'] else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
