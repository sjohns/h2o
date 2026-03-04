from __future__ import annotations

import asyncio
import base64
from io import BytesIO
import json

import httpx
import pytest
from openpyxl import Workbook

from api.admin.data_import import REQUIRED_COLUMNS
from api.app import app
from api import runtime

ADMIN_AUTH_HEADER = {
    "Authorization": "Basic " + base64.b64encode(b"admin_user:admin_pass").decode("ascii")
}
REVIEW_AUTH_HEADER = {
    "Authorization": "Basic " + base64.b64encode(b"review_user:review_pass").decode("ascii")
}


async def _request(method: str, path: str, **kwargs):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.request(method, path, **kwargs)


def request(method: str, path: str, **kwargs):
    return asyncio.run(_request(method, path, **kwargs))


def _build_workbook_bytes(rows: list[list[object]]) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "SKUs"
    sheet.append(REQUIRED_COLUMNS)
    for row in rows:
        sheet.append(row)
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


# One complete valid row: 14 columns matching REQUIRED_COLUMNS
# product_type_name, product_type_display_order, product_type_active_flag,
# sku_display_order, sku_active_flag, sku_description, size_nominal,
# length_feet, popularity_score, eagle_sticks_per_bundle,
# eagle_bundles_per_truckload, calculated_sticks_per_bundle,
# actual_sticks_per_truckload, notes
VALID_ROW = [
    "Schedule 40",   # product_type_name
    1,               # product_type_display_order
    "Y",             # product_type_active_flag
    1,               # sku_display_order
    "Y",             # sku_active_flag
    '1/2" PVC PIPE SCH 40 - BELL ENDED',  # sku_description
    '1/2"',          # size_nominal
    20,              # length_feet
    5,               # popularity_score
    "360",           # eagle_sticks_per_bundle (string — Eagle catalog reference)
    "36",            # eagle_bundles_per_truckload (string — Eagle catalog reference)
    360,             # calculated_sticks_per_bundle (admin-selected value for solver)
    12960,           # actual_sticks_per_truckload (independently measured)
    "",              # notes
]


@pytest.fixture
def isolated_snapshot_paths(tmp_path, monkeypatch):
    original_snapshot_path = runtime.SNAPSHOT_PATH
    original_versions_dir = runtime.VERSIONS_DIR

    temp_snapshot_path = tmp_path / "packing_data.json"
    temp_snapshot_path.write_text(original_snapshot_path.read_text(encoding="utf-8"), encoding="utf-8")
    temp_versions_dir = tmp_path / "versions"

    monkeypatch.setattr(runtime, "SNAPSHOT_PATH", temp_snapshot_path)
    monkeypatch.setattr(runtime, "VERSIONS_DIR", temp_versions_dir)
    runtime.reload_runtime_snapshot(temp_snapshot_path)

    try:
        yield {"snapshot_path": temp_snapshot_path, "versions_dir": temp_versions_dir}
    finally:
        runtime.reload_runtime_snapshot(original_snapshot_path)


def test_admin_validate_success():
    workbook = _build_workbook_bytes([VALID_ROW])
    response = request(
        "POST",
        "/admin/data/validate",
        files={"file": ("data.xlsx", workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=REVIEW_AUTH_HEADER,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["is_valid"] is True
    assert payload["counts"] == {"rows": 1, "product_types": 1, "skus": 1}


def test_admin_validate_mixed_bundle_string():
    """eagle_sticks_per_bundle accepts non-integer strings like '6 / 8'."""
    row = VALID_ROW[:]
    row[9] = "6 / 8"   # eagle_sticks_per_bundle column
    workbook = _build_workbook_bytes([row])
    response = request(
        "POST",
        "/admin/data/validate",
        files={"file": ("data.xlsx", workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=REVIEW_AUTH_HEADER,
    )
    assert response.status_code == 200
    assert response.json()["is_valid"] is True


def test_admin_validate_failure_duplicate_sku():
    row2 = VALID_ROW[:]
    row2[3] = 2  # different sku_display_order — same desc+size = duplicate
    workbook = _build_workbook_bytes([VALID_ROW, row2])
    response = request(
        "POST",
        "/admin/data/validate",
        files={"file": ("data.xlsx", workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=REVIEW_AUTH_HEADER,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["is_valid"] is False
    assert any("Duplicate" in e["message"] for e in payload["errors"])


def test_admin_preview_valid_returns_diff():
    row_existing = [
        "SCH 40 PVC NSF (Pools & Irrigation)",
        1, "Y", 1, "N",
        '1/2" PVC PIPE SCH 40 - BELL ENDED', '1/2"',
        20, 5, "360", "36", 360, 12960, "",
    ]
    row_new = [
        "SCH 40 PVC NSF (Pools & Irrigation)",
        1, "Y", 999, "Y",
        "TEST SKU", '9"',
        20, 1, "10", "1", 10, 200, "new sku",
    ]
    workbook = _build_workbook_bytes([row_existing, row_new])
    response = request(
        "POST",
        "/admin/data/preview",
        files={"file": ("data.xlsx", workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=REVIEW_AUTH_HEADER,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["validation"]["is_valid"] is True
    diff = payload["diff"]
    assert "counts" in diff
    assert "added_skus" in diff
    assert "removed_skus" in diff
    assert "changed_skus" in diff
    assert any("TEST SKU" in s for s in diff["added_skus"])


def test_admin_preview_invalid_returns_400():
    row2 = VALID_ROW[:]
    row2[3] = 2
    workbook = _build_workbook_bytes([VALID_ROW, row2])
    response = request(
        "POST",
        "/admin/data/preview",
        files={"file": ("data.xlsx", workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=REVIEW_AUTH_HEADER,
    )
    assert response.status_code == 400
    assert response.json()["is_valid"] is False


def test_admin_publish_valid_writes_versioned_files_and_reloads(isolated_snapshot_paths):
    rows = [
        [
            "Published Type", 1, "Y", 1, "Y",
            "PUBLISHED SKU 1", '1/2"', 20, 2, "120", "10", 120, 1200, "",
        ],
        [
            "Published Type", 1, "Y", 2, "Y",
            "PUBLISHED SKU 2", '3/4"', 20, 3, "90", "8", 90, 720, "",
        ],
    ]
    workbook = _build_workbook_bytes(rows)
    response = request(
        "POST",
        "/admin/data/publish",
        files={"file": ("data.xlsx", workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        data={"change_reason": "publish test dataset"},
        headers=ADMIN_AUTH_HEADER,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["ok"] is True
    assert payload["counts"] == {"rows": 2, "product_types": 1, "skus": 2}

    version_id = payload["version_id"]
    versioned_snapshot = isolated_snapshot_paths["versions_dir"] / f"{version_id}_packing_data.json"
    manifest_path = isolated_snapshot_paths["versions_dir"] / f"{version_id}_manifest.json"
    assert versioned_snapshot.exists()
    assert manifest_path.exists()

    active = json.loads(isolated_snapshot_paths["snapshot_path"].read_text(encoding="utf-8"))
    assert active["productTypes"][0]["productType"] == "Published Type"
    sku = list(active["productTypes"][0]["skus"].values())[0]
    assert sku["SKU"] == "PUBLISHED SKU 1"
    assert sku["eagleSticksPerBundle"] == "120"
    assert sku["actualSticksPerTruckLoad"] == 1200
    assert sku["calculatedSticksPerBundle"] == 120   # 1200 // 10

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["change_reason"] == "publish test dataset"

    skus_response = request("GET", "/skus")
    assert skus_response.status_code == 200
    assert skus_response.json()["count"] == 2


def test_admin_publish_round_trip(isolated_snapshot_paths):
    """Download current Excel, re-upload it, validate — must pass clean."""
    # Download
    dl = request("GET", "/admin/data/current_excel", headers=REVIEW_AUTH_HEADER)
    assert dl.status_code == 200

    # Re-upload for validation
    response = request(
        "POST",
        "/admin/data/validate",
        files={"file": ("roundtrip.xlsx", dl.content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=REVIEW_AUTH_HEADER,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["is_valid"] is True, f"Round-trip validation failed: {payload['errors']}"
