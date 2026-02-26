from __future__ import annotations

import json
import math
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import duckdb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


SKU_PARQUET_FILE_PATH = "skus.parquet"
PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
DEFAULT_DATA_ROOT_DIRECTORY = PROJECT_ROOT_DIRECTORY / "python_process" / "data" / "master"
CURRENT_VERSION_POINTER_FILE_PATH = DEFAULT_DATA_ROOT_DIRECTORY / "current.json"

BASE_SKU_CACHE_BY_IDENTIFIER: Dict[str, Dict[str, Any]] = {}
BASE_SKU_CACHE_LOCK = threading.Lock()


def _resolve_sku_parquet_file_path() -> Path:
    parquet_file_path = Path(SKU_PARQUET_FILE_PATH)
    if CURRENT_VERSION_POINTER_FILE_PATH.exists():
        try:
            current_pointer_payload = json.loads(CURRENT_VERSION_POINTER_FILE_PATH.read_text(encoding="utf-8"))
            current_version_name = str(current_pointer_payload.get("version", "")).strip()
            if current_version_name:
                candidate_file_path = DEFAULT_DATA_ROOT_DIRECTORY / current_version_name / "skus.parquet"
                if candidate_file_path.exists():
                    parquet_file_path = candidate_file_path
        except Exception:
            pass
    return parquet_file_path


def load_base_sku_dictionary_from_parquet() -> Dict[str, Dict[str, Any]]:
    parquet_file_path = _resolve_sku_parquet_file_path()
    duckdb_connection = duckdb.connect()
    data_frame = duckdb_connection.execute(f"SELECT * FROM '{parquet_file_path}'").df()
    duckdb_connection.close()

    normalized_legacy_dictionary: Dict[str, Dict[str, Any]] = {}

    for row in data_frame.to_dict("records"):
        sku_identifier = str(row.get("sku_id", row.get("skuId", "")))
        if not sku_identifier:
            continue

        product_type_identifier = str(row.get("product_type_id", row.get("productTypeId", "")))
        product_type_name = str(row.get("product_type", row.get("productType", "")))
        sku_description = str(row.get("sku", row.get("SKU", sku_identifier)))
        sku_size_text = str(row.get("size", ""))
        sku_length_in_feet = int(row.get("lingth", 0) or 0)
        active_flag = str(row.get("active_flag", row.get("activeFlag", "Y")) or "Y").upper()
        if active_flag not in {"Y", "N"}:
            active_flag = "Y"

        display_order = int(row.get("display_order", row.get("displayOrder", 0)) or 0)
        popularity_score = int(row.get("popularity_score", row.get("popularityScore", 0)) or 0)
        calculated_sticks_per_bundle = int(
            row.get("calculated_sticks_per_bundle", row.get("calculatedSticksPerBundle", 0)) or 0
        )
        eagle_sticks_per_truckload = int(
            row.get("eagle_sticks_per_truckload", row.get("eagleSticksPerTruckload", 0)) or 0
        )
        eagle_bundles_per_truckload = int(
            row.get("eagle_bundles_per_truckload", row.get("eagleBundlesPerTruckLoad", 0)) or 0
        )
        calculated_bundles_per_truckload = int(
            row.get("calculated_bundles_per_truckload", row.get("calculatedBundlesPerTruckload", 0)) or 0
        )

        normalized_legacy_dictionary[sku_identifier] = {
            "skuId": sku_identifier,
            "productTypeId": product_type_identifier,
            "productType": product_type_name,
            "SKU": sku_description,
            "size": sku_size_text,
            "lingth": sku_length_in_feet,
            "activeFlag": active_flag,
            "displayOrder": display_order,
            "popularityScore": popularity_score,
            "calculatedSticksPerBundle": calculated_sticks_per_bundle,
            "eagleSticksPerTruckload": eagle_sticks_per_truckload,
            "eagleBundlesPerTruckLoad": eagle_bundles_per_truckload,
            "calculatedBundlesPerTruckload": calculated_bundles_per_truckload,
        }

    return normalized_legacy_dictionary


def reload_base_sku_cache_from_parquet() -> None:
    global BASE_SKU_CACHE_BY_IDENTIFIER
    with BASE_SKU_CACHE_LOCK:
        BASE_SKU_CACHE_BY_IDENTIFIER = load_base_sku_dictionary_from_parquet()


def set_base_sku_cache(base_sku_cache_by_identifier: Dict[str, Dict[str, Any]]) -> None:
    global BASE_SKU_CACHE_BY_IDENTIFIER
    with BASE_SKU_CACHE_LOCK:
        BASE_SKU_CACHE_BY_IDENTIFIER = {
            sku_identifier: row.copy() for sku_identifier, row in base_sku_cache_by_identifier.items()
        }


try:
    reload_base_sku_cache_from_parquet()
except Exception:
    BASE_SKU_CACHE_BY_IDENTIFIER = {}


def build_api_sku_rows_from_cache() -> List[Dict[str, Any]]:
    with BASE_SKU_CACHE_LOCK:
        return [
            {
                "sku_id": str(row.get("skuId", sku_identifier)),
                "product_type_id": str(row.get("productTypeId", "")),
                "product_type": str(row.get("productType", "")),
                "sku": str(row.get("SKU", "")),
                "size": str(row.get("size", "")),
                "lingth": int(row.get("lingth", 0) or 0),
                "active_flag": str(row.get("activeFlag", "Y") or "Y"),
                "display_order": int(row.get("displayOrder", 0) or 0),
                "popularity_score": int(row.get("popularityScore", 0) or 0),
                "calculated_sticks_per_bundle": int(row.get("calculatedSticksPerBundle", 0) or 0),
                "eagle_sticks_per_truckload": int(row.get("eagleSticksPerTruckload", 0) or 0),
                "eagle_bundles_per_truckload": int(row.get("eagleBundlesPerTruckLoad", 0) or 0),
                "calculated_bundles_per_truckload": int(row.get("calculatedBundlesPerTruckload", 0) or 0),
            }
            for sku_identifier, row in BASE_SKU_CACHE_BY_IDENTIFIER.items()
        ]


def calculate_bundles_per_truckload_for_each_sku(sku_dictionary: Dict[str, Dict[str, Any]]) -> None:
    for sku_row in sku_dictionary.values():
        denominator = int(sku_row["calculatedSticksPerBundle"])
        if denominator <= 0:
            sku_row["calculatedBundlesPerTruckload"] = 0
            continue
        sku_row["calculatedBundlesPerTruckload"] = int(sku_row["eagleSticksPerTruckload"]) // denominator


def calculate_least_common_multiple_from_skus(sku_dictionary: Dict[str, Dict[str, Any]]) -> int:
    bundle_count_values = {
        max(1, int(sku_row["calculatedBundlesPerTruckload"]))
        for sku_row in sku_dictionary.values()
    }
    return math.lcm(*bundle_count_values) if bundle_count_values else 1


def calculate_additional_sku_fields_from_lcm(sku_dictionary: Dict[str, Dict[str, Any]], lcm_value: int) -> None:
    for sku_row in sku_dictionary.values():
        denominator = int(sku_row["calculatedBundlesPerTruckload"])
        if denominator == 0:
            raise ValueError(f"BundlesPerTruckload=0 for skuId={sku_row.get('skuId')}")
        sku_row["calculatedBundleSize"] = int(lcm_value) // denominator


class PopularityRatioCalculator:
    def __init__(self, sku_dictionary: Dict[str, Dict[str, Any]]):
        self.sku_dictionary = sku_dictionary

    def calculate_popularity_score_difference(self, solution_payload: Dict[str, Any]) -> Tuple[int, int]:
        popularity_difference_sum = 0
        total_stick_count = 0
        for solution_row in solution_payload["solution"]:
            sku_row = self.sku_dictionary[solution_row["skuId"]]
            stick_count = int(sku_row["calculatedSticksPerBundle"]) * int(solution_row["numberOfBundles"])
            popularity_difference_sum += abs(int(sku_row["popularityScore"]) - stick_count)
            total_stick_count += stick_count
        return popularity_difference_sum, total_stick_count


class BranchAndBoundSolverEngine:
    def __init__(
        self,
        sku_dictionary: Dict[str, Dict[str, Any]],
        full_truck_size: int,
        popularity_ratio_calculator: PopularityRatioCalculator,
    ):
        self.sku_dictionary = sku_dictionary
        self.full_truck_size = full_truck_size
        self.bundle_divisibility_modulus = 6
        self.minimum_fraction_when_not_divisible = 0.95
        self.maximum_fraction_when_not_divisible = 0.98
        self.bundle_constraints_by_sku_id: Dict[str, Dict[str, int]] = {}
        self.truck_size_constraints: Dict[str, int] = {}
        self.solution_candidates: List[Dict[str, Any]] = []
        self.popularity_ratio_calculator = popularity_ratio_calculator
        self.current_maximum_truck_size = 0
        self._initialize_constraints()

    def _initialize_constraints(self) -> None:
        if len(self.sku_dictionary) == 1:
            self.truck_size_constraints = {
                "minTruckSize": self.full_truck_size,
                "maxTruckSize": self.full_truck_size,
            }
        else:
            are_all_bundle_counts_divisible = all(
                int(sku_row["calculatedBundlesPerTruckload"]) % self.bundle_divisibility_modulus == 0
                for sku_row in self.sku_dictionary.values()
            )
            if are_all_bundle_counts_divisible:
                self.truck_size_constraints = {
                    "minTruckSize": self.full_truck_size,
                    "maxTruckSize": self.full_truck_size,
                }
            else:
                self.truck_size_constraints = {
                    "minTruckSize": math.floor(self.full_truck_size * self.minimum_fraction_when_not_divisible),
                    "maxTruckSize": math.floor(self.full_truck_size * self.maximum_fraction_when_not_divisible),
                }

        for sku_row in self.sku_dictionary.values():
            self.bundle_constraints_by_sku_id[str(sku_row["skuId"])] = {
                "minNumberOfBundles": 1,
                "maxNumberOfBundles": int(sku_row["calculatedBundlesPerTruckload"]),
            }

    def apply_bundle_overrides(
        self,
        fixed_bundles_by_sku_id: Optional[Dict[str, int]] = None,
        minimum_bundles_by_sku_id: Optional[Dict[str, int]] = None,
        maximum_bundles_by_sku_id: Optional[Dict[str, int]] = None,
    ) -> None:
        fixed_bundles = fixed_bundles_by_sku_id or {}
        minimum_bundles = minimum_bundles_by_sku_id or {}
        maximum_bundles = maximum_bundles_by_sku_id or {}

        for sku_id, bundle_constraint in self.bundle_constraints_by_sku_id.items():
            minimum_value = int(bundle_constraint["minNumberOfBundles"])
            maximum_value = int(bundle_constraint["maxNumberOfBundles"])
            if sku_id in minimum_bundles:
                minimum_value = max(0, int(minimum_bundles[sku_id]))
            if sku_id in maximum_bundles:
                maximum_value = max(0, int(maximum_bundles[sku_id]))
            if sku_id in fixed_bundles:
                fixed_value = max(0, int(fixed_bundles[sku_id]))
                minimum_value = fixed_value
                maximum_value = fixed_value
            if minimum_value > maximum_value:
                raise ValueError(f"Invalid bundle override for {sku_id}: min > max")
            bundle_constraint["minNumberOfBundles"] = minimum_value
            bundle_constraint["maxNumberOfBundles"] = maximum_value

    def _find_all_solutions(self) -> None:
        self.solution_candidates = []
        self.current_maximum_truck_size = 0
        sorted_sku_identifiers = sorted(
            self.bundle_constraints_by_sku_id.keys(),
            key=lambda sku_id: int(self.sku_dictionary[sku_id]["calculatedBundleSize"]),
            reverse=True,
        )
        self._find_sku_combinations(sorted_sku_identifiers, [], 0)
        self.solution_candidates = [
            solution
            for solution in self.solution_candidates
            if int(solution["totalSize"]) >= self.current_maximum_truck_size
        ]

    def _find_sku_combinations(
        self,
        sku_identifiers: List[str],
        candidate_solution_rows: List[Dict[str, Any]],
        total_size: int,
    ) -> None:
        if not sku_identifiers:
            if total_size < self.current_maximum_truck_size:
                return
            self.current_maximum_truck_size = total_size
            if self._is_valid_solution(candidate_solution_rows, total_size):
                self.solution_candidates.append(
                    {
                        "solution": candidate_solution_rows.copy(),
                        "totalSize": total_size,
                    }
                )
            return

        current_sku_id = sku_identifiers[0]
        remaining_sku_identifiers = sku_identifiers[1:]
        bundle_constraint = self.bundle_constraints_by_sku_id[current_sku_id]
        sku_row = self.sku_dictionary[current_sku_id]
        bundle_size = int(sku_row["calculatedBundleSize"])

        for bundle_count in range(
            int(bundle_constraint["minNumberOfBundles"]),
            int(bundle_constraint["maxNumberOfBundles"]) + 1,
        ):
            new_total_size = total_size + bundle_count * bundle_size
            if new_total_size > int(self.truck_size_constraints["maxTruckSize"]):
                break
            candidate_solution_rows.append({"skuId": current_sku_id, "numberOfBundles": bundle_count})
            self._find_sku_combinations(remaining_sku_identifiers, candidate_solution_rows, new_total_size)
            candidate_solution_rows.pop()

    def _is_valid_solution(self, solution_rows: List[Dict[str, Any]], total_size: int) -> bool:
        if not (
            int(self.truck_size_constraints["minTruckSize"])
            <= total_size
            <= int(self.truck_size_constraints["maxTruckSize"])
        ):
            return False

        bundle_count_by_sku_id: Dict[str, int] = {}
        for solution_row in solution_rows:
            sku_id = str(solution_row["skuId"])
            bundle_count_by_sku_id[sku_id] = (
                bundle_count_by_sku_id.get(sku_id, 0) + int(solution_row["numberOfBundles"])
            )

        for sku_id, bundle_count in bundle_count_by_sku_id.items():
            bundle_constraint = self.bundle_constraints_by_sku_id[sku_id]
            if not (
                int(bundle_constraint["minNumberOfBundles"])
                <= bundle_count
                <= int(bundle_constraint["maxNumberOfBundles"])
            ):
                return False

        return True

    def find_best_solution(self) -> Dict[str, Any]:
        self._find_all_solutions()
        if not self.solution_candidates:
            raise ValueError("No solutions found")
        if len(self.solution_candidates) == 1:
            return self.solution_candidates[0]

        best_solution: Optional[Dict[str, Any]] = None
        minimum_difference_sum = float("inf")
        maximum_total_stick_count = -1
        for candidate_solution in self.solution_candidates:
            difference_sum, total_stick_count = self.popularity_ratio_calculator.calculate_popularity_score_difference(
                candidate_solution
            )
            candidate_solution["differenceSum"] = difference_sum
            candidate_solution["totalSticks"] = total_stick_count
            if difference_sum < minimum_difference_sum or (
                difference_sum == minimum_difference_sum and total_stick_count > maximum_total_stick_count
            ):
                best_solution = candidate_solution
                minimum_difference_sum = difference_sum
                maximum_total_stick_count = total_stick_count

        if best_solution is None:
            raise ValueError("No best solution found")
        return best_solution


def _select_sku_dictionary_from_cache(selected_sku_identifiers: List[str]) -> Dict[str, Dict[str, Any]]:
    with BASE_SKU_CACHE_LOCK:
        return {
            sku_id: BASE_SKU_CACHE_BY_IDENTIFIER[sku_id].copy()
            for sku_id in selected_sku_identifiers
            if sku_id in BASE_SKU_CACHE_BY_IDENTIFIER
        }


def compute_solution_for_selected_skus(selected_sku_identifiers: List[str]) -> Dict[str, Any]:
    selected_sku_dictionary = _select_sku_dictionary_from_cache(selected_sku_identifiers)
    if not selected_sku_dictionary:
        raise ValueError("No valid SKUs selected")

    calculate_bundles_per_truckload_for_each_sku(selected_sku_dictionary)
    least_common_multiple_value = calculate_least_common_multiple_from_skus(selected_sku_dictionary)
    calculate_additional_sku_fields_from_lcm(selected_sku_dictionary, least_common_multiple_value)

    popularity_ratio_calculator = PopularityRatioCalculator(selected_sku_dictionary)
    solver_engine = BranchAndBoundSolverEngine(
        selected_sku_dictionary,
        least_common_multiple_value,
        popularity_ratio_calculator,
    )
    best_solution = solver_engine.find_best_solution()

    return {
        "lcmValue": least_common_multiple_value,
        "skus": selected_sku_dictionary,
        "best": best_solution,
    }


def compute_solution_for_selected_skus_with_constraints(
    selected_sku_identifiers: List[str],
    fixed_bundles_by_sku_id: Optional[Dict[str, int]] = None,
    minimum_bundles_by_sku_id: Optional[Dict[str, int]] = None,
    maximum_bundles_by_sku_id: Optional[Dict[str, int]] = None,
) -> Dict[str, Any]:
    selected_sku_dictionary = _select_sku_dictionary_from_cache(selected_sku_identifiers)
    if not selected_sku_dictionary:
        raise ValueError("No valid SKUs selected")

    calculate_bundles_per_truckload_for_each_sku(selected_sku_dictionary)
    least_common_multiple_value = calculate_least_common_multiple_from_skus(selected_sku_dictionary)
    calculate_additional_sku_fields_from_lcm(selected_sku_dictionary, least_common_multiple_value)

    popularity_ratio_calculator = PopularityRatioCalculator(selected_sku_dictionary)
    solver_engine = BranchAndBoundSolverEngine(
        selected_sku_dictionary,
        least_common_multiple_value,
        popularity_ratio_calculator,
    )
    solver_engine.apply_bundle_overrides(
        fixed_bundles_by_sku_id=fixed_bundles_by_sku_id,
        minimum_bundles_by_sku_id=minimum_bundles_by_sku_id,
        maximum_bundles_by_sku_id=maximum_bundles_by_sku_id,
    )
    best_solution = solver_engine.find_best_solution()

    formatted_solution_rows = []
    total_stick_count = 0
    for solution_row in best_solution.get("solution", []):
        sku_id = str(solution_row["skuId"])
        number_of_bundles = int(solution_row["numberOfBundles"])
        sku_row = selected_sku_dictionary[sku_id]
        sticks_per_bundle = int(sku_row["calculatedSticksPerBundle"])
        row_total_sticks = number_of_bundles * sticks_per_bundle
        total_stick_count += row_total_sticks
        formatted_solution_rows.append(
            {
                "sku_id": sku_id,
                "sku": str(sku_row["SKU"]),
                "number_of_bundles": number_of_bundles,
                "sticks_per_bundle": sticks_per_bundle,
                "total_sticks": row_total_sticks,
            }
        )

    return {
        "lcm": int(least_common_multiple_value),
        "total_truck_size": int(best_solution.get("totalSize", 0)),
        "total_sticks": int(total_stick_count),
        "solution": formatted_solution_rows,
    }


class SolveRequestModel(BaseModel):
    selected_sku_ids: List[str]


class CalculateRequestModel(BaseModel):
    selected_sku_ids: List[str]
    truck_fill_ratio: float = 1.0
    fixed_bundles: Dict[str, int] = {}
    min_bundles: Dict[str, int] = {}
    max_bundles: Dict[str, int] = {}


class OrderRequestModel(BaseModel):
    selected_sku_ids: List[str]


app = FastAPI(title="H2O Solver API")


@app.on_event("startup")
def startup() -> None:
    reload_base_sku_cache_from_parquet()


@app.post("/solve")
def solve(request: SolveRequestModel) -> Dict[str, Any]:
    try:
        return compute_solution_for_selected_skus(request.selected_sku_ids)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/reload")
def reload() -> Dict[str, str]:
    reload_base_sku_cache_from_parquet()
    return {"status": "reloaded"}


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "skuCount": len(BASE_SKU_CACHE_BY_IDENTIFIER)}


@app.get("/api/skus")
def api_skus() -> Dict[str, Any]:
    current_version_name = ""
    if CURRENT_VERSION_POINTER_FILE_PATH.exists():
        try:
            current_pointer_payload = json.loads(CURRENT_VERSION_POINTER_FILE_PATH.read_text(encoding="utf-8"))
            current_version_name = str(current_pointer_payload.get("version", ""))
        except Exception:
            current_version_name = ""
    return {"version": current_version_name, "skus": build_api_sku_rows_from_cache()}


@app.get("/parts")
def parts() -> List[Dict[str, str]]:
    with BASE_SKU_CACHE_LOCK:
        part_rows = []
        for sku_identifier, sku_row in BASE_SKU_CACHE_BY_IDENTIFIER.items():
            part_rows.append(
                {
                    "skuId": str(sku_identifier),
                    "description": str(sku_row.get("SKU", sku_identifier)),
                }
            )
    return part_rows


def prepare_order_for_selected_skus(selected_sku_identifiers: List[str]) -> Dict[str, Any]:
    selected_sku_dictionary = _select_sku_dictionary_from_cache(selected_sku_identifiers)
    if not selected_sku_dictionary:
        raise ValueError("No valid SKUs selected")

    calculate_bundles_per_truckload_for_each_sku(selected_sku_dictionary)
    least_common_multiple_value = calculate_least_common_multiple_from_skus(selected_sku_dictionary)
    calculate_additional_sku_fields_from_lcm(selected_sku_dictionary, least_common_multiple_value)

    return {
        "lcmValue": int(least_common_multiple_value),
        "skus": selected_sku_dictionary,
    }


@app.post("/order")
def order(request: OrderRequestModel) -> Dict[str, Any]:
    try:
        return prepare_order_for_selected_skus(request.selected_sku_ids)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/api/calculate")
def api_calculate(request: CalculateRequestModel) -> Dict[str, Any]:
    try:
        result = compute_solution_for_selected_skus_with_constraints(
            selected_sku_identifiers=request.selected_sku_ids,
            fixed_bundles_by_sku_id=request.fixed_bundles,
            minimum_bundles_by_sku_id=request.min_bundles,
            maximum_bundles_by_sku_id=request.max_bundles,
        )
        current_version_name = ""
        if CURRENT_VERSION_POINTER_FILE_PATH.exists():
            try:
                current_pointer_payload = json.loads(CURRENT_VERSION_POINTER_FILE_PATH.read_text(encoding="utf-8"))
                current_version_name = str(current_pointer_payload.get("version", ""))
            except Exception:
                current_version_name = ""
        return {"version": current_version_name, **result}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/api/calculate/replacement")
def api_calculate_replacement(request: CalculateRequestModel) -> Dict[str, Any]:
    return api_calculate(request)
