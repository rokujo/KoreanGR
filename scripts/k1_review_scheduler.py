"""Phase 2.1: window/debt scheduler. A selection is never an observed exposure."""
from collections import Counter
import heapq
import math

SCENES = ('food', 'kitchen', 'school', 'shopping', 'transport', 'travel', 'home',
          'health', 'body', 'outdoor', 'nature', 'work', 'communication',
          'friendship', 'family', 'object_problem', 'lost_and_found')


def make_windows(first):
    """Five nonoverlapping opportunities; final deadline is always text 300."""
    remaining = 300 - first
    if not 1 <= first <= 255:
        raise ValueError('Frozen introductions must leave at least 45 texts')
    if remaining >= 150:
        offsets = [(2, 5), (6, 24), (25, 65), (66, 119), (120, remaining)]
    elif remaining >= 90:
        offsets = [(2, 5), (6, 19), (20, 39), (40, 69), (70, remaining)]
    else:
        long_min = max(35, min(60, math.floor(.75 * remaining)))
        offsets = [(2, 5), (6, 15), (16, 23), (24, long_min - 1), (long_min, remaining)]
    return [{'from': first + a, 'to': first + b} for a, b in offsets]


def affinity(entry):
    """Coarse hints, never sufficient evidence for natural use or sense approval."""
    overrides = {
        '물고기': ['nature', 'outdoor'], '계산하다': ['shopping', 'food'],
        '찍다': ['school', 'work'], '새롭다': ['school', 'work', 'object_problem'],
        '급하다': ['transport', 'work', 'object_problem'], '이불': ['home', 'family'],
        '맵다': ['food', 'kitchen'], '테이프': ['shopping', 'object_problem', 'school'],
        '버리다': ['home', 'kitchen', 'object_problem'], '쓰다': ['food', 'kitchen'],
        '수영장': ['outdoor', 'health'], '미술관': ['travel', 'school'],
        '목': ['health', 'body'], '감': ['food', 'shopping'],
        '나뭇잎': ['nature', 'outdoor'], '회의': ['work', 'communication'],
        '벽': ['home', 'object_problem'], '돌': ['nature', 'outdoor'],
        '풀': ['nature', 'outdoor'] if entry['sense'] == 'grass' else ['school', 'object_problem'],
        '이': ['health', 'body'] if entry['sense'] == 'tooth' else ['communication', 'home'],
        '던지다': ['outdoor', 'object_problem'], '충전기': ['object_problem', 'travel'],
        '충전하다': ['object_problem', 'communication'], '시간표': ['school', 'transport'],
        '아저씨': ['shopping', 'home', 'communication'], '동갑': ['friendship', 'school'],
        '가만히': ['home', 'friendship'], '방금': ['communication', 'home'],
    }
    if entry['lemma'] in overrides:
        return overrides[entry['lemma']]
    tag_map = {'food': ['food', 'kitchen', 'shopping'], 'nature': ['nature', 'outdoor'],
               'weather': ['outdoor', 'travel'], 'school': ['school'], 'work': ['work'],
               'shopping': ['shopping'], 'transport': ['transport', 'travel'],
               'travel': ['travel'], 'body': ['body', 'health'], 'health': ['health'],
               'family': ['family', 'home'], 'communication': ['communication', 'friendship'],
               'emotion': ['friendship', 'family']}
    found = {s for tag in entry['tags'] for s in tag_map.get(tag, [])}
    defaults = {'people_social': ['family', 'friendship', 'communication'],
                'places_objects': ['home', 'shopping', 'object_problem'],
                'food_nature': ['food', 'nature'], 'verbs': ['home', 'object_problem', 'friendship'],
                'adjectives': ['home', 'friendship'], 'adverbs_connectors': ['communication', 'home'],
                'time_counters_units': ['home', 'shopping', 'transport'],
                'abstract_body_emotion': ['friendship', 'health'],
                'school_work_transport_info': ['school', 'work', 'transport']}
    return sorted(found or set(defaults[entry['category']]))


class ReviewScheduler:
    def __init__(self, window_data):
        self.entries = {e['vocab_id']: e for e in window_data['entries']}
        self.actual = {vid: set() for vid in self.entries}
        self.credits = {vid: {} for vid in self.entries}
        self.last_recorded_text = 0

    def new_ids(self, text):
        return sorted(vid for vid, e in self.entries.items() if e['first_introduction_text'] == text)

    def scene_candidates(self, text):
        """New-vocabulary anchors first; coarse hints to a scene author, not prose."""
        new_ids = self.new_ids(text)
        if new_ids:
            pools = [set(self.entries[vid]['scene_affinity']) for vid in new_ids]
            common = set.intersection(*pools)
            return {'new_vocab_ids': new_ids, 'candidate_scenes': sorted(common or set.union(*pools)),
                    'all_new_words_share_hint': bool(common), 'realization_review_required': True}
        counts = Counter()
        for vid, entry in self.entries.items():
            if entry['first_introduction_text'] not in self.actual[vid] or len(self.actual[vid]) >= 6:
                continue
            if any(i not in self.credits[vid] and w['from'] <= text
                   for i, w in enumerate(entry['review_windows'])):
                counts.update(entry['scene_affinity'])
        return {'new_vocab_ids': [], 'candidate_scenes': [s for s, n in counts.most_common()],
                'all_new_words_share_hint': None, 'realization_review_required': True}

    def record(self, text, confirmed_ids):
        """Only caller-confirmed body occurrences. Repeated tokens/text give one credit.

        Advance in text order; confirm introduction at its frozen text. Early extras
        count in actual quota, but do not prepay an unopened spaced opportunity.
        One event pays at most the oldest opened, unpaid window (including debt).
        """
        if isinstance(text, bool) or not isinstance(text, int) or not 1 <= text <= 300:
            raise ValueError('text must be 1..300')
        if text < self.last_recorded_text:
            raise ValueError('Records must be chronological')
        ids = set(confirmed_ids)
        if not ids <= self.entries.keys():
            raise ValueError('Unknown or retired vocabulary ID')
        for vid in ids:
            first = self.entries[vid]['first_introduction_text']
            if text < first or (text > first and first not in self.actual[vid]):
                raise ValueError('Review before confirmed introduction')
        self.last_recorded_text = text
        for vid in ids:
            if text in self.actual[vid]:
                continue
            self.actual[vid].add(text)
            if text == self.entries[vid]['first_introduction_text']:
                continue
            for index, w in enumerate(self.entries[vid]['review_windows']):
                if index not in self.credits[vid] and w['from'] <= text:
                    self.credits[vid][index] = text
                    break

    def pool(self, text, scene, approved_ids=(), veto_ids=()):
        """Semantic gate first. Deadline pressure never overrides a veto.

        approved_ids are positive, scene-specific realization judgments, not tags.
        They are provisional during dry-run, and require text/sense QA at runtime.
        """
        if not isinstance(text, int) or isinstance(text, bool) or not 1 <= text <= 300:
            raise ValueError('text must be 1..300')
        if text < self.last_recorded_text:
            raise ValueError('Cannot select reviews in an already passed text')
        if not scene or not set(scene) <= set(SCENES):
            raise ValueError('Unknown/empty scene')
        approved, veto = set(approved_ids), set(veto_ids)
        candidates, excluded = [], []
        for vid, e in self.entries.items():
            first = e['first_introduction_text']
            if first not in self.actual[vid] or text <= first or text in self.actual[vid]:
                continue
            if len(self.actual[vid]) >= 6:
                continue
            opened = [(i, w) for i, w in enumerate(e['review_windows'])
                      if i not in self.credits[vid] and w['from'] <= text]
            if not opened:
                continue
            stage, window = opened[0]
            match = len(set(scene) & set(e['scene_affinity'])) / len(set(scene))
            reason = ('semantic_veto' if vid in veto else 'no_scene_affinity' if not match
                      else 'realization_review_pending' if vid not in approved else None)
            if reason:
                excluded.append({'vocab_id': vid, 'reason': reason})
                continue
            gap = text - max(self.actual[vid])
            urgency = 20 / max(1, window['to'] - text + 1)
            debt = max(0, text - window['to'])
            score = 100 * match + urgency + min(debt, 25) + 4 * (6 - len(self.actual[vid])) + min(gap, 30) / 3
            if gap < 3:
                score -= 30  # spacing preference, not a deadline-breaking hard ban
            candidates.append({'vocab_id': vid, 'window_index': stage,
                               'deadline': window['to'], 'carry_debt': debt > 0,
                               'past_distinct_exposures': len(self.actual[vid]),
                               'gap': gap, 'semantic_match': match, 'score': round(score, 3),
                               'domain': e['semantic_domain']})
        return sorted(candidates, key=lambda r: (-r['score'], r['deadline'], r['vocab_id'])), excluded

    def select(self, text, scene, approved_ids=(), veto_ids=(), desired=8,
               coherent_extra_capacity=0):
        """5..8 soft goal. Caller must justify extra capacity with a coherent scene."""
        if not 0 <= desired <= 8 or not 0 <= coherent_extra_capacity <= 8:
            raise ValueError('Invalid soft capacity')
        pool, excluded = self.pool(text, scene, approved_ids, veto_ids)
        selected, domains = [], Counter()
        while pool and len(selected) < desired + coherent_extra_capacity:
            chosen = max(pool, key=lambda r: (r['score'] - 12 * domains[r['domain']],
                                              -r['deadline'], r['vocab_id']))
            pool.remove(chosen)
            selected.append(chosen)
            domains[chosen['domain']] += 1
        return {'new_vocab_ids': self.new_ids(text), 'selected_reviews': selected,
                'excluded': excluded, 'selection_is_observation': False,
                'load_warning': len(selected) > 10 or len(selected) + len(self.new_ids(text)) > 12}

    def audit(self, text=300, final=False):
        """Expired windows are debt warnings; final actual quota is a hard error."""
        if not isinstance(text, int) or isinstance(text, bool) or not 1 <= text <= 300:
            raise ValueError('Audit text must be 1..300')
        if text < self.last_recorded_text or (final and text != 300):
            raise ValueError('Final audit requires text 300; cannot audit before recorded history')
        warnings, errors = [], []
        for vid, e in self.entries.items():
            for i, w in enumerate(e['review_windows']):
                if i not in self.credits[vid] and w['to'] < text:
                    warnings.append({'vocab_id': vid, 'window_index': i, 'deadline': w['to'],
                                     'type': 'expired_window_debt'})
                elif i not in self.credits[vid] and w['from'] <= text <= w['to'] and w['to'] - text <= 3:
                    warnings.append({'vocab_id': vid, 'window_index': i, 'deadline': w['to'],
                                     'type': 'approaching_deadline'})
            if final:
                if e['first_introduction_text'] not in self.actual[vid]:
                    errors.append({'vocab_id': vid, 'type': 'unconfirmed_introduction'})
                if len(self.actual[vid]) < 6:
                    errors.append({'vocab_id': vid, 'type': 'fewer_than_six_actual_texts',
                                   'actual_count': len(self.actual[vid])})
            elif e['first_introduction_text'] <= text and 6 - len(self.actual[vid]) > 300 - text:
                warnings.append({'vocab_id': vid, 'type': 'final_quota_no_longer_feasible',
                                 'remaining_required': max(0, 6 - len(self.actual[vid])),
                                 'remaining_texts': 300 - text})
        return {'ok': not errors, 'warnings': warnings, 'errors': errors,
                'phase': 'final_actual' if final else 'in_progress',
                'spacing_credit_count': sum(map(len, self.credits.values())),
                'actual_entry_text_pairs': sum(map(len, self.actual.values()))}


def capacity_dry_run(window_data, capacity=10):
    """Interval EDF proof with NO semantic assumptions; output is never runtime hard schedule."""
    jobs = sorted((w['from'], w['to'], e['vocab_id'], i)
                  for e in window_data['entries'] for i, w in enumerate(e['review_windows']))
    heap, rows, misses = [], [], []
    index = 0
    for text in range(1, 301):
        while index < len(jobs) and jobs[index][0] <= text:
            low, high, vid, stage = jobs[index]
            heapq.heappush(heap, (high, vid, stage)); index += 1
        assigned = []
        while heap and heap[0][0] < text:
            high, vid, stage = heapq.heappop(heap)
            misses.append({'vocab_id': vid, 'window_index': stage, 'deadline': high})
        for _ in range(capacity):
            if not heap:
                break
            high, vid, stage = heapq.heappop(heap)
            assigned.append({'vocab_id': vid, 'window_index': stage})
        rows.append({'text': text, 'reviews': assigned})
    misses.extend({'vocab_id': vid, 'window_index': stage, 'deadline': high} for high, vid, stage in heap)
    return {'status': 'numeric_only_not_observed', 'capacity': capacity, 'rows': rows,
            'misses': misses, 'complete': not misses and index == len(jobs)}
