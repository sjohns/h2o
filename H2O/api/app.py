from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .data import flatten_skus, load_snapshot
from .logging import setup_logging
from .models import SKU
from .routes import initialize_runtime, router

BASE_DIR = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = BASE_DIR / "api" / "data" / "packing_data.json"

setup_logging()

raw_snapshot = load_snapshot(SNAPSHOT_PATH)
raw_skus = flatten_skus(raw_snapshot)
sku_dict = {sku["skuId"]: SKU(**sku).model_dump() for sku in raw_skus}
all_skus = [sku_dict[sku_id] for sku_id in sku_dict]

initialize_runtime(all_skus, sku_dict)
logger.info("Loaded SKU snapshot: {} SKUs", len(sku_dict))

app = FastAPI(title="H2O API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
