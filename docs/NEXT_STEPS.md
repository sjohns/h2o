# Next Steps

## Current State

All core workflow tasks are complete and all 26 tests pass.

- Export → import round-trip works cleanly
- All column types correct (Eagle fields as strings, `calculated_sticks_per_bundle` as admin-selected int)
- Admin browser UI: validate / preview / publish / version history (Bootstrap 5.3.3)
- Review browser UI: view current data + download only (Bootstrap 5.3.3)
- Versioned publish with manifest files
- Packing order UI fully rewritten — Bootstrap 5.3.3, all solving via Python API
- `load_packing_data.js` downloadable from admin/review page for legacy system compatibility
- Inactive SKU/product type support — items preserved in JSON, excluded from solver, reactivatable

## Potential Future Work

- Rollback endpoint to restore a versioned snapshot (currently manual)
- Multi-user concurrent publish protection (last-write-wins currently)
- User-facing version history UI improvements (diff between versions)
- Remove orphaned JS files from `H2O/html/` (`config.js`, `api_adapter.js`, `select_skus.js`, etc.) once legacy system is fully cut over
