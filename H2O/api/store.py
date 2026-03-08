from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Iterable
from uuid import uuid4

from models import OrderLineIn, StoredOrder


class InMemoryOrderStore:
    def __init__(self) -> None:
        self._orders: Dict[str, StoredOrder] = {}

    def create_order(self, selected_skus: Iterable[str]) -> StoredOrder:
        order_id = str(uuid4())
        items = [OrderLineIn(sku_id=sku_id, quantity=1) for sku_id in selected_skus]
        order = StoredOrder(
            order_id=order_id,
            created_at=datetime.now(timezone.utc),
            status="created",
            items=items,
            packing_result=None,
        )
        self._orders[order_id] = order
        return order

    def get_order(self, order_id: str) -> StoredOrder | None:
        return self._orders.get(order_id)

    def set_packing_result(self, order_id: str, packing_result: dict) -> StoredOrder | None:
        order = self._orders.get(order_id)
        if order is None:
            return None

        updated = order.model_copy(deep=True)
        updated.status = "packed"
        updated.packing_result = packing_result
        self._orders[order_id] = updated
        return updated
