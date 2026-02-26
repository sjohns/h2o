from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loguru import logger
from rich.console import Console
from rich.table import Table

from ..config import DEFAULT_JS_SOURCE, PROJECT_ROOT
from ..data.canonical_dataset_builder import (
    build_canonical_dataset_from_legacy_js,
    write_canonical_dataset_json,
)


def parse_command_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python3 -m python_process.cloud_app.scripts.convert_legacy_js_to_canonical_json",
        description="One-time conversion from legacy load_packing_data.js to canonical JSON.",
    )
    parser.add_argument(
        "--source-js-path",
        type=Path,
        default=DEFAULT_JS_SOURCE,
        help="Path to legacy load_packing_data.js file.",
    )
    parser.add_argument(
        "--dataset-identifier",
        type=str,
        default="h2o-packing-dataset",
        help="Dataset identifier stored in canonical JSON metadata.",
    )
    parser.add_argument(
        "--output-json-path",
        type=Path,
        default=PROJECT_ROOT / "python_process" / "data" / "canonical" / "packing_dataset_v1.json",
        help="Output path for canonical JSON file.",
    )
    return parser.parse_args()


def configure_logger() -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    )


def render_conversion_summary(
    console: Console,
    source_js_path: Path,
    output_json_path: Path,
    dataset_payload: dict,
) -> None:
    summary_table = Table(title="Canonical Dataset Conversion")
    summary_table.add_column("Field", style="cyan")
    summary_table.add_column("Value", style="white")
    summary_table.add_row("Source JS", str(source_js_path.resolve()))
    summary_table.add_row("Output JSON", str(output_json_path.resolve()))
    summary_table.add_row("Schema Version", str(dataset_payload["schema_version"]))
    summary_table.add_row("Dataset Identifier", str(dataset_payload["dataset_identifier"]))
    summary_table.add_row("Generated At", str(dataset_payload["generated_at"]))
    summary_table.add_row("Product Type Count", str(dataset_payload["row_counts"]["product_types"]))
    summary_table.add_row("SKU Count", str(dataset_payload["row_counts"]["skus"]))
    summary_table.add_row("Legacy Source SHA256", str(dataset_payload["source"]["legacy_js_sha256"]))
    console.print(summary_table)


def main() -> None:
    command_line_arguments = parse_command_line_arguments()
    configure_logger()
    rich_console = Console()

    source_js_path = command_line_arguments.source_js_path
    output_json_path = command_line_arguments.output_json_path
    dataset_identifier = command_line_arguments.dataset_identifier

    if not source_js_path.exists():
        raise FileNotFoundError(f"Legacy JS source file not found: {source_js_path}")

    canonical_dataset_payload = build_canonical_dataset_from_legacy_js(
        legacy_source_file_path=source_js_path,
        dataset_identifier=dataset_identifier,
    )
    write_canonical_dataset_json(canonical_dataset_payload, output_json_path)
    render_conversion_summary(
        console=rich_console,
        source_js_path=source_js_path,
        output_json_path=output_json_path,
        dataset_payload=canonical_dataset_payload,
    )


if __name__ == "__main__":
    main()
