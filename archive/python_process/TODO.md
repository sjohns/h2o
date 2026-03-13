# TODO

## Phase 1 (Core Readiness)
- [ ] Convert parity script output into assertions (fail on mismatch).
- [ ] Add unit tests for solver internals (constraints, scoring, tie-break rules).
- [ ] Add unit tests for importer normalization and versioning.
- [ ] Add API tests for `/admin/import/load-js`, `/admin/version/current`, `/api/calculate`.
- [ ] Add regression tests for fixed/min/max bundle overrides.
- [ ] Create full documentation for architecture, API contracts, data model, and deployment.
- [ ] Add endpoint examples for all admin/client routes (request/response JSON).
- [ ] Define and document metadata schema for each published data version.
- [ ] Record source file hash and row counts in metadata.
- [ ] Add metadata endpoint to return active and historical versions.
- [ ] Add rollback command/script to switch `current.json` to prior versions.
- [ ] Add validation script to verify required Parquet files per version.
- [ ] Finalize `.env` variable list and update `.env.example`.
- [ ] Ensure secret values are never logged.

## Phase 2 (Hardening and Scale)
- [ ] Profile branch-and-bound runtime on large SKU sets.
- [ ] Add pruning improvements and early-stop heuristics.
- [ ] Add optional caching for repeated SKU selections.
- [ ] Add performance benchmark script and baseline targets.
- [ ] Store parity test history with timestamped JSON reports.
- [ ] Track pass/fail trend across solver changes.
- [ ] Link parity behavior changes in changelog entries.
- [ ] Define retention policy for old versions and archives.
- [ ] Add troubleshooting section (common setup/runtime errors and fixes).
- [ ] Document parity workflow and how to add new parity cases.
- [ ] Separate local/dev/prod config defaults.
- [ ] Add production ASGI run instructions.
- [ ] Add containerization files (Dockerfile, optional compose).
- [ ] Add health and readiness checks for deployment environments.

