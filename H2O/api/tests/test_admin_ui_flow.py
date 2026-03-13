from __future__ import annotations

import asyncio
import base64
import json
from io import BytesIO

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


def _build_workbook_bytes() -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "SKUs"
    sheet.append(REQUIRED_COLUMNS)
    # product_type_name, product_type_display_order, product_type_active_flag,
    # sku_display_order, sku_active_flag, sku_description, size_nominal,
    # length_feet, popularity_score, eagle_sticks_per_bundle (str),
    # eagle_bundles_per_truckload, actual_sticks_per_truckload, notes
    sheet.append([
        "UI Flow Type", 1, "Y",
        1, "Y",
        "UI FLOW SKU 1", '1/2"',
        20, 2,
        "120",   # eagle_sticks_per_bundle (Eagle reference string)
        "10",    # eagle_bundles_per_truckload (Eagle reference string)
        120,     # calculated_sticks_per_bundle (admin-selected)
        1200, "",
    ])
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


@pytest.fixture
def isolated_snapshot_paths(tmp_path, monkeypatch):
    original_snapshot_path = runtime.SNAPSHOT_PATH

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


def test_admin_ui_http_flow(isolated_snapshot_paths):
    workbook = _build_workbook_bytes()

    validate_response = request(
        "POST",
        "/admin/data/validate",
        files={"file": ("ui_flow.xlsx", workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=ADMIN_AUTH_HEADER,
    )
    assert validate_response.status_code == 200
    assert validate_response.json()["is_valid"] is True

    preview_response = request(
        "POST",
        "/admin/data/preview",
        files={"file": ("ui_flow.xlsx", workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers=ADMIN_AUTH_HEADER,
    )
    assert preview_response.status_code == 200
    assert "diff" in preview_response.json()

    publish_response = request(
        "POST",
        "/admin/data/publish",
        files={"file": ("ui_flow.xlsx", workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        data={"change_reason": "ui flow test publish"},
        headers=ADMIN_AUTH_HEADER,
    )
    assert publish_response.status_code == 200
    payload = publish_response.json()
    assert payload["ok"] is True
    assert payload["version_id"]

    manifest = isolated_snapshot_paths["versions_dir"] / f"{payload['version_id']}_manifest.json"
    assert manifest.exists()
    manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert manifest_payload["change_reason"] == "ui flow test publish"
