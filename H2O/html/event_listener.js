/**
 * This script is responsible for managing the SKU selection interface within the web application.
 * 
 * It contains two primary functionalities:
 * 1. Clearing the contents of a DOM element.
 * 2. Initializing the application and processing SKU data when the DOM content has fully loaded.
 * 
 * Functionality Overview:
 * 
 * 1. **Clear Element**:
 *    - The `clearElement` function removes all child elements of a given DOM element. 
 *    - This can be useful when you need to reset the contents of a container before dynamically adding new elements.
 * 
 *    Parameters:
 *    - element (HTMLElement): The DOM element whose child elements are to be removed.
 * 
 *    Example Usage:
 * 
 *    const container = document.getElementById('container');
 *    clearElement(container);
 * 
 *    Output:
 *    - The container will be empty, with all child elements removed.
 * 
 * 2. **DOMContentLoaded Event Listener**:
 *    - This event listener waits for the DOM content to be fully loaded, ensuring that all necessary elements are available 
 *      for manipulation.
 *    - Once the DOM is ready, it processes packing data, extracts SKUs, renders the SKU selection interface, and ensures 
 *      the SKU selection is correctly displayed.
 * 
 *    Event:
 *    - DOMContentLoaded: Fired when the initial HTML document has been completely loaded and parsed.
 * 
 *    Example Usage:
 * 
 *    document.addEventListener('DOMContentLoaded', function () {
 *        // Initialization logic here
 *    });
 * 
 *    Output:
 *    - The application is initialized, and SKUs are processed and displayed as per the logic defined in the event listener.
 * 
 * Date: 2024-07-05
 * Author: Stephen Johns
 */

/**
 * The clearElement function is responsible for removing all child elements of a given DOM element.
 */
function clearElement(element) {
    // Continuously remove the first child element until there are no more child elements
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

/**
 * The DOMContentLoaded event listener is responsible for initializing the application once the DOM has been fully loaded.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Process packing data to extract SKUs
    const SKUs = processPackingData(packingData);

    // Log the processed SKUs to the console (for debugging purposes, uncomment if needed)
    // console.log(SKUs);

    // Call the selectSkus function with the processed SKUs to render the SKU selection interface
    selectSkus(SKUs);

    // Get the 'selectSkus' div element by its ID
    const selectSkusDiv = document.getElementById('selectSkus');

    // If the 'selectSkus' div is empty after the initial rendering
    if (selectSkusDiv.children.length === 0) {
        // Re-run the selectSkus function with the processed SKUs
        const selectedSkus = selectSkus(SKUs);

        // Log the selected SKUs to the console (for debugging purposes, uncomment if needed)
        // console.log("Selected Pipe SKUs:", selectedSkus);
    }
});
