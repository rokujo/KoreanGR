"""Route historical audits to immutable copies after an active vocabulary revision."""
import json
from pathlib import Path

def historical_root(root):
    root = Path(root)
    migration = root / 'config/languages/ko/k1/id_migration.json'
    if migration.is_file() and json.loads(migration.read_text(encoding='utf-8')).get('phase') == '2.1A':
        snapshot = root / 'reports/phase2_1_snapshot'
        if not (snapshot / 'manifest.json').is_file():
            raise RuntimeError('Missing pre-2.1A historical snapshot')
        return snapshot
    return root

def protect_historical_build(root):
    if historical_root(root) != Path(root):
        raise SystemExit('Historical generator disabled for active Phase 2.1A. '
                         'Use scripts/build_k1_phase2_1A.py; historical artifacts are read-only.')
