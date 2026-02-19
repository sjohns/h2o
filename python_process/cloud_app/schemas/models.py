from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    selected_sku_ids: list[str] = Field(min_length=1, max_length=8)
    truck_fill_ratio: float = Field(default=1.0, ge=0.1, le=1.0)
    fixed_bundles: dict[str, int] = Field(default_factory=dict)
    min_bundles: dict[str, int] = Field(default_factory=dict)
    max_bundles: dict[str, int] = Field(default_factory=dict)


class SolutionItem(BaseModel):
    sku_id: str
    sku: str
    number_of_bundles: int
    sticks_per_bundle: int
    total_sticks: int


class CalculateResponse(BaseModel):
    version: str
    lcm: int
    total_truck_size: int
    total_sticks: int
    solution: list[SolutionItem]
