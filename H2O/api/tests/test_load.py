"""
Load test: 1000 concurrent simulated users, each with a random SKU selection
and ~50 random increase/decrease adjustments via the /pack API.
"""

import asyncio
import random

import httpx
import pytest

from api.app import app

CONCURRENCY = 1000
ACTIONS_PER_USER = 50


def _apply_constraint_update(bundle_constraints, initial_constraints, sku_id, action, current_bundles):
    """Mirror of ApiEngine._updateConstraints — returns updated constraints dict."""
    constraints = {k: dict(v) for k, v in bundle_constraints.items()}
    init_min = initial_constraints[sku_id]["min_bundles"]
    init_max = initial_constraints[sku_id]["max_bundles"]

    if action == "increase":
        if current_bundles < init_max:
            constraints[sku_id]["min_bundles"] = max(0, current_bundles + 1)
            constraints[sku_id]["max_bundles"] = init_max
    elif action == "decrease":
        if current_bundles > init_min:
            constraints[sku_id]["max_bundles"] = max(0, current_bundles - 1)
            constraints[sku_id]["min_bundles"] = init_min

    return constraints


async def _simulate_user(client, all_skus, user_id):
    """One simulated user: create order, initial pack, then ACTIONS_PER_USER adjustments."""
    selected = random.sample(all_skus, random.randint(1, min(5, len(all_skus))))
    sku_ids = [s["skuId"] for s in selected]

    # Create order
    r = await client.post("/orders", json={"items": [{"sku_id": sid, "quantity": 1} for sid in sku_ids]})
    assert r.status_code == 200, f"user {user_id}: POST /orders returned {r.status_code}"
    order_id = r.json()["order_id"]

    # Initial pack
    r = await client.post("/pack", json={"order_id": order_id})
    assert r.status_code == 200, f"user {user_id}: initial POST /pack returned {r.status_code}"
    result = r.json()["packing_result"]

    # Initialise constraint tracking
    bundle_constraints = {}
    initial_constraints = {}
    last_constraints = {}
    for sku_id, sku_data in result["skus"].items():
        max_b = int(sku_data["calculatedBundlesPerTruckload"])
        bundle_constraints[sku_id] = {"min_bundles": 1, "max_bundles": max_b}
        initial_constraints[sku_id] = {"min_bundles": 1, "max_bundles": max_b}
        last_constraints[sku_id] = {"min_bundles": 1, "max_bundles": max_b}

    current_bundles = {item["skuId"]: item["numberOfBundles"] for item in result["solution"]}

    ok_count = 0
    no_solution_count = 0

    for _ in range(ACTIONS_PER_USER):
        sku_id = random.choice(sku_ids)
        action = random.choice(["increase", "decrease"])
        bundles = current_bundles.get(sku_id, 1)

        new_constraints = _apply_constraint_update(
            bundle_constraints, initial_constraints, sku_id, action, bundles
        )

        r = await client.post("/pack", json={"orderId": order_id, "bundleConstraints": new_constraints})

        if r.status_code == 200:
            result = r.json()["packing_result"]
            bundle_constraints = new_constraints
            last_constraints = {k: dict(v) for k, v in bundle_constraints.items()}
            current_bundles = {item["skuId"]: item["numberOfBundles"] for item in result["solution"]}
            ok_count += 1
        elif r.status_code == 400:
            # No valid solution for these constraints — revert, same as browser does
            bundle_constraints = {k: dict(v) for k, v in last_constraints.items()}
            no_solution_count += 1
        else:
            pytest.fail(f"user {user_id}: unexpected status {r.status_code} from POST /pack")

    return {"ok": ok_count, "no_solution": no_solution_count}


async def _run_all_users():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver", timeout=60.0) as client:
        skus = (await client.get("/skus")).json()["skus"]
        tasks = [_simulate_user(client, skus, i) for i in range(CONCURRENCY)]
        return await asyncio.gather(*tasks)


def test_load_1000_concurrent_users():
    results = asyncio.run(_run_all_users())

    total_ok = sum(r["ok"] for r in results)
    total_no_solution = sum(r["no_solution"] for r in results)
    total_actions = total_ok + total_no_solution

    print(f"\n{'─' * 50}")
    print(f"Users:              {CONCURRENCY}")
    print(f"Actions per user:   {ACTIONS_PER_USER}")
    print(f"Total actions:      {total_actions}")
    print(f"Solved OK:          {total_ok}  ({100 * total_ok / total_actions:.1f}%)")
    print(f"No solution (400):  {total_no_solution}  ({100 * total_no_solution / total_actions:.1f}%)")
    print(f"{'─' * 50}")

    # Every user must complete without exceptions
    assert len(results) == CONCURRENCY
    # Majority of actions should resolve successfully
    assert total_ok / total_actions >= 0.5, f"Too many solver failures: {total_no_solution}/{total_actions}"
