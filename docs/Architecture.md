# Architecture

## 1. System Overview

H2O is a SKU packing data admin system with a branch-and-bound packing solver.

Data flow:

```
Excel → API → JSON snapshot → solver
```

Users work with Excel files through the Admin browser page. The API validates and previews uploaded Excel workbooks, then publishes to the active JSON snapshot used by the runtime and solver.

## 2. Components

### FastAPI app (`api/`)

Entry point: `H2O/api/app.py`

- Loads `H2O/.env` at startup (required)
- Calls `reload_runtime_snapshot()` to load SKUs into memory
- Mounts `/html` → `H2O/html/` (static files)
- Mounts `/api/data` → `H2O/api/data/` (snapshot files)
- Registers two routers

### Solver routes (`api/routes.py`)

Public endpoints (no auth):

| Endpoint | Description |
|---|---|
| `GET /skus` | Returns in-memory SKU list (active only) |
| `POST /orders` | Creates an order |
| `POST /pack` | Runs solver, returns packing result |
| `GET /orders/{id}` | Retrieves a stored order |

### Admin routes (`api/admin/routes.py`)

Excel workflow endpoints (HTTP Basic auth):

| Endpoint | Auth | Description |
|---|---|---|
| `GET /admin/data/current` | review + admin | Current data as JSON for browser display |
| `GET /admin/data/current_excel` | review + admin | Download active snapshot as `.xlsx` |
| `GET /admin/data/current_json` | review + admin | Download active snapshot as `load_packing_data.js` (legacy JS format) |
| `GET /admin/data/versions` | admin only | Last 20 version manifests |
| `POST /admin/data/validate` | admin only | Validate uploaded `.xlsx` |
| `POST /admin/data/preview` | admin only | Validate + diff vs. active snapshot |
| `POST /admin/data/publish` | admin only | Publish workbook to active snapshot |

### Excel importer (`data_import.py`)

`H2O/api/admin/data_import.py`:

- Reads `.xlsx` from a `SKUs` sheet (or two-sheet format with `Product Types` + `SKUs`)
- Validates required columns (14 columns)
- Validates field types and constraints per row
- Enforces cross-row rules (duplicate SKUs, inconsistent product type metadata)
- Issues a warning if all SKUs in a product type are inactive
- Produces normalized internal `product_types → skus` dict

### Runtime snapshot loader (`runtime.py`)

`H2O/api/runtime.py`:

- `SNAPSHOT_PATH` — active snapshot path
- `VERSIONS_DIR` — versioned backup directory
- `reload_runtime_snapshot()` — hot-reloads in-memory SKU state without restart
- Called at startup and after every publish
- Only active product types and active SKUs are loaded into memory

### HTML UI (`html/`)

Static files served by FastAPI:

- `H2O/html/index.html` — Packing order UI. Bootstrap 5.3.3. All logic in `app.js`.
- `H2O/html/app.js` — Packing UI logic: `ApiEngine` class manages bundle constraints and calls the solver API (`GET /skus`, `POST /orders`, `POST /pack`). `OrderTable` renders the order summary and packing slip. Correct Amount checkbox locks a SKU's bundle count.
- `H2O/html/login.html` + `H2O/html/js/login.js` — HTTP Basic auth. Token stored in sessionStorage. Redirects to admin or review page based on role.
- `H2O/html/admin_data.html` — Admin: validate / preview / publish + version history
- `H2O/html/review_data.html` — Review: view current data + download only
- `H2O/html/js/admin_data.js` — shared admin/review UI logic, role-gated by `data-role` attribute on `<body>`
- `H2O/html/css/admin_data.css` — shared styles

Several JS files remain on disk from the previous architecture (`config.js`, `api_adapter.js`, `select_skus.js`, `event_listener.js`, `order_table.js`, etc.) but are not loaded by any active page.

### Solver (unchanged)

- `H2O/api/solver/branch_and_bound.py` — Python port of original JS solver
- `H2O/html/branch_and_bound_engine.js` — Original JS solver (reference)

These are not modified by the Excel admin workflow.

## 3. Data Flow

### Publish flow

1. User downloads current Excel (`GET /admin/data/current_excel`)
2. User edits locally
3. User uploads updated workbook
4. API validates workbook (`POST /admin/data/validate`)
5. API previews workbook differences (`POST /admin/data/preview`)
6. Admin publishes with change reason (`POST /admin/data/publish`)
7. API assigns stable IDs from existing snapshot (new entries get sequential IDs)
8. API serializes to legacy JSON snapshot shape (all PT and SKUs including inactive)
9. API writes versioned backup + manifest file
10. API atomically replaces active snapshot
11. API hot-reloads runtime in memory (active items only)

### ID assignment

Product types are matched by `product_type_name`. SKUs are matched by `(product_type_name, sku_description, size_nominal)`. Existing entries reuse their IDs. New entries get the next sequential `productTypeId_N` / `skuId_N`.

### Inactive SKU/product type behaviour

Setting `active_flag = N` does not delete the item. All product types and SKUs are stored in the JSON with an `"active"` boolean. On runtime load, only active product types with at least one active SKU are loaded into memory and available for packing.

- If a product type is marked inactive, its SKU flags are not changed.
- If all SKUs in a product type are inactive, the product type is excluded from packing regardless of its own flag.
- The Excel export adds a "Notes" column on the Product Types sheet and a "Status" column on the SKUs sheet with auto-generated informational notes. These columns are not imported.

## 4. Auth Model

HTTP Basic authentication. Credentials from `H2O/.env`:

```
H2O_ADMIN_USER=...
H2O_ADMIN_PASS=...
H2O_REVIEW_USER=...
H2O_REVIEW_PASS=...
```

- Review: view current data + download
- Admin: view + download + validate + preview + publish + version history

## 5. Storage

```
H2O/api/data/
  packing_data.json             ← Active snapshot (legacy JSON shape, includes inactive items)
  versions/
    <YYYYMMDD_HHMMSS>_packing_data.json   ← Versioned snapshot
    <YYYYMMDD_HHMMSS>_manifest.json       ← Publish metadata
```

Manifest fields: `version_id`, `published_at`, `source_filename`, `change_reason`, `counts`, `sha256`, `warnings`.

## 6. Excel Schema

Sheet name: `SKUs`. 14 required columns:

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
| `eagle_sticks_per_bundle` | string | Eagle catalog reference — display only, not used in solver |
| `eagle_bundles_per_truckload` | string | Eagle catalog reference — display only, not used in solver |
| `calculated_sticks_per_bundle` | int ≥ 1 | Admin-selected bundle size used by solver |
| `actual_sticks_per_truckload` | int ≥ 1 | Independently measured total sticks per truck |
| `notes` | string | Optional |

IDs (`sku_id`, `product_type_id`) are internal — assigned automatically on publish. Users never see them in Excel.

Eagle reference strings can contain any format e.g. `"360"`, `"6 / 8"`, `"9 / 12 / 12 / 16"`. They are stored as-is and never parsed for calculation.

`calculated_sticks_per_bundle` is manually selected by the admin from the Eagle options. It is not derived from other fields.

`actual_sticks_per_truckload` is independently measured. It is not calculated from other fields.

## 7. UI Architecture

Static HTML + browser JavaScript calling the FastAPI API directly via `fetch()` / `FormData`.

Admin and review pages share the same JS and CSS. Role is determined by `data-role` attribute on `<body>` — controls which actions are available.

- **Admin** (`data-role="admin"`): validate / preview / publish / version history
- **Review** (`data-role="review"`): view current data + download only

## 8. Constraints

- Solver files are treated as immutable in this workflow
- Active JSON snapshot schema remains fixed for compatibility with the existing solver API
- Rollback is manual — copy a versioned snapshot file to `packing_data.json` and restart
