from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from ..auth import verify_admin_credentials, verify_admin_credentials_from_body
from ..data.admin_store import (
    get_current_dataset_payload,
    get_storage_status_payload,
    run_storage_retention,
    update_product_type_and_create_version,
    update_sku_and_create_version,
)
from ..data.audit import append_audit_event
from ..data.importer import import_from_csv_text, import_from_load_js_file
from ..data.versioning import get_current_version
from ..schemas.models import (
    AdminDatasetResponse,
    StorageRetentionRequest,
    StorageStatusResponse,
    UpdateProductTypeRequest,
    UpdateSkuRequest,
)

router = APIRouter()


@router.post("/import/load-js")
def import_from_load_js(
    source_path: str | None = None,
    version: str | None = None,
    admin_id: str = Depends(verify_admin_credentials),
) -> dict:
    try:
        result = import_from_load_js_file(source_path=source_path, version=version)
        append_audit_event(
            event_type="admin.import_load_js",
            payload={"admin_id": admin_id, "source_path": source_path, "version": version, "result": result},
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Import failed: {exc}") from exc

    return result


@router.post("/import/csv")
async def import_from_csv_upload(
    file: UploadFile = File(...),
    version: str | None = None,
    admin_id: str = Depends(verify_admin_credentials),
) -> FileResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="CSV file name is required")
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are accepted")

    try:
        file_bytes = await file.read()
        csv_text = file_bytes.decode("utf-8")
        result = import_from_csv_text(
            csv_text=csv_text,
            source_name=file.filename,
            version=version,
        )
        append_audit_event(
            event_type="admin.import_csv",
            payload={"admin_id": admin_id, "filename": file.filename, "version": version, "result": result},
        )
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"CSV import failed: {exc}") from exc

    review_csv_path = result["review_csv_path"]
    response = FileResponse(
        path=review_csv_path,
        filename=f"review_{result['metadata']['version']}.csv",
        media_type="text/csv",
    )
    response.headers["X-H2O-Version"] = result["metadata"]["version"]
    response.headers["X-H2O-Product-Type-Count"] = str(result["metadata"]["rows"]["product_types"])
    response.headers["X-H2O-Sku-Count"] = str(result["metadata"]["rows"]["skus"])
    return response


@router.get("/version/current")
def current_version(admin_id: str = Depends(verify_admin_credentials)) -> dict:
    try:
        version = get_current_version()
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    append_audit_event(event_type="admin.version_current", payload={"admin_id": admin_id, "version": version})
    return {"version": version}


@router.get("/dataset", response_model=AdminDatasetResponse)
def get_dataset(admin_id: str = Depends(verify_admin_credentials)) -> AdminDatasetResponse:
    try:
        dataset_payload = get_current_dataset_payload()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    append_audit_event(
        event_type="admin.get_dataset",
        payload={
            "admin_id": admin_id,
            "version": dataset_payload["version"],
            "product_type_count": len(dataset_payload["product_types"]),
            "sku_count": len(dataset_payload["skus"]),
        },
    )
    return AdminDatasetResponse(**dataset_payload)


@router.patch("/product-type/{product_type_id}")
def update_product_type(product_type_id: str, request: UpdateProductTypeRequest) -> dict:
    verify_admin_credentials_from_body(request.admin_id, request.admin_password)
    try:
        result = update_product_type_and_create_version(
            product_type_id=product_type_id,
            product_type_name=request.product_type,
            actor=request.admin_id,
        )
        append_audit_event(
            event_type="admin.update_product_type",
            payload={
                "admin_id": request.admin_id,
                "product_type_id": product_type_id,
                "product_type": request.product_type,
                "result": result,
            },
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/sku/{sku_id}")
def update_sku(sku_id: str, request: UpdateSkuRequest) -> dict:
    verify_admin_credentials_from_body(request.admin_id, request.admin_password)
    update_fields = request.model_dump(exclude_none=True)
    update_fields.pop("admin_password", None)

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    try:
        result = update_sku_and_create_version(
            sku_id=sku_id,
            update_fields=update_fields,
            actor=request.admin_id,
        )
        append_audit_event(
            event_type="admin.update_sku",
            payload={"admin_id": request.admin_id, "sku_id": sku_id, "fields": update_fields, "result": result},
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/storage/status", response_model=StorageStatusResponse)
def storage_status(admin_id: str = Depends(verify_admin_credentials)) -> StorageStatusResponse:
    try:
        payload = get_storage_status_payload()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    append_audit_event(
        event_type="admin.storage_status",
        payload={"admin_id": admin_id, "current_version": payload["current_version"]},
    )
    return StorageStatusResponse(**payload)


@router.post("/storage/retention")
def storage_retention(request: StorageRetentionRequest) -> dict:
    verify_admin_credentials_from_body(request.admin_id, request.admin_password)
    try:
        result = run_storage_retention(keep_latest=request.keep_latest, dry_run=request.dry_run)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    append_audit_event(
        event_type="admin.storage_retention",
        payload={
            "admin_id": request.admin_id,
            "keep_latest": request.keep_latest,
            "dry_run": request.dry_run,
            "result": result,
        },
    )
    return result
