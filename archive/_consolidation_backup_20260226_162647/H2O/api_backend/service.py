from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict
from uuid import uuid4

from .data_loader import flatten_skus, load_packing_data_from_js
from .models import OrderResponse, PackingResult, SKU
from api.solver.solver_service import compute_packing_solution


class OrderService:
    def __init__(self, js_data_path: Path) -> None:
        self._packing_data = load_packing_data_from_js(js_data_path)
        self._all_skus: Dict[str, SKU] = flatten_skus(self._packing_data)
        self._orders: Dict[str, OrderResponse] = {}

    def list_skus(self) -> Dict[str, SKU]:
        return self._all_skus

    def create_order(self, sku_ids: list[str]) -> OrderResponse:
        missing = [sku_id for sku_id in sku_ids if sku_id not in self._all_skus]
        if missing:
            raise ValueError(f"Unknown skuIds: {missing}")

        order_id = str(uuid4())
        order = OrderResponse(
            orderId=order_id,
            skuIds=sku_ids,
            createdAt=datetime.now(timezone.utc),
            status="created",
            result=None,
        )
        self._orders[order_id] = order
        return order

    def pack_order(self, order_id: str) -> PackingResult:
        if order_id not in self._orders:
            raise KeyError(order_id)

        order = self._orders[order_id]
        selected_skus = {sku_id: self._all_skus[sku_id].model_copy(deep=True) for sku_id in order.skuIds}
        result = compute_packing_solution(selected_skus)

        updated = order.model_copy(deep=True)
        updated.status = "packed"
        updated.result = result
        self._orders[order_id] = updated

        return result

    def get_order(self, order_id: str) -> OrderResponse:
        if order_id not in self._orders:
            raise KeyError(order_id)
        return self._orders[order_id]
