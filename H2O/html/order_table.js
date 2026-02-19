/**
 * The OrderTable class is responsible for managing the creation and interaction of order tables and packing slips 
 * in a logistics or inventory management system. This class handles the display and modification of SKU (Stock Keeping Unit) 
 * data, allowing users to manage bundle amounts and generate packing slips based on the current order solution.
 * 
 * **Explanation:**
 * 
 * The `OrderTable` class provides a user interface for managing orders by creating dynamic HTML tables that represent 
 * the SKUs involved in an order. It allows for increasing or decreasing the number of bundles for each SKU, marking SKUs 
 * as correct or incorrect in quantity, and generating packing slips that summarize the order.
 * 
 * **Core Functionalities:**
 * 
 * 1. **Table Cell Creation**:
 *    - The `createTableCell` function creates table cells (`<td>`) either containing plain text or HTML elements.
 * 
 * 2. **Button Click Handling**:
 *    - The `handleButtonClick` function responds to user interactions, such as increasing or decreasing bundle amounts 
 *      or marking an SKU as having the correct amount.
 * 
 * 3. **Order Table Creation**:
 *    - The `createOrderTable` function generates the main order table, listing all SKUs with relevant data, such as 
 *      bundle amounts and stick counts.
 * 
 * 4. **Packing Slip Creation**:
 *    - The `createPackingSlip` function generates a detailed packing slip that summarizes the order, including SKUs, 
 *      bundles, and sticks.
 * 
 * 5. **Order Table Initialization**:
 *    - The `initializeOrderTable` function initializes the order table and packing slip by creating them based on the 
 *      current SKU data and solution.
 * 
 * **Example Usage:**
 * 
 * const skus = {
 *     sku1: { SKU: 'A123', calculatedSticksPerBundle: 10, eagleBundlesPerTruckload: 5, eagleSticksPerTruckload: 50 },
 *     sku2: { SKU: 'B456', calculatedSticksPerBundle: 15, eagleBundlesPerTruckload: 3, eagleSticksPerTruckload: 45 },
 * };
 * 
 * const solution = [
 *     { skuId: 'sku1', numberOfBundles: 5 },
 *     { skuId: 'sku2', numberOfBundles: 3 },
 * ];
 * 
 * const branchAndBoundEngine = new BranchAndBoundEngine(); // Assumes a pre-existing class
 * const orderTable = new OrderTable(skus, solution, branchAndBoundEngine);
 * 
 * Output:
 * - The web page will display an order table and packing slip based on the provided SKUs and solution.
 * 
 * Date: 2024-07-12
 * Author: Stephen Johns
 */

class OrderTable {
    constructor(skus, solution, branchAndBoundEngine) {
        this.skus = skus;
        this.solution = solution;
        this.branchAndBoundEngine = branchAndBoundEngine;
        this.initializeOrderTable();
    }

    /**
     * Creates a table cell with the given content.
     * @param {string|HTMLElement} content - The content to be placed in the cell.
     * @param {boolean} isElement - Flag indicating if the content is an HTML element.
     * @return {HTMLElement} The created table cell.
     */
    createTableCell(content, isElement = false) {
        const cell = document.createElement('td');
        if (isElement) {
            cell.appendChild(content);
        } else {
            cell.textContent = content;
        }
        return cell;
    }

    /**
     * Handles button click events for increasing or decreasing bundle amounts.
     * @param {string} skuId - The SKU ID.
     * @param {string} action - The action to be performed (increase, decrease, etc.).
     */
    handleButtonClick(skuId, action) {
        const row = document.getElementById(`orderTableDataRowId${skuId}`);
        const totalBundles = row.getAttribute('data-total-bundles');
        this.updateAll(skuId, action, totalBundles);
    }

    /**
     * Creates a table row for the order table.
     * @param {string} skuId - The SKU ID.
     * @param {string} description - The description of the SKU.
     * @param {number} numberOfBundles - The number of bundles.
     * @return {HTMLElement} The created table row.
     */
    createTableRow(skuId, description, numberOfBundles) {
        const row = document.createElement('tr');
        row.setAttribute('id', `orderTableDataRowId${skuId}`);
        row.setAttribute('data-sku-id', skuId);
        row.setAttribute('data-total-bundles', numberOfBundles);
        row.setAttribute('data-action', 'none');
        row.classList.add('orderTableDataRow');

        // Create and configure checkbox for marking the correct amount.
        const correctAmountCheckbox = document.createElement('input');
        correctAmountCheckbox.type = 'checkbox';
        correctAmountCheckbox.name = 'correctAmount';
        correctAmountCheckbox.setAttribute('data-sku-id', skuId);
        correctAmountCheckbox.id = `orderTableDataCorrectAmountId${skuId}`;
        correctAmountCheckbox.classList.add('orderTableDataCorrectAmount');
		correctAmountCheckbox.checked = false;

        correctAmountCheckbox.addEventListener('change', () => {
            const action = correctAmountCheckbox.checked ? 'correctAmount' : 'notCorrectAmount';
            this.handleButtonClick(skuId, action);
        });

        // Create and configure button for increasing the amount.
        const increaseButton = document.createElement('button');
        increaseButton.type = 'button';
        increaseButton.id = `orderTableDataIncreaseAmountId${skuId}`;
        increaseButton.textContent = 'Increase Amount';
        increaseButton.classList.add('orderTableDataIncreaseAmount');
        increaseButton.addEventListener('click', () => this.handleButtonClick(skuId, 'increase'));

        // Create and configure button for decreasing the amount.
        const decreaseButton = document.createElement('button');
        decreaseButton.type = 'button';
        decreaseButton.id = `orderTableDataDecreaseAmountId${skuId}`;
        decreaseButton.textContent = 'Decrease Amount';
        decreaseButton.classList.add('orderTableDataDecreaseAmount');
        decreaseButton.addEventListener('click', () => this.handleButtonClick(skuId, 'decrease'));

        // Append all created elements to the row.
        row.appendChild(this.createTableCell(description));
        row.appendChild(this.createTableCell(correctAmountCheckbox, true));
        row.appendChild(this.createTableCell(increaseButton, true));
        row.appendChild(this.createTableCell(decreaseButton, true));

        return row;
    }

    /**
     * Creates the order table with the current SKUs and solution.
     */
    createOrderTable() {
        console.log('solution: ', this.solution);
        const tbody = document.getElementById('orderTableTbody');
        tbody.innerHTML = ''; // Clear existing rows

        if (Object.keys(this.skus).length === 1) {
            // Handle the case where there is only one SKU
            const skuId = Object.keys(this.skus)[0];
            const sku = this.skus[skuId];
            const description = `${sku.SKU},  ${sku.eagleSticksPerTruckload} sticks`;
            tbody.appendChild(this.createTableRow(skuId, description, sku.eagleBundlesPerTruckload));
        } else {
            // Handle the case where there are multiple SKUs
            for (const skuId in this.skus) {
                if (this.skus.hasOwnProperty(skuId)) {
                    const sku = this.skus[skuId];
//                    console.log('sku: ', sku);
                    let totalSticks = 0;
                    let totalBundles = 0;

                    for (let i = 0; i < this.solution.length; i++) {
                        if (this.solution[i].skuId === skuId) {
                            const numberOfBundles = this.solution[i].numberOfBundles;
                            const sticksPerBundle = sku.calculatedSticksPerBundle * numberOfBundles;
//                            console.log('sticksPerBundle: ', sticksPerBundle);
                            totalSticks += sticksPerBundle;
                            totalBundles += numberOfBundles;
                            break;
                        }
                    }

                    const description = `${sku.SKU}, ${totalBundles} bundles, ${totalSticks} sticks`;
                    tbody.appendChild(this.createTableRow(skuId, description, totalBundles));
                }
            }
        }
    // Check all checkboxes in the table after rows are created
    const checkboxes = tbody.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        console.log(`Checkbox ID: ${checkbox.id}, Checked: ${checkbox.checked}`);
    });		
	
    }

    /**
     * Creates the packing slip table with the combined SKU and solution data.
     */
    createPackingSlip() {
        const tbody = document.getElementById('orderTableDetailTbody');
        tbody.innerHTML = ''; // Clear existing rows

        if (Object.keys(this.skus).length === 1) {
            // Handle the case where there is only one SKU
            const skuId = Object.keys(this.skus)[0];
            const sku = this.skus[skuId];
            const bundles = sku.eagleBundlesPerTruckload;
            const sticks = sku.eagleSticksPerTruckload;

            // Create header row
            const headerRow = document.createElement('tr');
            const headers = ['SKU', 'Bundles', 'Sticks'];

            headers.forEach(header => {
                const headerCell = document.createElement('th');
                headerCell.innerHTML = header.replace(/([a-z])([A-Z])/g, '$1<br>$2'); // Convert camelCase to multi-line header
                headerRow.appendChild(headerCell);
            });

            tbody.appendChild(headerRow);

            // Create data row
            const row = document.createElement('tr');
            const data = [sku.SKU, bundles, sticks];

            data.forEach(value => {
                const td = document.createElement('td');
                td.textContent = value;
                row.appendChild(td);
            });

            tbody.appendChild(row);
        } else {
            // Handle the case where there are multiple SKUs
            // Get the solution information and combine with SKU data
            const combinedData = this.solution.map(solutionItem => {
                const sku = this.skus[solutionItem.skuId];
                return {
                    ...sku,
                    numberOfBundles: solutionItem.numberOfBundles,
                    totalSticks: sku.calculatedSticksPerBundle * solutionItem.numberOfBundles
                };
            });

            // Get the first SKU to extract the column headers
            const firstSku = combinedData[0];
            let headers = Object.keys(firstSku).filter(header => header !== 'productType' && header !== 'product_type'); // Remove 'productType' and 'product_type'

            // Ensure 'SKU' is the first column
            headers = headers.filter(header => header !== 'SKU');
            headers.unshift('SKU');

            // Create header row dynamically
            const headerRow = document.createElement('tr');
            headers.forEach(header => {
                const headerCell = document.createElement('th');
                headerCell.innerHTML = header.replace(/([a-z])([A-Z])/g, '$1<br>$2'); // Convert camelCase to multi-line header
                headerRow.appendChild(headerCell);
            });

            // Add custom header for total sticks
            const thTotalSticks = document.createElement('th');
            thTotalSticks.innerHTML = 'Total<br>Sticks';
            headerRow.appendChild(thTotalSticks);

            tbody.appendChild(headerRow);

            // Create data rows dynamically
            combinedData.forEach((data, index) => {
                const row = document.createElement('tr');

                headers.forEach((header, headerIndex) => {
                    const td = document.createElement('td');
                    if (headerIndex < 3) {
                        td.classList.add('left'); // Left-align first 3 columns
                    }
                    let cellValue = data[header] || ''; // Add cell value or empty string if undefined
                    if (headerIndex >= 3 && header !== 'length' && header !== 'data') {
                        cellValue = parseInt(cellValue).toLocaleString(); // Format as integer with comma thousand separator
                    }
                    td.textContent = cellValue;
                    row.appendChild(td);
                });

                // Add total sticks
                const tdTotalSticks = document.createElement('td');
                tdTotalSticks.textContent = data.totalSticks.toLocaleString(); // Format total sticks with comma thousand separator
                row.appendChild(tdTotalSticks);

                tbody.appendChild(row);
            });
        }

        console.log('Packing slip created successfully.'); // Debug log
    }

    /**
     * Updates all relevant parts of the system based on the action performed.
     * @param {string} skuId - The SKU ID.
     * @param {string} action - The action to be performed.
     * @param {number} totalBundles - The total number of bundles.
     */
    updateAll(skuId, action, totalBundles) {
        this.branchAndBoundEngine.updateAll(skuId, action, totalBundles);
    }

    /**
     * Initializes the order table and packing slip by creating them.
     */
    initializeOrderTable() {
        this.createOrderTable();
        this.createPackingSlip();
    }
}

// Example initialization
let orderTable;
