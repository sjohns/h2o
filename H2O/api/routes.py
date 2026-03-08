from __future__ import annotations

import threading
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from loguru import logger

from .cache import configure_solver_cache, solve_cached
from .models import (
    CreateOrderResponse,
    OrderRequest,
    PackRequest,
    PackResponse,
    PackingResult,
    SolutionItem,
    StoredOrder,
)
from .store import InMemoryOrderStore
from .solver import solve

all_skus: list[dict[str, Any]] = []
all_skus_by_id: dict[str, dict[str, Any]] = {}
valid_sku_ids: set[str] = set()
order_store = InMemoryOrderStore()
_state_lock = threading.RLock()

router = APIRouter()


def initialize_runtime(loaded_skus: list[dict[str, Any]], loaded_sku_map: dict[str, dict[str, Any]]) -> None:
    global all_skus, all_skus_by_id, valid_sku_ids
    with _state_lock:
        all_skus = loaded_skus
        all_skus_by_id = loaded_sku_map
        valid_sku_ids = set(loaded_sku_map.keys())
    configure_solver_cache(_solver_function)


def _solver_function(ids: list[str]) -> dict:
    solver_order = {"items": [{"sku_id": sku_id, "quantity": 1} for sku_id in ids]}
    return solve(solver_order, all_skus_by_id)


def _solver_function_constrained(ids: list[str], bundle_constraints: dict) -> dict:
    solver_order = {"items": [{"sku_id": sku_id, "quantity": 1} for sku_id in ids]}
    raw_constraints = {k: {"min_bundles": v.min_bundles, "max_bundles": v.max_bundles} for k, v in bundle_constraints.items()}
    return solve(solver_order, all_skus_by_id, raw_constraints)


@router.get("/health")
async def health(request: Request) -> dict:
    logger.info("API {} {}", request.method, request.url.path)
    return {"status": "ok"}


@router.get("/skus")
async def get_skus(request: Request) -> dict:
    logger.info("API {} {}", request.method, request.url.path)
    return {"count": len(all_skus), "skus": all_skus}


@router.post("/orders", response_model=CreateOrderResponse)
async def create_order(request: Request, req: OrderRequest) -> CreateOrderResponse:
    logger.info("API {} {}", request.method, request.url.path)

    if len(req.selectedSkus) > 100:
        raise HTTPException(status_code=400, detail="Too many SKUs")

    unknown = [sku_id for sku_id in req.selectedSkus if sku_id not in valid_sku_ids]
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown sku_id values: {unknown}")

    # preserve first-seen ordering and remove duplicates
    deduped = list(dict.fromkeys(req.selectedSkus))
    order = order_store.create_order(deduped)
    return CreateOrderResponse(order_id=order.order_id)


@router.post("/pack", response_model=PackResponse)
async def pack_order(request: Request, req: PackRequest) -> PackResponse:
    logger.info("API {} {}", request.method, request.url.path)

    order = order_store.get_order(req.orderId)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    selected_skus = [item.sku_id for item in order.items]
    if len(selected_skus) > 100:
        raise HTTPException(status_code=400, detail="Too many SKUs")

    logger.info("Solver request: {} SKUs", len(selected_skus))

    if req.bundleConstraints:
        order_sku_ids = set(selected_skus)
        unknown = [k for k in req.bundleConstraints if k not in order_sku_ids]
        if unknown:
            raise HTTPException(status_code=400, detail=f"bundleConstraints contains SKU IDs not in order: {unknown}")

    try:
        if req.bundleConstraints:
            solver_result = _solver_function_constrained(selected_skus, req.bundleConstraints)
        else:
            key = tuple(sorted(selected_skus))
            solver_result = solve_cached(key)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    packing_result = PackingResult(
        skus=solver_result["skus"],
        solution=[SolutionItem(**item) for item in solver_result["solution"]],
        lcmValue=solver_result["lcmValue"],
        minTruckSize=solver_result["minTruckSize"],
        maxTruckSize=solver_result["maxTruckSize"],
        totalSize=solver_result["totalSize"],
        totalSticks=solver_result["totalSticks"],
        differenceSum=solver_result["differenceSum"],
    )

    updated = order_store.set_packing_result(req.orderId, packing_result)
    if updated is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return PackResponse(order_id=updated.order_id, packing_result=packing_result)


@router.get("/orders/{order_id}", response_model=StoredOrder)
async def get_order(request: Request, order_id: str) -> StoredOrder:
    logger.info("API {} {}", request.method, request.url.path)

    order = order_store.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
