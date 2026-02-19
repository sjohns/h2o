from fastapi import APIRouter, HTTPException

from python_process.cloud_app.data.importer import import_from_load_js_file
from python_process.cloud_app.data.versioning import get_current_version

router = APIRouter()


@router.post("/import/load-js")
def import_from_load_js(source_path: str | None = None, version: str | None = None) -> dict:
    try:
        result = import_from_load_js_file(source_path=source_path, version=version)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Import failed: {exc}") from exc

    return result


@router.get("/version/current")
def current_version() -> dict:
    try:
        version = get_current_version()
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {"version": version}
