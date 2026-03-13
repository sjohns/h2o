import math
from functools import reduce
from math import lcm
from typing import Any


def calculate_lcm_of_array(numbers: list[int]) -> int:
    return reduce(lcm, (int(number) for number in numbers), 1)


def calculate_lcm_from_skus(skus: dict[str, dict[str, Any]]) -> int:
    unique_bundle_counts = {
        int(sku["calculatedBundlesPerTruckload"])
        for sku in skus.values()
    }
    return calculate_lcm_of_array(sorted(unique_bundle_counts))


def calculate_additional_fields(skus: dict[str, dict[str, Any]], lcm_value: int) -> None:
    for sku in skus.values():
        calculated_bundles_per_truckload = int(sku["calculatedBundlesPerTruckload"])
        sku["calculatedBundleSize"] = int(lcm_value) // calculated_bundles_per_truckload


def calculate_bundles_per_truckload(skus: dict[str, dict[str, Any]]) -> None:
    for sku in skus.values():
        eagle_sticks_per_truckload = int(sku["eagleSticksPerTruckload"])
        calculated_sticks_per_bundle = int(sku["calculatedSticksPerBundle"])
        sku["calculatedBundlesPerTruckload"] = math.floor(
            eagle_sticks_per_truckload / calculated_sticks_per_bundle
        )


def calculate_bundles_per_truckload_value(eagle_sticks_per_truckload: int, calculated_sticks_per_bundle: int) -> int:
    return math.floor(int(eagle_sticks_per_truckload) / int(calculated_sticks_per_bundle))


def calculate_lcm_from_rows(rows: list[dict]) -> int:
    bundle_counts = sorted({int(row["bundles_per_truckload"]) for row in rows})
    return calculate_lcm_of_array(bundle_counts)
