from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from math import floor, lcm
from typing import Dict, List, Tuple

from .models import PackingResult, SKU


def calculate_lcm_of_array(numbers: List[int]) -> int:
    return reduce(lcm, numbers, 1)


def enrich_skus(selected_skus: Dict[str, SKU]) -> Tuple[Dict[str, SKU], int]:
    unique_bundles: List[int] = []
    seen = set()

    for sku in selected_skus.values():
        calculated_bundles = floor(sku.eagleSticksPerTruckload / sku.calculatedSticksPerBundle)
        sku.calculatedBundlesPerTruckload = calculated_bundles
        if calculated_bundles not in seen:
            seen.add(calculated_bundles)
            unique_bundles.append(calculated_bundles)

    lcm_value = calculate_lcm_of_array(unique_bundles)

    for sku in selected_skus.values():
        sku.calculatedBundleSize = lcm_value // int(sku.calculatedBundlesPerTruckload)

    return selected_skus, lcm_value


@dataclass
class SolutionScore:
    difference_sum: int
    total_sticks: int


class RatioCalculator:
    def __init__(self, skus: Dict[str, SKU]) -> None:
        self.skus = skus
        self.target_normalized = self._calculate_target_normalized_weights()

    def _calculate_target_normalized_weights(self) -> Dict[str, float]:
        filtered = list(self.skus.values())
        distinct_scores: List[int] = []
        for sku in filtered:
            if sku.popularityScore not in distinct_scores:
                distinct_scores.append(sku.popularityScore)

        weights = [1 / score for score in distinct_scores]
        total_weight = sum(weights)
        normalized = [w / total_weight for w in weights]

        mapped: Dict[str, float] = {}
        for sku in filtered:
            idx = distinct_scores.index(sku.popularityScore)
            mapped[sku.skuId] = normalized[idx]
        return mapped

    def score(self, solution: List[Dict[str, int]]) -> SolutionScore:
        total_sticks_per_sku: Dict[str, int] = {}
        for item in solution:
            sku_id = item["skuId"]
            sku = self.skus[sku_id]
            sticks = int(sku.calculatedSticksPerBundle) * int(item["numberOfBundles"])
            total_sticks_per_sku[sku_id] = sticks

        total_sticks = sum(total_sticks_per_sku.values())
        normalized_weights = {
            sku_id: sticks / total_sticks for sku_id, sticks in total_sticks_per_sku.items()
        }

        difference_sum = 0
        for sku_id, weight in normalized_weights.items():
            popularity = self.skus[sku_id].popularityScore
            difference = round(abs(weight - self.target_normalized[sku_id]) * popularity * 10000)
            difference_sum += difference

        return SolutionScore(difference_sum=difference_sum, total_sticks=total_sticks)


def compute_packing_solution(selected_skus: Dict[str, SKU]) -> PackingResult:
    if not selected_skus:
        raise ValueError("No SKUs selected")

    enriched_skus, lcm_value = enrich_skus(selected_skus)

    if len(enriched_skus) == 1:
        min_truck_size = lcm_value
        max_truck_size = lcm_value
    else:
        all_divisible_by_six = all(
            (int(sku.calculatedBundlesPerTruckload) % 6 == 0) for sku in enriched_skus.values()
        )
        if all_divisible_by_six:
            min_truck_size = lcm_value
            max_truck_size = lcm_value
        else:
            min_truck_size = floor(lcm_value * 0.95)
            max_truck_size = floor(lcm_value * 0.98)

    sku_ids = list(enriched_skus.keys())
    bundle_constraints = {
        sku_id: (1, int(enriched_skus[sku_id].calculatedBundlesPerTruckload)) for sku_id in sku_ids
    }

    solutions: List[Tuple[List[Dict[str, int]], int]] = []
    current_max_total_size = 0

    def search(idx: int, running_solution: List[Dict[str, int]], total_size: int) -> None:
        nonlocal current_max_total_size

        if idx == len(sku_ids):
            if total_size < current_max_total_size:
                return
            if min_truck_size <= total_size <= max_truck_size:
                current_max_total_size = total_size
                solutions.append(([item.copy() for item in running_solution], total_size))
            return

        sku_id = sku_ids[idx]
        sku = enriched_skus[sku_id]
        min_bundles, max_bundles = bundle_constraints[sku_id]

        for number_of_bundles in range(min_bundles, max_bundles + 1):
            new_size = total_size + number_of_bundles * int(sku.calculatedBundleSize)
            if new_size > max_truck_size:
                break
            running_solution.append({"skuId": sku_id, "numberOfBundles": number_of_bundles})
            search(idx + 1, running_solution, new_size)
            running_solution.pop()

    search(0, [], 0)
    solutions = [s for s in solutions if s[1] >= current_max_total_size]

    if not solutions:
        raise ValueError("No solutions available for this SKU set")

    if len(solutions) == 1:
        best_solution, best_total_size = solutions[0]
        score = RatioCalculator(enriched_skus).score(best_solution)
        return PackingResult(
            lcmValue=lcm_value,
            minTruckSize=min_truck_size,
            maxTruckSize=max_truck_size,
            totalSize=best_total_size,
            totalSticks=score.total_sticks,
            differenceSum=score.difference_sum,
            solution=best_solution,
            skus=enriched_skus,
        )

    ratio_calculator = RatioCalculator(enriched_skus)
    scored = []
    for solution, total_size in solutions:
        score = ratio_calculator.score(solution)
        scored.append((solution, total_size, score.difference_sum, score.total_sticks))

    min_difference = min(item[2] for item in scored)
    filtered = [item for item in scored if item[2] == min_difference]
    max_sticks = max(item[3] for item in filtered)
    filtered = [item for item in filtered if item[3] == max_sticks]

    best_solution, best_total_size, best_difference, best_total_sticks = filtered[0]
    return PackingResult(
        lcmValue=lcm_value,
        minTruckSize=min_truck_size,
        maxTruckSize=max_truck_size,
        totalSize=best_total_size,
        totalSticks=best_total_sticks,
        differenceSum=best_difference,
        solution=best_solution,
        skus=enriched_skus,
    )
