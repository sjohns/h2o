# Python Process

Cloud refactor of the pipe loading workflow using FastAPI + DuckDB.

Storage: SQLite is the authoritative store for app data (foreign/unique constraints enforced).

## Install

```bash
python3 -m pip install -r python_process/requirements.txt
```

## Configuration

```bash
cp python_process/.env.example python_process/.env
```

Set values in `python_process/.env`.

## Bootstrap Master Data

Loads `H2O/html/load_packing_data.js` and writes a versioned dataset into SQLite, then updates `current.json`.

```bash
python3 -m python_process.cloud_app.scripts.bootstrap_from_js
```

## One-Time Legacy JS to Canonical JSON Conversion

Use this once to convert the hand-created legacy `load_packing_data.js` source into
the new canonical JSON structure.

```bash
python3 -m python_process.cloud_app.scripts.convert_legacy_js_to_canonical_json \
  --source-js-path "H2O/html/load_packing_data.js" \
  --output-json-path "python_process/data/canonical/packing_dataset_v1.json" \
  --dataset-identifier "h2o-packing-dataset"
```

The converter validates IDs, packaging values, and bundle constraints before writing output.

## Run API

```bash
python3 -m uvicorn python_process.cloud_app.main:app --reload --port 8080
```

## UI Pages

- Admin UI: `http://localhost:8080/admin-ui`
- Client UI: `http://localhost:8080/client-ui`

## Endpoints

- `GET /health`
- `POST /admin/import/load-js?source_path=/abs/path/to/load_packing_data.js` (requires `x-admin-id` + `x-admin-password`)
- `POST /admin/import/csv` multipart upload (requires `x-admin-id` + `x-admin-password`; returns review CSV download)
- `GET /admin/version/current` (requires `x-admin-id` + `x-admin-password`)
- `GET /admin/dataset` (requires `x-admin-id` + `x-admin-password`)
- `GET /admin/storage/status` (requires `x-admin-id` + `x-admin-password`)
- `POST /admin/storage/retention` (body includes `admin_id` + `admin_password` + `keep_latest` + `dry_run`)
- `PATCH /admin/product-type/{product_type_id}` (body includes `admin_id` + `admin_password`)
- `PATCH /admin/sku/{sku_id}` (body includes `admin_id` + `admin_password`)
- `GET /api/skus`
- `POST /api/calculate`

Set both `H2O_ADMIN_ID` and `H2O_ADMIN_PASSWORD` in `python_process/.env` before using admin endpoints/UI.

## Parity Check

```bash
python3 -m python_process.cloud_app.scripts.run_parity_check
```

## Predeploy Smoke Checks

```bash
python3 -m python_process.cloud_app.scripts.run_predeploy_smoke
```
