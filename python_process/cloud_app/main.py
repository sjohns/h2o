from fastapi import FastAPI

from python_process.cloud_app.api.admin import router as admin_router
from python_process.cloud_app.api.client import router as client_router


app = FastAPI(title="H2O Cloud API", version="0.1.0")
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(client_router, prefix="/api", tags=["client"])


@app.get("/health")
def health() -> dict:
    payload = {"status": "ok"}
    return payload
