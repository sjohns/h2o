/**
 * This script provides utilities for calculating the Least Common Multiple (LCM) of various numbers, particularly 
 * focusing on its application to SKU data in the context of logistics and inventory management.
 * 
 * **Explanation of LCM (Least Common Multiple):**
 * 
 * The Least Common Multiple (LCM) of two or more integers is the smallest positive integer that is divisible by each of the 
 * integers. For example, the LCM of 4 and 5 is 20 because 20 is the smallest number that both 4 and 5 divide into without 
 * leaving a remainder.
 * 
 * **Usage of LCM:**
 * 
 * LCM is widely used in various mathematical and practical applications where synchronization or alignment of cycles is 
 * necessary. In the context of this script, the LCM is used to determine the optimal bundle size for transporting goods 
 * (e.g., SKUs) by truckload, ensuring that all SKUs can be evenly distributed without leftover space.
 * 
 * **Calculation Process:**
 * 
 * 1. **Greatest Common Divisor (GCD) Calculation:**
 *    - The GCD is the largest positive integer that divides each of the integers without leaving a remainder.
 *    - The LCM of two numbers can be calculated using their GCD with the formula:
 *      \[
 *      \text{LCM}(a, b) = \frac{|a \times b|}{\text{GCD}(a, b)}
 *      \]
 * 
 * 2. **LCM of Multiple Numbers:**
 *    - The LCM of an array of numbers is calculated iteratively using the LCM of pairs of numbers.
 *    - The `calculateLCMOfArray` function implements this by reducing the array to a single LCM value.
 * 
 * 3. **Application to SKUs:**
 *    - The LCM is applied to SKU data to determine the `calculatedBundleSize` for each SKU, ensuring that bundles are 
 *      optimally sized for truckload transportation.
 * 
 * **Example Usage:**
 * 
 * const SKUs = {
 *     sku1: { calculatedBundlesPerTruckload: 4, calculatedSticksPerBundle: 10, eagleSticksPerTruckload: 40 },
 *     sku2: { calculatedBundlesPerTruckload: 5, calculatedSticksPerBundle: 8, eagleSticksPerTruckload: 40 },
 * };
 * 
 * calculateBundlesPerTruckload(SKUs);
 * const lcmValue = calculateLCMFromSKUs(SKUs);
 * calculateAdditionalFields(SKUs, lcmValue);
 * 
 * Output:
 * - The SKUs object will be updated with a `calculatedBundleSize` field based on the calculated LCM.
 * 
 * Date: 2024-07-12
 * Author: Stephen Johns
 */

/**
 * Helper function to calculate the Greatest Common Divisor (GCD)
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} - The GCD of the two numbers
 */
function gcd(a, b) {
    while (b) {
        const t = b;
        b = a % b;
        a = t;
    }
    return a;
}

/**
 * Helper function to calculate the Least Common Multiple (LCM) of two numbers
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} - The LCM of the two numbers
 */
function lcm(a, b) {
    return (a * b) / gcd(a, b);
}

/**
 * Function to calculate the LCM of an array of numbers
 * @param {number[]} numbers - Array of numbers
 * @returns {number} - The LCM of the array of numbers
 */
function calculateLCMOfArray(numbers) {
    return numbers.reduce((acc, num) => lcm(acc, num), 1);
}

/**
 * Function to extract calculatedBundlesPerTruckload values from SKUs object and calculate their LCM
 * @param {Object} SKUs - The SKUs object containing SKU information
 * @returns {number} - The LCM of the calculatedBundlesPerTruckload values
 */
function calculateLCMFromSKUs(SKUs) {
    const calculatedBundlesPerTruckloadValues = [...new Set(Object.values(SKUs).map(SKU => SKU.calculatedBundlesPerTruckload))];
    return calculateLCMOfArray(calculatedBundlesPerTruckloadValues);
}

/**
 * Function to update SKUs with additional fields based on the LCM value
 * @param {Object} SKUs - The SKUs object containing SKU information
 * @param {number} lcmValue - The LCM value to use for calculations
 */
function calculateAdditionalFields(SKUs, lcmValue) {
    Object.values(SKUs).forEach(SKU => {
        SKU.calculatedBundleSize = lcmValue / SKU.calculatedBundlesPerTruckload;
    });
}

/**
 * Function to calculate the number of bundles per truckload for each SKU
 * @param {Object} SKUs - The SKUs object containing SKU information
 */
function calculateBundlesPerTruckload(SKUs) {
    Object.values(SKUs).forEach(SKU => {
        SKU.calculatedBundlesPerTruckload = Math.floor(SKU.eagleSticksPerTruckload / SKU.calculatedSticksPerBundle);
    });
}
