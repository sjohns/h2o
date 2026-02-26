import json
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import pandas as pd

from ..config import DEFAULT_JS_SOURCE
from .repository import write_version_data
from .versioning import (
    get_version_dir,
    make_version_name,
    set_current_version,
)


REQUIRED_CSV_COLUMNS = [
    "productType",
    "SKU",
    "popularityScore",
    "eagleSticksPerBundle",
    "eagleBundlesPerTruckLoad",
    "calculatedSticksPerBundle",
]


def _clean_string(value: object) -> str:
    text = str(value if value is not None else "")
    text = text.replace("\n", " ").replace("\r", " ").strip()
    return " ".join(text.split())


def _derive_size_from_sku_text(sku_text: str) -> str:
    if '"' in sku_text:
        return sku_text.split('"', 1)[0] + '"'
    return ""


def _parse_non_negative_int(raw_value: object, field_name: str) -> int:
    if raw_value is None:
        return 0
    na_check = pd.isna(raw_value)
    if isinstance(na_check, bool):
        if na_check:
            return 0
    value_text = str(raw_value).strip()
    if "/" in value_text:
        value_text = value_text.split("/", 1)[0].strip()
    value_text = value_text.replace("'", "").replace('"', "").strip()
    parsed_value = int(float(value_text)) if value_text else 0
    if parsed_value < 0:
        raise ValueError(f"CSV contains {field_name} < 0")
    return parsed_value


def _validate_required_columns(csv_dataframe: pd.DataFrame) -> None:
    missing_columns = [column_name for column_name in REQUIRED_CSV_COLUMNS if column_name not in csv_dataframe.columns]
    if missing_columns:
        raise ValueError(f"CSV missing required columns: {missing_columns}")


def _normalize_csv_dataframe(csv_dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = csv_dataframe.copy()
    dataframe.columns = [str(column_name).strip() for column_name in dataframe.columns]
    dataframe = dataframe.dropna(how="all", axis=0).dropna(how="all", axis=1)

    if "calculatedSticksPerBundle" not in dataframe.columns and "eagleSticksPerBundle" in dataframe.columns:
        dataframe["calculatedSticksPerBundle"] = dataframe["eagleSticksPerBundle"]

    _validate_required_columns(dataframe)
    dataframe = dataframe.dropna(subset=["productType", "SKU", "popularityScore"])
    for column_name in dataframe.columns:
        dataframe[column_name] = dataframe[column_name].map(_clean_string)

    dataframe["popularityScore"] = [
        _parse_non_negative_int(value, "popularityScore")
        for value in dataframe["popularityScore"].tolist()
    ]
    dataframe["eagleSticksPerBundle"] = [
        _parse_non_negative_int(value, "eagleSticksPerBundle")
        for value in dataframe["eagleSticksPerBundle"].tolist()
    ]
    dataframe["eagleBundlesPerTruckLoad"] = [
        _parse_non_negative_int(value, "eagleBundlesPerTruckLoad")
        for value in dataframe["eagleBundlesPerTruckLoad"].tolist()
    ]
    dataframe["calculatedSticksPerBundle"] = [
        _parse_non_negative_int(value, "calculatedSticksPerBundle")
        for value in dataframe["calculatedSticksPerBundle"].tolist()
    ]

    dataframe = dataframe.reset_index(drop=True)
    dataframe["displayOrder"] = dataframe.index + 1
    if "size" not in dataframe.columns:
        dataframe["size"] = dataframe["SKU"].map(_derive_size_from_sku_text)
    dataframe["size"] = dataframe["size"].map(_clean_string)

    lingth_source_column = "lingth" if "lingth" in dataframe.columns else "length" if "length" in dataframe.columns else None
    if lingth_source_column is None:
        dataframe["lingth"] = 0
    else:
        lingth_values: list[int] = []
        for raw_length_value in dataframe[lingth_source_column].tolist():
            lingth_values.append(_parse_non_negative_int(raw_length_value, "lingth"))
        dataframe["lingth"] = lingth_values

    if "active" in dataframe.columns:
        source_active_values = dataframe["active"].tolist()
    elif "activeFlag" in dataframe.columns:
        source_active_values = dataframe["activeFlag"].tolist()
    elif "active_flag" in dataframe.columns:
        source_active_values = dataframe["active_flag"].tolist()
    else:
        source_active_values = ["Y"] * len(dataframe)

    normalized_active_values: list[str] = []
    for active_value in source_active_values:
        normalized_value = str(active_value).strip().upper()
        if normalized_value not in {"Y", "N"}:
            normalized_value = "Y"
        normalized_active_values.append(normalized_value)
    dataframe["active_flag"] = normalized_active_values

    dataframe["eagleSticksPerTruckload"] = (
        dataframe["eagleSticksPerBundle"] * dataframe["eagleBundlesPerTruckLoad"]
    ).astype(int)
    return dataframe


def _build_normalized_tables_from_csv(csv_dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    normalized_dataframe = _normalize_csv_dataframe(csv_dataframe)

    product_type_rows: list[dict] = []
    sku_rows: list[dict] = []
    bundle_rows: list[dict] = []

    product_type_id_by_name: dict[str, str] = {}
    sku_counter = 0

    for row in normalized_dataframe.to_dict(orient="records"):
        product_type_name = str(row["productType"])
        if product_type_name not in product_type_id_by_name:
            product_type_id = f"productTypeId_{len(product_type_id_by_name) + 1}"
            product_type_id_by_name[product_type_name] = product_type_id
            product_type_rows.append(
                {
                    "product_type_id": product_type_id,
                    "product_type": product_type_name,
                }
            )

        sku_counter += 1
        sku_id = f"skuId_{sku_counter}"
        sticks_per_bundle = int(float(str(row["calculatedSticksPerBundle"])))
        eagle_sticks_per_truckload = int(float(str(row["eagleSticksPerTruckload"])))
        eagle_bundles_per_truckload = int(float(str(row["eagleBundlesPerTruckLoad"])))
        calculated_bundles_per_truckload = eagle_bundles_per_truckload

        sku_rows.append(
            {
                "sku_id": sku_id,
                "product_type_id": product_type_id_by_name[product_type_name],
                "product_type": product_type_name,
                "sku": str(row["SKU"]),
                "size": str(row["size"]),
                "lingth": int(float(str(row["lingth"]))),
                "active_flag": str(row["active_flag"]),
                "display_order": int(float(str(row["displayOrder"]))),
                "popularity_score": int(float(str(row["popularityScore"]))),
                "calculated_sticks_per_bundle": sticks_per_bundle,
                "eagle_sticks_per_truckload": eagle_sticks_per_truckload,
                "eagle_bundles_per_truckload": eagle_bundles_per_truckload,
                "calculated_bundles_per_truckload": calculated_bundles_per_truckload,
            }
        )
        bundle_rows.append(
            {
                "sku_id": sku_id,
                "min_number_of_bundles": 1,
                "max_number_of_bundles": calculated_bundles_per_truckload,
            }
        )

    return pd.DataFrame(product_type_rows), pd.DataFrame(sku_rows), pd.DataFrame(bundle_rows)


def _write_version_artifacts(
    out_dir: Path,
    product_types_dataframe: pd.DataFrame,
    skus_dataframe: pd.DataFrame,
    bundles_dataframe: pd.DataFrame,
) -> dict[str, str]:
    product_types_parquet_path = out_dir / "product_types.parquet"
    skus_parquet_path = out_dir / "skus.parquet"
    bundles_parquet_path = out_dir / "bundles.parquet"
    review_csv_path = out_dir / "review_skus.csv"

    product_types_dataframe.to_parquet(product_types_parquet_path, index=False)
    skus_dataframe.to_parquet(skus_parquet_path, index=False)
    bundles_dataframe.to_parquet(bundles_parquet_path, index=False)
    skus_dataframe.to_csv(review_csv_path, index=False)

    return {
        "product_types_parquet": str(product_types_parquet_path),
        "skus_parquet": str(skus_parquet_path),
        "bundles_parquet": str(bundles_parquet_path),
        "review_csv": str(review_csv_path),
    }


def import_from_csv_text(csv_text: str, source_name: str, version: str | None = None) -> dict:
    csv_dataframe = pd.read_csv(StringIO(csv_text))
    product_types_dataframe, skus_dataframe, bundles_dataframe = _build_normalized_tables_from_csv(csv_dataframe)

    new_version = version or make_version_name()
    out_dir = get_version_dir(new_version)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_version_data(
        version=new_version,
        product_type_dataframe=product_types_dataframe,
        sku_dataframe=skus_dataframe,
        bundle_dataframe=bundles_dataframe,
    )
    artifact_paths = _write_version_artifacts(
        out_dir=out_dir,
        product_types_dataframe=product_types_dataframe,
        skus_dataframe=skus_dataframe,
        bundles_dataframe=bundles_dataframe,
    )
    pointer = set_current_version(new_version)

    metadata = {
        "version": new_version,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source": source_name,
        "rows": {
            "product_types": int(len(product_types_dataframe)),
            "skus": int(len(skus_dataframe)),
            "bundles": int(len(bundles_dataframe)),
        },
        "artifacts": artifact_paths,
    }
    metadata_path = out_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return {
        "current": pointer,
        "metadata": metadata,
        "review_csv_path": artifact_paths["review_csv"],
    }


def parse_load_js(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    prefix = "const packingData ="
    if prefix not in text:
        raise ValueError("Expected 'const packingData =' in source JS file.")

    payload = text.split(prefix, 1)[1].strip()
    if payload.endswith(";"):
        payload = payload[:-1]

    return json.loads(payload)


def normalize_packing_data(
    packing_data: dict,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    product_rows: list[dict] = []
    sku_rows: list[dict] = []
    bundle_rows: list[dict] = []

    display_order = 0
    for product_type in packing_data.get("productTypes", []):
        product_type_id = str(product_type.get("productTypeId"))
        product_type_name = str(product_type.get("productType"))
        product_rows.append(
            {
                "product_type_id": product_type_id,
                "product_type": product_type_name,
            }
        )

        skus = product_type.get("skus", {})
        for sku_id, sku in skus.items():
            display_order += 1
            sticks_per_bundle = int(float(sku.get("calculatedSticksPerBundle", 1)))
            truck_sticks = int(float(sku.get("eagleSticksPerTruckload", sticks_per_bundle)))
            bundles_per_truckload = max(1, round(truck_sticks / max(1, sticks_per_bundle)))
            sku_rows.append(
                {
                    "sku_id": str(sku_id),
                    "product_type_id": product_type_id,
                    "product_type": product_type_name,
                    "sku": str(sku.get("SKU", sku_id)),
                    "size": str(sku.get("size", "")),
                    "lingth": 0,
                    "active_flag": "Y",
                    "display_order": int(sku.get("displayOrder", display_order)),
                    "popularity_score": int(float(sku.get("popularityScore", 1))),
                    "calculated_sticks_per_bundle": sticks_per_bundle,
                    "eagle_sticks_per_truckload": truck_sticks,
                    "calculated_bundles_per_truckload": bundles_per_truckload,
                }
            )
            bundle_rows.append(
                {
                    "sku_id": str(sku_id),
                    "min_number_of_bundles": 1,
                    "max_number_of_bundles": bundles_per_truckload,
                }
            )

    return pd.DataFrame(product_rows), pd.DataFrame(sku_rows), pd.DataFrame(bundle_rows)


def import_from_load_js_file(source_path: str | None = None, version: str | None = None) -> dict:
    source = Path(source_path) if source_path else DEFAULT_JS_SOURCE
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    packing_data = parse_load_js(source)
    df_product_types, df_skus, df_bundles = normalize_packing_data(packing_data)

    new_version = version or make_version_name()
    out_dir = get_version_dir(new_version)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_version_data(
        version=new_version,
        product_type_dataframe=df_product_types,
        sku_dataframe=df_skus,
        bundle_dataframe=df_bundles,
    )
    artifact_paths = _write_version_artifacts(
        out_dir=out_dir,
        product_types_dataframe=df_product_types,
        skus_dataframe=df_skus,
        bundles_dataframe=df_bundles,
    )
    pointer = set_current_version(new_version)

    metadata = {
        "version": new_version,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source),
        "rows": {
            "product_types": int(len(df_product_types)),
            "skus": int(len(df_skus)),
            "bundles": int(len(df_bundles)),
        },
        "artifacts": artifact_paths,
    }
    metadata_path = out_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return {"current": pointer, "metadata": metadata}
