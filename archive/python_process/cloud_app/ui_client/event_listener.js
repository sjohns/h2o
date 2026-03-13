function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    try {
        await loadPackingData();
        const SKUs = processPackingData(packingData);
        selectSkus(SKUs);

        const selectSkusDiv = document.getElementById('selectSkus');
        if (selectSkusDiv.children.length === 0) {
            selectSkus(SKUs);
        }
    } catch (error) {
        const orderTableContainer = document.getElementById('orderTableContainer');
        if (orderTableContainer) {
            const pre = document.createElement('pre');
            pre.textContent = `Failed to load data from API: ${error.message}`;
            orderTableContainer.appendChild(pre);
        }
    }
});
