function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function listToSkuObject(skuList) {
    const skus = {};
    skuList.forEach(function (sku) {
        skus[sku.skuId] = sku;
    });
    return skus;
}

document.addEventListener('DOMContentLoaded', async function () {
    let skus;

    if (window.h2oApiAdapter && window.h2oApiAdapter.enabled) {
        try {
            const apiSkus = await window.h2oApiAdapter.fetchSkus();
            skus = listToSkuObject(apiSkus);
        } catch (error) {
            console.error('API SKU fetch failed, falling back to local data:', error);
            skus = processPackingData(packingData);
        }
    } else {
        skus = processPackingData(packingData);
    }

    selectSkus(skus);

    const selectSkusDiv = document.getElementById('selectSkus');
    if (selectSkusDiv.children.length === 0) {
        selectSkus(skus);
    }
});
