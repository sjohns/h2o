class OrderTable {
    constructor(skus, solution, branchAndBoundEngine) {
        this.skus = skus;
        this.solution = solution;
        this.branchAndBoundEngine = branchAndBoundEngine;
        this.initializeOrderTable();
    }

    createTableCell(content, isElement = false) {
        const cell = document.createElement('td');
        if (isElement) {
            cell.appendChild(content);
        } else {
            cell.textContent = content;
        }
        return cell;
    }

    async handleButtonClick(skuId, action) {
        const row = document.getElementById(`orderTableDataRowId${skuId}`);
        const totalBundles = row ? Number(row.getAttribute('data-total-bundles') || 0) : 0;
        await this.updateAll(skuId, action, totalBundles);
    }

    createTableRow(skuId, description, numberOfBundles) {
        const row = document.createElement('tr');
        row.setAttribute('id', `orderTableDataRowId${skuId}`);
        row.setAttribute('data-sku-id', skuId);
        row.setAttribute('data-total-bundles', String(numberOfBundles));
        row.classList.add('orderTableDataRow');

        const correctAmountCheckbox = document.createElement('input');
        correctAmountCheckbox.type = 'checkbox';
        correctAmountCheckbox.name = 'correctAmount';
        correctAmountCheckbox.setAttribute('data-sku-id', skuId);
        correctAmountCheckbox.id = `orderTableDataCorrectAmountId${skuId}`;
        correctAmountCheckbox.classList.add('orderTableDataCorrectAmount');
        correctAmountCheckbox.checked = false;

        correctAmountCheckbox.addEventListener('change', async () => {
            const action = correctAmountCheckbox.checked ? 'correctAmount' : 'notCorrectAmount';
            await this.handleButtonClick(skuId, action);
        });

        const increaseButton = document.createElement('button');
        increaseButton.type = 'button';
        increaseButton.id = `orderTableDataIncreaseAmountId${skuId}`;
        increaseButton.textContent = 'Increase Amount';
        increaseButton.classList.add('orderTableDataIncreaseAmount');
        increaseButton.addEventListener('click', async () => this.handleButtonClick(skuId, 'increase'));

        const decreaseButton = document.createElement('button');
        decreaseButton.type = 'button';
        decreaseButton.id = `orderTableDataDecreaseAmountId${skuId}`;
        decreaseButton.textContent = 'Decrease Amount';
        decreaseButton.classList.add('orderTableDataDecreaseAmount');
        decreaseButton.addEventListener('click', async () => this.handleButtonClick(skuId, 'decrease'));

        row.appendChild(this.createTableCell(description));
        row.appendChild(this.createTableCell(correctAmountCheckbox, true));
        row.appendChild(this.createTableCell(increaseButton, true));
        row.appendChild(this.createTableCell(decreaseButton, true));

        return row;
    }

    createOrderTable() {
        const tbody = document.getElementById('orderTableTbody');
        tbody.innerHTML = '';

        if (Object.keys(this.skus).length === 1) {
            const skuId = Object.keys(this.skus)[0];
            const sku = this.skus[skuId];
            const bundles = Number(sku.eagleBundlesPerTruckLoad || sku.calculatedBundlesPerTruckload || 0);
            const sticks = Number(sku.eagleSticksPerTruckload || 0);
            const description = `${sku.SKU}, ${sticks} sticks`;
            tbody.appendChild(this.createTableRow(skuId, description, bundles));
            return;
        }

        for (const skuId in this.skus) {
            if (!Object.prototype.hasOwnProperty.call(this.skus, skuId)) {
                continue;
            }
            const sku = this.skus[skuId];
            let totalSticks = 0;
            let totalBundles = 0;

            for (let index = 0; index < this.solution.length; index += 1) {
                if (this.solution[index].skuId === skuId) {
                    const numberOfBundles = Number(this.solution[index].numberOfBundles || 0);
                    const sticksPerBundle = Number(sku.calculatedSticksPerBundle || 0) * numberOfBundles;
                    totalSticks += sticksPerBundle;
                    totalBundles += numberOfBundles;
                    break;
                }
            }

            const description = `${sku.SKU}, ${totalBundles} bundles, ${totalSticks} sticks`;
            tbody.appendChild(this.createTableRow(skuId, description, totalBundles));
        }
    }

    createPackingSlip() {
        const tbody = document.getElementById('orderTableDetailTbody');
        tbody.innerHTML = '';

        if (Object.keys(this.skus).length === 1) {
            const skuId = Object.keys(this.skus)[0];
            const sku = this.skus[skuId];
            const bundles = Number(sku.eagleBundlesPerTruckLoad || sku.calculatedBundlesPerTruckload || 0);
            const sticks = Number(sku.eagleSticksPerTruckload || 0);

            const headerRow = document.createElement('tr');
            ['SKU', 'Bundles', 'Sticks'].forEach((header) => {
                const headerCell = document.createElement('th');
                headerCell.innerHTML = header.replace(/([a-z])([A-Z])/g, '$1<br>$2');
                headerRow.appendChild(headerCell);
            });
            tbody.appendChild(headerRow);

            const row = document.createElement('tr');
            [sku.SKU, bundles, sticks].forEach((value) => {
                const td = document.createElement('td');
                td.textContent = String(value);
                row.appendChild(td);
            });
            tbody.appendChild(row);
            return;
        }

        const combinedData = this.solution.map((solutionItem) => {
            const sku = this.skus[solutionItem.skuId];
            return {
                ...sku,
                numberOfBundles: Number(solutionItem.numberOfBundles || 0),
                totalSticks: Number(sku.calculatedSticksPerBundle || 0) * Number(solutionItem.numberOfBundles || 0),
            };
        });

        if (combinedData.length === 0) {
            return;
        }

        let headers = Object.keys(combinedData[0]).filter((header) => header !== 'productType' && header !== 'product_type');
        headers = headers.filter((header) => header !== 'SKU');
        headers.unshift('SKU');

        const headerRow = document.createElement('tr');
        headers.forEach((header) => {
            const headerCell = document.createElement('th');
            headerCell.innerHTML = header.replace(/([a-z])([A-Z])/g, '$1<br>$2');
            headerRow.appendChild(headerCell);
        });
        const thTotalSticks = document.createElement('th');
        thTotalSticks.innerHTML = 'Total<br>Sticks';
        headerRow.appendChild(thTotalSticks);
        tbody.appendChild(headerRow);

        combinedData.forEach((data) => {
            const row = document.createElement('tr');
            headers.forEach((header, headerIndex) => {
                const td = document.createElement('td');
                if (headerIndex < 3) {
                    td.classList.add('left');
                }
                let cellValue = data[header] ?? '';
                if (headerIndex >= 3 && header !== 'lingth' && header !== 'date') {
                    const numericValue = Number(cellValue);
                    cellValue = Number.isFinite(numericValue) ? Math.trunc(numericValue).toLocaleString() : String(cellValue);
                }
                td.textContent = String(cellValue);
                row.appendChild(td);
            });

            const tdTotalSticks = document.createElement('td');
            tdTotalSticks.textContent = Number(data.totalSticks || 0).toLocaleString();
            row.appendChild(tdTotalSticks);
            tbody.appendChild(row);
        });
    }

    async updateAll(skuId, action, totalBundles) {
        await this.branchAndBoundEngine.updateAll(skuId, action, totalBundles);
    }

    initializeOrderTable() {
        this.createOrderTable();
        this.createPackingSlip();
    }
}

let orderTable;
