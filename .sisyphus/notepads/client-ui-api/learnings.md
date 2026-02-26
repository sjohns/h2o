# Client UI API Learnings

## 2026-02-19: Initial Client UI Skeleton

### Task
Created `python_process/cloud_app/ui_client/index.html` mirroring legacy `H2O/html/index.html` DOM structure.

### Required DOM IDs (all verified present)
- `selectSkus` - SKU selection container
- `orderTableContainer` - Order table wrapper
- `orderTableHeading` - Page heading
- `orderTableTbody` - Order table body
- `finalizeOrder` - Finalize button
- `orderTableDetail` - Packing slip detail table
- `orderTableDetailTbody` - Detail table body

### Notes
- CSS table styling copied unchanged from legacy (lines 8-37)
- No legacy `<script src="...">` tags included
- Empty `<script></script>` block added at end of body for future JS
- Legacy HTML had extensive comments (lines 40-91) explaining JS file dependencies - these were omitted as they're documented separately and will be replaced with new client-side code

### File Structure
```
python_process/cloud_app/ui_client/
└── index.html (78 lines)
```