from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from loguru import logger
from rich.console import Console
from rich.table import Table

from ..data.repository import write_version_data
from ..data.versioning import get_version_dir, make_version_name, set_current_version

import pandas as pd


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python3 -m python_process.cloud_app.scripts.migrate_current_json_to_normalized",
        description="One-time migration: current packing JSON to normalized SQLite structure.",
    )
    parser.add_argument("--input-json-path", type=Path, required=True)
    parser.add_argument("--version", type=str, default="")
    parser.add_argument("--dataset-id", type=str, default="h2o-normalized-dataset")
    return parser.parse_args()


def _required_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if value is None:
        raise ValueError(f"Missing required key: {key}")
    return str(value)


def _required_int(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    if value is None:
        raise ValueError(f"Missing required key: {key}")
    return int(float(value))


def _parse_legacy_bundle_count(raw_value: Any, sku_id: str) -> int:
    if raw_value is None:
        raise ValueError(f"Missing eagleBundlesPerTruckLoad for {sku_id}")
    token = str(raw_value).split("/")[0].strip()
    bundle_count = int(float(token))
    if bundle_count <= 0:
        raise ValueError(f"Invalid eagleBundlesPerTruckLoad for {sku_id}: {raw_value}")
    return bundle_count


def _build_normalized_rows(source_payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    product_type_records: list[dict[str, Any]] = []
    sku_records: list[dict[str, Any]] = []
    bundle_constraint_records: list[dict[str, Any]] = []

    for product_type_entry in source_payload.get("productTypes", []):
        product_type_id = _required_string(product_type_entry, "productTypeId")
        product_type_name = _required_string(product_type_entry, "productType")
        product_type_records.append(
            {
                "product_type_id": product_type_id,
                "product_type": product_type_name,
            }
        )

        sku_map = product_type_entry.get("skus", {})
        if not isinstance(sku_map, dict):
            raise ValueError(f"Expected 'skus' map for product type {product_type_id}")

        for sku_id_from_map, sku_entry in sku_map.items():
            sku_id = str(sku_id_from_map)
            sku_description = _required_string(sku_entry, "SKU")
            size = _required_string(sku_entry, "size")
            display_order = _required_int(sku_entry, "displayOrder")
            popularity_score = _required_int(sku_entry, "popularityScore")
            eagle_sticks_per_truckload = _required_int(sku_entry, "eagleSticksPerTruckload")

            calculated_sticks_per_bundle = _required_int(sku_entry, "calculatedSticksPerBundle")
            if calculated_sticks_per_bundle <= 0:
                raise ValueError(f"Invalid calculatedSticksPerBundle for {sku_id}")

            source_eagle_bundles_per_truckload = _parse_legacy_bundle_count(
                sku_entry.get("eagleBundlesPerTruckLoad"),
                sku_id,
            )
            bundles_per_truckload = max(1, round(eagle_sticks_per_truckload / calculated_sticks_per_bundle))

            sku_records.append(
                {
                    "sku_id": sku_id,
                    "product_type_id": product_type_id,
                    "product_type": product_type_name,
                    "sku": sku_description,
                    "size": size,
                    "display_order": display_order,
                    "popularity_score": popularity_score,
                    "eagle_sticks_per_truckload": eagle_sticks_per_truckload,
                    "eagle_bundles_per_truckload": source_eagle_bundles_per_truckload,
                    "calculated_bundles_per_truckload": bundles_per_truckload,
                    "calculated_sticks_per_bundle": calculated_sticks_per_bundle,
                }
            )

            bundle_constraint_records.append(
                {
                    "sku_id": sku_id,
                    "min_number_of_bundles": 1,
                    "max_number_of_bundles": bundles_per_truckload,
                }
            )

    return product_type_records, sku_records, bundle_constraint_records


def main() -> None:
    arguments = parse_arguments()
    console = Console()

    source_payload = json.loads(arguments.input_json_path.read_text(encoding="utf-8"))
    product_type_rows, sku_rows, bundle_rows = _build_normalized_rows(source_payload)

    version_name = arguments.version or make_version_name(prefix="v")
    version_directory = get_version_dir(version_name)
    version_directory.mkdir(parents=True, exist_ok=True)

    product_type_dataframe = pd.DataFrame(product_type_rows)
    sku_dataframe = pd.DataFrame(sku_rows)
    bundle_dataframe = pd.DataFrame(bundle_rows)

    write_version_data(
        version=version_name,
        product_type_dataframe=product_type_dataframe,
        sku_dataframe=sku_dataframe,
        bundle_dataframe=bundle_dataframe,
    )

    current_pointer_payload = set_current_version(version_name)

    metadata_payload = {
        "schema_version": "normalized_packing_dataset/v1",
        "dataset_id": arguments.dataset_id,
        "migrated_at": datetime.now(timezone.utc).isoformat(),
        "source_json": str(arguments.input_json_path.resolve()),
        "source_date": source_payload.get("date"),
        "rows": {
            "product_types": int(len(product_type_dataframe)),
            "skus": int(len(sku_dataframe)),
            "bundles": int(len(bundle_dataframe)),
        },
    }
    metadata_path = version_directory / "metadata.json"
    metadata_path.write_text(json.dumps(metadata_payload, indent=2), encoding="utf-8")

    logger.info("Wrote normalized structure to {}", version_directory)

    summary_table = Table(title="Migration Complete")
    summary_table.add_column("Field")
    summary_table.add_column("Value")
    summary_table.add_row("Input JSON", str(arguments.input_json_path))
    summary_table.add_row("Version", version_name)
    summary_table.add_row("Version Directory", str(version_directory))
    summary_table.add_row("Current Pointer", json.dumps(current_pointer_payload))
    summary_table.add_row("Dataset ID", metadata_payload["dataset_id"])
    summary_table.add_row("Product Types", str(metadata_payload["rows"]["product_types"]))
    summary_table.add_row("SKUs", str(metadata_payload["rows"]["skus"]))
    summary_table.add_row("Bundle Constraints", str(metadata_payload["rows"]["bundles"]))
    console.print(summary_table)


if __name__ == "__main__":
    main()
