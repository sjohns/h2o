# cloud_app/scripts

Purpose: operational entry points for local tasks (bootstrap, parity checks, conversion).

## Scripts

- `bootstrap_from_js.py`
  - Loads legacy `load_packing_data.js` into versioned parquet snapshots.

- `run_parity_check.py`
  - Runs JS and Python solver parity checks against `cloud_app/tests/parity_cases.json`.

- `migrate_current_json_to_normalized.py`
  - One-time migration from current legacy JSON payload into normalized SQLite version data.

- `compare_normalized_to_legacy.py`
  - Reconstructs legacy-style payload from current normalized version and compares field-by-field.

- `run_predeploy_smoke.py`
  - Fast API smoke checks for health, client routes, and admin routes.

- `convert_legacy_js_to_canonical_json.py`
  - One-time converter from legacy JS payload to canonical JSON.
  - Uses `loguru` for logs and `rich` for conversion summary output.

## Converter CLI

```bash
python3 -m python_process.cloud_app.scripts.convert_legacy_js_to_canonical_json \
  --source-js-path "H2O/html/load_packing_data.js" \
  --output-json-path "python_process/data/canonical/packing_dataset_v1.json" \
  --dataset-identifier "h2o-packing-dataset"
```

Arguments:
- `--source-js-path`: legacy JS data file.
- `--output-json-path`: canonical JSON destination.
- `--dataset-identifier`: metadata identifier written into output.
