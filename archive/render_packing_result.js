(function () {
    function buildCombinedPackingData(skus, solution) {
        return solution.map(function (solutionItem) {
            const sku = skus[solutionItem.skuId];
            return {
                ...sku,
                numberOfBundles: solutionItem.numberOfBundles,
                totalSticks: sku.calculatedSticksPerBundle * solutionItem.numberOfBundles,
            };
        });
    }

    if (typeof window !== 'undefined') {
        window.buildCombinedPackingData = buildCombinedPackingData;
    }

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { buildCombinedPackingData };
    }
})();
