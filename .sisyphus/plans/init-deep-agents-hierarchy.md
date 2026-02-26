# init-deep: Hierarchical AGENTS.md Knowledge Base

## TL;DR
> Create (and/or update) a small hierarchy of `AGENTS.md` files so agents have accurate, non-generic navigation + guardrails for this repo’s two domains: `H2O/` (static UI + scripts) and `python_process/` (FastAPI + DuckDB).

**Deliverables**:
- Updated repo-root `AGENTS.md` (broaden scope: include `python_process/`, explicit exclusions)
- New subdir `AGENTS.md` where complexity warrants (see “Target Locations”)
- Agent-executable verification script ensuring depth/exclusion/content constraints

**Mode**: Update (no deletions)
**Max Depth**: 3 (from repo root)
**Artifact Policy**: Exclude backups/zips/generated/caches from scoring + placement

---

## Context

### Original Request
- “/init-deep” to generate hierarchical `AGENTS.md` files (root + complexity-scored subdirectories), maximizing search effort and parallelism.

### Repo Facts (confirmed)
- Two primary domains:
  - `H2O/`: browser UI in `H2O/html/` (plain HTML+JS) + Python automation/data scripts
  - `python_process/`: FastAPI + DuckDB cloud refactor (`python_process/cloud_app/`)
- Existing knowledge file: `AGENTS.md` at repo root (currently H2O-centric)
- No CI config detected (`.github/workflows` absent); no Makefile detected; workflow is script-driven.
- Python test infra exists (pytest config) but the `python_process/cloud_app/tests/` folder currently contains `parity_cases.json` and no `test_*.py`.
- JS/HTML has no Node toolchain in-repo (no `package.json` observed).

### Complexity Hotspots (inputs to scoring)
- `H2O/html/load_packing_data.js` (~1216 LOC)
- `H2O/calculate_load_packing_data/load_packing_data.js` (~1216 LOC)
- `H2O/html/branch_and_bound_engine.js` (~735 LOC)
- `H2O/html/order_table.js` (~312 LOC)
- `H2O/Initial/process_MySQL_charts_data_from JSON.py` (~413 LOC)
- `H2O/calculate_load_packing_data/mysqlPacking_data_josn_process.py` (~340 LOC)
- `python_process/cloud_app/core/solver.py` (~267 LOC; dense control flow)

### Metis Review (guardrails to bake in)
- Avoid parent/child duplication; children contain deltas only.
- Exclude backups/snapshots, zips, caches, `__pycache__`, and generated/minified assets from scoring and file placement.
- Don’t invent tooling/workflows; list only commands confirmed in repo.
- Include agent-executable acceptance checks (depth, exclusion list, section presence, size limits).
- Handle paths with spaces by quoting paths in any command snippets.

---

## Work Objectives

### Core Objective
Create a concise, accurate `AGENTS.md` hierarchy that (1) directs agents to the right files fast and (2) prevents common repo-specific mistakes (editing snapshots, treating artifacts as source, etc.).

### Target Locations (decided)
- Root: `AGENTS.md` (update existing)
- Subdirectories (create new `AGENTS.md`):
  - `H2O/AGENTS.md`
  - `H2O/html/AGENTS.md`
  - `H2O/calculate_load_packing_data/AGENTS.md`
  - `H2O/Initial/AGENTS.md`
  - `python_process/AGENTS.md`
  - `python_process/cloud_app/AGENTS.md`

### Must NOT Do (scope guardrails)
- Do not edit or describe historical snapshot `.zip` folders as active modules.
- Do not add new lint/test/tooling configs (ruff/black/eslint/pre-commit) as part of this task.
- Do not attempt refactors or code behavior changes.
- Do not include secrets; never reference any real `.env` values (only `.env.example`).

---

## Verification Strategy

> No human manual verification required. All checks must be runnable via scripts/commands.

### Automated Checks (agent-executable)
- File existence: root + selected subdir `AGENTS.md` files exist.
- Depth constraint: no `AGENTS.md` created deeper than 3 levels from repo root.
- Exclusion constraint: no `AGENTS.md` inside excluded directories.
- Content constraint: each `AGENTS.md` contains required sections/keywords (see task acceptance criteria).
- Size constraint: no file exceeds a maximum size (prevents accidental doc dumps).

---

## Execution Strategy

### Parallel Waves

Wave 1 (Foundation: rules + scoring inputs)
1) Define exclusion list + scoring rubric (repo-specific)
2) Inventory existing `AGENTS.md` + confirm target directories exist
3) Draft a single verification script (depth/exclusions/sections/size)

Wave 2 (Write subdir AGENTS in parallel)
4) `H2O/html/AGENTS.md`
5) `H2O/calculate_load_packing_data/AGENTS.md`
6) `H2O/Initial/AGENTS.md`
7) `python_process/cloud_app/AGENTS.md`
8) `python_process/AGENTS.md`

Wave 3 (Integrate and dedupe)
9) Update root `AGENTS.md` (repo-wide, links to subdirs)
10) Add `H2O/AGENTS.md` (H2O-wide delta; link to its subdirs)

Wave 4 (Review)
11) Run verification script; fix violations
12) Deduplicate/trim; ensure children don’t repeat root

---

## TODOs

- [ ] 1. Define Scoring + Exclusion Rules

  **What to do**:
  - Define exclusion globs (minimum): `**/__pycache__/**`, `**/.venv/**`, `**/.pytest_cache/**`, `**/*.zip`, `**/*backup*/**`, root-level timestamped artifacts, and other non-source outputs.
  - Decide how to treat likely-generated files (notably `H2O/html/load_packing_data.js`): exclude from “hotspot” weighting if confirmed generated.
  - Produce a scoring rubric (simple, deterministic): file count, LOC hotspots, distinct domain boundary, presence of configs/entry points.

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: (none)

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 2-3)

  **References**:
  - `AGENTS.md` (existing) - current exclusions/guardrails focus on `H2O/`.
  - Repo root contains many `.zip` snapshots - ensure they are excluded from scoring.

  **Acceptance Criteria**:
  - [ ] Exclusion list documented (as bullets) and reused consistently across subsequent tasks.
  - [ ] Scoring rubric documented in a short table (max 10 rows).

  **QA Scenarios**:
  ```
  Scenario: Confirm exclusions prevent scope creep
    Tool: Bash
    Steps:
      1. Search for excluded dirs (e.g., __pycache__, zip snapshots).
      2. Verify exclusions list contains patterns covering them.
    Expected Result: Exclusions cover all common artifact/caches present.
    Evidence: .sisyphus/evidence/task-1-exclusions.txt
  ```

- [ ] 2. Confirm Target Locations Exist + Decide Final AGENTS.md Set

  **What to do**:
  - Verify each target directory exists.
  - If a directory is missing, adjust target list (do not create new code directories).

  **Recommended Agent Profile**:
  - **Category**: `quick`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1, 3)

  **References**:
  - `H2O/`
  - `H2O/html/`
  - `H2O/calculate_load_packing_data/`
  - `H2O/Initial/`
  - `python_process/`
  - `python_process/cloud_app/`

  **Acceptance Criteria**:
  - [ ] Final list of AGENTS.md targets is recorded with reasons (1 line each).

  **QA Scenarios**:
  ```
  Scenario: Directories exist
    Tool: Bash
    Steps:
      1. ls each target directory.
    Expected Result: All targets exist or are explicitly removed from plan.
    Evidence: .sisyphus/evidence/task-2-target-dirs.txt
  ```

- [ ] 3. Create Agent-Executable Verification Script

  **What to do**:
  - Create `.sisyphus/scripts/verify_agents_hierarchy.py` that validates:
    - `AGENTS.md` count in expected range (guard against explosion)
    - max depth <= 3
    - none within excluded dirs
    - required sections present
    - max file size threshold
  - Script must exit non-zero on failure.
  - Ensure `.sisyphus/evidence/` exists; script (or wrapper command) writes a short report to `.sisyphus/evidence/verify-agents-report.txt`.

  **Recommended Agent Profile**:
  - **Category**: `quick`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1-2)

  **References**:
  - `python_process/pyproject.toml` - project uses Python >=3.11 (OK to rely on `pathlib`).

  **Acceptance Criteria**:
  - [ ] Script runs successfully on a clean tree and fails when constraints are violated.

  **QA Scenarios**:
  ```
  Scenario: Verification script passes after generation
    Tool: Bash
    Steps:
      1. python3 .sisyphus/scripts/verify_agents_hierarchy.py | tee .sisyphus/evidence/task-3-verify-pass.txt
    Expected Result: Exit code 0; prints a short PASS summary.
    Evidence: .sisyphus/evidence/task-3-verify-pass.txt
  ```

- [ ] 4. Write `H2O/html/AGENTS.md`

  **What to do**:
  - Document UI entry point (`H2O/html/index.html`), module roles, and where to change UI behavior.
  - Call out hotspots: `branch_and_bound_engine.js`, `order_table.js`.
  - Include run steps: `python3 -m http.server 8000` from `H2O/` then open `/html/`.

  **Must NOT do**:
  - Do not repeat root-level artifact warnings except as a short “see root” pointer.

  **Recommended Agent Profile**:
  - **Category**: `writing`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 2)

  **References**:
  - `H2O/html/index.html` - script list + high-level system notes.
  - `H2O/html/branch_and_bound_engine.js` - algorithm module.
  - `H2O/html/order_table.js` - UI table logic.

  **Acceptance Criteria**:
  - [ ] 30-80 lines; includes “Where to look” mapping Task→File.
  - [ ] Contains a clear “Do not edit generated data files” note if `load_packing_data.js` is generated.

  **QA Scenarios**:
  ```
  Scenario: AGENTS.md created and concise
    Tool: Bash
    Steps:
      1. test -f H2O/html/AGENTS.md
      2. wc -l H2O/html/AGENTS.md
    Expected Result: File exists; line count within target range.
    Evidence: .sisyphus/evidence/task-4-h2o-html-agents.txt
  ```

- [ ] 5. Write `H2O/calculate_load_packing_data/AGENTS.md`

  **What to do**:
  - Document the data generation flow: `calculate_load_packing_data.py` → `H2O/html/load_packing_data.js`.
  - Document primary input(s) (CSV) and output locations.
  - Note scripts with spaces in filenames and the need to quote paths.

  **Recommended Agent Profile**:
  - **Category**: `writing`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 2)

  **References**:
  - `H2O/calculate_load_packing_data/calculate_load_packing_data.py` - generator entry.
  - `H2O/html/load_packing_data.js` - downstream consumer.

  **Acceptance Criteria**:
  - [ ] Includes exact command(s) from repo guidance to regenerate data.
  - [ ] Includes explicit output file paths.

  **QA Scenarios**:
  ```
  Scenario: Subdir AGENTS exists and is concise
    Tool: Bash
    Steps:
      1. test -f H2O/calculate_load_packing_data/AGENTS.md
      2. wc -l H2O/calculate_load_packing_data/AGENTS.md | tee .sisyphus/evidence/task-5-calc-load-agents.txt
    Expected Result: File exists; line count is reasonable (target 30-80).
    Evidence: .sisyphus/evidence/task-5-calc-load-agents.txt
  ```

- [ ] 6. Write `H2O/Initial/AGENTS.md`

  **What to do**:
  - Explain that this is one-off/seed data prep.
  - Point to heavy scripts and any expected inputs/outputs.

  **Recommended Agent Profile**:
  - **Category**: `writing`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 2)

  **References**:
  - `H2O/Initial/read_new_initial_csv_file.py` - ingestion.
  - `H2O/Initial/process_MySQL_charts_data_from JSON.py` - chart processing.

  **Acceptance Criteria**:
  - [ ] States clearly this folder is one-off/seed scripts; warns against treating as production runtime.
  - [ ] “Where to look” includes at least the two referenced scripts.

  **QA Scenarios**:
  ```
  Scenario: Initial AGENTS exists
    Tool: Bash
    Steps:
      1. test -f H2O/Initial/AGENTS.md
      2. wc -l H2O/Initial/AGENTS.md | tee .sisyphus/evidence/task-6-initial-agents.txt
    Expected Result: File exists; concise.
    Evidence: .sisyphus/evidence/task-6-initial-agents.txt
  ```

- [ ] 7. Write `python_process/cloud_app/AGENTS.md`

  **What to do**:
  - Document FastAPI entry (`python_process/cloud_app/main.py`) and routers.
  - Document data root/env vars (point to `.env.example` only).
  - Document solver hotspot and parity cases file.

  **Recommended Agent Profile**:
  - **Category**: `writing`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 2)

  **References**:
  - `python_process/cloud_app/main.py` - app entry.
  - `python_process/cloud_app/core/solver.py` - solver hotspot.
  - `python_process/cloud_app/tests/parity_cases.json` - parity cases.

  **Acceptance Criteria**:
  - [ ] Includes API run command and lists key endpoints (from `python_process/README.md`).
  - [ ] Mentions parity cases file and what it is (test data, not test code).
  - [ ] Mentions solver hotspot and where to change it.

  **QA Scenarios**:
  ```
  Scenario: cloud_app AGENTS exists
    Tool: Bash
    Steps:
      1. test -f python_process/cloud_app/AGENTS.md
      2. wc -l python_process/cloud_app/AGENTS.md | tee .sisyphus/evidence/task-7-cloud-app-agents.txt
    Expected Result: File exists; concise.
    Evidence: .sisyphus/evidence/task-7-cloud-app-agents.txt
  ```

- [ ] 8. Write `python_process/AGENTS.md`

  **What to do**:
  - Document how to install/run API (from `python_process/README.md`).
  - Note that pytest config exists in *both* `pyproject.toml` and `pytest.ini`.
  - Point to `.env.example` and explain variables (no real values).

  **Recommended Agent Profile**:
  - **Category**: `writing`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 2)

  **References**:
  - `python_process/README.md` - canonical run commands.
  - `python_process/pyproject.toml` - deps + pytest options.
  - `python_process/pytest.ini` - duplicate config.
  - `python_process/.env.example` - env var names.

  **Acceptance Criteria**:
  - [ ] Includes install + run commands exactly as in `python_process/README.md`.
  - [ ] Calls out duplicate pytest config (pyproject + pytest.ini) without “fixing” it.
  - [ ] Mentions `.env.example` and explains env var names only.

  **QA Scenarios**:
  ```
  Scenario: python_process AGENTS exists
    Tool: Bash
    Steps:
      1. test -f python_process/AGENTS.md
      2. wc -l python_process/AGENTS.md | tee .sisyphus/evidence/task-8-python-process-agents.txt
    Expected Result: File exists; concise.
    Evidence: .sisyphus/evidence/task-8-python-process-agents.txt
  ```

- [ ] 9. Update Root `AGENTS.md`

  **What to do**:
  - Keep existing H2O guidance.
  - Add repo-level map that explicitly includes `python_process/` as a first-class area.
  - Add explicit “Artifacts/snapshots are out of scope” section.
  - Add pointers to each subdir `AGENTS.md` (do not duplicate child content).

  **Recommended Agent Profile**:
  - **Category**: `writing`

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Wave 2 content so it can link accurately)

  **References**:
  - Existing `AGENTS.md` - preserve current repo guidance style.
  - `python_process/README.md` - for accurate backend commands.

  **Acceptance Criteria**:
  - [ ] Root `AGENTS.md` includes both domains (`H2O/` and `python_process/`).
  - [ ] Root `AGENTS.md` links to each new subdir `AGENTS.md` (paths only, no duplication).

  **QA Scenarios**:
  ```
  Scenario: Root AGENTS points to sub-AGENTS
    Tool: Bash
    Steps:
      1. test -f AGENTS.md
      2. grep -n "python_process/AGENTS.md" AGENTS.md | tee .sisyphus/evidence/task-9-root-links.txt
    Expected Result: Root AGENTS includes links to new subdir AGENTS.
    Evidence: .sisyphus/evidence/task-9-root-links.txt
  ```

- [ ] 10. Write `H2O/AGENTS.md`

  **What to do**:
  - Provide H2O-wide navigation and point down to `H2O/html/`, `H2O/calculate_load_packing_data/`, `H2O/Initial/`.
  - Include the validated run loop from root guidance (data gen → serve UI → compare).

  **Recommended Agent Profile**:
  - **Category**: `writing`

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Wave 2 so it can link accurately)

  **Acceptance Criteria**:
  - [ ] Links to `H2O/html/AGENTS.md`, `H2O/calculate_load_packing_data/AGENTS.md`, and `H2O/Initial/AGENTS.md`.
  - [ ] Includes the script-driven dev loop (data gen → serve UI → compare) without inventing new commands.

  **QA Scenarios**:
  ```
  Scenario: H2O AGENTS exists and links downward
    Tool: Bash
    Steps:
      1. test -f H2O/AGENTS.md
      2. grep -n "H2O/html/AGENTS.md" H2O/AGENTS.md | tee .sisyphus/evidence/task-10-h2o-links.txt
    Expected Result: H2O/AGENTS.md links to its subdir AGENTS files.
    Evidence: .sisyphus/evidence/task-10-h2o-links.txt
  ```

- [ ] 11. Run Verification Script + Fix Violations

  **What to do**:
  - Run the script from Task 3.
  - Fix any failures (depth, exclusions, missing sections, size).

  **Recommended Agent Profile**:
  - **Category**: `quick`

  **Parallelization**:
  - **Can Run In Parallel**: NO (final gate)

  **QA Scenarios**:
  ```
  Scenario: Verification passes
    Tool: Bash
    Steps:
      1. python3 .sisyphus/scripts/verify_agents_hierarchy.py | tee .sisyphus/evidence/task-11-verify-final.txt
    Expected Result: Exit code 0.
    Evidence: .sisyphus/evidence/task-11-verify-final.txt
  ```

- [ ] 12. Deduplicate + Trim

  **What to do**:
  - Ensure each child adds only local deltas.
  - Remove generic advice; keep each file telegraphic.
  - Ensure non-ASCII isn’t introduced unless already present.

  **Recommended Agent Profile**:
  - **Category**: `writing`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with peers reviewing different files)

  **Acceptance Criteria**:
  - [ ] No child AGENTS repeats large sections from root; children contain local deltas only.
  - [ ] All AGENTS files stay within the size/line-count constraints enforced by the verification script.

  **QA Scenarios**:
  ```
  Scenario: Re-run verification after trimming
    Tool: Bash
    Steps:
      1. python3 .sisyphus/scripts/verify_agents_hierarchy.py | tee .sisyphus/evidence/task-12-verify-after-trim.txt
    Expected Result: Exit code 0.
    Evidence: .sisyphus/evidence/task-12-verify-after-trim.txt
  ```

---

## Final Verification Wave

- Run verification script from Task 3.
- Spot-check that commands listed in `AGENTS.md` exist in repo docs and don’t require secrets.

---

## Commit Strategy

- Single commit (recommended): `docs(agents): add hierarchical repo guidance`

---

## Success Criteria

- Root `AGENTS.md` updated without losing existing H2O guidance.
- New `AGENTS.md` present in each target subdir, concise and non-duplicative.
- Verification script passes: depth/exclusions/sections/size.
