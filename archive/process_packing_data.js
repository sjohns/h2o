/**
 * Function Description:
 * This script processes packing data for various SKUs, extracting and formatting the information
 * into a structured format.
 * 
 * Overview:
 * The function iterates through the packing data, processes each product type, and extracts 
 * all SKUs. It dynamically adds all properties from each SKU to a structured format and returns
 * the processed SKUs.
 * 
 * Functions:
 * - processPackingData(packingData): Processes the packing data to extract and format SKUs.
 * 
 * Example Usage:
 * const packingData = {
 *     productTypes: [
 *         {
 *             productType: "Example Type",
 *             skus: {
 *                 skuId_1: {
 *                     skuId: "skuId_1",
 *                     // Other SKU properties...
 *                 },
 *                 skuId_2: {
 *                     skuId: "skuId_2",
 *                     // Other SKU properties...
 *                 }
 *             }
 *         },
 *         {
 *             productType: "Another Type",
 *             skus: {
 *                 // SKUs for this product type...
 *             }
 *         }
 *     ]
 * };
 * 
 * const processedSKUs = processPackingData(packingData);
 * console.log(processedSKUs);
 * 
 * Output:
 * - An object containing the processed SKUs with their properties.
 * 
 * Date: 2024-06-26
 * Author: Stephen Johns
 */

/**
 * Processes the packing data to extract and format SKUs.
 * @param {Object} packingData - The packing data containing product types and SKUs.
 * @returns {Object} - An object containing the processed SKUs with their properties.
 */
function processPackingData(packingData) {
    const skus = {};

    // Iterate through each product type in the packing data
    packingData.productTypes.forEach(productType => {
        // Iterate through each SKU in the current product type
        Object.values(productType.skus).forEach(SKU => {
            // Store the SKU object in the skus object, using the SKU ID as the key
            skus[SKU.skuId] = SKU;
        });
    });
console.log('processPackingData skus: ',skus);
    return skus;
}

function mround(number, multiple) {
    if (multiple === 0) {
        return 0;
    }
    return Math.round(number / multiple) * multiple;
}
