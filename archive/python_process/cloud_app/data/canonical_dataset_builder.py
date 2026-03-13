from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from loguru import logger

from .importer import normalize_packing_data, parse_load_js


def read_file_sha256_hex(source_file_path: Path) -> str:
    file_bytes = source_file_path.read_bytes()
    return hashlib.sha256(file_bytes).hexdigest()


def _build_constraints_lookup(bundle_rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    constraints_by_sku_identifier: dict[str, dict[str, int]] = {}
    for bundle_row in bundle_rows:
        sku_identifier = str(bundle_row["sku_id"])
        constraints_by_sku_identifier[sku_identifier] = {
            "min_number_of_bundles": int(bundle_row["min_number_of_bundles"]),
            "max_number_of_bundles": int(bundle_row["max_number_of_bundles"]),
        }
    return constraints_by_sku_identifier


def build_canonical_dataset_from_legacy_js(
    legacy_source_file_path: Path,
    dataset_identifier: str,
) -> dict[str, Any]:
    logger.info("Parsing legacy JS payload from {}", legacy_source_file_path)
    parsed_legacy_payload = parse_load_js(legacy_source_file_path)
    product_type_dataframe, sku_dataframe, bundle_dataframe = normalize_packing_data(parsed_legacy_payload)

    product_type_rows = product_type_dataframe.to_dict(orient="records")
    sku_rows = sku_dataframe.to_dict(orient="records")
    bundle_rows = bundle_dataframe.to_dict(orient="records")
    constraints_by_sku_identifier = _build_constraints_lookup(bundle_rows)

    canonical_product_types: list[dict[str, Any]] = []
    for product_type_row in product_type_rows:
        canonical_product_types.append(
            {
                "product_type_id": str(product_type_row["product_type_id"]),
                "name": str(product_type_row["product_type"]),
            }
        )

    canonical_skus: list[dict[str, Any]] = []
    for sku_row in sku_rows:
        sku_identifier = str(sku_row["sku_id"])
        canonical_skus.append(
            {
                "sku_id": sku_identifier,
                "product_type_id": str(sku_row["product_type_id"]),
                "description": str(sku_row["sku"]),
                "size": str(sku_row["size"]),
                "display_order": int(sku_row["display_order"]),
                "popularity_score": int(sku_row["popularity_score"]),
                "packaging": {
                    "sticks_per_bundle": int(sku_row["calculated_sticks_per_bundle"]),
                    "sticks_per_truckload": int(sku_row["eagle_sticks_per_truckload"]),
                    "bundles_per_truckload": int(sku_row["calculated_bundles_per_truckload"]),
                },
                "constraints": constraints_by_sku_identifier[sku_identifier],
            }
        )

    canonical_dataset_payload: dict[str, Any] = {
        "schema_version": "packing_dataset/v1",
        "dataset_identifier": dataset_identifier,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "legacy_js_path": str(legacy_source_file_path.resolve()),
            "legacy_js_sha256": read_file_sha256_hex(legacy_source_file_path),
            "legacy_dataset_date": parsed_legacy_payload.get("date"),
        },
        "row_counts": {
            "product_types": len(canonical_product_types),
            "skus": len(canonical_skus),
        },
        "product_types": canonical_product_types,
        "skus": canonical_skus,
    }

    _validate_canonical_dataset_payload(canonical_dataset_payload)
    logger.info(
        "Built canonical dataset: {} product types, {} skus",
        canonical_dataset_payload["row_counts"]["product_types"],
        canonical_dataset_payload["row_counts"]["skus"],
    )
    return canonical_dataset_payload


def _validate_canonical_dataset_payload(canonical_dataset_payload: dict[str, Any]) -> None:
    product_types = canonical_dataset_payload["product_types"]
    skus = canonical_dataset_payload["skus"]

    product_type_identifier_set = {entry["product_type_id"] for entry in product_types}
    if len(product_type_identifier_set) != len(product_types):
        raise ValueError("Duplicate product_type_id detected in canonical product_types.")

    sku_identifier_set = {entry["sku_id"] for entry in skus}
    if len(sku_identifier_set) != len(skus):
        raise ValueError("Duplicate sku_id detected in canonical skus.")

    for sku_entry in skus:
        if sku_entry["product_type_id"] not in product_type_identifier_set:
            raise ValueError(
                f"SKU {sku_entry['sku_id']} references unknown product_type_id {sku_entry['product_type_id']}."
            )

        packaging = sku_entry["packaging"]
        constraints = sku_entry["constraints"]
        sticks_per_bundle = int(packaging["sticks_per_bundle"])
        sticks_per_truckload = int(packaging["sticks_per_truckload"])
        bundles_per_truckload = int(packaging["bundles_per_truckload"])
        minimum_bundle_count = int(constraints["min_number_of_bundles"])
        maximum_bundle_count = int(constraints["max_number_of_bundles"])

        if sticks_per_bundle <= 0:
            raise ValueError(f"SKU {sku_entry['sku_id']} has non-positive sticks_per_bundle.")
        if sticks_per_truckload <= 0:
            raise ValueError(f"SKU {sku_entry['sku_id']} has non-positive sticks_per_truckload.")
        if bundles_per_truckload <= 0:
            raise ValueError(f"SKU {sku_entry['sku_id']} has non-positive bundles_per_truckload.")
        if minimum_bundle_count <= 0:
            raise ValueError(f"SKU {sku_entry['sku_id']} has non-positive min_number_of_bundles.")
        if minimum_bundle_count > maximum_bundle_count:
            raise ValueError(f"SKU {sku_entry['sku_id']} has min_number_of_bundles > max_number_of_bundles.")
        if maximum_bundle_count > bundles_per_truckload:
            raise ValueError(f"SKU {sku_entry['sku_id']} has max_number_of_bundles > bundles_per_truckload.")


def write_canonical_dataset_json(canonical_dataset_payload: dict[str, Any], output_file_path: Path) -> None:
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    output_file_path.write_text(
        json.dumps(canonical_dataset_payload, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )
    logger.info("Wrote canonical dataset JSON to {}", output_file_path)
