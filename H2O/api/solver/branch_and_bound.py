from __future__ import annotations

from math import floor, lcm
from typing import Any


def _calculate_lcm_of_array(numbers: list[int]) -> int:
    result = 1
    for num in numbers:
        result = lcm(result, num)
    return result


def _calculate_bundles_per_truckload(skus: dict[str, dict[str, Any]]) -> None:
    for sku in skus.values():
        sku["calculatedBundlesPerTruckload"] = floor(
            int(sku["eagleSticksPerTruckload"]) / int(sku["calculatedSticksPerBundle"])
        )


def _calculate_lcm_from_skus(skus: dict[str, dict[str, Any]]) -> int:
    unique_values: list[int] = []
    for sku in skus.values():
        value = int(sku["calculatedBundlesPerTruckload"])
        if value not in unique_values:
            unique_values.append(value)
    return _calculate_lcm_of_array(unique_values)


def _calculate_additional_fields(skus: dict[str, dict[str, Any]], lcm_value: int) -> None:
    for sku in skus.values():
        sku["calculatedBundleSize"] = int(lcm_value / int(sku["calculatedBundlesPerTruckload"]))


class _CalculateRatios:
    def __init__(self, skus: dict[str, dict[str, Any]]) -> None:
        self.skus = skus
        self.target_normalized = self._calculate_target_normalized_weights_by_sku()

    def _calculate_target_normalized_weights_by_sku(self) -> dict[str, float]:
        filtered_skus = list(self.skus.values())
        distinct_popularity_scores: list[int] = []
        for sku in filtered_skus:
            score = int(sku["popularityScore"])
            if score not in distinct_popularity_scores:
                distinct_popularity_scores.append(score)

        weights = [1 / score for score in distinct_popularity_scores]
        total_weight = sum(weights)
        target_normalized_weights = [weight / total_weight for weight in weights]

        out: dict[str, float] = {}
        for sku in filtered_skus:
            idx = distinct_popularity_scores.index(int(sku["popularityScore"]))
            out[sku["skuId"]] = target_normalized_weights[idx]
        return out

    def popularity_score_difference(self, sku_data: dict[str, Any]) -> dict[str, int]:
        total_sticks_per_sku: dict[str, int] = {}
        solution = sku_data["solution"]

        for sku_data_item in solution:
            sku_id = sku_data_item["skuId"]
            if sku_id in self.skus:
                sku = self.skus[sku_id]
                total_sticks = int(
                    sku_data_item.get("calculatedBundleSize", sku["calculatedSticksPerBundle"])
                ) * int(sku_data_item["numberOfBundles"])
                total_sticks_per_sku[sku_id] = total_sticks

        total_sticks = sum(total_sticks_per_sku.values())

        normalized_weights_per_sku = {
            sku_id: sticks / total_sticks for sku_id, sticks in total_sticks_per_sku.items()
        }

        difference_sum = 0
        for sku_id, weight in normalized_weights_per_sku.items():
            popularity = int(self.skus[sku_id]["popularityScore"])
            difference = round(abs(weight - self.target_normalized[sku_id]) * popularity * 10000)
            difference_sum += difference

        return {"differenceSum": int(difference_sum), "totalSticks": int(total_sticks)}


class _BranchAndBoundEngine:
    def __init__(self, skus: dict[str, dict[str, Any]], lcm_value: int, ratios_calculator: _CalculateRatios) -> None:
        self.skus = skus
        self.full_truck_size = lcm_value
        self.mod_size = 6
        self.min_fraction_where_skus_not_divisible = 0.95
        self.max_fraction_where_skus_not_divisible = 0.98
        self.bundle_constraints: dict[str, dict[str, int]] = {}
        self.initial_bundle_constraints: dict[str, dict[str, int]] = {}
        self.last_bundle_constraints: dict[str, dict[str, int]] = {}
        self.truck_size_constraints: dict[str, int] = {}
        self.ratios_calculator = ratios_calculator
        self.solutions: list[dict[str, Any]] = []
        self.current_max_truck_size = 0
        self.initial_calculation = True
        self._initialize_constraints()

    def _initialize_constraints(self) -> None:
        if len(self.skus) == 1:
            self.truck_size_constraints = {
                "minTruckSize": self.full_truck_size,
                "maxTruckSize": self.full_truck_size,
            }
        else:
            all_divisible = True
            for sku in self.skus.values():
                calculated = int(sku["calculatedBundlesPerTruckload"])
                if calculated % self.mod_size != 0:
                    all_divisible = False
                    break

            if all_divisible:
                self.truck_size_constraints = {
                    "minTruckSize": self.full_truck_size,
                    "maxTruckSize": self.full_truck_size,
                }
            else:
                self._set_truck_size_constraints(
                    self.min_fraction_where_skus_not_divisible,
                    self.max_fraction_where_skus_not_divisible,
                )

        for sku in self.skus.values():
            self.bundle_constraints[sku["skuId"]] = {
                "minNumberOfBundles": 1,
                "maxNumberOfBundles": int(sku["calculatedBundlesPerTruckload"]),
            }

        self.initial_bundle_constraints = {
            sku_id: constraints.copy() for sku_id, constraints in self.bundle_constraints.items()
        }
        self.last_bundle_constraints = {
            sku_id: constraints.copy() for sku_id, constraints in self.bundle_constraints.items()
        }

    def _set_truck_size_constraints(self, min_fraction: float, max_fraction: float) -> None:
        min_truck_size = floor(self.full_truck_size * min_fraction)
        max_truck_size = floor(self.full_truck_size * max_fraction)
        self.truck_size_constraints = {
            "minTruckSize": int(min_truck_size),
            "maxTruckSize": int(max_truck_size),
        }

    def _count_bundles_per_sku(self, solution: list[dict[str, int]]) -> dict[str, int]:
        sku_bundles_count: dict[str, int] = {}
        for item in solution:
            sku_id = item["skuId"]
            if sku_id not in sku_bundles_count:
                sku_bundles_count[sku_id] = 0
            sku_bundles_count[sku_id] += int(item["numberOfBundles"])
            self._validate_bundle_constraints(item)
        return sku_bundles_count

    def _validate_bundle_constraints(self, item: dict[str, int]) -> None:
        constraints = self.bundle_constraints[item["skuId"]]
        bundles = int(item["numberOfBundles"])
        if bundles < constraints["minNumberOfBundles"] or bundles > constraints["maxNumberOfBundles"]:
            raise ValueError(f"Number of bundles for skuId {item['skuId']} is out of bounds.")

    def _check_bundles_per_sku_constraints(self, solution: list[dict[str, int]]) -> bool:
        sku_bundles = self._count_bundles_per_sku(solution)
        for sku_id, count in sku_bundles.items():
            constraints = self.bundle_constraints[sku_id]
            if count < constraints["minNumberOfBundles"] or count > constraints["maxNumberOfBundles"]:
                return False
        return True

    def _is_valid_solution(self, solution: list[dict[str, int]], total_size: int) -> bool:
        return (
            self._check_bundles_per_sku_constraints(solution)
            and total_size >= self.truck_size_constraints["minTruckSize"]
            and total_size <= self.truck_size_constraints["maxTruckSize"]
        )

    def _find_sku_combinations(
        self, sku_ids: list[str], solution: list[dict[str, int]], total_size: int
    ) -> None:
        if len(sku_ids) == 0:
            if total_size < self.current_max_truck_size:
                return
            self.current_max_truck_size = total_size
            if self._is_valid_solution(solution, total_size):
                self.solutions.append(
                    {"solution": [item.copy() for item in solution], "totalSize": int(total_size)}
                )
            self.solutions = [
                sol for sol in self.solutions if int(sol["totalSize"]) >= self.current_max_truck_size
            ]
            return

        sku_id = sku_ids[0]
        remaining = sku_ids[1:]
        constraints = self.bundle_constraints[sku_id]
        sku_info = self.skus[sku_id]

        for number_of_bundles in range(
            int(constraints["minNumberOfBundles"]), int(constraints["maxNumberOfBundles"]) + 1
        ):
            new_size = total_size + number_of_bundles * int(sku_info["calculatedBundleSize"])
            if new_size > self.truck_size_constraints["maxTruckSize"]:
                break
            solution.append({"skuId": sku_id, "numberOfBundles": int(number_of_bundles)})
            self._find_sku_combinations(remaining, solution, int(new_size))
            solution.pop()

    def _find_all_solutions(self) -> list[dict[str, Any]]:
        self.solutions = []
        self.current_max_truck_size = 0
        all_sku_ids = list(self.bundle_constraints.keys())
        self._find_sku_combinations(all_sku_ids, [], 0)
        self.solutions = [
            solution
            for solution in self.solutions
            if int(solution["totalSize"]) >= self.current_max_truck_size
        ]

        if len(self.solutions) < 1 and not self.initial_calculation:
            self.bundle_constraints = {
                sku_id: constraints.copy() for sku_id, constraints in self.last_bundle_constraints.items()
            }
            return self.best_solution()["solution"]  # mirrors JS fallback branch

        return self.solutions

    def _find_optimal_solution(self) -> dict[str, Any]:
        if len(self.solutions) == 0:
            raise ValueError("No solutions available")

        if len(self.solutions) == 1:
            return self.solutions[0]

        min_difference = float("inf")
        for solution in self.solutions:
            score = self.ratios_calculator.popularity_score_difference(solution)
            solution["differenceSum"] = int(score["differenceSum"])
            solution["totalSticks"] = int(score["totalSticks"])
            if solution["differenceSum"] < min_difference:
                min_difference = solution["differenceSum"]

        self.solutions = [s for s in self.solutions if s.get("differenceSum") == min_difference]

        if len(self.solutions) == 1:
            return self.solutions[0]

        max_total_sticks = max(int(s.get("totalSticks", 0)) for s in self.solutions)
        self.solutions = [s for s in self.solutions if int(s.get("totalSticks", 0)) == max_total_sticks]

        if len(self.solutions) == 0:
            raise ValueError("No solutions available")

        return self.solutions[0]

    def best_solution(self) -> dict[str, Any]:
        self._find_all_solutions()
        optimal = self._find_optimal_solution()
        self.last_bundle_constraints = {
            sku_id: constraints.copy() for sku_id, constraints in self.bundle_constraints.items()
        }
        self.initial_calculation = False
        return optimal

    def calculate_truck_size(self, solution: list[dict[str, int]]) -> int:
        total = 0
        for item in solution:
            sku = self.skus[item["skuId"]]
            total += int(sku["calculatedBundleSize"]) * int(item["numberOfBundles"])
        return int(total)


def solve(order: Any, sku_data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if hasattr(order, "model_dump"):
        order_dict = order.model_dump()
    elif isinstance(order, dict):
        order_dict = order
    else:
        raise TypeError("order must be dict-like")

    items = order_dict.get("items", [])
    if not items:
        raise ValueError("Order has no items")

    selected_ids: list[str] = []
    for item in items:
        sku_id = item["sku_id"] if isinstance(item, dict) else item.sku_id
        if sku_id not in selected_ids:
            selected_ids.append(sku_id)

    selected_id_set = set(selected_ids)
    selected_skus: dict[str, dict[str, Any]] = {}
    for sku_id, sku in sku_data.items():
        if sku_id in selected_id_set:
            selected_skus[sku_id] = sku.copy()

    _calculate_bundles_per_truckload(selected_skus)
    lcm_value = _calculate_lcm_from_skus(selected_skus)
    _calculate_additional_fields(selected_skus, lcm_value)

    ratios_calculator = _CalculateRatios(selected_skus)
    engine = _BranchAndBoundEngine(selected_skus, lcm_value, ratios_calculator)
    optimal_solution_obj = engine.best_solution()
    solution = optimal_solution_obj["solution"]
    total_size = int(optimal_solution_obj.get("totalSize", engine.calculate_truck_size(solution)))

    solution_with_totals = [item.copy() for item in solution]
    score = ratios_calculator.popularity_score_difference({"solution": solution_with_totals})

    return {
        "skus": selected_skus,
        "solution": [
            {
                "skuId": s["skuId"],
                "numberOfBundles": int(s["numberOfBundles"]),
                "totalSticks": int(selected_skus[s["skuId"]]["calculatedSticksPerBundle"])
                * int(s["numberOfBundles"]),
            }
            for s in solution_with_totals
        ],
        "lcmValue": int(lcm_value),
        "minTruckSize": int(engine.truck_size_constraints["minTruckSize"]),
        "maxTruckSize": int(engine.truck_size_constraints["maxTruckSize"]),
        "totalSize": int(total_size),
        "totalSticks": int(score["totalSticks"]),
        "differenceSum": int(score["differenceSum"]),
    }
