# h2o

## Overview

H2O is an Excel-driven SKU packing data admin system with a branch-and-bound packing solver.

The current implementation provides:

- a FastAPI server
- Excel upload validation, preview, and publish
- versioned snapshot backups
- inactive SKU/product type support (inactive items are preserved, not deleted)
- Admin and Review access via HTTP Basic credentials from `.env`
- static browser UIs served by the same FastAPI server

## Architecture

The implemented data flow is:

1. User downloads the current Excel dataset from `GET /admin/data/current_excel`
2. User edits the workbook locally
3. User uploads the workbook through the Admin UI
4. Backend validates the workbook
5. Backend previews differences against the current active dataset
6. Admin publishes with a change reason
7. Publish writes the JSON snapshot used by the solver API

Active snapshot:

- `H2O/api/data/packing_data.json`

Versioned backups:

- `H2O/api/data/versions/<version_id>_packing_data.json`
- `H2O/api/data/versions/<version_id>_manifest.json`

The runtime API reloads the snapshot in memory after publish.

## Inactive SKU Behaviour

Setting `sku_active_flag = N` or `product_type_active_flag = N` does not delete the SKU or product type. They are stored in the JSON with `"active": false` and excluded from the solver. They can be reactivated at any time by setting the flag back to `Y` and publishing.

- If all SKUs in a product type are inactive, the product type is also excluded from packing. A warning is shown during validate/preview.
- If a product type is marked inactive, its individual SKU flags are not changed.
- The Excel export shows auto-generated notes: a "Notes" column on the Product Types sheet and a "Status" column on the SKUs sheet indicating inactive status.

## Roles

Two roles are implemented.

### Review

Review users can:

- view current published data in the browser
- download current Excel

Review users cannot validate, preview, or publish.

### Admin

Admin users can:

- view current published data in the browser
- download current Excel
- validate uploaded Excel
- preview uploaded Excel against the active dataset
- publish a validated workbook
- view publish history

## Running Locally

Start the FastAPI server from the `H2O` directory:

```bash
cd H2O
python -m uvicorn api.app:app --host 127.0.0.1 --port 8001 --reload
```

Production:

```bash
cd H2O
python -m uvicorn api.app:app --host 0.0.0.0 --port 8080
```

## Auth Setup

Credentials are loaded from `H2O/.env`. Example: `H2O/api/.env.example`.

Required variables:

- `H2O_ADMIN_USER`
- `H2O_ADMIN_PASS`
- `H2O_REVIEW_USER`
- `H2O_REVIEW_PASS`

Authentication is HTTP Basic.

## UI URLs

When running locally on port `8001`:

- Packing UI: `http://127.0.0.1:8001/html/index.html`
- Admin UI: `http://127.0.0.1:8001/html/admin_data.html`
- Review UI: `http://127.0.0.1:8001/html/review_data.html`

Production:

- `https://h2o-api-97ivf.ondigitalocean.app/html/index.html`
- `https://h2o-api-97ivf.ondigitalocean.app/html/admin_data.html`
- `https://h2o-api-97ivf.ondigitalocean.app/html/review_data.html`

## API Endpoints

Solver endpoints (no auth):

- `GET /skus` — returns in-memory SKU list (active only)
- `POST /orders` — creates an order
- `POST /pack` — runs solver, returns packing result
- `GET /orders/{id}` — retrieves a stored order

Excel workflow endpoints:

- `GET /admin/data/current` — current data as JSON for browser display (review+admin)
- `GET /admin/data/current_excel` — download active snapshot as `.xlsx` (review+admin)
- `GET /admin/data/current_json` — download active snapshot as `load_packing_data.js` (review+admin)
- `GET /admin/data/versions` — last 20 version manifests (admin only)
- `POST /admin/data/validate` — validate uploaded `.xlsx` (admin only)
- `POST /admin/data/preview` — validate + diff vs. active dataset (admin only)
- `POST /admin/data/publish` — publish workbook to active snapshot (admin only)

## Publish Workflow

1. Download current Excel
2. Upload updated Excel workbook
3. Validate workbook
4. Preview workbook differences
5. Publish from Admin UI with required change reason
6. Versioned backup files written
7. Active snapshot atomically replaced
8. Runtime snapshot hot-reloaded in memory

## Data Storage and Versions

- Active: `H2O/api/data/packing_data.json`
- Versioned: `H2O/api/data/versions/<version_id>_packing_data.json` + `_manifest.json`

Manifest includes: `version_id`, `published_at`, `source_filename`, `change_reason`, `counts`, `sha256`, warnings.

## Constraints

- Rollback is manual — copy the desired versioned snapshot to `H2O/api/data/packing_data.json` and restart
- Admin and Review auth use shared HTTP Basic credentials from `.env`

## Testing

```bash
cd H2O
pytest -q api/tests
python3 api/tests/harness/run_harness.py
python3 api/tests/harness/run_harness.py --historical
```

All 26 pytest tests pass. Local harness 12/12. Historical harness 26/26.
