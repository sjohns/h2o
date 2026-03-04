# Project Status

## What Works (18/18 tests passing)

- FastAPI server starts from `H2O/api/app.py`
- Static HTML served by the same FastAPI server
- HTTP Basic authentication enforced from `.env`
- Excel upload validate / preview / publish flow fully implemented
- Current Excel download endpoint implemented
- Export → import round-trip validated (passes clean)
- Versioned snapshot backups written on every publish
- In-memory SKU runtime hot-reloaded after publish
- Admin and Review browser UIs implemented
- Current data browser view (`GET /admin/data/current`)
- Publish history (`GET /admin/data/versions`, admin only)
- Solver and packing UI unchanged and fully functional

## Excel Column Schema (14 columns, sheet name: SKUs)

| Column | Type | Notes |
|---|---|---|
| `product_type_name` | string | |
| `product_type_display_order` | int ≥ 1 | |
| `product_type_active_flag` | Y / N | |
| `sku_display_order` | int ≥ 1 | |
| `sku_active_flag` | Y / N | |
| `sku_description` | string | |
| `size_nominal` | string | |
| `length_feet` | int ≥ 1 | |
| `popularity_score` | int ≥ 1 | |
| `eagle_sticks_per_bundle` | string | Eagle catalog reference, e.g. "360" or "6 / 8" |
| `eagle_bundles_per_truckload` | string | Eagle catalog reference, e.g. "36" or "6 / 6" |
| `calculated_sticks_per_bundle` | int ≥ 1 | Admin-selected bundle size for solver |
| `actual_sticks_per_truckload` | int ≥ 1 | Independently measured, not calculated |
| `notes` | string | Optional |

## What Was Not Changed

- Solver (`H2O/api/solver/branch_and_bound.py`)
- Packing UI (`H2O/html/index.html`)
- Active JSON snapshot schema

## Environment

- Python 3.11, FastAPI, uvicorn
- Single-port server (port 8001)
- HTTP Basic auth from `.env`
- 18 pytest tests, all passing
