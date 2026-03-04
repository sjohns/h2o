# h2o

## Overview

H2O is an Excel-driven SKU packing data admin system.

The current implementation provides:

- a FastAPI server
- Excel upload validation
- Excel preview against the active dataset
- Excel publish into the active JSON snapshot
- versioned snapshot backups
- Admin and Review access via HTTP Basic credentials from `.env`
- static browser UIs served by the same FastAPI server

The solver and packing workflow remain in the project, but the Excel admin workflow is separate from the packing UI.

## Architecture

The implemented data flow is:

1. User downloads the current Excel dataset from `GET /admin/data/current_excel`
2. User edits the workbook locally
3. User uploads the workbook through the Review or Admin UI
4. Backend validates the workbook
5. Backend previews differences against the current active dataset
6. Admin can publish the workbook
7. Publish writes the compatibility JSON snapshot used by the API

Active snapshot:

- `H2O/api/data/packing_data.json`

Versioned backups:

- `H2O/api/data/versions/<version_id>_packing_data.json`
- `H2O/api/data/versions/<version_id>_manifest.json`

The runtime API reloads the snapshot in memory after publish.

## Roles

Two roles are implemented.

### Review

Review users can:

- download current Excel
- validate uploaded Excel
- preview uploaded Excel against the active dataset

Review users cannot publish.

### Admin

Admin users can:

- download current Excel
- validate uploaded Excel
- preview uploaded Excel against the active dataset
- publish a validated workbook

## Running Locally

Start the FastAPI server from the `H2O` directory:

```bash
cd /media/stephen/Data/development/h2o/H2O
python3 -m uvicorn api.app:app --host 127.0.0.1 --port 8001 --reload
```

This single server currently serves:

- API routes
- admin/review Excel workflow pages
- static files under `/html`
- snapshot files under `/api/data`

## Auth Setup

Credentials are loaded automatically from:

- `H2O/.env`

Example file:

- `H2O/api/.env.example`

Required variables:

- `H2O_ADMIN_USER`
- `H2O_ADMIN_PASS`
- `H2O_REVIEW_USER`
- `H2O_REVIEW_PASS`

Authentication is HTTP Basic.

The browser will prompt for credentials when protected endpoints are accessed.

## UI URLs

When running locally on port `8001`:

Review UI:

- `http://127.0.0.1:8001/html/review_data.html`

Admin UI:

- `http://127.0.0.1:8001/html/admin_data.html`

Current packing UI:

- `http://127.0.0.1:8001/html/index.html`

Current Excel download:

- `http://127.0.0.1:8001/admin/data/current_excel`

## API Endpoints

Excel workflow endpoints:

- `GET /admin/data/current` — current data as JSON for browser display (review+admin)
- `GET /admin/data/current_excel` — download active snapshot as `.xlsx` (review+admin)
- `GET /admin/data/versions` — last 20 version manifests (admin only)
- `POST /admin/data/validate` — validate uploaded `.xlsx` (review+admin)
- `POST /admin/data/preview` — validate + diff vs. active dataset (review+admin)
- `POST /admin/data/publish` — publish workbook to active snapshot (admin only)

## Publish Workflow

The implemented publish workflow is:

1. Download current Excel
2. Upload updated Excel workbook
3. Validate workbook
4. Preview workbook differences
5. Publish from Admin UI with required change reason
6. Write versioned backup files
7. Atomically replace active snapshot
8. Reload runtime snapshot in memory

Publish requires Admin credentials.

Review users can validate and preview only.

## Data Storage and Versions

Active data file:

- `H2O/api/data/packing_data.json`

Versioned publish artifacts:

- `H2O/api/data/versions/<version_id>_packing_data.json`
- `H2O/api/data/versions/<version_id>_manifest.json`

The manifest currently includes:

- `version_id`
- `published_at`
- `source_filename`
- `change_reason`
- `counts`
- `sha256`
- validation warnings

## Constraints

- Rollback is manual — restore a versioned snapshot file to `H2O/api/data/packing_data.json`
- Excel uses a single `SKUs` sheet with 14 fixed columns
- Admin and Review auth use shared HTTP Basic credentials from `.env`

## Solver Status

The solver files remain separate from this Excel admin workflow.

Solver files intentionally not changed by this workflow:

- `H2O/api/solver/branch_and_bound.py`
- `H2O/html/branch_and_bound_engine.js`

## Development Status

Current implemented status:

- FastAPI server running as a single-port app
- static UI served by FastAPI
- Excel validate / preview / publish flow implemented
- current Excel export implemented
- env-based auth implemented
- versioned snapshot backups implemented

Validation commands used in this repository:

```bash
cd /media/stephen/Data/development/h2o/H2O
pytest -q api/tests
python3 api/tests/harness/run_harness.py --historical
python3 api/smoke_test.py
```

These commands validate:

- API tests
- historical solver harness parity
- end-to-end API smoke flow
