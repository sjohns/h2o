#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_JSON = ROOT / 'html' / 'load_packing_data.json'
TARGET_JSON = ROOT / 'api' / 'data' / 'packing_data.json'


def main() -> None:
    if not SOURCE_JSON.exists():
        raise RuntimeError(
            f'Missing source snapshot: {SOURCE_JSON}. Create this snapshot first, then rerun export_api_snapshot.py.'
        )

    data = json.loads(SOURCE_JSON.read_text(encoding='utf-8'))
    TARGET_JSON.parent.mkdir(parents=True, exist_ok=True)
    TARGET_JSON.write_text(json.dumps(data, indent=4), encoding='utf-8')
    print(f'Wrote {TARGET_JSON}')


if __name__ == '__main__':
    main()
