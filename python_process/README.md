# Python Process

Cloud refactor of the pipe loading workflow using FastAPI + DuckDB.

## Install

```bash
python3 -m pip install -r python_process/requirements.txt
```

## Configuration

```bash
cp python_process/.env.example python_process/.env
```

Set values in `python_process/.env` as needed.

## Bootstrap Master Data

Loads `H2O/html/load_packing_data.js` and writes versioned Parquet snapshots.

```bash
python3 -m python_process.cloud_app.scripts.bootstrap_from_js
```

## Run API

```bash
python3 -m uvicorn python_process.cloud_app.main:app --reload --port 8080
```

## Endpoints

- `GET /health`
- `POST /admin/import/load-js?source_path=/abs/path/to/load_packing_data.js`
- `GET /admin/version/current`
- `POST /api/calculate`

## Parity Check

```bash
python3 -m python_process.cloud_app.scripts.run_parity_check
```
