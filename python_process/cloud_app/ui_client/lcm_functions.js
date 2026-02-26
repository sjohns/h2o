function gcd(a, b) {
    while (b) {
        const t = b;
        b = a % b;
        a = t;
    }
    return a;
}

function lcm(a, b) {
    return (a * b) / gcd(a, b);
}

function calculateLCMOfArray(numbers) {
    return numbers.reduce((acc, num) => lcm(acc, num), 1);
}

function calculateLCMFromSKUs(SKUs) {
    const values = [...new Set(Object.values(SKUs).map((sku) => sku.calculatedBundlesPerTruckload))];
    return calculateLCMOfArray(values);
}

function calculateAdditionalFields(SKUs, lcmValue) {
    Object.values(SKUs).forEach((sku) => {
        sku.calculatedBundleSize = lcmValue / Math.max(1, sku.calculatedBundlesPerTruckload);
    });
}

function calculateBundlesPerTruckload(SKUs) {
    Object.values(SKUs).forEach((sku) => {
        const sticks = Number(sku.eagleSticksPerTruckload || 0);
        const perBundle = Math.max(1, Number(sku.calculatedSticksPerBundle || 0));
        sku.calculatedBundlesPerTruckload = Math.floor(sticks / perBundle);
    });
}
