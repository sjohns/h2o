# Next Steps

## Current State

All core admin workflow tasks are complete and all 18 tests pass.

- Export → import round-trip works cleanly
- All column types correct (Eagle fields as strings, `calculated_sticks_per_bundle` as admin-selected int)
- Both Admin and Review browser UIs working
- Versioned publish with manifest files

## Potential Future Work

- Rollback endpoint to restore a versioned snapshot (currently manual)
- Multi-user concurrent publish protection (last-write-wins currently)
- Excel template download (blank template with headers pre-filled)
- User-facing version history UI improvements (diff between versions)
