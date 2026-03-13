# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Behaviour Rules

- Only do exactly what the user explicitly instructs. Nothing more.
- If you think something else should be done, do not do it — ask the user first and wait for approval.

## Three Systems in This Repo

This repo contains three distinct, independently-runnable systems at different stages of development:

| System | Path | Status | Port |
|---|---|---|---|
| **H2O FastAPI app** | `H2O/api/` | Active / production | 8001 |
| **python_process cloud refactor** | `python_process/` | Experimental, separate codebase | 8080 |
| **Legacy api_backend** | `H2O/api_backend/` | Superseded, not in use | — |

The AGENTS.md at the repo root is **stale** — it describes a pre-API state and incorrectly says there is no automated test suite.

---

## System 1: H2O FastAPI App (primary)

### Commands (run from `H2O/`)

```bash
# Start server
python -m uvicorn api.app:app --host 0.0.0.0 --port 8080               # production
python -m uvicorn api.app:app --host 127.0.0.1 --port 8001 --reload   # local dev

# Run all tests
pytest -q api/tests

# Run a single test file
pytest -q api/tests/test_admin_endpoints.py

# Run a single test by name
pytest -q api/tests/test_endpoints.py::test_get_skus_returns_list

# Local solver harness (runs against orders.json + expected_results.json)
python3 api/tests/harness/run_harness.py

# Historical harness (26 cases, must all match JS solver — must never regress)
python3 api/tests/harness/run_harness.py --historical

# Regenerate local harness expected outputs from current solver
python3 api/tests/harness/run_harness.py --regenerate

# End-to-end smoke test (starts/stops server internally, requires H2O/.env)
python3 api/smoke_test.py
```

### Auth

Credentials are read from `H2O/.env` (never committed). See `H2O/api/.env.example`:

```
H2O_ADMIN_USER=admin
H2O_ADMIN_PASS=admin_password
H2O_REVIEW_USER=review
H2O_REVIEW_PASS=review_password
```

Auth is HTTP Basic. Tests monkeypatch these via `conftest.py` — no `.env` needed for `pytest`.

### Architecture

**Entry point:** `H2O/api/app.py`
- Loads `H2O/.env` before anything else (fails hard if missing)
- Calls `reload_runtime_snapshot()` at startup to load SKUs into memory
- Mounts `/html` → `H2O/html/` (static files)
- Mounts `/api/data` → `H2O/api/data/` (snapshot files)
- Registers two routers

**Two routers:**

1. **Solver API** (`H2O/api/routes.py`) — public, no auth:
   - `GET /skus` — returns in-memory SKU list
   - `POST /orders` — creates order, returns `order_id`
   - `POST /pack` — runs solver (with `lru_cache`), returns packing result
   - `GET /orders/{id}` — retrieves stored order

2. **Admin/Excel workflow** (`H2O/api/admin/routes.py`) — HTTP Basic auth:
   - `GET /admin/data/current` — current data as JSON for browser display (review+admin)
   - `GET /admin/data/current_excel` — export active snapshot as `.xlsx` (review+admin)
   - `GET /admin/data/current_json` — export active snapshot as `load_packing_data.js` legacy format (review+admin)
   - `GET /admin/data/versions` — last 20 version manifests (admin only)
   - `POST /admin/data/validate` — validate uploaded `.xlsx` (review+admin)
   - `POST /admin/data/preview` — validate + diff vs. active snapshot (review+admin)
   - `POST /admin/data/publish` — publish to active snapshot (admin only)

**Runtime state** (`H2O/api/runtime.py`):
- `SNAPSHOT_PATH = H2O/api/data/packing_data.json` — active snapshot
- `VERSIONS_DIR = H2O/api/data/versions/` — versioned backups
- `reload_runtime_snapshot()` hot-reloads in-memory SKU state without restart
- Called at startup and after every publish
- Calls `initialize_runtime()` in `routes.py` to inject SKUs into the global solver state
- The `lru_cache` in `cache.py` (maxsize=10000) is cleared on every reload

**Auth** (`H2O/api/auth.py`):
- `require_review` — accepts admin or review credentials
- `require_admin` — accepts admin credentials only
- Both read env vars fresh on every request via `os.getenv`

**Solver** (`H2O/api/solver/branch_and_bound.py`):
- Python port of the original JS branch-and-bound algorithm
- Intentionally not modified by the Excel admin workflow
- `solver_service.py` in the same directory is a **dead file** — it imports from `api_backend.models` (the legacy system) and is not imported by anything in the active app

**Data storage:**
- Active snapshot: `H2O/api/data/packing_data.json` — legacy JSON shape with `productTypes` list + nested `skus` dict
- Versioned backups: `H2O/api/data/versions/<YYYYMMDD_HHMMSS>_packing_data.json`
- Version manifests: `H2O/api/data/versions/<YYYYMMDD_HHMMSS>_manifest.json` (includes `version_id`, `published_at`, `source_filename`, `change_reason`, `counts`, `sha256`, warnings)

**Excel schema** — workbook must have sheet named `SKUs` with 14 columns (`H2O/api/admin/data_import.py::REQUIRED_COLUMNS`):

`product_type_name`, `product_type_display_order`, `product_type_active_flag`, `sku_display_order`, `sku_active_flag`, `sku_description`, `size_nominal`, `length_feet`, `popularity_score`, `eagle_sticks_per_bundle`, `eagle_bundles_per_truckload`, `calculated_sticks_per_bundle`, `actual_sticks_per_truckload`, `notes`

IDs are internal — assigned automatically on publish, never in Excel. `eagle_sticks_per_bundle` and `eagle_bundles_per_truckload` are Eagle catalog reference strings (e.g. `"6 / 8"`, `"9 / 12 / 12 / 16"`) — stored as-is, never parsed. `calculated_sticks_per_bundle` is admin-selected (int) and is what the solver uses. `actual_sticks_per_truckload` is independently measured (int), not calculated. Export → import round-trip is fully functional.

### Tests

- `test_endpoints.py` — solver API integration tests via `httpx.ASGITransport`
- `test_admin_endpoints.py` — Excel admin endpoint tests; publish tests use `isolated_snapshot_paths` fixture to avoid touching real data
- `test_admin_ui_flow.py` — validate → preview → publish end-to-end flow test
- `test_harness.py` — runs local solver harness as a pytest assertion (`mismatches == 0`)
- `test_historical_harness.py` — runs historical harness (26 JS parity cases) as a pytest assertion
- `test_solver_parity.py` — tests 3 specific SKU combos by running both Python and JS solvers and comparing outputs (requires `node`)

The `isolated_snapshot_paths` fixture (defined in both `test_admin_endpoints.py` and `test_admin_ui_flow.py`) copies the real snapshot to `tmp_path`, patches `runtime.SNAPSHOT_PATH` and `runtime.VERSIONS_DIR`, and restores after the test.

### Browser UIs (served at port 8001)

- `http://127.0.0.1:8001/html/index.html` — packing order UI (JS-driven, uses solver API)
- `http://127.0.0.1:8001/html/admin_data.html` — admin Excel workflow (validate/preview/publish)
- `http://127.0.0.1:8001/html/review_data.html` — review workflow (validate/preview only)

Both admin and review HTML pages use `H2O/html/js/admin_data.js` and `H2O/html/css/admin_data.css`. The page role (`admin` vs `review`) is determined by `data-role` attribute on `<body>`, which controls whether the publish button is wired.

`H2O/html/app.js` is the single JS file for the packing UI. It contains `ApiEngine` (manages bundle constraints and calls the Python solver API) and `OrderTable` (renders the order and packing slip). It calls `GET /skus`, `POST /orders`, and `POST /pack` directly — no intermediate adapter. `login.html` + `H2O/html/js/login.js` handle auth (HTTP Basic, token stored in sessionStorage).

Several JS files remain on disk from the previous architecture (`config.js`, `api_adapter.js`, `select_skus.js`, `event_listener.js`, `order_table.js`, etc.) but are **not loaded by any active page** and can be ignored.

### Data Generation Pipeline

`H2O/html/load_packing_data.js` is a **generated file** (~1200 LOC, contains packing data as a JS `const`). Do not edit it directly.

To regenerate from CSV:
```bash
cd H2O/calculate_load_packing_data
python3 calculate_load_packing_data.py
```
Input: `h2o_packing_data.csv`
Output: `H2O/html/load_packing_data.js` and `H2O/api/data/packing_data.json`

---

## System 2: python_process (experimental cloud refactor)

A separate FastAPI + DuckDB system with its own solver and data pipeline.

### Commands (run from repo root)

```bash
# Install dependencies
python3 -m pip install -r python_process/requirements.txt

# Copy and configure env
cp python_process/.env.example python_process/.env

# Bootstrap master data from load_packing_data.js
python3 -m python_process.cloud_app.scripts.bootstrap_from_js

# Run the cloud_app API server (port 8080)
python3 -m uvicorn python_process.cloud_app.main:app --reload --port 8080

# Run parity checks
python3 -m python_process.cloud_app.scripts.run_parity_check

# Run replacement.py as a standalone API (alternative entrypoint)
python3 -m uvicorn python_process.replacement:app --reload --port 8080
```

### Two Entrypoints

1. **`python_process/cloud_app/main.py`** — full cloud app with admin + client routers, SQLite store, admin UI at `/admin-ui`, client UI at `/client-ui`. Auth via `x-admin-id` + `x-admin-password` headers.

2. **`python_process/replacement.py`** — single-file lightweight API. Loads SKUs from Parquet into a thread-safe dict at startup. Endpoints: `GET /parts`, `POST /order`, `POST /api/calculate`, `POST /solve`, `GET /api/skus`, `GET /health`, `POST /reload`. The last HANDOFF noted this is the current active entrypoint for UI wiring.

### Data

- Parquet-backed versioned data: `python_process/data/master/v<timestamp>/skus.parquet`
- Current version pointer: `python_process/data/master/current.json`
- Config env vars: `H2O_DATA_ROOT`, `H2O_LOAD_JS_SOURCE`, `H2O_SQLITE_DB_PATH`, `H2O_ADMIN_ID`, `H2O_ADMIN_PASSWORD`

### Key files

- `python_process/cloud_app/core/solver.py` — DuckDB/pandas solver (different implementation from `H2O/api/solver/`)
- `python_process/cloud_app/data/importer.py` — reads `load_packing_data.js`, writes versioned Parquet
- `python_process/cloud_app/data/README.md` — canonical JSON shape documentation

---

## System 3: H2O/api_backend (legacy, not in use)

`H2O/api_backend/` is a superseded backend. It has `app.py`, `models.py`, `service.py`, `solver.py`, and `data_loader.py`. Do not modify this code — it exists for historical reference only. The active backend is `H2O/api/`.

---

## Repository Layout (key paths only)

```
H2O/
  api/                    ← Active FastAPI app
    app.py                ← Entry point
    routes.py             ← Solver API routes
    admin/routes.py       ← Excel admin routes
    admin/data_import.py  ← Excel importer/validator
    auth.py               ← HTTP Basic auth dependencies
    runtime.py            ← Snapshot loader + hot-reload
    cache.py              ← lru_cache wrapper for solver
    store.py              ← In-memory order store
    solver/
      branch_and_bound.py ← Primary solver (do not change lightly)
      solver_service.py   ← Dead file (imports legacy api_backend)
    data/
      packing_data.json   ← Active snapshot
      versions/           ← Versioned backups
    tests/
      harness/
        orders_historical.json    ← 26 historical orders
        expected_historical.json  ← Expected outputs from JS solver
  api_backend/            ← Legacy backend (not in use)
  html/
    index.html            ← Packing order UI
    admin_data.html       ← Admin Excel UI
    review_data.html      ← Review Excel UI
    js/admin_data.js      ← Admin/Review UI logic
    load_packing_data.js  ← GENERATED data file (do not edit)
    branch_and_bound_engine.js  ← Original JS solver (reference)
  calculate_load_packing_data/
    calculate_load_packing_data.py  ← Regenerates load_packing_data.js + packing_data.json

python_process/
  replacement.py          ← Lightweight single-file API (current active entrypoint)
  cloud_app/
    main.py               ← Full cloud_app entry point
    core/solver.py        ← pandas/DuckDB solver
    data/importer.py      ← JS → Parquet import
  data/master/            ← Versioned Parquet data

docs/                     ← Architecture + workflow documentation
AGENTS.md                 ← Stale (pre-API state; do not trust for commands)
```
