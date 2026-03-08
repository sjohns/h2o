from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SKU(BaseModel):
    model_config = ConfigDict(extra="allow")

    skuId: str
    calculatedBundleSize: int = Field(gt=0)
    calculatedBundlesPerTruckload: int = Field(gt=0)
    popularityScore: int = Field(ge=1)

    @model_validator(mode="before")
    @classmethod
    def _coerce_calculated_fields(cls, value: Any) -> Any:
        """Bridge legacy JSON snapshot field names to the canonical model fields.

        The legacy snapshot format uses:
          - calculatedSticksPerBundle  → mapped to calculatedBundleSize
          - actualSticksPerTruckLoad (preferred) or eagleSticksPerTruckload (fallback)
            → used with calculatedSticksPerBundle to derive calculatedBundlesPerTruckload

        These fields are populated by the solver before the SKU is serialised into
        a PackingResult, but the raw snapshot stores only the legacy names.
        """
        if not isinstance(value, dict):
            return value

        data = dict(value)
        sticks = data.get("calculatedSticksPerBundle")
        truck_sticks = data.get("actualSticksPerTruckLoad", data.get("eagleSticksPerTruckload"))

        if "calculatedBundleSize" not in data and sticks is not None:
            data["calculatedBundleSize"] = int(sticks)

        if "calculatedBundlesPerTruckload" not in data and sticks and truck_sticks is not None:
            data["calculatedBundlesPerTruckload"] = int(int(truck_sticks) // int(sticks))

        return data


class OrderLineIn(BaseModel):
    sku_id: str
    quantity: int = Field(gt=0)


class OrderRequest(BaseModel):
    selectedSkus: List[str] = Field(min_length=1)

    @model_validator(mode="before")
    @classmethod
    def _coerce_legacy_payload(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value

        if "selectedSkus" in value:
            return value

        items = value.get("items")
        if isinstance(items, list):
            selected = []
            for item in items:
                if not isinstance(item, dict) or "sku_id" not in item:
                    continue
                quantity = int(item.get("quantity", 1))
                if quantity < 1:
                    quantity = 1
                selected.extend([item["sku_id"]] * quantity)
            return {"selectedSkus": selected}

        return value


class CreateOrderResponse(BaseModel):
    order_id: str


class BundleConstraintItem(BaseModel):
    min_bundles: int = Field(ge=0)
    max_bundles: int = Field(ge=1)

    @model_validator(mode="after")
    def _min_le_max(self) -> BundleConstraintItem:
        if self.min_bundles > self.max_bundles:
            raise ValueError(f"min_bundles ({self.min_bundles}) must be <= max_bundles ({self.max_bundles})")
        return self


class PackRequest(BaseModel):
    orderId: str = Field(min_length=1)
    bundleConstraints: dict[str, BundleConstraintItem] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def _coerce_legacy_payload(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        if "orderId" in value:
            return value
        if "order_id" in value:
            return {"orderId": value["order_id"], "bundleConstraints": value.get("bundleConstraints", {})}
        return value


class SolutionItem(BaseModel):
    skuId: str
    numberOfBundles: int
    totalSticks: Optional[int] = None


class PackingResult(BaseModel):
    skus: Dict[str, Dict[str, Any]]
    solution: List[SolutionItem]
    lcmValue: int
    minTruckSize: int
    maxTruckSize: int
    totalSize: int
    totalSticks: int
    differenceSum: int


class PackResponse(BaseModel):
    order_id: str
    packing_result: PackingResult


class StoredOrder(BaseModel):
    order_id: str
    created_at: datetime
    status: str
    items: List[OrderLineIn]
    packing_result: Optional[PackingResult] = None
