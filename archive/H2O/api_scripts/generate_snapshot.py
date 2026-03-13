#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATOR_DIR = ROOT / 'calculate_load_packing_data'
SNAPSHOT_PATH = ROOT / 'api' / 'data' / 'packing_data.json'


def main() -> None:
    subprocess.run(
        ['python3', 'export_api_snapshot.py'],
        cwd=str(GENERATOR_DIR),
        check=True,
    )

    if not SNAPSHOT_PATH.exists():
        raise RuntimeError(f'Snapshot not generated at {SNAPSHOT_PATH}')

    print(f'Generated snapshot: {SNAPSHOT_PATH}')


if __name__ == '__main__':
    main()
