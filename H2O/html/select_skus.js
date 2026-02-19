/**
 * selectSkus function:
 * - This function dynamically creates a SKU selection interface and allows users to select SKUs for creating orders.
 * 
 * Overview:
 * The purpose of this function is to create a user interface for selecting SKUs (Stock Keeping Units) from a provided SKU object.
 * It dynamically generates a table where each row represents a SKU, and users can select SKUs by clicking on their descriptions.
 * After selecting the desired SKUs, users can create an order by clicking the "Create Order" button.
 * 
 * Description:
 * This function sets up a table to display SKUs, allows users to select SKUs by clicking on their descriptions, and includes a button to create an order.
 * It performs various checks to ensure that valid SKUs are selected and then proceeds with further actions using the selected SKUs.
 * 
 * Variables:
 * - skus: The SKUs containing SKU information.
 * 
 * Methods:
 * 
 * 1. Validate SKUs:
 *    - Checks if the provided SKUs object is valid.
 *    - Ensures the 'selectSkus' div element exists in the DOM.
 * 
 * 2. Create SKU Selection Table:
 *    - Dynamically generates a table to display SKU descriptions.
 *    - Adds click event listeners to SKU descriptions for selection.
 * 
 * 3. Create Order Button:
 *    - Adds a "Create Order" button to the interface.
 *    - Validates the selected SKUs and performs further actions.
 * 
 * Example Usage:
 * 
 * const skus = {
 *     sku1: { skuId: 'sku1', SKU: 'Pipe A', sticksPerBundle: 10, popularityScore: 5 },
 *     sku2: { skuId: 'sku2', SKU: 'Pipe B', sticksPerBundle: 20, popularityScore: 3 },
 * };
 * 
 * selectSkus(skus);
 * 
 * Output:
 * - A dynamically generated SKU selection interface.
 * 
 * Date: 2024-06-26
 * Author: Stephen Johns
 */

function selectSkus(skus) {
    // Check if skus object is valid
    if (!skus || typeof skus !== 'object' || Object.keys(skus).length === 0) {
        console.error('Invalid skus object provided.');
        return;
    }

    // Get the 'selectSkus' div element
    const selectSkusDiv = document.getElementById('selectSkus');
    if (!selectSkusDiv) {
        console.error('Element with id "selectSkus" not found.');
        return;
    }

    // Create a container for the sku selection content
    let contentDiv = document.createElement('div');
    contentDiv.style.display = 'flex';
    contentDiv.style.flexDirection = 'column';
    contentDiv.style.alignItems = 'center';

    // Create a title for the sku selection
    const title = document.createElement('h1');
    title.textContent = 'Select Pipe(s)';
    title.style.textAlign = 'center';
    contentDiv.appendChild(title);

    // Create a table for sku selection
    const table = document.createElement('table');
    table.border = '1';

    // Create a table header
    const tableHeader = document.createElement('tr');
    const headerText = ['Pipes'];

    // Add headers to the table header
    headerText.forEach(text => {
        const header = document.createElement('th');
        header.textContent = text;
        tableHeader.appendChild(header);
    });

    // Append the table header to the table
    table.appendChild(tableHeader);

    // Iterate over each active sku
    Object.values(skus).forEach(sku => {
        const skuDescription = sku.SKU;

        // Create a row for sku details
        const row = document.createElement('tr');

        // Create cells for each property
        const skuIdCell = document.createElement('td');
        skuIdCell.style.display = 'none'; // Hide the skuId cell
        skuIdCell.textContent = sku.skuId;

        const skuDescriptionCell = document.createElement('td');
        skuDescriptionCell.textContent = skuDescription;
        skuDescriptionCell.style.cursor = 'pointer'; // Change cursor to pointer
        skuDescriptionCell.addEventListener('click', function () {
            const selectCheckbox = this.querySelector('input[type="checkbox"]');
            selectCheckbox.checked = !selectCheckbox.checked; // Toggle checkbox
            if (selectCheckbox.checked) {
                this.parentNode.style.backgroundColor = 'lightgreen'; // Highlight row
            } else {
                this.parentNode.style.backgroundColor = ''; // Reset to default
            }
        });

        // Append cells to the row
        row.appendChild(skuIdCell);
        row.appendChild(skuDescriptionCell);

        // Create a hidden checkbox
        const selectCheckbox = document.createElement('input');
        selectCheckbox.type = 'checkbox';
        selectCheckbox.name = 'selectedsku'; // Fixed name attribute
        selectCheckbox.value = sku.skuId; // Assuming skuId is the unique identifier
        selectCheckbox.style.display = 'none'; // Hide the checkbox
        skuDescriptionCell.appendChild(selectCheckbox);

        // Append the row to the table
        table.appendChild(row);
    });

    // Append the table to the content div
    contentDiv.appendChild(table);

    // Create a "Create Order" button
    const createOrderButton = document.createElement('button');
    createOrderButton.textContent = 'Create Order';
    contentDiv.appendChild(createOrderButton);

    // Append the content div to the 'selectSkus' div
    selectSkusDiv.appendChild(contentDiv);

    // Add a click event listener to the "Create Order" button
    createOrderButton.addEventListener('click', function () {
        // Get selected skus
        let selectedskus = Array.from(document.querySelectorAll('input[name=selectedsku]:checked')).map(checkbox => checkbox.value);

        // Check if at least one sku is selected
        if (selectedskus.length === 0) {
            alert('Please select at least one pipe sku before creating an order.');
        } else if (selectedskus.length > 5) {
            alert('Please select a maximum of 5 pipe skus before creating an order.');
        } else {
            // Filter out skus not in selectedskus from skus object
            for (const skuId in skus) {
                if (!selectedskus.includes(skuId)) {
                    delete skus[skuId];
                }
            }
            console.log('Selected SKUs:', skus);
            
                    const skuIds = Object.keys(skus);

            
            // Calculate the least common multiple (LCM) for the selected SKUs
             calculateBundlesPerTruckload(skus);
            const lcmValue = calculateLCMFromSKUs(skus);
            console.log("LCM of calculatedBundlesPerTruckload values:", lcmValue);
            
            // Calculate additional fields for each SKU
            calculateAdditionalFields(skus, lcmValue);

            // Initialize the ratios calculator with the selected SKUs
            const ratiosCalculator = new CalculateRatios(skus);

            // Initialize the Branch and Bound engine with the selected SKUs and the calculated LCM value
            branchAndBoundEngine = new BranchAndBoundEngine(skus, lcmValue, ratiosCalculator);

            // Get the best solution from the Branch and Bound engine
            const solution = branchAndBoundEngine.bestSolution();

            // Initialize the order table with the selected SKUs and the best solution
            const orderTable = new OrderTable(skus, solution, branchAndBoundEngine);

            // Update the button states in the Branch and Bound engine
            branchAndBoundEngine.updateButtonStates();
        }
    });
    
    
}
