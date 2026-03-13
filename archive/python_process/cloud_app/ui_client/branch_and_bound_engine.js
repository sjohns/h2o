class BranchAndBoundEngine {
    constructor(SKUs, lcmValue, ratiosCalculator) {
        this.SKUs = SKUs;
        this.fullTruckSize = lcmValue;
        this.ratiosCalculator = ratiosCalculator;
        this.bundleConstraints = {};
        this.lastSolution = [];
        this._initializeConstraints();
    }

    _initializeConstraints() {
        Object.values(this.SKUs).forEach((sku) => {
            this.bundleConstraints[sku.skuId] = {
                minNumberOfBundles: 0,
                maxNumberOfBundles: Math.max(0, Number(sku.calculatedBundlesPerTruckload || 0)),
            };
        });
    }

    _buildPayload() {
        const fixedBundles = {};
        const minBundles = {};
        const maxBundles = {};

        Object.entries(this.bundleConstraints).forEach(([skuId, constraints]) => {
            if (constraints.minNumberOfBundles === constraints.maxNumberOfBundles) {
                fixedBundles[skuId] = constraints.minNumberOfBundles;
            } else {
                minBundles[skuId] = constraints.minNumberOfBundles;
                maxBundles[skuId] = constraints.maxNumberOfBundles;
            }
        });

        return {
            selected_sku_ids: Object.keys(this.SKUs),
            truck_fill_ratio: 1,
            fixed_bundles: fixedBundles,
            min_bundles: minBundles,
            max_bundles: maxBundles,
        };
    }

    async _calculateFromApi() {
        const payload = this._buildPayload();
        let response = await fetch('/api/calculate/replacement', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload),
            });
        }

        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.detail || JSON.stringify(result));
        }

        this.fullTruckSize = Number(result.lcm || this.fullTruckSize);
        this.lastSolution = (result.solution || []).map((item) => ({
            skuId: item.sku_id,
            numberOfBundles: Number(item.number_of_bundles),
            totalSticks: Number(item.total_sticks || 0),
        }));
        return this.lastSolution;
    }

    async bestSolution() {
        return this._calculateFromApi();
    }

    updateButtonStates() {
        Object.keys(this.SKUs).forEach((skuId) => {
            const row = document.querySelector(`#orderTableDataRowId${skuId}`);
            if (!row) {
                return;
            }
            const numberOfBundles = Number(row.getAttribute('data-total-bundles') || 0);
            const constraints = this.bundleConstraints[skuId];

            const increaseButton = document.querySelector(`#orderTableDataIncreaseAmountId${skuId}`);
            const decreaseButton = document.querySelector(`#orderTableDataDecreaseAmountId${skuId}`);
            if (increaseButton) {
                increaseButton.disabled = numberOfBundles >= constraints.maxNumberOfBundles;
            }
            if (decreaseButton) {
                decreaseButton.disabled = numberOfBundles <= constraints.minNumberOfBundles;
            }
        });
    }

    _updateConstraints(skuId, action, numberOfBundles) {
        const constraints = this.bundleConstraints[skuId];
        if (!constraints) {
            return;
        }

        switch (action) {
            case 'correctAmount':
                constraints.minNumberOfBundles = numberOfBundles;
                constraints.maxNumberOfBundles = numberOfBundles;
                break;
            case 'notCorrectAmount':
                constraints.minNumberOfBundles = 0;
                constraints.maxNumberOfBundles = Math.max(0, Number(this.SKUs[skuId].calculatedBundlesPerTruckload || 0));
                break;
            case 'increase':
                constraints.minNumberOfBundles = Math.max(0, numberOfBundles + 1);
                break;
            case 'decrease':
                constraints.maxNumberOfBundles = Math.max(0, numberOfBundles - 1);
                break;
            default:
                break;
        }
    }

    async updateAll(skuId, action, bundles) {
        const parsedBundles = Number(bundles || 0);
        this._updateConstraints(skuId, action, parsedBundles);
        const bestSolution = await this.bestSolution();
        orderTable = new OrderTable(this.SKUs, bestSolution, this);
        this.updateButtonStates();
    }
}
