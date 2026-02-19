/**
 * The CalculateRatios class is responsible for calculating the normalized weights of SKUs based on their popularity scores and 
 * determining the difference in these weights for given SKU data.
 * 
 * Explanation of Weighted Ratios:
 * Weighted ratios are used to represent the relative importance or contribution of different items in a set. 
 * In this context, the items are SKUs (Stock Keeping Units) and their popularity scores determine their importance. 
 * The weighted ratio of an SKU is calculated by dividing its inverse popularity score by the total of all inverse popularity scores. 
 * This normalization ensures that the sum of all weighted ratios is 1.
 * 
 * Calculation Process:
 * 1. **Normalization**:
 *    - Each SKU's popularity score is converted to a weight by taking the inverse (1/popularityScore).
 *    - These weights are then normalized by dividing each weight by the sum of all weights, ensuring the sum of normalized weights equals 1.
 * 
 * 2. **Weight Comparison**:
 *    - The function `popularityScoreDifference` calculates the total sticks per SKU based on the provided data.
 *    - Normalized weights are then calculated for each SKU based on the actual number of sticks.
 *    - The difference between the target normalized weights (based on popularity scores) and the actual normalized weights (based on sticks) is computed.
 *    - This difference, weighted by the SKU's popularity score, provides a measure of how well the actual distribution of SKUs matches the expected distribution based on popularity scores.
 * 
 * Example Usage:
 * 
 * const skus = {
 *     sku1: { skuId: 'sku1', sticksPerBundle: 10, popularityScore: 5 },
 *     sku2: { skuId: 'sku2', sticksPerBundle: 20, popularityScore: 3 },
 * };
 * 
 * const calculateRatios = new CalculateRatios(skus);
 * const skuData = {
 *     solution: [
 *         { skuId: 'sku1', numberOfBundles: 5 },
 *         { skuId: 'sku2', numberOfBundles: 3 },
 *     ]
 * };
 * 
 * const result = calculateRatios.popularityScoreDifference(skuData);
 * console.log(result);
 * 
 * Output:
 * - The result object will contain the difference sum and total sticks for the given SKU data.
 * 
 * Date: 2024-07-05
 * Author: Stephen Johns
 */

class CalculateRatios {
    /**
     * Initialize the CalculateRatios with SKUs.
     * @param {Object} skus - The SKUs containing SKU information.
     */
    constructor(skus) {
        console.log("Initializing CalculateRatios...");
        this.skus = skus;  // Directly assign the skus to the class property
        this.targetNormalized = this.calculateTargetNormalizedWeightsBySKU();
//        console.log("SKUs initialized:", this.skus);
        console.log("Target Normalized Weights:", this.targetNormalized);
    }

    /**
     * Calculate the normalized weights based on SKU popularity scores.
     * Normalized weights represent the relative importance of each SKU.
     * @returns {Object} - Object containing SKU IDs and their normalized weights.
     */
    calculateTargetNormalizedWeightsBySKU() {
        console.log('Calculating target normalized weights...');
        const filteredSKUs = Object.values(this.skus);
//        console.log('Filtered SKUs:', filteredSKUs);
        const distinctPopularityScores = [...new Set(filteredSKUs.map(sku => sku.popularityScore))];
        console.log('Distinct popularity scores:', distinctPopularityScores);
        const weights = distinctPopularityScores.map(score => 1 / score);
        const totalWeight = weights.reduce((acc, val) => acc + val, 0);
        const targetNormalizedWeights = weights.map(weight => weight / totalWeight);
        const targetNormalizedWeightsBySKU = {};
        filteredSKUs.forEach(sku => {
            targetNormalizedWeightsBySKU[sku.skuId] = targetNormalizedWeights[distinctPopularityScores.indexOf(sku.popularityScore)];
        });
//        console.log('Target Normalized Weights By SKU:', targetNormalizedWeightsBySKU);
        return targetNormalizedWeightsBySKU;
    }

    /**
     * Calculate the difference in popularity score weights for a given set of SKU data.
     * @param {Object} skuData - Object containing the number of bundles for each SKU ID.
     * @returns {Object} - Object containing the sum of differences in popularity score weights and total sticks per SKU.
     */
    popularityScoreDifference(skuData) {
//        console.log("Calculating popularity score difference...");
        const totalSticksPerSKU = {};
        const solution = skuData.solution;

        // Calculate total sticks for each SKU and update this.skus
        solution.forEach(skuDataItem => {
            const skuId = skuDataItem.skuId;
            if (this.skus.hasOwnProperty(skuId)) {
                const sku = this.skus[skuId];
                const sticksPerBundle = sku.calculatedSticksPerBundle * skuDataItem.numberOfBundles;
                totalSticksPerSKU[skuId] = sticksPerBundle;
                skuDataItem.totalSticks = sticksPerBundle;
                this.skus[skuId].totalSticks = sticksPerBundle;
            }
        });

//        console.log("Total Sticks Per SKU:", totalSticksPerSKU);

        // Calculate total sticks across all SKUs
        const totalSticks = Object.values(totalSticksPerSKU).reduce((acc, quantity) => acc + quantity, 0);
//        console.log("Total Sticks:", totalSticks);
        solution.totalSticks = totalSticks;

        // Calculate normalized weights for each SKU based on sticks
        const normalizedWeightsPerSKU = {};
        Object.entries(totalSticksPerSKU).forEach(([skuId, sticks]) => {
            normalizedWeightsPerSKU[skuId] = sticks / totalSticks;
        });
//        console.log("Normalized Weights Per SKU:", normalizedWeightsPerSKU);

        // Calculate difference in weights for each SKU and sum the differences
        const differenceSum = Object.entries(normalizedWeightsPerSKU).reduce((acc, [skuId, weight]) => {
			const difference = Math.round(Math.abs(weight - this.targetNormalized[skuId]) * this.skus[skuId].popularityScore * 10000);
            //const difference = Math.abs(this.targetNormalized[skuId] - weight) * this.skus[skuId].popularityScore;
            return acc + difference;
        }, 0);

//        console.log("Difference Sum:", differenceSum);

        return {
            differenceSum,
            totalSticks
        };
    }
}
