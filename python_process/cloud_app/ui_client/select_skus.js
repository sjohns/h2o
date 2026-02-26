let branchAndBoundEngine;

function selectSkus(skus) {
    if (!skus || typeof skus !== 'object' || Object.keys(skus).length === 0) {
        return;
    }

    const selectSkusDiv = document.getElementById('selectSkus');
    if (!selectSkusDiv) {
        return;
    }

    let contentDiv = document.createElement('div');
    contentDiv.style.display = 'flex';
    contentDiv.style.flexDirection = 'column';
    contentDiv.style.alignItems = 'center';

    const title = document.createElement('h1');
    title.textContent = 'Select Pipe(s)';
    title.style.textAlign = 'center';
    contentDiv.appendChild(title);

    const table = document.createElement('table');
    table.border = '1';

    const tableHeader = document.createElement('tr');
    const header = document.createElement('th');
    header.textContent = 'Pipes';
    tableHeader.appendChild(header);
    table.appendChild(tableHeader);

    Object.values(skus)
        .sort((left, right) => Number(left.displayOrder || 0) - Number(right.displayOrder || 0))
        .forEach((sku) => {
            if (String(sku.activeFlag || 'Y').toUpperCase() !== 'Y') {
                return;
            }

            const row = document.createElement('tr');

            const skuIdCell = document.createElement('td');
            skuIdCell.style.display = 'none';
            skuIdCell.textContent = sku.skuId;

            const skuDescriptionCell = document.createElement('td');
            skuDescriptionCell.textContent = sku.SKU;
            skuDescriptionCell.style.cursor = 'pointer';
            skuDescriptionCell.addEventListener('click', function () {
                const checkbox = this.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
                this.parentNode.style.backgroundColor = checkbox.checked ? 'lightgreen' : '';
            });

            row.appendChild(skuIdCell);
            row.appendChild(skuDescriptionCell);

            const selectCheckbox = document.createElement('input');
            selectCheckbox.type = 'checkbox';
            selectCheckbox.name = 'selectedsku';
            selectCheckbox.value = sku.skuId;
            selectCheckbox.style.display = 'none';
            skuDescriptionCell.appendChild(selectCheckbox);

            table.appendChild(row);
        });

    contentDiv.appendChild(table);

    const createOrderButton = document.createElement('button');
    createOrderButton.textContent = 'Create Order';
    contentDiv.appendChild(createOrderButton);

    selectSkusDiv.appendChild(contentDiv);

    createOrderButton.addEventListener('click', async function () {
        const selectedskus = Array.from(document.querySelectorAll('input[name=selectedsku]:checked')).map((checkbox) => checkbox.value);

        if (selectedskus.length === 0) {
            alert('Please select at least one pipe sku before creating an order.');
            return;
        }
        if (selectedskus.length > 5) {
            alert('Please select a maximum of 5 pipe skus before creating an order.');
            return;
        }

        const selectedSkuMap = {};
        selectedskus.forEach((skuId) => {
            if (skus[skuId]) {
                selectedSkuMap[skuId] = {...skus[skuId]};
            }
        });

        try {
            const orderResponse = await fetch('/order', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({selected_sku_ids: Object.keys(selectedSkuMap)}),
            });
            const orderPayload = await orderResponse.json();
            if (!orderResponse.ok) {
                throw new Error(orderPayload.detail || JSON.stringify(orderPayload));
            }

            const preparedSkus = orderPayload.skus || {};
            const lcmValue = Number(orderPayload.lcmValue || 1);
            const ratiosCalculator = new CalculateRatios(preparedSkus);
            branchAndBoundEngine = new BranchAndBoundEngine(preparedSkus, lcmValue, ratiosCalculator);

            const solution = await branchAndBoundEngine.bestSolution();
            orderTable = new OrderTable(preparedSkus, solution, branchAndBoundEngine);
            branchAndBoundEngine.updateButtonStates();
        } catch (error) {
            alert(`No possible solutions for current selection: ${error.message}`);
        }
    });
}
