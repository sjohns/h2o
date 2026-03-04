# Excel Admin Workflow

## 1. Purpose

Use this workflow to manage SKU packing data through Excel.

Download the current data, edit it, upload it, validate it, preview the changes, then publish (Admin only).

## 2. Roles

### Review

Review users can:

- View current published data in the browser
- Download the current Excel file
- Validate an uploaded Excel file
- Preview changes before publish

### Admin

Admin users can do everything a Review user can do, and additionally:

- Publish the updated Excel file
- View publish history

## 3. Download Current Excel

Download from the Admin or Review page, or directly:

```
GET /admin/data/current_excel
```

The downloaded file has all 14 required columns pre-filled with the current active data.

## 4. Excel Column Format

The workbook must have a sheet named `SKUs` with these 14 columns in order:

| Column | Type | Notes |
|---|---|---|
| `product_type_name` | text | Group name |
| `product_type_display_order` | number | Sort order for the product type |
| `product_type_active_flag` | Y or N | |
| `sku_display_order` | number | Sort order within the product type |
| `sku_active_flag` | Y or N | |
| `sku_description` | text | Full SKU description |
| `size_nominal` | text | e.g. `1/2"` |
| `length_feet` | number | |
| `popularity_score` | number | |
| `eagle_sticks_per_bundle` | text | Eagle catalog reference, e.g. `"360"` or `"6 / 8"` |
| `eagle_bundles_per_truckload` | text | Eagle catalog reference, e.g. `"36"` or `"6 / 6"` |
| `calculated_sticks_per_bundle` | number | Admin-selected bundle size for the solver |
| `actual_sticks_per_truckload` | number | Independently measured sticks per truck |
| `notes` | text | Optional |

**Eagle reference strings** (`eagle_sticks_per_bundle`, `eagle_bundles_per_truckload`) are display-only values from Eagle's tables. They are stored as-is and never used in calculations. They can be any string like `"9 / 12 / 12 / 16"`.

**`calculated_sticks_per_bundle`** is the admin-selected value the solver uses. This is manually chosen from the Eagle reference options and must be entered as a plain integer.

**`actual_sticks_per_truckload`** is the independently measured total sticks on a truck. It is not calculated from any other field.

## 5. Validate

Validate checks the workbook structure and field values.

Catches issues before preview or publish:
- Missing required columns
- Invalid field types
- Empty required fields
- Duplicate SKUs
- Inconsistent product type metadata across rows

## 6. Preview

Preview compares the uploaded workbook against the current active dataset.

Shows:
- Added SKUs
- Removed SKUs
- Changed SKU fields (with before/after values)

## 7. Publish (Admin only)

Publishing replaces the active dataset with the uploaded Excel data.

A change reason is required.

What happens on publish:
1. Workbook is validated
2. Existing IDs are matched by name; new entries get sequential IDs
3. A versioned backup is saved
4. The active snapshot is atomically replaced
5. The in-memory runtime reloads immediately

## 8. Versioning

Each publish saves a versioned copy to:

```
api/data/versions/<YYYYMMDD_HHMMSS>_packing_data.json
api/data/versions/<YYYYMMDD_HHMMSS>_manifest.json
```

The manifest records: publish time, source filename, change reason, SKU counts, SHA-256 hash, and any warnings.

## 9. Authentication

Access is protected by HTTP Basic credentials. The browser will prompt for username and password.

Credentials are set by the system administrator in `H2O/.env`.

## 10. Rollback

To restore a previous version, copy the desired versioned snapshot file to:

```
H2O/api/data/packing_data.json
```

Then restart the server (or use a reload endpoint if available).
