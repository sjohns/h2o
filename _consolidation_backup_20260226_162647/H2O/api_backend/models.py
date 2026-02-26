from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class SKU(BaseModel):
    skuId: str
    productTypeId: str
    displayOrder: int
    popularityScore: int
    productType: str
    SKU: str
    eagleSticksPerBundle: str
    eagleBundlesPerTruckLoad: str
    eagleSticksPerTruckload: int
    length: str
    calculatedSticksPerBundle: int
    size: str
    calculatedBundlesPerTruckload: Optional[int] = None
    calculatedBundleSize: Optional[int] = None


class PackingResult(BaseModel):
    lcmValue: int
    minTruckSize: int
    maxTruckSize: int
    totalSize: int
    totalSticks: int
    differenceSum: Optional[int] = None
    solution: List[Dict[str, int]]
    skus: Dict[str, SKU]


class CreateOrderRequest(BaseModel):
    skuIds: List[str] = Field(min_length=1, max_length=5)


class OrderResponse(BaseModel):
    orderId: str
    skuIds: List[str]
    createdAt: datetime
    status: Literal["created", "packed"]
    result: Optional[PackingResult] = None


class PackOrderRequest(BaseModel):
    orderId: str
