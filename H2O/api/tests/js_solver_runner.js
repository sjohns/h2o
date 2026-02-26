#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function loadScript(filePath) {
  const code = fs.readFileSync(filePath, 'utf8');
  vm.runInThisContext(code, { filename: filePath });
}

function main() {
  const root = path.resolve(__dirname, '..', '..');
  const snapshotPath = path.join(root, 'api', 'data', 'packing_data.json');
  const selectedSkuIds = JSON.parse(process.argv[2]);

  globalThis.packingData = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  globalThis.alert = function () {};
  console.log = function () {};

  loadScript(path.join(root, 'html', 'process_packing_data.js'));
  loadScript(path.join(root, 'html', 'lcm_functions.js'));
  loadScript(path.join(root, 'html', 'calculate_ratios.js'));
  loadScript(path.join(root, 'html', 'branch_and_bound_engine.js'));

  const allSkus = processPackingData(packingData);
  const selected = {};
  for (const skuId of Object.keys(allSkus)) {
    if (selectedSkuIds.includes(skuId)) {
      selected[skuId] = JSON.parse(JSON.stringify(allSkus[skuId]));
    }
  }

  calculateBundlesPerTruckload(selected);
  const lcmValue = calculateLCMFromSKUs(selected);
  calculateAdditionalFields(selected, lcmValue);

  const ratiosCalculator = new CalculateRatios(selected);
  const engine = new BranchAndBoundEngine(selected, lcmValue, ratiosCalculator);
  const solution = engine.bestSolution();

  const score = ratiosCalculator.popularityScoreDifference({
    solution: solution.map((item) => ({ ...item })),
  });

  const totalSize = solution.reduce((acc, item) => {
    return acc + selected[item.skuId].calculatedBundleSize * item.numberOfBundles;
  }, 0);

  const bundlesValues = [...new Set(Object.values(selected).map((s) => s.calculatedBundlesPerTruckload))];
  const allDivBySix = Object.values(selected).every((s) => s.calculatedBundlesPerTruckload % 6 === 0);
  const minTruckSize = Object.keys(selected).length === 1 || allDivBySix ? lcmValue : Math.floor(lcmValue * 0.95);
  const maxTruckSize = Object.keys(selected).length === 1 || allDivBySix ? lcmValue : Math.floor(lcmValue * 0.98);

  const out = {
    skus: selected,
    solution,
    lcmValue,
    minTruckSize,
    maxTruckSize,
    totalSize,
    totalSticks: score.totalSticks,
    differenceSum: score.differenceSum,
  };

  process.stdout.write(JSON.stringify(out));
}

main();
