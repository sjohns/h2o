from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .models import SKU


def load_packing_data_from_js(js_path: Path) -> Dict[str, Any]:
    raw = js_path.read_text(encoding="utf-8").strip()
    prefix = "const packingData ="
    if not raw.startswith(prefix):
        raise ValueError(f"Unexpected JS format in {js_path}")

    payload = raw[len(prefix) :].strip()
    if payload.endswith(";"):
        payload = payload[:-1].strip()

    return json.loads(payload)


def flatten_skus(packing_data: Dict[str, Any]) -> Dict[str, SKU]:
    skus: Dict[str, SKU] = {}
    for product_type in packing_data.get("productTypes", []):
        for sku_id, sku_data in product_type.get("skus", {}).items():
            skus[sku_id] = SKU(**sku_data)
    return skus
