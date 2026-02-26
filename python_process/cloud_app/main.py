from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import PROJECT_ROOT
from .api.admin import router as admin_router
from .api.client import router as client_router


app = FastAPI(title="H2O Cloud API", version="0.1.0")
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(client_router, prefix="/api", tags=["client"])

ADMIN_UI_FILE_PATH = PROJECT_ROOT / "python_process" / "cloud_app" / "ui" / "admin.html"
CLIENT_UI_FILE_PATH = PROJECT_ROOT / "python_process" / "cloud_app" / "ui_client" / "index.html"
CLIENT_UI_ASSETS_DIRECTORY = PROJECT_ROOT / "python_process" / "cloud_app" / "ui_client"

app.mount("/client-ui-assets", StaticFiles(directory=str(CLIENT_UI_ASSETS_DIRECTORY)), name="client-ui-assets")


@app.get("/health")
def health() -> dict:
    payload = {"status": "ok"}
    return payload


@app.get("/admin-ui")
def admin_ui() -> FileResponse:
    return FileResponse(path=ADMIN_UI_FILE_PATH)


@app.get("/client-ui")
def client_ui() -> FileResponse:
    return FileResponse(path=CLIENT_UI_FILE_PATH)
