import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from python_process.cloud_app.config import DEFAULT_JS_SOURCE
from python_process.cloud_app.data.repository import write_parquet
from python_process.cloud_app.data.versioning import (
    get_version_dir,
    make_version_name,
    set_current_version,
)


def parse_load_js(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    prefix = "const packingData ="
    if prefix not in text:
        raise ValueError("Expected 'const packingData =' in source JS file.")

    payload = text.split(prefix, 1)[1].strip()
    if payload.endswith(";"):
        payload = payload[:-1]

    return json.loads(payload)


def normalize_packing_data(
    packing_data: dict,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    product_rows: list[dict] = []
    sku_rows: list[dict] = []
    bundle_rows: list[dict] = []

    display_order = 0
    for product_type in packing_data.get("productTypes", []):
        product_type_id = str(product_type.get("productTypeId"))
        product_type_name = str(product_type.get("productType"))
        product_rows.append(
            {
                "product_type_id": product_type_id,
                "product_type": product_type_name,
            }
        )

        skus = product_type.get("skus", {})
        for sku_id, sku in skus.items():
            display_order += 1
            sticks_per_bundle = int(float(sku.get("calculatedSticksPerBundle", 1)))
            truck_sticks = int(float(sku.get("eagleSticksPerTruckload", sticks_per_bundle)))
            bundles_per_truckload = max(1, round(truck_sticks / max(1, sticks_per_bundle)))
            sku_rows.append(
                {
                    "sku_id": str(sku_id),
                    "product_type_id": product_type_id,
                    "product_type": product_type_name,
                    "sku": str(sku.get("SKU", sku_id)),
                    "size": str(sku.get("size", "")),
                    "display_order": int(sku.get("displayOrder", display_order)),
                    "popularity_score": int(float(sku.get("popularityScore", 1))),
                    "calculated_sticks_per_bundle": sticks_per_bundle,
                    "eagle_sticks_per_truckload": truck_sticks,
                    "calculated_bundles_per_truckload": bundles_per_truckload,
                }
            )
            bundle_rows.append(
                {
                    "sku_id": str(sku_id),
                    "min_number_of_bundles": 1,
                    "max_number_of_bundles": bundles_per_truckload,
                }
            )

    return pd.DataFrame(product_rows), pd.DataFrame(sku_rows), pd.DataFrame(bundle_rows)


def import_from_load_js_file(source_path: str | None = None, version: str | None = None) -> dict:
    source = Path(source_path) if source_path else DEFAULT_JS_SOURCE
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    packing_data = parse_load_js(source)
    df_product_types, df_skus, df_bundles = normalize_packing_data(packing_data)

    new_version = version or make_version_name()
    out_dir = get_version_dir(new_version)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_parquet(df_product_types, out_dir / "product_types.parquet")
    write_parquet(df_skus, out_dir / "skus.parquet")
    write_parquet(df_bundles, out_dir / "bundles.parquet")
    pointer = set_current_version(new_version)

    metadata = {
        "version": new_version,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source),
        "rows": {
            "product_types": int(len(df_product_types)),
            "skus": int(len(df_skus)),
            "bundles": int(len(df_bundles)),
        },
    }
    metadata_path = out_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return {"current": pointer, "metadata": metadata}
