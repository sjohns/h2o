#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.data import flatten_skus, load_snapshot  # noqa: E402
from api.solver.branch_and_bound import solve  # noqa: E402

ORDERS_PATH = ROOT / "api" / "tests" / "harness" / "orders.json"
EXPECTED_PATH = ROOT / "api" / "tests" / "harness" / "expected_results.json"
ORDERS_HISTORICAL_PATH = ROOT / "api" / "tests" / "harness" / "orders_historical.json"
EXPECTED_HISTORICAL_PATH = ROOT / "api" / "tests" / "harness" / "expected_historical.json"
SNAPSHOT_PATH = ROOT / "api" / "data" / "packing_data.json"

COMPARE_FIELDS = [
    "solution",
    "totalSize",
    "totalSticks",
    "lcmValue",
    "minTruckSize",
    "maxTruckSize",
    "differenceSum",
]


def _normalize_solution(solution: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for row in solution:
        normalized.append(
            {
                "skuId": row["skuId"],
                "numberOfBundles": int(row["numberOfBundles"]),
            }
        )
    return sorted(normalized, key=lambda x: x["skuId"])


def _load_orders(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_expected(path: Path) -> dict[str, dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_sku_data() -> dict[str, dict[str, Any]]:
    snapshot = load_snapshot(SNAPSHOT_PATH)
    return {sku["skuId"]: sku for sku in flatten_skus(snapshot)}


def _actual_results(orders: list[dict[str, Any]], sku_data: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for order in orders:
        order_id = order["order_id"]
        out[order_id] = solve({"items": order["items"]}, sku_data)
    return out


def run_harness(orders_path: Path = ORDERS_PATH, expected_path: Path = EXPECTED_PATH) -> dict[str, Any]:
    orders = _load_orders(orders_path)
    expected = _load_expected(expected_path)
    sku_data = _load_sku_data()
    actual = _actual_results(orders, sku_data)

    mismatches: list[dict[str, Any]] = []
    max_size_diff = 0
    max_sticks_diff = 0

    for order in orders:
        order_id = order["order_id"]
        expected_result = expected.get(order_id)
        actual_result = actual.get(order_id)

        if expected_result is None:
            mismatches.append({"order_id": order_id, "reason": "missing_expected_result"})
            continue

        field_diffs: dict[str, Any] = {}
        for field in COMPARE_FIELDS:
            actual_value = actual_result[field]
            expected_value = expected_result[field]
            if field == "solution":
                actual_value = _normalize_solution(actual_value)
                expected_value = _normalize_solution(expected_value)

            if actual_value != expected_value:
                field_diffs[field] = {
                    "expected": expected_value,
                    "actual": actual_value,
                }

        size_diff = abs(int(actual_result["totalSize"]) - int(expected_result["totalSize"]))
        sticks_diff = abs(int(actual_result["totalSticks"]) - int(expected_result["totalSticks"]))
        max_size_diff = max(max_size_diff, size_diff)
        max_sticks_diff = max(max_sticks_diff, sticks_diff)

        if field_diffs:
            mismatches.append({"order_id": order_id, "field_diffs": field_diffs})

    total_orders = len(orders)
    mismatch_count = len(mismatches)

    return {
        "total_orders": total_orders,
        "exact_matches": total_orders - mismatch_count,
        "mismatches": mismatch_count,
        "max_size_diff": max_size_diff,
        "max_sticks_diff": max_sticks_diff,
        "details": mismatches,
    }


def regenerate_expected(orders_path: Path = ORDERS_PATH, expected_path: Path = EXPECTED_PATH) -> None:
    orders = _load_orders(orders_path)
    sku_data = _load_sku_data()
    expected = _actual_results(orders, sku_data)
    with expected_path.open("w", encoding="utf-8") as f:
        json.dump(expected, f, indent=2)


def _print_summary(summary: dict[str, Any]) -> None:
    print(f"total_orders: {summary['total_orders']}")
    print(f"exact_matches: {summary['exact_matches']}")
    print(f"mismatches: {summary['mismatches']}")
    print(f"max_size_diff: {summary['max_size_diff']}")
    print(f"max_sticks_diff: {summary['max_sticks_diff']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run solver harness against expected outputs.")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate expected_results.json from current solver.")
    parser.add_argument(
        "--historical",
        action="store_true",
        help="Run harness using historical JS parity dataset and expected outputs.",
    )
    args = parser.parse_args()

    orders_path = ORDERS_HISTORICAL_PATH if args.historical else ORDERS_PATH
    expected_path = EXPECTED_HISTORICAL_PATH if args.historical else EXPECTED_PATH

    if args.regenerate:
        if args.historical:
            raise SystemExit("--regenerate is not allowed with --historical")
        regenerate_expected(orders_path=orders_path, expected_path=expected_path)
        print(f"Regenerated {expected_path}")
        return

    summary = run_harness(orders_path=orders_path, expected_path=expected_path)
    _print_summary(summary)
    if summary["mismatches"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
