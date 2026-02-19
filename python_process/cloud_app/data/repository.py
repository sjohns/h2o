from pathlib import Path

import duckdb
import pandas as pd

from python_process.cloud_app.data.versioning import get_version_dir


def get_skus_parquet_path(version: str) -> Path:
    base_dir = get_version_dir(version)
    return base_dir / "skus.parquet"


def get_product_types_parquet_path(version: str) -> Path:
    base_dir = get_version_dir(version)
    return base_dir / "product_types.parquet"


def get_bundles_parquet_path(version: str) -> Path:
    base_dir = get_version_dir(version)
    return base_dir / "bundles.parquet"


def load_skus(version: str) -> pd.DataFrame:
    skus_parquet = get_skus_parquet_path(version)
    if not skus_parquet.exists():
        raise FileNotFoundError(f"Missing {skus_parquet}")

    con = duckdb.connect()
    try:
        df = con.execute(
            "SELECT * FROM read_parquet(?) ORDER BY display_order",
            [str(skus_parquet)],
        ).df()
    finally:
        con.close()

    return df


def write_parquet(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_df = df.copy()
    for column in write_df.columns:
        if pd.api.types.is_string_dtype(write_df[column]):
            write_df[column] = write_df[column].astype("object")
    con = duckdb.connect()
    try:
        con.register("df_view", write_df)
        con.execute("COPY df_view TO ? (FORMAT PARQUET)", [str(output_path)])
    finally:
        con.close()
