class CalculateRatios {
    constructor(skus) {
        this.skus = skus;
    }

    popularityScoreDifference(solutionData) {
        let totalSticks = 0;
        solutionData.solution.forEach((item) => {
            const sku = this.skus[item.skuId];
            if (!sku) {
                return;
            }
            totalSticks += Number(sku.calculatedSticksPerBundle || 0) * Number(item.numberOfBundles || 0);
        });
        return {differenceSum: 0, totalSticks};
    }
}
