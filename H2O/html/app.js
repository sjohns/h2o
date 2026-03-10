// ── Config ────────────────────────────────────────────────────────────────────
const params = new URLSearchParams(window.location.search);
const API_BASE_URL = params.get('apiBase') || (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' ? 'http://127.0.0.1:8001' : 'https://h2o-api-97ivf.ondigitalocean.app');

// ── API adapter ───────────────────────────────────────────────────────────────
const h2oApi = {
    async fetchSkus() {
        const res = await fetch(`${API_BASE_URL}/skus`);
        if (!res.ok) throw new Error(`GET /skus failed: ${res.status}`);
        return (await res.json()).skus || [];
    },

    async createAndPack(skuIds) {
        const orderRes = await fetch(`${API_BASE_URL}/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items: skuIds.map(id => ({ sku_id: id, quantity: 1 })) }),
        });
        if (!orderRes.ok) throw new Error(`POST /orders failed: ${orderRes.status}`);
        const { order_id } = await orderRes.json();

        const packRes = await fetch(`${API_BASE_URL}/pack`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_id }),
        });
        if (!packRes.ok) throw new Error(`POST /pack failed: ${packRes.status}`);
        return { orderId: order_id, packingResult: (await packRes.json()).packing_result };
    },

    async pack(orderId, bundleConstraints) {
        const res = await fetch(`${API_BASE_URL}/pack`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ orderId, bundleConstraints }),
        });
        if (!res.ok) throw new Error(`POST /pack failed: ${res.status}`);
        return (await res.json()).packing_result;
    },
};

// ── ApiEngine ─────────────────────────────────────────────────────────────────
class ApiEngine {
    constructor(skus, orderId) {
        this.SKUs = skus;
        this.orderId = orderId;
        this.bundleConstraints = {};
        this.initialBundleConstraints = {};
        this.lastBundleConstraints = {};
        this.lockedSkus = new Set();

        Object.values(skus).forEach(sku => {
            const max = parseInt(sku.calculatedBundlesPerTruckload);
            this.bundleConstraints[sku.skuId] = { minNumberOfBundles: 1, maxNumberOfBundles: max };
        });
        Object.keys(this.bundleConstraints).forEach(id => {
            this.initialBundleConstraints[id] = { ...this.bundleConstraints[id] };
            this.lastBundleConstraints[id] = { ...this.bundleConstraints[id] };
        });
    }

    _updateConstraints(skuId, action, numberOfBundles) {
        const initMin = this.initialBundleConstraints[skuId].minNumberOfBundles;
        const initMax = this.initialBundleConstraints[skuId].maxNumberOfBundles;
        const lastMin = this.lastBundleConstraints[skuId].minNumberOfBundles;
        const lastMax = this.lastBundleConstraints[skuId].maxNumberOfBundles;

        switch (action) {
            case 'correctAmount':
                this.bundleConstraints[skuId].minNumberOfBundles = numberOfBundles;
                this.bundleConstraints[skuId].maxNumberOfBundles = numberOfBundles;
                this.lockedSkus.add(skuId);
                break;
            case 'notCorrectAmount':
                this.bundleConstraints[skuId].minNumberOfBundles = lastMin;
                this.bundleConstraints[skuId].maxNumberOfBundles = lastMax;
                this.lockedSkus.delete(skuId);
                break;
            case 'increase':
                if (numberOfBundles < initMax) {
                    this.bundleConstraints[skuId].minNumberOfBundles = Math.max(0, numberOfBundles + 1);
                    this.bundleConstraints[skuId].maxNumberOfBundles = initMax;
                }
                this.lockedSkus.delete(skuId);
                break;
            case 'decrease':
                if (numberOfBundles > initMin) {
                    this.bundleConstraints[skuId].maxNumberOfBundles = Math.max(0, numberOfBundles - 1);
                    this.bundleConstraints[skuId].minNumberOfBundles = initMin;
                }
                this.lockedSkus.delete(skuId);
                break;
            default:
                throw new Error(`Unknown action: ${action}`);
        }
    }

    updateButtonStates() {
        Object.keys(this.SKUs).forEach(skuId => {
            const row = document.querySelector(`#orderTableDataRowId${skuId}`);
            if (!row) return;
            const bundles = parseInt(row.getAttribute('data-total-bundles'));
            const inc = document.querySelector(`#orderTableDataIncreaseAmountId${skuId}`);
            const dec = document.querySelector(`#orderTableDataDecreaseAmountId${skuId}`);
            const cb = document.querySelector(`#orderTableDataCorrectAmountId${skuId}`);
            const locked = this.lockedSkus.has(skuId);
            if (inc) inc.disabled = locked || bundles >= this.initialBundleConstraints[skuId].maxNumberOfBundles;
            if (dec) dec.disabled = locked || bundles <= this.initialBundleConstraints[skuId].minNumberOfBundles;
            if (cb) { cb.checked = locked; cb.disabled = false; }
        });
    }

    async updateAll(skuId, action, bundles) {
        bundles = parseInt(bundles, 10);
        this._updateConstraints(skuId, action, bundles);

        Object.keys(this.SKUs).forEach(id => {
            const inc = document.querySelector(`#orderTableDataIncreaseAmountId${id}`);
            const dec = document.querySelector(`#orderTableDataDecreaseAmountId${id}`);
            const cb = document.querySelector(`#orderTableDataCorrectAmountId${id}`);
            if (inc) inc.disabled = true;
            if (dec) dec.disabled = true;
            if (cb) cb.disabled = true;
        });

        const apiConstraints = {};
        Object.keys(this.bundleConstraints).forEach(id => {
            apiConstraints[id] = {
                min_bundles: this.bundleConstraints[id].minNumberOfBundles,
                max_bundles: this.bundleConstraints[id].maxNumberOfBundles,
            };
        });

        try {
            const result = await h2oApi.pack(this.orderId, apiConstraints);
            Object.keys(this.bundleConstraints).forEach(id => {
                this.lastBundleConstraints[id] = { ...this.bundleConstraints[id] };
            });
            orderTable = new OrderTable(result.skus, result.solution, this);
        } catch (e) {
            console.error('Pack failed, reverting constraints:', e);
            Object.keys(this.bundleConstraints).forEach(id => {
                this.bundleConstraints[id] = { ...this.lastBundleConstraints[id] };
            });
        }
        this.updateButtonStates();
    }
}

// ── OrderTable ────────────────────────────────────────────────────────────────
let orderTable;

class OrderTable {
    constructor(skus, solution, engine) {
        this.skus = skus;
        this.solution = solution;
        this.engine = engine;
        this.initializeOrderTable();
    }

    handleButtonClick(skuId, action) {
        const row = document.getElementById(`orderTableDataRowId${skuId}`);
        this.engine.updateAll(skuId, action, row.getAttribute('data-total-bundles'));
    }

    createTableRow(skuId, description, numberOfBundles) {
        const row = document.createElement('tr');
        row.id = `orderTableDataRowId${skuId}`;
        row.setAttribute('data-sku-id', skuId);
        row.setAttribute('data-total-bundles', numberOfBundles);
        row.classList.add('orderTableDataRow');

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'correctAmount';
        checkbox.id = `orderTableDataCorrectAmountId${skuId}`;
        checkbox.style.width = '1.1em';
        checkbox.style.height = '1.1em';
        checkbox.style.cursor = 'pointer';
        checkbox.checked = false;
        checkbox.addEventListener('change', () => {
            this.handleButtonClick(skuId, checkbox.checked ? 'correctAmount' : 'notCorrectAmount');
        });

        const incBtn = document.createElement('button');
        incBtn.type = 'button';
        incBtn.id = `orderTableDataIncreaseAmountId${skuId}`;
        incBtn.textContent = 'Increase';
        incBtn.className = 'btn btn-sm btn-outline-primary w-100';
        incBtn.addEventListener('click', () => this.handleButtonClick(skuId, 'increase'));

        const decBtn = document.createElement('button');
        decBtn.type = 'button';
        decBtn.id = `orderTableDataDecreaseAmountId${skuId}`;
        decBtn.textContent = 'Decrease';
        decBtn.className = 'btn btn-sm btn-outline-danger w-100';
        decBtn.addEventListener('click', () => this.handleButtonClick(skuId, 'decrease'));

        const descCell = document.createElement('td');
        descCell.className = 'align-middle';
        descCell.textContent = description;

        const checkCell = document.createElement('td');
        checkCell.className = 'text-center align-middle';
        checkCell.appendChild(checkbox);

        const incCell = document.createElement('td');
        incCell.className = 'align-middle p-1';
        incCell.appendChild(incBtn);

        const decCell = document.createElement('td');
        decCell.className = 'align-middle p-1';
        decCell.appendChild(decBtn);

        row.appendChild(descCell);
        row.appendChild(checkCell);
        row.appendChild(incCell);
        row.appendChild(decCell);
        return row;
    }

    createOrderTable() {
        const tbody = document.getElementById('orderTableTbody');
        tbody.innerHTML = '';

        if (Object.keys(this.skus).length === 1) {
            const skuId = Object.keys(this.skus)[0];
            const sku = this.skus[skuId];
            tbody.appendChild(this.createTableRow(skuId, `${sku.SKU}, ${sku.eagleSticksPerTruckload} sticks`, sku.eagleBundlesPerTruckload));
        } else {
            for (const skuId in this.skus) {
                const sku = this.skus[skuId];
                let totalBundles = 0, totalSticks = 0;
                for (const item of this.solution) {
                    if (item.skuId === skuId) {
                        totalBundles = item.numberOfBundles;
                        totalSticks = sku.calculatedSticksPerBundle * totalBundles;
                        break;
                    }
                }
                tbody.appendChild(this.createTableRow(skuId, `${sku.SKU}, ${totalBundles} bundles, ${totalSticks} sticks`, totalBundles));
            }
        }
    }

    createPackingSlip() {
        const table = document.getElementById('orderTableDetail');
        const thead = table.querySelector('thead');
        const tbody = document.getElementById('orderTableDetailTbody');
        thead.innerHTML = '';
        tbody.innerHTML = '';

        if (Object.keys(this.skus).length === 1) {
            const skuId = Object.keys(this.skus)[0];
            const sku = this.skus[skuId];

            const headerRow = document.createElement('tr');
            ['SKU', 'Bundles', 'Sticks'].forEach(h => {
                const th = document.createElement('th');
                th.textContent = h;
                headerRow.appendChild(th);
            });
            thead.className = 'table-dark';
            thead.appendChild(headerRow);

            const row = document.createElement('tr');
            [sku.SKU, sku.eagleBundlesPerTruckload, sku.eagleSticksPerTruckload].forEach(v => {
                const td = document.createElement('td');
                td.textContent = v;
                row.appendChild(td);
            });
            tbody.appendChild(row);
        } else {
            const combinedData = this.solution.map(item => {
                const sku = this.skus[item.skuId];
                return { ...sku, numberOfBundles: item.numberOfBundles, totalSticks: sku.calculatedSticksPerBundle * item.numberOfBundles };
            });

            let headers = Object.keys(combinedData[0]).filter(h => h !== 'productType' && h !== 'product_type');
            headers = ['SKU', ...headers.filter(h => h !== 'SKU')];

            const headerRow = document.createElement('tr');
            headers.forEach(h => {
                const th = document.createElement('th');
                th.innerHTML = h.replace(/([a-z])([A-Z])/g, '$1<br>$2');
                headerRow.appendChild(th);
            });
            const thTotal = document.createElement('th');
            thTotal.innerHTML = 'Total<br>Sticks';
            headerRow.appendChild(thTotal);
            thead.className = 'table-dark';
            thead.appendChild(headerRow);

            combinedData.forEach(data => {
                const row = document.createElement('tr');
                headers.forEach((h, i) => {
                    const td = document.createElement('td');
                    if (i < 3) td.className = 'text-start';
                    let val = data[h] || '';
                    if (i >= 3 && h !== 'length' && h !== 'data') val = parseInt(val).toLocaleString();
                    td.textContent = val;
                    row.appendChild(td);
                });
                const tdTotal = document.createElement('td');
                tdTotal.className = 'text-end';
                tdTotal.textContent = data.totalSticks.toLocaleString();
                row.appendChild(tdTotal);
                tbody.appendChild(row);
            });
        }
    }

    initializeOrderTable() {
        this.createOrderTable();
        this.createPackingSlip();
        const orderCard = document.getElementById('orderCard');
        const slipCard = document.getElementById('packingSlipCard');
        if (orderCard) orderCard.hidden = false;
        if (slipCard) slipCard.hidden = false;
    }
}

// ── SKU selection UI ──────────────────────────────────────────────────────────
function selectSkus(skus) {
    const body = document.getElementById('skuPickerBody');
    if (!body) return;

    const errDiv = document.createElement('div');
    errDiv.id = 'skuPickerError';
    errDiv.className = 'alert alert-danger d-none mb-3';

    const tableWrap = document.createElement('div');
    tableWrap.className = 'table-responsive mb-3';

    const table = document.createElement('table');
    table.className = 'table table-bordered table-hover mb-0';

    const thead = document.createElement('thead');
    thead.className = 'table-dark';
    const headerRow = document.createElement('tr');
    const th = document.createElement('th');
    th.textContent = 'Pipe';
    headerRow.appendChild(th);
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    Object.values(skus).forEach(sku => {
        const row = document.createElement('tr');
        row.style.cursor = 'pointer';

        const td = document.createElement('td');
        td.className = 'align-middle';
        td.textContent = sku.SKU;

        const cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.name = 'selectedsku';
        cb.value = sku.skuId;
        cb.style.display = 'none';
        td.appendChild(cb);

        td.addEventListener('click', function () {
            cb.checked = !cb.checked;
            row.classList.toggle('table-success', cb.checked);
        });

        row.appendChild(td);
        tbody.appendChild(row);
    });
    table.appendChild(tbody);
    tableWrap.appendChild(table);

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn btn-primary';
    btn.textContent = 'Create Order';

    btn.addEventListener('click', async function () {
        const selected = Array.from(document.querySelectorAll('input[name=selectedsku]:checked')).map(cb => cb.value);
        errDiv.classList.add('d-none');

        if (selected.length === 0) {
            errDiv.textContent = 'Please select at least one pipe before creating an order.';
            errDiv.classList.remove('d-none');
            return;
        }
        if (selected.length > 5) {
            errDiv.textContent = 'Please select a maximum of 5 pipes before creating an order.';
            errDiv.classList.remove('d-none');
            return;
        }

        btn.disabled = true;
        btn.textContent = 'Creating\u2026';
        try {
            const { orderId, packingResult } = await h2oApi.createAndPack(selected);
            const engine = new ApiEngine(packingResult.skus, orderId);
            orderTable = new OrderTable(packingResult.skus, packingResult.solution, engine);
            engine.updateButtonStates();
        } catch (e) {
            errDiv.textContent = 'Failed to create order: ' + e.message;
            errDiv.classList.remove('d-none');
        } finally {
            btn.disabled = false;
            btn.textContent = 'Create Order';
        }
    });

    body.innerHTML = '';
    body.appendChild(errDiv);
    body.appendChild(tableWrap);
    body.appendChild(btn);
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async function () {
    try {
        const skuList = await h2oApi.fetchSkus();
        const skus = {};
        skuList.forEach(sku => { skus[sku.skuId] = sku; });
        selectSkus(skus);
    } catch (e) {
        const body = document.getElementById('skuPickerBody');
        if (body) body.innerHTML = '<p class="text-danger mb-0">Could not load pipe data: ' + e.message + '</p>';
    }
});
