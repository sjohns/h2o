function processPackingData(packingData) {
    const skus = {};
    packingData.productTypes.forEach((productType) => {
        Object.values(productType.skus).forEach((sku) => {
            skus[sku.skuId] = sku;
        });
    });
    return skus;
}

function mround(number, multiple) {
    if (multiple === 0) {
        return 0;
    }
    return Math.round(number / multiple) * multiple;
}
