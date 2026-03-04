from __future__ import annotations

from pathlib import Path

from loguru import logger

from .data import flatten_skus, load_snapshot
from .models import SKU
from .routes import initialize_runtime


BASE_DIR = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = BASE_DIR / "api" / "data" / "packing_data.json"
VERSIONS_DIR = BASE_DIR / "api" / "data" / "versions"


def reload_runtime_snapshot(snapshot_path: Path | None = None) -> dict[str, object]:
    active_snapshot_path = snapshot_path or SNAPSHOT_PATH
    raw_snapshot = load_snapshot(active_snapshot_path)
    raw_skus = flatten_skus(raw_snapshot)
    sku_dict = {sku["skuId"]: SKU(**sku).model_dump() for sku in raw_skus}
    all_skus = [sku_dict[sku_id] for sku_id in sku_dict]
    initialize_runtime(all_skus, sku_dict)
    logger.info("Loaded SKU snapshot: {} SKUs", len(sku_dict))
    return {"snapshot": raw_snapshot, "skus": all_skus, "sku_dict": sku_dict}
