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
            const packResponse = await fetch(`${this.baseUrl}/pack`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ order_id: order.order_id }),
            });
            if (!packResponse.ok) {
                throw new Error(`POST /pack failed: ${packResponse.status}`);
            }

            const packed = await packResponse.json();
            return packed.packing_result;
        },
    };
})();
