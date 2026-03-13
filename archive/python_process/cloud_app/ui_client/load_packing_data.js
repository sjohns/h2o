let packingData = null;

async function loadPackingData() {
    const response = await fetch('/parts');
    const payload = await response.json();
    if (!response.ok) {
        throw new Error(JSON.stringify(payload));
    }

    const skuRows = Array.isArray(payload) ? payload : [];
    const skuMap = {};

    skuRows.forEach((row, index) => {
        const skuId = String(row.skuId || '');
        if (!skuId) {
            return;
        }
        skuMap[skuId] = {
            skuId,
            SKU: String(row.description || skuId),
            activeFlag: 'Y',
            displayOrder: index,
        };
    });

    packingData = {
        date: new Date().toISOString(),
        productTypes: [
            {
                productTypeId: 'parts',
                productType: 'Parts',
                skus: skuMap,
            },
        ],
    };

    return packingData;
}
