(function () {
    const cfg = window.H2O_CONFIG || {};

    window.h2oApiAdapter = {
        enabled: Boolean(cfg.USE_API),
        baseUrl: cfg.API_BASE_URL || 'http://127.0.0.1:8001',

        async fetchSkus() {
            const response = await fetch(`${this.baseUrl}/skus`);
            if (!response.ok) {
                throw new Error(`GET /skus failed: ${response.status}`);
            }
            const payload = await response.json();
            return payload.skus || [];
        },

        async createAndPack(skuIds) {
            const orderResponse = await fetch(`${this.baseUrl}/orders`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    items: skuIds.map(function (skuId) {
                        return { sku_id: skuId, quantity: 1 };
                    }),
                }),
            });
            if (!orderResponse.ok) {
                throw new Error(`POST /orders failed: ${orderResponse.status}`);
            }

            const order = await orderResponse.json();
            const orderId = order.order_id;

            const packResponse = await fetch(`${this.baseUrl}/pack`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ order_id: orderId }),
            });
            if (!packResponse.ok) {
                throw new Error(`POST /pack failed: ${packResponse.status}`);
            }

            const packed = await packResponse.json();
            return { orderId, packingResult: packed.packing_result };
        },

        async pack(orderId, bundleConstraints) {
            const packResponse = await fetch(`${this.baseUrl}/pack`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ orderId, bundleConstraints }),
            });
            if (!packResponse.ok) {
                throw new Error(`POST /pack failed: ${packResponse.status}`);
            }
            const packed = await packResponse.json();
            return packed.packing_result;
        },
    };
})();

class ApiEngine {
    constructor(skus, baseUrl, orderId) {
        this.SKUs = skus;
        this.baseUrl = baseUrl;
        this.orderId = orderId;

        this.bundleConstraints = {};
        this.initialBundleConstraints = {};
        this.lastBundleConstraints = {};

        Object.values(skus).forEach(sku => {
            const skuId = sku.skuId;
            const maxBundles = parseInt(sku.calculatedBundlesPerTruckload);
            this.bundleConstraints[skuId] = { minNumberOfBundles: 1, maxNumberOfBundles: maxBundles };
        });

        Object.keys(this.bundleConstraints).forEach(skuId => {
            this.initialBundleConstraints[skuId] = { ...this.bundleConstraints[skuId] };
            this.lastBundleConstraints[skuId] = { ...this.bundleConstraints[skuId] };
        });
    }

    _updateConstraints(skuId, action, numberOfBundles) {
        const minNumberOfBundlesInitial = this.initialBundleConstraints[skuId].minNumberOfBundles;
        const maxNumberOfBundlesInitial = this.initialBundleConstraints[skuId].maxNumberOfBundles;
        const minNumberOfBundlesLast = this.lastBundleConstraints[skuId].minNumberOfBundles;
        const maxNumberOfBundlesLast = this.lastBundleConstraints[skuId].maxNumberOfBundles;
        const correctAmountCheckbox = document.querySelector(`#orderTableDataCorrectAmountId${skuId}`);

        switch (action) {
            case 'correctAmount':
                this.bundleConstraints[skuId].minNumberOfBundles = numberOfBundles;
                this.bundleConstraints[skuId].maxNumberOfBundles = numberOfBundles;
                if (correctAmountCheckbox) correctAmountCheckbox.checked = true;
                break;
            case 'notCorrectAmount':
                this.bundleConstraints[skuId].minNumberOfBundles = minNumberOfBundlesLast;
                this.bundleConstraints[skuId].maxNumberOfBundles = maxNumberOfBundlesLast;
                break;
            case 'increase':
                if (numberOfBundles < maxNumberOfBundlesInitial) {
                    const newBundles = Math.max(0, parseInt(numberOfBundles) + 1);
                    this.bundleConstraints[skuId].minNumberOfBundles = newBundles;
                    this.bundleConstraints[skuId].maxNumberOfBundles = maxNumberOfBundlesInitial;
                }
                break;
            case 'decrease':
                if (numberOfBundles > minNumberOfBundlesInitial) {
                    const newBundles = Math.max(0, parseInt(numberOfBundles) - 1);
                    this.bundleConstraints[skuId].maxNumberOfBundles = newBundles;
                    this.bundleConstraints[skuId].minNumberOfBundles = minNumberOfBundlesInitial;
                }
                break;
            default:
                throw new Error(`Unknown action: ${action}`);
        }
    }

    updateButtonStates() {
        Object.keys(this.SKUs).forEach(skuId => {
            const row = document.querySelector(`#orderTableDataRowId${skuId}`);
            if (!row) return;
            const numberOfBundles = parseInt(row.getAttribute('data-total-bundles'));
            const minNumberOfBundles = this.initialBundleConstraints[skuId].minNumberOfBundles;
            const maxNumberOfBundles = this.initialBundleConstraints[skuId].maxNumberOfBundles;

            const increaseButton = document.querySelector(`#orderTableDataIncreaseAmountId${skuId}`);
            const decreaseButton = document.querySelector(`#orderTableDataDecreaseAmountId${skuId}`);

            if (increaseButton) increaseButton.disabled = numberOfBundles >= maxNumberOfBundles;
            if (decreaseButton) decreaseButton.disabled = numberOfBundles <= minNumberOfBundles;
        });
    }

    async updateAll(skuId, action, bundles) {
        bundles = parseInt(bundles, 10);
        this._updateConstraints(skuId, action, bundles);

        // Disable all buttons during API call
        Object.keys(this.SKUs).forEach(id => {
            const inc = document.querySelector(`#orderTableDataIncreaseAmountId${id}`);
            const dec = document.querySelector(`#orderTableDataDecreaseAmountId${id}`);
            if (inc) inc.disabled = true;
            if (dec) dec.disabled = true;
        });

        const apiConstraints = {};
        Object.keys(this.bundleConstraints).forEach(id => {
            apiConstraints[id] = {
                min_bundles: this.bundleConstraints[id].minNumberOfBundles,
                max_bundles: this.bundleConstraints[id].maxNumberOfBundles,
            };
        });

        const result = await window.h2oApiAdapter.pack(this.orderId, apiConstraints);

        this.lastBundleConstraints = {};
        Object.keys(this.bundleConstraints).forEach(id => {
            this.lastBundleConstraints[id] = { ...this.bundleConstraints[id] };
        });

        orderTable = new OrderTable(result.skus, result.solution, this);
        this.updateButtonStates();
    }
}
