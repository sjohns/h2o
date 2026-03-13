from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import CreateOrderRequest, OrderResponse, PackOrderRequest
from .service import OrderService

BASE_DIR = Path(__file__).resolve().parents[1]
service = OrderService(BASE_DIR / "html" / "load_packing_data.js")

app = FastAPI(title="H2O Packing API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/skus")
def list_skus() -> dict[str, object]:
    return {"skus": list(service.list_skus().values())}


@app.post("/orders", response_model=OrderResponse)
def create_order(payload: CreateOrderRequest) -> OrderResponse:
    try:
        return service.create_order(payload.skuIds)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/pack")
def pack_order(payload: PackOrderRequest) -> dict[str, object]:
    try:
        result = service.pack_order(payload.orderId)
        return {"orderId": payload.orderId, "result": result}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Order not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str) -> OrderResponse:
    try:
        return service.get_order(order_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Order not found") from exc
