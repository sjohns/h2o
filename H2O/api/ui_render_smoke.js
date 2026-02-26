#!/usr/bin/env node
const { buildCombinedPackingData } = require('../html/render_packing_result.js');

const API_BASE = process.env.API_BASE_URL || 'http://127.0.0.1:8001';

async function request(path, options = {}) {
    const response = await fetch(`${API_BASE}${path}`, options);
    if (!response.ok) {
        throw new Error(`${options.method || 'GET'} ${path} failed: ${response.status}`);
    }
    return response.json();
}

async function main() {
    const skusPayload = await request('/skus');
    const skus = skusPayload.skus;
    const skuIds = [skus[0].skuId, skus[1].skuId, skus[2].skuId];

    const order = await request('/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            items: skuIds.map((skuId) => ({ sku_id: skuId, quantity: 1 })),
        }),
    });

    const packed = await request('/pack', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: order.order_id }),
    });

    const result = packed.packing_result;
    const combined = buildCombinedPackingData(result.skus, result.solution);

    if (!Array.isArray(combined) || combined.length === 0) {
        throw new Error('Renderer transform returned empty data.');
    }

    for (const row of combined) {
        if (!('numberOfBundles' in row) || !('totalSticks' in row) || !('SKU' in row)) {
            throw new Error('Renderer transform is missing expected fields.');
        }
    }

    console.log('ui_render_smoke passed');
}

main().catch((err) => {
    console.error(err.message || err);
    process.exit(1);
});
