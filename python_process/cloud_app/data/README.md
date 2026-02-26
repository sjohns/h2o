# cloud_app/data

Purpose: data ingestion, normalization, versioning, and canonical dataset conversion.

## Files

- `importer.py`: reads legacy `load_packing_data.js`, normalizes to tabular rows, writes versioned parquet snapshots.
- `versioning.py`: current-version pointer and version directory helpers.
- `repository.py`: read/write helpers for parquet-backed tables.
- `canonical_dataset_builder.py`: one-time conversion from legacy JS payload to canonical JSON.

## canonical_dataset_builder.py Function Reference

- `read_file_sha256_hex(source_file_path)`
  - Input: source file path.
  - Output: SHA256 hex digest.
  - Validation role: source integrity metadata.

- `_build_constraints_lookup(bundle_rows)`
  - Input: normalized bundle rows (`sku_id`, min/max bundles).
  - Output: lookup map keyed by `sku_id`.
  - Validation role: guarantees each canonical SKU has explicit constraints.

- `build_canonical_dataset_from_legacy_js(legacy_source_file_path, dataset_identifier)`
  - Input: legacy JS path and dataset identifier.
  - Output: canonical payload dictionary.
  - Calculation role: maps normalized rows into canonical `product_types` and `skus` structures.

- `_validate_canonical_dataset_payload(canonical_dataset_payload)`
  - Input: canonical payload dictionary.
  - Output: none (raises on invalid data).
  - Validation role: enforces uniqueness, foreign-key integrity, and bundle/packaging invariants.

- `write_canonical_dataset_json(canonical_dataset_payload, output_file_path)`
  - Input: canonical payload and output path.
  - Output: writes JSON to disk.
  - Validation role: writes only validated payloads.

## Canonical JSON Shape (v1)

- Root fields: `schema_version`, `dataset_identifier`, `generated_at`, `source`, `row_counts`, `product_types`, `skus`.
- `product_types[]`: `product_type_id`, `name`.
- `skus[]`: `sku_id`, `product_type_id`, `description`, `size`, `display_order`, `popularity_score`, `packaging`, `constraints`.
- `packaging`: `sticks_per_bundle`, `sticks_per_truckload`, `bundles_per_truckload`.
- `constraints`: `min_number_of_bundles`, `max_number_of_bundles`.
