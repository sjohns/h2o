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
    const apiSkus = await window.h2oApiAdapter.fetchSkus();
    const skus = listToSkuObject(apiSkus);
    selectSkus(skus);
});
