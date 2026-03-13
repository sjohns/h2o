from pathlib import Path

from api_backend.data_loader import flatten_skus, load_packing_data_from_js
from api.solver.solver_service import compute_packing_solution


def _all_skus():
    data = load_packing_data_from_js(Path(__file__).resolve().parents[1] / "html" / "load_packing_data.js")
    return flatten_skus(data)


def test_single_sku_solution_matches_full_truck_lcm():
    skus = _all_skus()
    selected = {"skuId_2": skus["skuId_2"].model_copy(deep=True)}

    result = compute_packing_solution(selected)

    assert result.lcmValue == result.totalSize
    assert result.solution == [{"skuId": "skuId_2", "numberOfBundles": 24}]
    assert result.totalSticks == 9600


def test_multi_sku_solution_within_constraints_and_nonempty():
    skus = _all_skus()
    selected_ids = ["skuId_2", "skuId_3", "skuId_9"]
    selected = {sku_id: skus[sku_id].model_copy(deep=True) for sku_id in selected_ids}

    result = compute_packing_solution(selected)

    assert result.solution
    assert result.minTruckSize <= result.totalSize <= result.maxTruckSize
    assert all(item["skuId"] in selected_ids for item in result.solution)
    assert all(item["numberOfBundles"] >= 1 for item in result.solution)
    assert result.totalSticks > 0
