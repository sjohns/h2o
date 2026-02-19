# Repository Guidelines

## Project Structure & Module Organization
Primary work happens in `H2O/`.
- `H2O/html/`: browser app for SKU selection and order/packing-slip generation (`index.html` + modular JS files).
- `H2O/calculate_load_packing_data/`: data transformation scripts that generate `load_packing_data.js` from CSV/JSON sources.
- `H2O/Initial/`: one-off data prep scripts and seed files used to build initial chart/load datasets.
- `H2O/*.py`: automation and validation scripts (`packing_slip_scraper.py`, `compare_packing_slips.py`).
- Root-level ZIP folders (for example `H2O_2024-08-21/`, `html_backup/`) are historical snapshots; avoid editing them unless explicitly needed.

## Build, Test, and Development Commands
No package manager or Makefile is configured; run scripts directly.
- `cd H2O`
- `python3 calculate_load_packing_data/calculate_load_packing_data.py`: regenerate packing data JS from CSV.
- `python3 packing_slip_scraper.py`: run Selenium flow to create/update packing slip outputs.
- `python3 compare_packing_slips.py`: compare generated HTML/ZIP artifacts with reference files.
- `python3 -m http.server 8000` then open `http://localhost:8000/html/`: quick local UI test.

## Coding Style & Naming Conventions
- Python: 4-space indentation, `snake_case` for functions/variables, clear docstrings for non-trivial functions.
- JavaScript: 4-space indentation, `camelCase` for functions/variables, `PascalCase` for classes (for example `BranchAndBoundEngine`).
- Keep generated files named consistently (`load_packing_data.js`, timestamped `packing_slips_YYYYMMDD_HHMMSS.html/.zip`).
- Prefer small, focused modules in `H2O/html/` over large monolithic scripts.

## Testing Guidelines
- No automated test suite is currently present.
- Validate by running:
  1. data generation script,
  2. local UI load in browser,
  3. `compare_packing_slips.py` against `packing_slips_correct.*`.
- For algorithm changes, add a reproducible input sample and expected output notes in the PR.

## Commit & Pull Request Guidelines
- This workspace snapshot does not include `.git` history; use concise, imperative commit messages (recommended: `type(scope): summary`, e.g., `fix(scraper): wait for order table before export`).
- PRs should include:
  - purpose and affected paths,
  - before/after behavior,
  - commands run for validation,
  - screenshots for `H2O/html/` UI changes.
