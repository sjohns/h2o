# h2o

## H2O API + Frontend Integration

### Generate or refresh deterministic API snapshot

```bash
cd H2O
python3 api/scripts/generate_snapshot.py
```

This writes:

- `H2O/api/data/packing_data.json`

### Start API server

```bash
cd H2O
python3 -m uvicorn api.app:app --host 127.0.0.1 --port 8001 --reload
```

API URL:

- `http://127.0.0.1:8001`

### Start static frontend server

```bash
cd H2O
python3 -m http.server 8000
```

Frontend URL:

- `http://127.0.0.1:8000/html/index.html`

Toggle API mode in the browser:

- API mode on: `http://127.0.0.1:8000/html/index.html?useApi=1`
- Client-side fallback mode: `http://127.0.0.1:8000/html/index.html?useApi=0`

### Run tests

```bash
cd H2O
pytest -q api/tests
```

### Run API smoke test

```bash
cd H2O
python3 api/smoke_test.py
```

### Run UI-adjacent renderer smoke test

Start API first, then run:

```bash
cd H2O
node api/ui_render_smoke.js
```

### Run solver batch harness

```bash
cd H2O
python3 api/tests/harness/run_harness.py
```

Regenerate expected harness outputs (after intentional solver changes):

```bash
cd H2O
python3 api/tests/harness/run_harness.py --regenerate
```
