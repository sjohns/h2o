#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PARITY_CASES = ROOT.parent / "python_process" / "cloud_app" / "tests" / "parity_cases.json"
JS_RUNNER = ROOT / "api" / "tests" / "js_solver_runner.js"
ORDERS_HISTORICAL = ROOT / "api" / "tests" / "harness" / "orders_historical.json"
EXPECTED_HISTORICAL = ROOT / "api" / "tests" / "harness" / "expected_historical.json"


def _js_solve(selected_ids: list[str]) -> dict:
    proc = subprocess.run(
        ["node", str(JS_RUNNER), json.dumps(selected_ids)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def main() -> None:
    cases = json.loads(PARITY_CASES.read_text(encoding="utf-8"))

    orders = []
    expected = {}

    for case in cases:
        order_id = case["name"]
        selected_ids = case["selected_sku_ids"]

        orders.append(
            {
                "order_id": order_id,
                "items": [{"sku_id": sku_id, "quantity": 1} for sku_id in selected_ids],
            }
        )

        expected[order_id] = _js_solve(selected_ids)

    ORDERS_HISTORICAL.write_text(json.dumps(orders, indent=2), encoding="utf-8")
    EXPECTED_HISTORICAL.write_text(json.dumps(expected, indent=2), encoding="utf-8")

    print(f"Wrote {ORDERS_HISTORICAL}")
    print(f"Wrote {EXPECTED_HISTORICAL}")


if __name__ == "__main__":
    main()
