from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

from admin.routes import router as admin_router
from app_logging import setup_logging
from routes import router
from runtime import reload_runtime_snapshot

BASE_DIR = PROJECT_ROOT
HTML_DIR = BASE_DIR / "html"
API_DATA_DIR = BASE_DIR / "api" / "data"

setup_logging()
reload_runtime_snapshot()

app = FastAPI(title="H2O API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/html", StaticFiles(directory=str(HTML_DIR), html=True), name="html")
app.mount("/api/data", StaticFiles(directory=str(API_DATA_DIR)), name="api-data")
app.include_router(admin_router)
app.include_router(router)
