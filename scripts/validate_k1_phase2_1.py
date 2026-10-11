"""Validate Phase 2.1 overlay/design; final actual exposure validation is separate."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys
from jsonschema import Draft202012Validator
from build_k1_phase2_1 import DATA, REPORTS, ROOT, digest, dry_run, load, read
from k1_review_scheduler import SCENES, ReviewScheduler
from validate_k1_vocab import validate as validate_frozen_vocab


def validate():
    errors, warnings = [], []
    old = validate_frozen_vocab(DATA)
    errors.extend('FROZEN: ' + e for e in old['errors'])
    for manifest_name in ('k1_phase2_input_freeze.json', 'k1_phase2_pilot_artifact_manifest.json'):
        for name, checksum in read(REPORTS / manifest_name)['files'].items():
            if not (ROOT / name).is_file() or digest(ROOT / name) != checksum:
                errors.append('Frozen history changed: ' + name)
    core, expansion, intro, historical, records = load()
    windows = read(DATA / 'vocab_review_windows.json')
    schema = read(DATA / 'vocab_review_windows.schema.json')
    Draft202012Validator.check_schema(schema)
    errors.extend('SCHEMA: ' + e.message for e in Draft202012Validator(schema).iter_errors(windows))
    if errors:
        return {'ok': False, 'errors': errors, 'warnings': warnings, 'scope': 'design_only'}
    for path, checksum in windows['source'].items():
        if not (ROOT / path).is_file() or digest(ROOT / path) != checksum:
            errors.append('Overlay source mismatch: ' + path)
    entries = {e['vocab_id']: e for e in windows['entries']}
    active = {e['id'] for e in expansion}
    first = {vid: r['text'] for r in intro for vid in r['entry_ids']}
    if len(entries) != 500 or set(entries) != active:
        errors.append('Windows must cover all 500 active Expansion IDs exactly once')
    if set(windows['scene_catalog']) != set(SCENES):
        errors.append('Scene catalog mismatch')
    profile = read(DATA / 'profile.json')
    for key in ('controlled_vocab_coverage_hard_min', 'previous_vocab_coverage_hard_min', 'previous_vocab_coverage_target'):
        if windows['policy'][key] != profile[key]:
            errors.append('Coverage policy mismatch: ' + key)
    for vid, entry in entries.items():
        f = entry['first_introduction_text']
        if first.get(vid) != f:
            errors.append(vid + ': frozen introduction changed')
        if f >= 276:
            errors.append(vid + ': fast zone introduction')
        previous = f
        for w in entry['review_windows']:
            if not previous < w['from'] <= w['to'] <= 300:
                errors.append(vid + ': reversed, overlapping or pre-introduction window')
            previous = w['to']
        if previous != 300:
            errors.append(vid + ': terminal window must end at 300')
        if not set(entry['scene_affinity']) <= set(SCENES):
            errors.append(vid + ': unknown scene affinity')
        if entry['review_windows'][0]['to'] - f > 5:
            errors.append(vid + ': near opportunity missing')
        if not any(6 <= w['from'] - f <= 30 for w in entry['review_windows'][1:]):
            errors.append(vid + ': medium opportunity missing')
        if entry['review_windows'][-1]['from'] - f < min(60, int(.75 * (300 - f))):
            errors.append(vid + ': long opportunity missing')
    if errors:
        return {'ok': False, 'errors': errors, 'warnings': warnings, 'scope': 'design_only'}
    dry = dry_run(windows, core, expansion, intro, historical, records)
    saved = read(REPORTS / 'k1_phase2_1_dry_run.json')
    if saved != dry:
        errors.append('Saved dry-run differs from recomputation')
    numerical = dry['numeric_capacity']
    if not numerical['complete']:
        errors.append('Numeric window capacity insufficient')
    simulator = ReviewScheduler(windows)
    by_text = {r['text']: r['entry_ids'] for r in intro}
    exposures = defaultdict(list)
    for row in numerical['rows']:
        t = row['text']
        review_ids = [r['vocab_id'] for r in row['reviews']]
        if len(set(review_ids)) != len(review_ids):
            errors.append(f'{t}: duplicate word in numeric review slots')
        for job in row['reviews']:
            vid, stage = job['vocab_id'], job['window_index']
            w = entries[vid]['review_windows'][stage]
            if not w['from'] <= t <= w['to']:
                errors.append(vid + ': numeric review outside opportunity')
            exposures[vid].append(t)
        try:
            simulator.record(t, by_text[t] + review_ids)
        except ValueError as exc:
            errors.append(f'{t}: numeric ledger: {exc}')
    final_simulated = simulator.audit(300, final=True)
    if not final_simulated['ok']:
        errors.append('Simulated, not actual, final six-text quota failed')
    replay = dry['conflict_replay']
    source = {(r['text_number'], c['vocab_id']) for r in records for c in r['semantic_schedule_conflicts']}
    if len(replay) != 23 or {(r['source_text'], r['vocab_id']) for r in replay} != source:
        errors.append('Replay must cover all 23 frozen conflicts once')
    assigned = set()
    for r in replay:
        if r['actual_exposure_confirmed'] or not r['candidate_scene_provisional']:
            errors.append('Replay is being misrepresented as actual prose/exposure')
        if r['original_semantic_gate'] != 'rejected':
            errors.append('Original conflict bypasses semantic veto')
        t = r['candidate_text']
        if t is None:
            warnings.append(f'{r["vocab_id"]}: scene redesign still required')
            continue
        if not r['source_text'] < t <= 300:
            errors.append('Invalid replay date')
        key = (r['vocab_id'], t)
        if key in assigned:
            errors.append('Replay counted duplicate word/text')
        assigned.add(key)
        stage = r['candidate_window_index']
        w = entries[r['vocab_id']]['review_windows'][stage]
        if not w['from'] <= t <= w['to']:
            errors.append('Replay reservation outside declared destination window')
        if stage < r['original_window_index']:
            errors.append('Replay moved backwards')
        if r['unregistered_helper_risk']:
            if r['scheduler_selected']:
                errors.append('Unregistered helper gap bypasses positive gate')
            warnings.append(f'{r["vocab_id"]}: placement only; lexical helper {r["unregistered_helper_risk"]}')
    annotation = dry['annotation_triage']
    if annotation['total_occurrences'] != 269 or sum(annotation['occurrence_counts'].values()) != 269:
        errors.append('Annotation issue count changed')
    if annotation['occurrence_counts']['true_unresolved']:
        warnings.append('True unresolved annotation groups need individual review')
    warnings += ['Numeric capacity does not prove semantic feasibility or actual six-text exposure.',
                 'Scene cards and annotation templates require human review before production.',
                 'If all 2500 reviews rely on scheduling, average >8. Confirmed incidental previous appearances can reduce scheduled demand.']
    coverage_expected_misses = sum(r['coverage']['new_tokens_U'] == 2 and
                                  r['coverage']['denominator_N'] < 200 for r in records)
    test_runs = []
    test_result_path = REPORTS / 'k1_phase2_1_test_result.json'
    if test_result_path.exists():
        evidence = read(test_result_path)
        if all((ROOT / p).is_file() and digest(ROOT / p) == checksum
               for p, checksum in evidence['final_source_hashes'].items()):
            test_runs = evidence['runs']
        else:
            warnings.append('Stored test evidence predates a source change; rerun affected checks.')
    return {'ok': not errors, 'errors': errors, 'warnings': warnings,
        'scope': 'phase2_1_window_design_not_mass_generation_approval',
        'frozen_history_integrity': 'PASS' if not any('Frozen' in e or 'source mismatch' in e for e in errors) else 'FAIL',
        'counts': {'core': len(core), 'expansion': len(expansion), 'total': len(core) + len(expansion),
                   'tiers': dict(Counter(e['tier'] for e in expansion)), 'grammar': len(read(DATA / 'grammar.json'))},
        'numeric_capacity': {'complete': numerical['complete'], 'assigned_reviews': sum(map(len, exposures.values())),
            'capacity': numerical['capacity'], 'min_distinct_simulated_texts': min(1 + len(set(ts)) for ts in exposures.values()),
            'review_statistics': numerical['review_statistics'], 'fast_zone_review_statistics': numerical['fast_zone_review_statistics'],
            'actual_exposures_verified': False},
        'conflict_replay': {'count': len(replay), 'outcomes': dict(Counter(r['outcome'] for r in replay)),
            'statuses': dict(Counter(r['status'] for r in replay)),
            'scheduler_selected_provisional_scenes': sum(r['scheduler_selected'] for r in replay),
            'actual_prose_verified': False},
        'annotation_triage': {k: v for k, v in annotation.items() if k != 'groups'},
        'coverage_policy': {'controlled_hard': 1.0, 'previous_hard': .98, 'previous_target': .99,
            'two_new_tokens_N_under_200_expected_target_misses': coverage_expected_misses,
            'target_miss_is_blocker': False},
        'vocab_changes_applied': False, 'new_texts_generated': 0, 'recommended_next_step': 'A_then_B',
        'mass_generation_approved': False, 'test_runs': test_runs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--actual-ledger', type=Path,
        help='JSON list of {text, confirmed_ids}; genuine body-confirmed events only')
    parser.add_argument('--through-text', type=int, default=300)
    parser.add_argument('--final', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.through_text <= 300 or (args.final and args.through_text != 300):
        parser.error('--final requires --through-text 300; text range 1..300')
    if args.actual_ledger:
        design = validate()
        if not design['ok']:
            print(json.dumps(design, ensure_ascii=False, indent=2))
            return 1
        scheduler = ReviewScheduler(read(DATA / 'vocab_review_windows.json'))
        try:
            events = read(args.actual_ledger)
            if not isinstance(events, list):
                raise ValueError('Ledger must be an event array')
            for event in events:
                if set(event) != {'text', 'confirmed_ids'} or not isinstance(event['confirmed_ids'], list):
                    raise ValueError('Invalid event fields')
                if event['text'] > args.through_text:
                    raise ValueError('Ledger event after audit date')
                scheduler.record(event['text'], event['confirmed_ids'])
            output = scheduler.audit(args.through_text, args.final)
        except (ValueError, TypeError, KeyError) as exc:
            output = {'ok': False, 'errors': [str(exc)], 'warnings': []}
    else:
        if args.final:
            parser.error('--final requires --actual-ledger; dry-run is not actual evidence')
        output = validate()
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(('PASS' if output['ok'] else 'FAIL') + ' (Phase 2.1 design/ledger scope)')
        print('errors:', len(output['errors']), 'warnings:', len(output['warnings']))
        for message in output['errors']:
            print(message)
    return 0 if output['ok'] else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
