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


class ProductTypeItem(BaseModel):
    product_type_id: str
    product_type: str


class SkuItem(BaseModel):
    sku_id: str
    product_type_id: str
    product_type: str
    sku: str
    size: str
    lingth: int
    active_flag: str
    display_order: int
    popularity_score: int
    calculated_sticks_per_bundle: int
    eagle_sticks_per_truckload: int
    eagle_bundles_per_truckload: int | None = None
    calculated_bundles_per_truckload: int


class AdminDatasetResponse(BaseModel):
    version: str
    product_types: list[ProductTypeItem]
    skus: list[SkuItem]


class UpdateProductTypeRequest(BaseModel):
    admin_id: str = Field(min_length=1)
    admin_password: str = Field(min_length=1)
    product_type: str = Field(min_length=1)


class UpdateSkuRequest(BaseModel):
    admin_id: str = Field(min_length=1)
    admin_password: str = Field(min_length=1)
    product_type_id: str | None = None
    sku: str | None = None
    size: str | None = None
    display_order: int | None = Field(default=None, ge=1)
    popularity_score: int | None = Field(default=None, ge=1)
    eagle_sticks_per_truckload: int | None = Field(default=None, ge=1)
    bundles_per_truckload: int | None = Field(default=None, ge=1)


class StorageRetentionRequest(BaseModel):
    admin_id: str = Field(min_length=1)
    admin_password: str = Field(min_length=1)
    keep_latest: int = Field(default=10, ge=1)
    dry_run: bool = False


class StorageStatusResponse(BaseModel):
    storage_engine: str
    sqlite_db_path: str
    sqlite_db_exists: bool
    current_version: str
    version_count: int
    versions: list[str]
    current_counts: dict[str, int]
