# Handoff

## Current State
- FastAPI + DuckDB scaffold is implemented under `python_process/cloud_app/`.
- Data import from `H2O/html/load_packing_data.js` to versioned Parquet is working.
- Branch-and-bound parity port is implemented in Python.
- Parity checker is implemented and currently passing all defined cases (`case_a` to `case_z`).
- Data version pointer exists at `python_process/data/master/current.json`.
- `fastapi`/`uvicorn` may still need to be installed in the environment before running the API server.

## Key Paths
- App entrypoint: `python_process/cloud_app/main.py`
- Solver: `python_process/cloud_app/core/solver.py`
- Data importer: `python_process/cloud_app/data/importer.py`
- Current data pointer: `python_process/data/master/current.json`
- Versioned data: `python_process/data/master/v*/`
- Parity cases: `python_process/cloud_app/tests/parity_cases.json`
- Parity runner: `python_process/cloud_app/scripts/run_parity_check.py`
- Config/env: `python_process/.env.example`, `python_process/cloud_app/config.py`
- Project plan: `python_process/TODO.md`

## How To Start
```bash
python3 -m pip install -r python_process/requirements.txt
cp python_process/.env.example python_process/.env
python3 -m python_process.cloud_app.scripts.bootstrap_from_js
python3 -m uvicorn python_process.cloud_app.main:app --reload --port 8080
```

## Validation Commands
```bash
python3 -m python_process.cloud_app.scripts.run_parity_check
python3 -m py_compile $(find python_process/cloud_app -name '*.py' | tr '\n' ' ')
```

## Open Work (Top 3)
1. Convert parity script into assert-based tests that fail CI on mismatch.
2. Add API tests for admin/client endpoints.
3. Add metadata history endpoint and rollback script for version management.

## Recent Changes
- Moved refactor assets into `python_process/`.
- Added dotenv-based config loading and `.env.example`.
- Added `pyproject.toml`, `pytest.ini`, `CHANGELOG.md`, `TODO.md`, and standard `README.md`.
- Expanded parity scenarios to 26 cases and validated exact JS/Python matches.

## Risks / Notes
- Full API run depends on installing `fastapi` and `uvicorn`.
- Solver currently expects explicit `selected_sku_ids` (empty selection is rejected by design).
- Keep parity cases updated whenever solver or data-shaping logic changes.

## Definition Of Done (Next Session)
- [ ] Parity check integrated as assert-based test suite.
- [ ] API endpoint tests added and passing.
- [ ] Metadata history + rollback workflow implemented and documented.
- [ ] `README.md` updated with test and rollback usage examples.

