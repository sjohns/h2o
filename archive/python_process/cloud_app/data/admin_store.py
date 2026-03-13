from __future__ import annotations

import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from .repository import (
    get_sqlite_db_path,
    get_version_counts,
    list_versions,
    load_bundles,
    load_product_types,
    load_skus,
    write_version_data,
)
from ..config import DATA_ROOT
from .versioning import get_current_version, get_version_dir, make_version_name, set_current_version


def _load_product_types(version: str) -> pd.DataFrame:
    return load_product_types(version)


def _load_bundles(version: str) -> pd.DataFrame:
    return load_bundles(version)


def _calculate_sticks_per_bundle(eagle_sticks_per_truckload: int, bundles_per_truckload: int) -> int:
    if eagle_sticks_per_truckload <= 0:
        raise ValueError("eagle_sticks_per_truckload must be > 0")
    if bundles_per_truckload <= 0:
        raise ValueError("bundles_per_truckload must be > 0")
    if eagle_sticks_per_truckload % bundles_per_truckload != 0:
        raise ValueError("eagle_sticks_per_truckload must be divisible by bundles_per_truckload")
    return int(eagle_sticks_per_truckload // bundles_per_truckload)


def _write_version_snapshot(
    product_type_dataframe: pd.DataFrame,
    sku_dataframe: pd.DataFrame,
    bundle_dataframe: pd.DataFrame,
    source_version: str,
    action: str,
    actor: str,
) -> dict[str, Any]:
    new_version = make_version_name(prefix="v")
    version_directory = get_version_dir(new_version)
    version_directory.mkdir(parents=True, exist_ok=True)

    write_version_data(
        version=new_version,
        product_type_dataframe=product_type_dataframe,
        sku_dataframe=sku_dataframe,
        bundle_dataframe=bundle_dataframe,
    )

    metadata_payload = {
        "version": new_version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_version": source_version,
        "action": action,
        "actor": actor,
        "rows": {
            "product_types": int(len(product_type_dataframe)),
            "skus": int(len(sku_dataframe)),
            "bundles": int(len(bundle_dataframe)),
        },
    }
    metadata_file_path = version_directory / "metadata.json"
    metadata_file_path.write_text(json.dumps(metadata_payload, indent=2), encoding="utf-8")
    current_pointer_payload = set_current_version(new_version)
    return {"version": new_version, "current": current_pointer_payload, "metadata": metadata_payload}


def get_current_dataset_payload() -> dict[str, Any]:
    current_version = get_current_version()
    sku_dataframe = load_skus(current_version)
    product_type_dataframe = _load_product_types(current_version)

    return {
        "version": current_version,
        "product_types": product_type_dataframe.to_dict(orient="records"),
        "skus": sku_dataframe.to_dict(orient="records"),
    }


def update_sku_and_create_version(
    sku_id: str,
    update_fields: dict[str, Any],
    actor: str,
) -> dict[str, Any]:
    source_version = get_current_version()
    sku_dataframe = load_skus(source_version)
    product_type_dataframe = _load_product_types(source_version)
    bundle_dataframe = _load_bundles(source_version)

    matching_rows = sku_dataframe.index[sku_dataframe["sku_id"] == sku_id].tolist()
    if not matching_rows:
        raise ValueError(f"SKU not found: {sku_id}")

    sku_row_index = matching_rows[0]

    if "product_type_id" in update_fields:
        candidate_product_type_id = str(update_fields["product_type_id"])
        available_product_type_ids = set(product_type_dataframe["product_type_id"].astype(str).tolist())
        if candidate_product_type_id not in available_product_type_ids:
            raise ValueError(f"Unknown product_type_id: {candidate_product_type_id}")
        sku_dataframe.at[sku_row_index, "product_type_id"] = candidate_product_type_id

    if "sku" in update_fields:
        sku_dataframe.at[sku_row_index, "sku"] = str(update_fields["sku"])
    if "size" in update_fields:
        sku_dataframe.at[sku_row_index, "size"] = str(update_fields["size"])
    if "display_order" in update_fields:
        sku_dataframe.at[sku_row_index, "display_order"] = int(update_fields["display_order"])
    if "popularity_score" in update_fields:
        popularity_score = int(update_fields["popularity_score"])
        if popularity_score <= 0:
            raise ValueError("popularity_score must be > 0")
        sku_dataframe.at[sku_row_index, "popularity_score"] = popularity_score

    computed_bundles_per_truckload = int(
        update_fields.get(
            "bundles_per_truckload",
            sku_dataframe.at[sku_row_index, "calculated_bundles_per_truckload"],
        )
    )
    computed_sticks_per_truckload = int(
        update_fields.get(
            "eagle_sticks_per_truckload",
            sku_dataframe.at[sku_row_index, "eagle_sticks_per_truckload"],
        )
    )
    computed_sticks_per_bundle = _calculate_sticks_per_bundle(
        eagle_sticks_per_truckload=computed_sticks_per_truckload,
        bundles_per_truckload=computed_bundles_per_truckload,
    )

    sku_dataframe.at[sku_row_index, "eagle_sticks_per_truckload"] = computed_sticks_per_truckload
    sku_dataframe.at[sku_row_index, "calculated_bundles_per_truckload"] = computed_bundles_per_truckload
    sku_dataframe.at[sku_row_index, "calculated_sticks_per_bundle"] = computed_sticks_per_bundle

    bundle_matching_rows = bundle_dataframe.index[bundle_dataframe["sku_id"] == sku_id].tolist()
    if bundle_matching_rows:
        bundle_row_index = bundle_matching_rows[0]
        bundle_dataframe.at[bundle_row_index, "max_number_of_bundles"] = computed_bundles_per_truckload

    return _write_version_snapshot(
        product_type_dataframe=product_type_dataframe,
        sku_dataframe=sku_dataframe,
        bundle_dataframe=bundle_dataframe,
        source_version=source_version,
        action=f"update_sku:{sku_id}",
        actor=actor,
    )


def update_product_type_and_create_version(
    product_type_id: str,
    product_type_name: str,
    actor: str,
) -> dict[str, Any]:
    source_version = get_current_version()
    sku_dataframe = load_skus(source_version)
    product_type_dataframe = _load_product_types(source_version)
    bundle_dataframe = _load_bundles(source_version)

    matching_rows = product_type_dataframe.index[
        product_type_dataframe["product_type_id"].astype(str) == str(product_type_id)
    ].tolist()
    if not matching_rows:
        raise ValueError(f"Product type not found: {product_type_id}")

    row_index = matching_rows[0]
    product_type_dataframe.at[row_index, "product_type"] = product_type_name
    sku_dataframe.loc[sku_dataframe["product_type_id"].astype(str) == str(product_type_id), "product_type"] = (
        product_type_name
    )

    return _write_version_snapshot(
        product_type_dataframe=product_type_dataframe,
        sku_dataframe=sku_dataframe,
        bundle_dataframe=bundle_dataframe,
        source_version=source_version,
        action=f"update_product_type:{product_type_id}",
        actor=actor,
    )


def get_storage_status_payload() -> dict[str, Any]:
    current_version = get_current_version()
    versions = list_versions()
    current_counts = get_version_counts(current_version)
    sqlite_db_path = get_sqlite_db_path()

    return {
        "storage_engine": "sqlite",
        "sqlite_db_path": str(sqlite_db_path),
        "sqlite_db_exists": sqlite_db_path.exists(),
        "current_version": current_version,
        "version_count": len(versions),
        "versions": versions,
        "current_counts": current_counts,
    }


def run_storage_retention(keep_latest: int, dry_run: bool) -> dict[str, Any]:
    if keep_latest < 1:
        raise ValueError("keep_latest must be >= 1")

    versions = list_versions()
    current_version = get_current_version()
    keep_set = set(versions[:keep_latest])
    keep_set.add(current_version)
    archive_candidates = [version for version in versions if version not in keep_set]

    archive_directory = DATA_ROOT / "archive"
    archive_directory.mkdir(parents=True, exist_ok=True)
    archive_file_path = archive_directory / (
        "versions_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".zip"
    )

    archived_versions: list[str] = []
    removed_directories: list[str] = []

    if not dry_run and archive_candidates:
        with zipfile.ZipFile(archive_file_path, mode="a", compression=zipfile.ZIP_DEFLATED) as archive_file:
            for version in archive_candidates:
                version_directory = DATA_ROOT / version
                if not version_directory.exists() or not version_directory.is_dir():
                    continue
                for file_path in version_directory.rglob("*"):
                    if file_path.is_file():
                        archive_file.write(
                            file_path,
                            arcname=f"{version}/{file_path.relative_to(version_directory)}",
                        )
                archived_versions.append(version)

        for version in archived_versions:
            version_directory = DATA_ROOT / version
            if version_directory.exists() and version_directory.is_dir():
                shutil.rmtree(version_directory)
                removed_directories.append(version)

    return {
        "keep_latest": keep_latest,
        "dry_run": dry_run,
        "current_version": current_version,
        "total_versions": len(versions),
        "kept_versions": sorted(list(keep_set), reverse=True),
        "archive_candidates": archive_candidates,
        "archive_file": str(archive_file_path) if archive_candidates else None,
        "archived_versions": archived_versions,
        "removed_directories": removed_directories,
    }
