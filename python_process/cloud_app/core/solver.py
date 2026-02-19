import math

import pandas as pd

from python_process.cloud_app.core.lcm import calculate_lcm_from_rows
from python_process.cloud_app.core.ratios import calculate_target_weights, score_solution


def _build_solver_rows(df: pd.DataFrame) -> list[dict]:
    rows: list[dict] = []
    for _, r in df.iterrows():
        sticks_per_bundle = max(1, int(r["calculated_sticks_per_bundle"]))
        bundles_per_truckload = max(1, int(r["calculated_bundles_per_truckload"]))
        bundle_size = 0
        row = {
            "sku_id": str(r["sku_id"]),
            "sku": str(r["sku"]),
            "popularity_score": max(1, int(r["popularity_score"])),
            "sticks_per_bundle": sticks_per_bundle,
            "bundles_per_truckload": bundles_per_truckload,
            "bundle_size": bundle_size,
        }
        rows.append(row)
    return rows


def _assign_bundle_sizes(rows: list[dict], lcm: int) -> None:
    for row in rows:
        row["bundle_size"] = max(1, int(lcm // row["bundles_per_truckload"]))


def _get_truck_constraints(rows: list[dict], full_truck_size: int, truck_fill_ratio: float) -> dict:
    if len(rows) == 1:
        min_truck_size = full_truck_size
        max_truck_size = full_truck_size
    else:
        all_divisible_by_six = True
        for row in rows:
            if row["bundles_per_truckload"] % 6 != 0:
                all_divisible_by_six = False
                break

        if all_divisible_by_six:
            min_truck_size = full_truck_size
            max_truck_size = full_truck_size
        else:
            min_truck_size = math.floor(full_truck_size * 0.95)
            max_truck_size = math.floor(full_truck_size * 0.98)

    if truck_fill_ratio < 1.0:
        min_truck_size = math.floor(min_truck_size * truck_fill_ratio)
        max_truck_size = math.floor(max_truck_size * truck_fill_ratio)

    min_truck_size = max(1, min_truck_size)
    max_truck_size = max(min_truck_size, max_truck_size)
    return {
        "min_truck_size": min_truck_size,
        "max_truck_size": max_truck_size,
    }


def _get_bundle_constraints(rows: list[dict], truck_fill_ratio: float) -> dict:
    constraints: dict = {}
    for row in rows:
        max_bundles = max(1, int(math.floor(row["bundles_per_truckload"] * truck_fill_ratio)))
        constraints[row["sku_id"]] = {
            "min_number_of_bundles": 1,
            "max_number_of_bundles": max_bundles,
        }
    return constraints


def _apply_bundle_overrides(
    bundle_constraints: dict,
    fixed_bundles: dict[str, int],
    min_bundles: dict[str, int],
    max_bundles: dict[str, int],
) -> dict:
    adjusted: dict = {}
    for sku_id, constraint in bundle_constraints.items():
        min_value = int(constraint["min_number_of_bundles"])
        max_value = int(constraint["max_number_of_bundles"])

        if sku_id in min_bundles:
            min_value = max(1, int(min_bundles[sku_id]))
        if sku_id in max_bundles:
            max_value = max(1, int(max_bundles[sku_id]))
        if sku_id in fixed_bundles:
            fixed_value = max(1, int(fixed_bundles[sku_id]))
            min_value = fixed_value
            max_value = fixed_value

        if min_value > max_value:
            raise ValueError(f"Invalid bundle override for {sku_id}: min > max")

        adjusted[sku_id] = {
            "min_number_of_bundles": min_value,
            "max_number_of_bundles": max_value,
        }

    return adjusted


def _calculate_truck_size(solution: list[dict], rows_by_id: dict) -> int:
    total = 0
    for item in solution:
        sku_id = item["sku_id"]
        row = rows_by_id[sku_id]
        total += int(item["number_of_bundles"]) * int(row["bundle_size"])
    return total


def _search(
    sku_ids: list[str],
    index: int,
    running_solution: list[dict],
    running_size: int,
    rows_by_id: dict,
    bundle_constraints: dict,
    truck_constraints: dict,
    state: dict,
) -> None:
    if running_size > truck_constraints["max_truck_size"]:
        return

    if index >= len(sku_ids):
        if running_size < truck_constraints["min_truck_size"]:
            return
        if running_size < state["best_size"]:
            return
        if running_size > state["best_size"]:
            state["best_size"] = running_size
            state["candidates"] = []
        state["candidates"].append([item.copy() for item in running_solution])
        return

    sku_id = sku_ids[index]
    row = rows_by_id[sku_id]
    constraint = bundle_constraints[sku_id]
    min_bundles = int(constraint["min_number_of_bundles"])
    max_bundles = int(constraint["max_number_of_bundles"])
    bundle_size = int(row["bundle_size"])

    for number_of_bundles in range(min_bundles, max_bundles + 1):
        new_size = running_size + (number_of_bundles * bundle_size)
        if new_size > truck_constraints["max_truck_size"]:
            break
        running_solution.append(
            {"sku_id": sku_id, "number_of_bundles": int(number_of_bundles)}
        )
        _search(
            sku_ids=sku_ids,
            index=index + 1,
            running_solution=running_solution,
            running_size=new_size,
            rows_by_id=rows_by_id,
            bundle_constraints=bundle_constraints,
            truck_constraints=truck_constraints,
            state=state,
        )
        running_solution.pop()


def _pick_best_solution(candidates: list[list[dict]], rows_by_id: dict, target_weights: dict) -> dict:
    if not candidates:
        raise ValueError("No solutions available for current constraints.")

    best_solution = candidates[0]
    best_score, best_total_sticks = score_solution(best_solution, rows_by_id, target_weights)

    for candidate in candidates[1:]:
        score, total_sticks = score_solution(candidate, rows_by_id, target_weights)
        if score < best_score:
            best_solution = candidate
            best_score = score
            best_total_sticks = total_sticks
            continue
        if score == best_score and total_sticks > best_total_sticks:
            best_solution = candidate
            best_score = score
            best_total_sticks = total_sticks

    total_truck_size = _calculate_truck_size(best_solution, rows_by_id)
    solution_output: list[dict] = []
    for item in best_solution:
        sku_id = item["sku_id"]
        row = rows_by_id[sku_id]
        number_of_bundles = int(item["number_of_bundles"])
        sticks_per_bundle = int(row["sticks_per_bundle"])
        total_sticks = int(number_of_bundles * sticks_per_bundle)
        solution_output.append(
            {
                "sku_id": sku_id,
                "sku": row["sku"],
                "number_of_bundles": number_of_bundles,
                "sticks_per_bundle": sticks_per_bundle,
                "total_sticks": total_sticks,
            }
        )

    return {
        "total_truck_size": int(total_truck_size),
        "total_sticks": int(best_total_sticks),
        "solution": solution_output,
    }


def solve(
    sku_df: pd.DataFrame,
    selected_sku_ids: list[str],
    truck_fill_ratio: float,
    fixed_bundles: dict[str, int] | None = None,
    min_bundles: dict[str, int] | None = None,
    max_bundles: dict[str, int] | None = None,
) -> dict:
    if not selected_sku_ids:
        raise ValueError("selected_sku_ids is required.")

    working_df = sku_df.copy()
    selected = set(selected_sku_ids)
    working_df = working_df[working_df["sku_id"].isin(selected)]

    if working_df.empty:
        raise ValueError("No matching SKUs found for request.")

    rows = _build_solver_rows(working_df)
    lcm = calculate_lcm_from_rows(rows)
    _assign_bundle_sizes(rows, lcm)
    rows_by_id = {row["sku_id"]: row for row in rows}
    truck_constraints = _get_truck_constraints(rows, lcm, truck_fill_ratio)
    bundle_constraints = _get_bundle_constraints(rows, truck_fill_ratio)
    safe_fixed = fixed_bundles or {}
    safe_min = min_bundles or {}
    safe_max = max_bundles or {}
    bundle_constraints = _apply_bundle_overrides(
        bundle_constraints=bundle_constraints,
        fixed_bundles=safe_fixed,
        min_bundles=safe_min,
        max_bundles=safe_max,
    )
    sku_ids = [row["sku_id"] for row in rows]
    target_weights = calculate_target_weights(rows)

    search_state = {"best_size": 0, "candidates": []}
    _search(
        sku_ids=sku_ids,
        index=0,
        running_solution=[],
        running_size=0,
        rows_by_id=rows_by_id,
        bundle_constraints=bundle_constraints,
        truck_constraints=truck_constraints,
        state=search_state,
    )

    picked = _pick_best_solution(
        candidates=search_state["candidates"],
        rows_by_id=rows_by_id,
        target_weights=target_weights,
    )

    return {
        "lcm": int(lcm),
        "total_truck_size": int(picked["total_truck_size"]),
        "total_sticks": int(picked["total_sticks"]),
        "solution": picked["solution"],
    }
