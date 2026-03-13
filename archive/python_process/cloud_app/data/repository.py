from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from ..config import SQLITE_DB_PATH


def _get_connection() -> sqlite3.Connection:
    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(SQLITE_DB_PATH))
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_schema() -> None:
    connection = _get_connection()
    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS product_types (
                version TEXT NOT NULL,
                product_type_id TEXT NOT NULL,
                product_type TEXT NOT NULL,
                PRIMARY KEY (version, product_type_id),
                UNIQUE (version, product_type)
            );

            CREATE TABLE IF NOT EXISTS skus (
                version TEXT NOT NULL,
                sku_id TEXT NOT NULL,
                product_type_id TEXT NOT NULL,
                product_type TEXT NOT NULL,
                sku TEXT NOT NULL,
                size TEXT NOT NULL,
                lingth INTEGER NOT NULL DEFAULT 0,
                active_flag TEXT NOT NULL DEFAULT 'Y',
                display_order INTEGER NOT NULL,
                popularity_score INTEGER NOT NULL,
                calculated_sticks_per_bundle INTEGER NOT NULL,
                eagle_sticks_per_truckload INTEGER NOT NULL,
                eagle_bundles_per_truckload INTEGER,
                calculated_bundles_per_truckload INTEGER NOT NULL,
                PRIMARY KEY (version, sku_id),
                UNIQUE (version, display_order),
                CHECK (display_order > 0),
                CHECK (popularity_score >= 0),
                CHECK (calculated_sticks_per_bundle >= 0),
                CHECK (eagle_sticks_per_truckload >= 0),
                CHECK (calculated_bundles_per_truckload >= 0),
                CHECK (lingth >= 0),
                CHECK (active_flag IN ('Y', 'N')),
                FOREIGN KEY (version, product_type_id)
                    REFERENCES product_types(version, product_type_id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS bundles (
                version TEXT NOT NULL,
                sku_id TEXT NOT NULL,
                min_number_of_bundles INTEGER NOT NULL,
                max_number_of_bundles INTEGER NOT NULL,
                PRIMARY KEY (version, sku_id),
                FOREIGN KEY (version, sku_id)
                    REFERENCES skus(version, sku_id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CHECK (min_number_of_bundles > 0),
                CHECK (max_number_of_bundles >= min_number_of_bundles)
            );
            """
        )
        existing_columns = {
            str(row[1]) for row in connection.execute("PRAGMA table_info('skus')").fetchall()
        }
        if "lingth" not in existing_columns:
            connection.execute("ALTER TABLE skus ADD COLUMN lingth INTEGER NOT NULL DEFAULT 0")
        if "active_flag" not in existing_columns:
            connection.execute("ALTER TABLE skus ADD COLUMN active_flag TEXT NOT NULL DEFAULT 'Y'")
        connection.commit()
    finally:
        connection.close()


def _require_columns(dataframe: pd.DataFrame, required_columns: list[str], table_name: str) -> None:
    missing_columns = [column_name for column_name in required_columns if column_name not in dataframe.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for {table_name}: {missing_columns}")


def write_version_data(
    version: str,
    product_type_dataframe: pd.DataFrame,
    sku_dataframe: pd.DataFrame,
    bundle_dataframe: pd.DataFrame,
) -> None:
    _require_columns(product_type_dataframe, ["product_type_id", "product_type"], "product_types")
    _require_columns(
        sku_dataframe,
        [
            "sku_id",
            "product_type_id",
            "product_type",
            "sku",
            "size",
            "lingth",
            "active_flag",
            "display_order",
            "popularity_score",
            "calculated_sticks_per_bundle",
            "eagle_sticks_per_truckload",
            "calculated_bundles_per_truckload",
        ],
        "skus",
    )
    _require_columns(bundle_dataframe, ["sku_id", "min_number_of_bundles", "max_number_of_bundles"], "bundles")

    initialize_schema()
    connection = _get_connection()
    try:
        connection.execute("BEGIN")
        connection.execute("DELETE FROM bundles WHERE version = ?", (version,))
        connection.execute("DELETE FROM skus WHERE version = ?", (version,))
        connection.execute("DELETE FROM product_types WHERE version = ?", (version,))

        product_type_rows = [
            (version, str(row["product_type_id"]), str(row["product_type"]))
            for row in product_type_dataframe.to_dict(orient="records")
        ]
        connection.executemany(
            "INSERT INTO product_types (version, product_type_id, product_type) VALUES (?, ?, ?)",
            product_type_rows,
        )

        sku_rows: list[tuple[object, ...]] = []
        for row in sku_dataframe.to_dict(orient="records"):
            eagle_bundles_per_truckload = row.get("eagle_bundles_per_truckload")
            sqlite_eagle_bundles_per_truckload = (
                int(eagle_bundles_per_truckload)
                if eagle_bundles_per_truckload is not None and pd.notna(eagle_bundles_per_truckload)
                else None
            )
            sku_rows.append(
                (
                    version,
                    str(row["sku_id"]),
                    str(row["product_type_id"]),
                    str(row["product_type"]),
                    str(row["sku"]),
                    str(row["size"]),
                    int(row["lingth"]),
                    str(row["active_flag"]),
                    int(row["display_order"]),
                    int(row["popularity_score"]),
                    int(row["calculated_sticks_per_bundle"]),
                    int(row["eagle_sticks_per_truckload"]),
                    sqlite_eagle_bundles_per_truckload,
                    int(row["calculated_bundles_per_truckload"]),
                )
            )
        connection.executemany(
            """
            INSERT INTO skus (
                version,
                sku_id,
                product_type_id,
                product_type,
                sku,
                size,
                lingth,
                active_flag,
                display_order,
                popularity_score,
                calculated_sticks_per_bundle,
                eagle_sticks_per_truckload,
                eagle_bundles_per_truckload,
                calculated_bundles_per_truckload
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            sku_rows,
        )

        bundle_rows = [
            (
                version,
                str(row["sku_id"]),
                int(row["min_number_of_bundles"]),
                int(row["max_number_of_bundles"]),
            )
            for row in bundle_dataframe.to_dict(orient="records")
        ]
        connection.executemany(
            "INSERT INTO bundles (version, sku_id, min_number_of_bundles, max_number_of_bundles) VALUES (?, ?, ?, ?)",
            bundle_rows,
        )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def load_product_types(version: str) -> pd.DataFrame:
    initialize_schema()
    connection = _get_connection()
    try:
        dataframe = pd.read_sql_query(
            "SELECT product_type_id, product_type FROM product_types WHERE version = ? ORDER BY product_type_id",
            connection,
            params=[version],
        )
    finally:
        connection.close()
    if dataframe.empty:
        raise FileNotFoundError(f"No product_types found for version '{version}' in SQLite store.")
    return dataframe


def load_skus(version: str) -> pd.DataFrame:
    initialize_schema()
    connection = _get_connection()
    try:
        dataframe = pd.read_sql_query(
            """
            SELECT
                sku_id,
                product_type_id,
                product_type,
                sku,
                size,
                lingth,
                active_flag,
                display_order,
                popularity_score,
                calculated_sticks_per_bundle,
                eagle_sticks_per_truckload,
                eagle_bundles_per_truckload,
                calculated_bundles_per_truckload
            FROM skus
            WHERE version = ?
            ORDER BY display_order
            """,
            connection,
            params=[version],
        )
    finally:
        connection.close()
    if dataframe.empty:
        raise FileNotFoundError(f"No skus found for version '{version}' in SQLite store.")
    return dataframe


def load_bundles(version: str) -> pd.DataFrame:
    initialize_schema()
    connection = _get_connection()
    try:
        dataframe = pd.read_sql_query(
            "SELECT sku_id, min_number_of_bundles, max_number_of_bundles FROM bundles WHERE version = ? ORDER BY sku_id",
            connection,
            params=[version],
        )
    finally:
        connection.close()
    if dataframe.empty:
        raise FileNotFoundError(f"No bundles found for version '{version}' in SQLite store.")
    return dataframe


def get_sqlite_db_path() -> Path:
    return SQLITE_DB_PATH


def list_versions() -> list[str]:
    initialize_schema()
    connection = _get_connection()
    try:
        rows = connection.execute(
            """
            SELECT version
            FROM skus
            GROUP BY version
            ORDER BY version DESC
            """
        ).fetchall()
    finally:
        connection.close()
    return [str(row[0]) for row in rows]


def get_version_counts(version: str) -> dict[str, int]:
    initialize_schema()
    connection = _get_connection()
    try:
        product_types_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM product_types WHERE version = ?",
                (version,),
            ).fetchone()[0]
        )
        skus_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM skus WHERE version = ?",
                (version,),
            ).fetchone()[0]
        )
        bundles_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM bundles WHERE version = ?",
                (version,),
            ).fetchone()[0]
        )
    finally:
        connection.close()
    return {
        "product_types": product_types_count,
        "skus": skus_count,
        "bundles": bundles_count,
    }
