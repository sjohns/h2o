import json
import subprocess
import tempfile
from pathlib import Path

from python_process.cloud_app.core.solver import solve
from python_process.cloud_app.data.repository import load_skus
from python_process.cloud_app.data.versioning import get_current_version


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CASES_PATH = PROJECT_ROOT / "python_process" / "cloud_app" / "tests" / "parity_cases.json"
JS_DIR = PROJECT_ROOT / "H2O" / "html"


def _load_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def _node_runner_source() -> str:
    return r'''
const fs = require("fs");
const vm = require("vm");

function loadIntoContext(ctx, path, exposes) {
  let code = fs.readFileSync(path, "utf8");
  if (exposes && exposes.length > 0) {
    code += "\n" + exposes.map((name) => `globalThis.${name} = ${name};`).join("\n");
  }
  vm.runInContext(code, ctx, { filename: path });
}

function runCase(jsDir, selectedSkuIds) {
  const ctx = {
    console: { log() {}, warn() {}, error() {} },
    alert: () => {},
    orderTable: null,
    branchAndBoundEngine: null,
  };
  vm.createContext(ctx);

  loadIntoContext(ctx, `${jsDir}/load_packing_data.js`, ["packingData"]);
  loadIntoContext(ctx, `${jsDir}/process_packing_data.js`, ["processPackingData"]);
  loadIntoContext(ctx, `${jsDir}/lcm_functions.js`, [
    "calculateBundlesPerTruckload",
    "calculateLCMFromSKUs",
    "calculateAdditionalFields",
  ]);
  loadIntoContext(ctx, `${jsDir}/calculate_ratios.js`, ["CalculateRatios"]);
  loadIntoContext(ctx, `${jsDir}/branch_and_bound_engine.js`, ["BranchAndBoundEngine"]);

  const allSkus = ctx.processPackingData(ctx.packingData);
  const skus = {};
  selectedSkuIds.forEach((skuId) => {
    if (allSkus[skuId]) {
      skus[skuId] = allSkus[skuId];
    }
  });

  ctx.calculateBundlesPerTruckload(skus);
  const lcm = ctx.calculateLCMFromSKUs(skus);
  ctx.calculateAdditionalFields(skus, lcm);

  const ratios = new ctx.CalculateRatios(skus);
  const engine = new ctx.BranchAndBoundEngine(skus, lcm, ratios);
  const solution = engine.bestSolution();

  const bundles = {};
  solution.forEach((item) => {
    bundles[item.skuId] = item.numberOfBundles;
  });

  return { lcm, bundles };
}

function main() {
  const payload = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const jsDir = payload.js_dir;
  const cases = payload.cases;

  const results = [];
  for (const c of cases) {
    try {
      const out = runCase(jsDir, c.selected_sku_ids);
      results.push({ name: c.name, ok: true, lcm: out.lcm, bundles: out.bundles });
    } catch (err) {
      results.push({ name: c.name, ok: false, error: String(err && err.message ? err.message : err) });
    }
  }

  process.stdout.write(JSON.stringify(results));
}

main();
'''


def _run_js_cases(cases: list[dict]) -> list[dict]:
    payload = {
        "js_dir": str(JS_DIR),
        "cases": cases,
    }

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        runner_path = tmp_path / "runner.js"
        payload_path = tmp_path / "payload.json"
        runner_path.write_text(_node_runner_source(), encoding="utf-8")
        payload_path.write_text(json.dumps(payload), encoding="utf-8")

        proc = subprocess.run(
            ["node", str(runner_path), str(payload_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or "Node parity runner failed")

        return json.loads(proc.stdout)


def _python_case_result(case: dict) -> dict:
    version = get_current_version()
    sku_df = load_skus(version)
    output = solve(sku_df=sku_df, selected_sku_ids=case["selected_sku_ids"], truck_fill_ratio=1.0)

    bundles: dict = {}
    for item in output["solution"]:
        bundles[item["sku_id"]] = int(item["number_of_bundles"])

    return {
        "lcm": int(output["lcm"]),
        "bundles": bundles,
    }


def _compare(js_result: dict, py_result: dict) -> dict:
    js_bundles = js_result["bundles"]
    py_bundles = py_result["bundles"]
    all_keys = sorted(set(js_bundles.keys()) | set(py_bundles.keys()))
    diffs: list[dict] = []
    for key in all_keys:
        js_value = js_bundles.get(key)
        py_value = py_bundles.get(key)
        if js_value != py_value:
            diffs.append({"sku_id": key, "js": js_value, "py": py_value})

    return {
        "lcm_match": js_result["lcm"] == py_result["lcm"],
        "bundle_match": len(diffs) == 0,
        "diffs": diffs,
    }


def main() -> None:
    cases = _load_cases()
    js_results = _run_js_cases(cases)
    js_by_name = {item["name"]: item for item in js_results}

    report: list[dict] = []
    for case in cases:
        name = case["name"]
        js_result = js_by_name[name]
        if not js_result.get("ok"):
            report.append(
                {
                    "name": name,
                    "ok": False,
                    "error": js_result.get("error", "unknown js error"),
                }
            )
            continue

        py_result = _python_case_result(case)
        cmp_result = _compare(js_result, py_result)
        report.append(
            {
                "name": name,
                "ok": cmp_result["lcm_match"] and cmp_result["bundle_match"],
                "lcm": {
                    "js": js_result["lcm"],
                    "py": py_result["lcm"],
                    "match": cmp_result["lcm_match"],
                },
                "bundle_match": cmp_result["bundle_match"],
                "diffs": cmp_result["diffs"],
            }
        )

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
