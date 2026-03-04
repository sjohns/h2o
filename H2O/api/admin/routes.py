from __future__ import annotations

import hashlib
import json
from io import BytesIO
from datetime import datetime
from typing import Any
from pathlib import Path

from fastapi import APIRouter, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from openpyxl import Workbook

from ..auth import require_admin, require_review
from ..data import load_snapshot
from .. import runtime
from .data_import import REQUIRED_COLUMNS, ValidationIssue, ValidationResult, import_workbook, _sku_key

router = APIRouter(prefix="/admin/data", tags=["admin-data"])


def _require_xlsx(upload: UploadFile) -> None:
    if not upload.filename or not upload.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx uploads are supported")


def _coerce_int(value: Any) -> int:
    if isinstance(value, int):
        return value
    return int(str(value).replace(",", "").strip())


def _coerce_length_feet(value: Any) -> int:
    text = str(value).strip().replace("'", "").replace("ft", "").strip()
    return int(text)


def _normalize_current_snapshot(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Convert the legacy JSON snapshot to the same format produced by import_workbook.

    Product types are keyed by product_type_name.
    SKUs are keyed by _sku_key(sku_description, size_nominal).
    """
    product_types: dict[str, dict[str, Any]] = {}

    for display_order, product_type in enumerate(snapshot.get("productTypes", []), start=1):
        pt_name = product_type.get("productType", "")
        if not pt_name:
            continue

        if pt_name not in product_types:
            product_types[pt_name] = {
                "product_type_name": pt_name,
                "product_type_display_order": display_order,
                "product_type_active_flag": "Y",
                "skus": {},
            }

        for _sku_id, sku in product_type.get("skus", {}).items():
            sku_desc = sku.get("SKU", "")
            size = sku.get("size", "")
            # Eagle reference strings — stored as-is, never parsed as numbers
            eagle_sticks = str(sku.get("eagleSticksPerBundle", "")).strip()
            eagle_bundles = str(sku.get("eagleBundlesPerTruckLoad", "")).strip()
            # calculatedSticksPerBundle is the admin-selected value, always an integer
            calc_sticks = int(sku.get("calculatedSticksPerBundle", 0))
            actual_sticks = _coerce_int(
                sku.get("actualSticksPerTruckLoad", sku.get("eagleSticksPerTruckload", 0))
            )

            product_types[pt_name]["skus"][_sku_key(sku_desc, size)] = {
                "sku_description": sku_desc,
                "size_nominal": size,
                "sku_display_order": int(sku.get("displayOrder", 0)),
                "sku_active_flag": "Y",
                "length_feet": _coerce_length_feet(sku.get("length", "0")),
                "popularity_score": int(sku.get("popularityScore", 1)),
                "eagle_sticks_per_bundle": eagle_sticks,
                "eagle_bundles_per_truckload": eagle_bundles,
                "calculated_sticks_per_bundle": calc_sticks,
                "actual_sticks_per_truckload": actual_sticks,
                "notes": "",
            }

    return product_types


def _response_from_validation(validation: ValidationResult, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=validation.model_dump())


def _build_diff_summary(
    current_product_types: dict[str, dict[str, Any]],
    uploaded_product_types: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    def _flatten(product_types: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for pt_name, pt in product_types.items():
            for sk, sku in pt["skus"].items():
                display_key = f"{sku['sku_description']} ({sku['size_nominal']})"
                result[display_key] = {**sku, "_pt_name": pt_name}
        return result

    current_flat = _flatten(current_product_types)
    uploaded_flat = _flatten(uploaded_product_types)

    added_skus = sorted(set(uploaded_flat) - set(current_flat))
    removed_skus = sorted(set(current_flat) - set(uploaded_flat))
    shared_skus = sorted(set(current_flat) & set(uploaded_flat))

    fields_to_compare = [
        "sku_display_order",
        "sku_active_flag",
        "length_feet",
        "popularity_score",
        "eagle_sticks_per_bundle",
        "eagle_bundles_per_truckload",
        "actual_sticks_per_truckload",
        "notes",
    ]

    changed_skus: dict[str, list[dict[str, Any]]] = {}
    active_flag_changes: list[dict[str, Any]] = []

    for key in shared_skus:
        before = current_flat[key]
        after = uploaded_flat[key]
        changes: list[dict[str, Any]] = []
        for field in fields_to_compare:
            if before.get(field) != after.get(field):
                change = {"field": field, "before": before.get(field), "after": after.get(field)}
                if field == "sku_active_flag":
                    change["highlight"] = "active_flag"
                    active_flag_changes.append(
                        {"sku": key, "before": before.get(field), "after": after.get(field)}
                    )
                changes.append(change)
        if changes:
            changed_skus[key] = changes

    return {
        "counts": {
            "current": {
                "product_types": len(current_product_types),
                "skus": len(current_flat),
            },
            "uploaded": {
                "product_types": len(uploaded_product_types),
                "skus": len(uploaded_flat),
            },
        },
        "added_skus": added_skus,
        "removed_skus": removed_skus,
        "changed_skus": changed_skus,
        "active_flag_changes": active_flag_changes,
    }


def _build_current_excel_workbook(product_types: dict[str, dict[str, Any]]) -> bytes:
    """Export current data as Excel using the same 12-column format as the import template."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "SKUs"
    sheet.append(REQUIRED_COLUMNS)

    sorted_pts = sorted(
        product_types.values(),
        key=lambda pt: (int(pt["product_type_display_order"]), pt["product_type_name"].lower()),
    )

    for pt in sorted_pts:
        sorted_skus = sorted(
            pt["skus"].values(),
            key=lambda s: (int(s["sku_display_order"]), s["sku_description"].lower()),
        )
        for sku in sorted_skus:
            sheet.append([
                pt["product_type_name"],
                int(pt["product_type_display_order"]),
                pt["product_type_active_flag"],
                int(sku["sku_display_order"]),
                sku["sku_active_flag"],
                sku["sku_description"],
                sku["size_nominal"],
                int(sku["length_feet"]),
                int(sku["popularity_score"]),
                str(sku["eagle_sticks_per_bundle"]),
                str(sku["eagle_bundles_per_truckload"]),
                int(sku["calculated_sticks_per_bundle"]),
                int(sku["actual_sticks_per_truckload"]),
                sku.get("notes", ""),
            ])

    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


def _assign_ids_from_snapshot(
    imported_product_types: dict[str, dict[str, Any]],
    current_snapshot: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Assign stable IDs to imported data by matching against the current snapshot.

    Existing product_type_names and (pt_name, sku_description, size_nominal) tuples
    reuse their existing IDs. New entries get the next sequential ID.
    """
    pt_name_to_id: dict[str, str] = {}
    sku_composite_to_id: dict[str, str] = {}
    existing_pt_ids: set[str] = set()
    existing_sku_ids: set[str] = set()

    for pt in current_snapshot.get("productTypes", []):
        pt_id = pt["productTypeId"]
        pt_name = pt.get("productType", "")
        pt_name_to_id[pt_name] = pt_id
        existing_pt_ids.add(pt_id)
        for sku_id, sku in pt.get("skus", {}).items():
            existing_sku_ids.add(sku_id)
            composite = f"{pt_name}||{sku.get('SKU', '')}||{sku.get('size', '')}"
            sku_composite_to_id[composite] = sku_id

    def _next_pt_id() -> str:
        nums = [
            int(pid[len("productTypeId_"):])
            for pid in existing_pt_ids
            if pid.startswith("productTypeId_") and pid[len("productTypeId_"):].isdigit()
        ]
        n = max(nums, default=0) + 1
        while f"productTypeId_{n}" in existing_pt_ids:
            n += 1
        new_id = f"productTypeId_{n}"
        existing_pt_ids.add(new_id)
        return new_id

    def _next_sku_id() -> str:
        nums = [
            int(sid[len("skuId_"):])
            for sid in existing_sku_ids
            if sid.startswith("skuId_") and sid[len("skuId_"):].isdigit()
        ]
        n = max(nums, default=0) + 1
        while f"skuId_{n}" in existing_sku_ids:
            n += 1
        new_id = f"skuId_{n}"
        existing_sku_ids.add(new_id)
        return new_id

    result: dict[str, dict[str, Any]] = {}

    for pt_name, pt_data in imported_product_types.items():
        pt_id = pt_name_to_id.get(pt_name)
        if pt_id is None:
            pt_id = _next_pt_id()
            pt_name_to_id[pt_name] = pt_id

        id_assigned_pt: dict[str, Any] = {
            "product_type_id": pt_id,
            "product_type_name": pt_data["product_type_name"],
            "product_type_display_order": pt_data["product_type_display_order"],
            "product_type_active_flag": pt_data["product_type_active_flag"],
            "skus": {},
        }

        for _sk, sku_data in pt_data["skus"].items():
            composite = f"{pt_name}||{sku_data['sku_description']}||{sku_data['size_nominal']}"
            sku_id = sku_composite_to_id.get(composite)
            if sku_id is None:
                sku_id = _next_sku_id()
                sku_composite_to_id[composite] = sku_id

            id_assigned_pt["skus"][sku_id] = {
                "sku_id": sku_id,
                "product_type_id": pt_id,
                **sku_data,
            }

        result[pt_id] = id_assigned_pt

    return result


def _serialize_legacy_snapshot(product_types: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Convert ID-assigned product_types back to the legacy JSON snapshot format."""
    snapshot_product_types: list[dict[str, Any]] = []

    active_pts = sorted(
        (pt for pt in product_types.values() if pt["product_type_active_flag"] == "Y"),
        key=lambda pt: (int(pt["product_type_display_order"]), pt["product_type_name"].lower()),
    )

    for pt in active_pts:
        active_skus = sorted(
            (sku for sku in pt["skus"].values() if sku["sku_active_flag"] == "Y"),
            key=lambda s: (int(s["sku_display_order"]), int(s["popularity_score"]), s["sku_description"].lower()),
        )
        if not active_skus:
            continue

        legacy_skus: dict[str, dict[str, Any]] = {}
        for sku in active_skus:
            actual = int(sku["actual_sticks_per_truckload"])
            calculated_bundle_size = int(sku["calculated_sticks_per_bundle"])
            legacy_skus[sku["sku_id"]] = {
                "skuId": sku["sku_id"],
                "productTypeId": sku["product_type_id"],
                "displayOrder": int(sku["sku_display_order"]),
                "popularityScore": int(sku["popularity_score"]),
                "productType": pt["product_type_name"],
                "SKU": sku["sku_description"],
                "eagleSticksPerBundle": str(sku["eagle_sticks_per_bundle"]),
                "eagleBundlesPerTruckLoad": str(sku["eagle_bundles_per_truckload"]),
                "eagleSticksPerTruckload": actual,
                "actualSticksPerTruckLoad": actual,
                "length": f"{int(sku['length_feet'])}'",
                "calculatedSticksPerBundle": calculated_bundle_size,
                "size": sku["size_nominal"],
            }

        snapshot_product_types.append({
            "productTypeId": pt["product_type_id"],
            "productType": pt["product_type_name"],
            "skus": legacy_skus,
        })

    return {
        "date": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        "productTypes": snapshot_product_types,
    }


def _write_active_snapshot(snapshot: dict[str, Any]) -> tuple[str, str]:
    version_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_text = json.dumps(snapshot, indent=4)
    json_hash = hashlib.sha256(json_text.encode("utf-8")).hexdigest()

    runtime.VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    versioned_path = runtime.VERSIONS_DIR / f"{version_id}_packing_data.json"
    versioned_path.write_text(json_text, encoding="utf-8")

    return version_id, json_hash


def _write_manifest(
    version_id: str,
    source_filename: str,
    change_reason: str,
    validation: ValidationResult,
    json_hash: str,
) -> Path:
    manifest_path = runtime.VERSIONS_DIR / f"{version_id}_manifest.json"
    manifest = {
        "version_id": version_id,
        "published_at": datetime.now().isoformat(),
        "source_filename": source_filename,
        "change_reason": change_reason,
        "counts": validation.counts,
        "sha256": json_hash,
        "warnings": [w.model_dump() for w in validation.warnings],
    }
    manifest_path.write_text(json.dumps(manifest, indent=4), encoding="utf-8")
    return manifest_path


def _activate_snapshot(snapshot: dict[str, Any]) -> None:
    runtime.SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = runtime.SNAPSHOT_PATH.with_suffix(".json.tmp")
    temp_path.write_text(json.dumps(snapshot, indent=4), encoding="utf-8")
    temp_path.replace(runtime.SNAPSHOT_PATH)
    runtime.reload_runtime_snapshot(runtime.SNAPSHOT_PATH)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/current")
async def get_current_data(
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Return the current active packing data in a browser-friendly format."""
    require_review(authorization)
    current_snapshot = load_snapshot(runtime.SNAPSHOT_PATH)
    product_types = _normalize_current_snapshot(current_snapshot)

    sorted_pts = sorted(
        product_types.values(),
        key=lambda pt: (int(pt["product_type_display_order"]), pt["product_type_name"].lower()),
    )
    for pt in sorted_pts:
        pt["skus"] = dict(
            sorted(
                pt["skus"].items(),
                key=lambda kv: (int(kv[1]["sku_display_order"]), kv[1]["sku_description"].lower()),
            )
        )

    return {
        "product_types": {pt["product_type_name"]: pt for pt in sorted_pts},
        "counts": {
            "product_types": len(sorted_pts),
            "skus": sum(len(pt["skus"]) for pt in sorted_pts),
        },
    }


@router.get("/versions")
async def list_versions(
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Return the last 20 version manifests, newest first."""
    require_admin(authorization)
    if not runtime.VERSIONS_DIR.exists():
        return {"versions": []}

    manifests = sorted(
        runtime.VERSIONS_DIR.glob("*_manifest.json"),
        key=lambda p: p.name,
        reverse=True,
    )[:20]

    versions = []
    for mp in manifests:
        try:
            versions.append(json.loads(mp.read_text(encoding="utf-8")))
        except Exception:
            pass

    return {"versions": versions}


@router.get("/current_excel")
async def download_current_excel(
    authorization: str | None = Header(default=None),
) -> StreamingResponse:
    require_review(authorization)
    current_snapshot = load_snapshot(runtime.SNAPSHOT_PATH)
    product_types = _normalize_current_snapshot(current_snapshot)
    workbook_bytes = _build_current_excel_workbook(product_types)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"packing_data_{timestamp}.xlsx"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(
        BytesIO(workbook_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


@router.post("/validate")
async def validate_workbook(
    file: UploadFile = File(...),
    authorization: str | None = Header(default=None),
) -> ValidationResult:
    require_review(authorization)
    _require_xlsx(file)
    return import_workbook(await file.read())


@router.post("/preview")
async def preview_workbook(
    file: UploadFile = File(...),
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    require_review(authorization)
    _require_xlsx(file)
    validation = import_workbook(await file.read())
    if not validation.is_valid:
        return _response_from_validation(validation, 400)

    current_snapshot = load_snapshot(runtime.SNAPSHOT_PATH)
    current_product_types = _normalize_current_snapshot(current_snapshot)
    diff = _build_diff_summary(current_product_types, validation.product_types)
    return {"validation": validation.model_dump(), "diff": diff}


@router.post("/publish")
async def publish_workbook(
    file: UploadFile = File(...),
    change_reason: str = Form(...),
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    require_admin(authorization)
    _require_xlsx(file)
    if not change_reason or not change_reason.strip():
        raise HTTPException(status_code=400, detail="change_reason is required")

    file_bytes = await file.read()
    validation = import_workbook(file_bytes)
    if not validation.is_valid:
        return _response_from_validation(validation, 400)

    current_snapshot = load_snapshot(runtime.SNAPSHOT_PATH)
    id_assigned = _assign_ids_from_snapshot(validation.product_types, current_snapshot)
    snapshot = _serialize_legacy_snapshot(id_assigned)
    version_id, json_hash = _write_active_snapshot(snapshot)
    _write_manifest(
        version_id=version_id,
        source_filename=file.filename or "upload.xlsx",
        change_reason=change_reason.strip(),
        validation=validation,
        json_hash=json_hash,
    )
    _activate_snapshot(snapshot)

    return {
        "ok": True,
        "version_id": version_id,
        "active_snapshot_path": str(runtime.SNAPSHOT_PATH),
        "counts": validation.counts,
    }
