import json
import subprocess
from pathlib import Path

from api.data import flatten_skus, load_snapshot
from api.solver.branch_and_bound import solve


ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "api" / "data" / "packing_data.json"
JS_RUNNER = ROOT / "api" / "tests" / "js_solver_runner.js"


def _sku_data_by_id():
    data = load_snapshot(SNAPSHOT)
    skus = flatten_skus(data)
    return {sku["skuId"]: sku for sku in skus}


def _python_solve(selected_ids):
    order = {
        "items": [{"sku_id": sku_id, "quantity": 1} for sku_id in selected_ids],
    }
    return solve(order, _sku_data_by_id())


def _js_solve(selected_ids):
    proc = subprocess.run(
        ["node", str(JS_RUNNER), json.dumps(selected_ids)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def _assert_core_fields_equal(py_result, js_result):
    assert py_result["solution"] == js_result["solution"]
    assert py_result["totalSize"] == js_result["totalSize"]
    assert py_result["totalSticks"] == js_result["totalSticks"]
    assert py_result["lcmValue"] == js_result["lcmValue"]
    assert py_result["minTruckSize"] == js_result["minTruckSize"]
    assert py_result["maxTruckSize"] == js_result["maxTruckSize"]
    assert py_result["differenceSum"] == js_result["differenceSum"]


def test_solver_parity_combo_1():
    selected = ["skuId_71", "skuId_72"]
    _assert_core_fields_equal(_python_solve(selected), _js_solve(selected))


def test_solver_parity_combo_2():
    selected = ["skuId_68", "skuId_69", "skuId_70"]
    _assert_core_fields_equal(_python_solve(selected), _js_solve(selected))


def test_solver_parity_combo_3():
    selected = ["skuId_63", "skuId_71", "skuId_72"]
    _assert_core_fields_equal(_python_solve(selected), _js_solve(selected))
