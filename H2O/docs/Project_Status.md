# Project Status

## What Works (26/26 tests passing)

- FastAPI server starts from `H2O/api/app.py`
- Static HTML served by the same FastAPI server
- HTTP Basic authentication enforced from `.env`
- Excel upload validate / preview / publish flow fully implemented (Admin only)
- Current Excel download endpoint implemented (Review + Admin)
- Current data download as `load_packing_data.js` (legacy JS format, `GET /admin/data/current_json`)
- Export → import round-trip validated (passes clean)
- Versioned snapshot backups written on every publish
- In-memory SKU runtime hot-reloaded after publish
- Admin browser UI: validate / preview / publish / version history (Bootstrap 5.3.3)
- Review browser UI: view current data + download only (Bootstrap 5.3.3)
- Current data browser view (`GET /admin/data/current`)
- Publish history (`GET /admin/data/versions`, admin only)
- Packing order UI fully operational — Bootstrap 5.3.3, all logic in `app.js`
- All solving goes through the Python API (no local JS solver used for computation)
- Correct Amount checkbox locks a SKU's bundle count, disables Increase + Decrease
- Inactive SKU/product type support — items are preserved in JSON, not deleted; excluded from solver

## Inactive SKU/Product Type Behaviour

- `sku_active_flag = N` or `product_type_active_flag = N` stores the item with `"active": false` in JSON
- Inactive items are excluded from the solver and `GET /skus`
- Items can be reactivated by setting the flag back to `Y` and publishing
- If a product type is marked inactive, its SKU flags are not changed
- Excel export shows auto-generated "Notes" column (Product Types sheet) and "Status" column (SKUs sheet) — informational only, not imported

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

## Environment

- Python 3.11, FastAPI, uvicorn
- Single-port server (port 8001 local / 8080 production)
- HTTP Basic auth from `.env`
- 26 pytest tests, all passing
- Local solver harness: 12/12
- Historical solver harness: 26/26
