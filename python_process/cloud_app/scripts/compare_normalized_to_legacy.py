from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

from ..data.repository import load_product_types, load_skus
from ..data.versioning import get_current_version


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python3 -m python_process.cloud_app.scripts.compare_normalized_to_legacy",
        description="Rebuild legacy-style JSON from normalized version data and compare with original file.",
    )
    parser.add_argument("--original-file-path", type=Path, required=True)
    parser.add_argument("--version", type=str, default="")
    parser.add_argument("--write-reconstructed-json", type=Path, default=None)
    parser.add_argument("--report-path", type=Path, default=None)
    return parser.parse_args()


def _load_original_payload(original_file_path: Path) -> dict[str, Any]:
    text = original_file_path.read_text(encoding="utf-8")
    if original_file_path.suffix.lower() == ".js":
        prefix = "const packingData ="
        if prefix not in text:
            raise ValueError("Expected 'const packingData =' in legacy JS file.")
        payload_text = text.split(prefix, 1)[1].strip()
        if payload_text.endswith(";"):
            payload_text = payload_text[:-1]
        return json.loads(payload_text)

    return json.loads(text)


def _safe_bundle_value(value: Any) -> int:
    text = str(value)
    first_token = text.split("/")[0].strip()
    return int(float(first_token))


def _load_normalized_tables(version: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    product_type_rows = load_product_types(version).to_dict(orient="records")
    sku_rows = load_skus(version).to_dict(orient="records")

    return product_type_rows, sku_rows


def _build_reconstructed_payload(
    original_payload: dict[str, Any],
    product_type_rows: list[dict[str, Any]],
    sku_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    skus_by_product_type: dict[str, dict[str, Any]] = {}
    for sku_row in sku_rows:
        sku_id = str(sku_row["sku_id"])
        product_type_id = str(sku_row["product_type_id"])
        skus_by_product_type.setdefault(product_type_id, {})
        skus_by_product_type[product_type_id][sku_id] = {
            "skuId": sku_id,
            "productTypeId": product_type_id,
            "displayOrder": int(sku_row["display_order"]),
            "popularityScore": int(sku_row["popularity_score"]),
            "productType": str(sku_row["product_type"]),
            "SKU": str(sku_row["sku"]),
            "eagleSticksPerBundle": str(int(sku_row["calculated_sticks_per_bundle"])),
            "eagleBundlesPerTruckLoad": str(
                int(sku_row.get("eagle_bundles_per_truckload", sku_row["calculated_bundles_per_truckload"]))
            ),
            "eagleSticksPerTruckload": int(sku_row["eagle_sticks_per_truckload"]),
            "length": "",
            "calculatedSticksPerBundle": int(sku_row["calculated_sticks_per_bundle"]),
            "size": str(sku_row["size"]),
        }

    product_types_payload: list[dict[str, Any]] = []
    for product_type_row in product_type_rows:
        product_type_id = str(product_type_row["product_type_id"])
        product_types_payload.append(
            {
                "productTypeId": product_type_id,
                "productType": str(product_type_row["product_type"]),
                "skus": skus_by_product_type.get(product_type_id, {}),
            }
        )

    return {
        "date": original_payload.get("date"),
        "productTypes": product_types_payload,
    }


def _flatten_legacy_skus(legacy_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    flat_map: dict[str, dict[str, Any]] = {}
    for product_type_entry in legacy_payload.get("productTypes", []):
        product_type_id = str(product_type_entry.get("productTypeId"))
        product_type_name = str(product_type_entry.get("productType"))
        sku_map = product_type_entry.get("skus", {})
        for sku_id, sku_entry in sku_map.items():
            flat_map[str(sku_id)] = {
                "productTypeId": str(sku_entry.get("productTypeId", product_type_id)),
                "productType": str(sku_entry.get("productType", product_type_name)),
                "SKU": str(sku_entry.get("SKU", "")),
                "size": str(sku_entry.get("size", "")),
                "displayOrder": int(float(sku_entry.get("displayOrder", 0))),
                "popularityScore": int(float(sku_entry.get("popularityScore", 0))),
                "eagleSticksPerTruckload": int(float(sku_entry.get("eagleSticksPerTruckload", 0))),
                "calculatedSticksPerBundle": int(float(sku_entry.get("calculatedSticksPerBundle", 0))),
                "eagleBundlesPerTruckLoad": _safe_bundle_value(sku_entry.get("eagleBundlesPerTruckLoad", 0)),
            }
    return flat_map


def compare_payloads(original_payload: dict[str, Any], reconstructed_payload: dict[str, Any]) -> dict[str, Any]:
    original_sku_map = _flatten_legacy_skus(original_payload)
    reconstructed_sku_map = _flatten_legacy_skus(reconstructed_payload)

    original_ids = set(original_sku_map.keys())
    reconstructed_ids = set(reconstructed_sku_map.keys())

    missing_in_reconstructed = sorted(original_ids - reconstructed_ids)
    missing_in_original = sorted(reconstructed_ids - original_ids)

    fields_to_compare = [
        "productTypeId",
        "productType",
        "SKU",
        "size",
        "displayOrder",
        "popularityScore",
        "eagleSticksPerTruckload",
        "calculatedSticksPerBundle",
        "eagleBundlesPerTruckLoad",
    ]

    mismatches: list[dict[str, Any]] = []
    for sku_id in sorted(original_ids & reconstructed_ids):
        original_entry = original_sku_map[sku_id]
        reconstructed_entry = reconstructed_sku_map[sku_id]
        for field_name in fields_to_compare:
            if original_entry[field_name] != reconstructed_entry[field_name]:
                mismatches.append(
                    {
                        "sku_id": sku_id,
                        "field": field_name,
                        "original": original_entry[field_name],
                        "reconstructed": reconstructed_entry[field_name],
                    }
                )

    return {
        "original_sku_count": len(original_ids),
        "reconstructed_sku_count": len(reconstructed_ids),
        "missing_in_reconstructed": missing_in_reconstructed,
        "missing_in_original": missing_in_original,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
    }


def main() -> None:
    arguments = parse_arguments()
    console = Console()

    version = arguments.version or get_current_version()
    original_payload = _load_original_payload(arguments.original_file_path)
    product_type_rows, sku_rows = _load_normalized_tables(version)
    reconstructed_payload = _build_reconstructed_payload(original_payload, product_type_rows, sku_rows)
    comparison_report = compare_payloads(original_payload, reconstructed_payload)

    if arguments.write_reconstructed_json:
        arguments.write_reconstructed_json.parent.mkdir(parents=True, exist_ok=True)
        arguments.write_reconstructed_json.write_text(
            json.dumps(reconstructed_payload, indent=2),
            encoding="utf-8",
        )

    if arguments.report_path:
        arguments.report_path.parent.mkdir(parents=True, exist_ok=True)
        arguments.report_path.write_text(json.dumps(comparison_report, indent=2), encoding="utf-8")

    summary = Table(title="Legacy Comparison Summary")
    summary.add_column("Field")
    summary.add_column("Value")
    summary.add_row("Version", version)
    summary.add_row("Original SKU Count", str(comparison_report["original_sku_count"]))
    summary.add_row("Reconstructed SKU Count", str(comparison_report["reconstructed_sku_count"]))
    summary.add_row("Missing in Reconstructed", str(len(comparison_report["missing_in_reconstructed"])))
    summary.add_row("Missing in Original", str(len(comparison_report["missing_in_original"])))
    summary.add_row("Field Mismatches", str(comparison_report["mismatch_count"]))
    console.print(summary)

    if comparison_report["mismatch_count"] > 0:
        preview = Table(title="Mismatch Preview (first 20)")
        preview.add_column("SKU")
        preview.add_column("Field")
        preview.add_column("Original")
        preview.add_column("Reconstructed")
        for mismatch in comparison_report["mismatches"][:20]:
            preview.add_row(
                mismatch["sku_id"],
                mismatch["field"],
                str(mismatch["original"]),
                str(mismatch["reconstructed"]),
            )
        console.print(preview)


if __name__ == "__main__":
    main()
