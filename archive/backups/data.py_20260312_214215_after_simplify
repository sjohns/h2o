from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_ACTIVE = True


def load_snapshot(snapshot_path: Path) -> Dict[str, Any]:
    with snapshot_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def flatten_skus(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    skus: List[Dict[str, Any]] = []
    for product_type in snapshot.get("productTypes", []):
        if not product_type.get("active", DEFAULT_ACTIVE):
            continue
        for sku in product_type.get("skus", {}).values():
            if sku.get("active", DEFAULT_ACTIVE):
                skus.append(sku)
    return skus
