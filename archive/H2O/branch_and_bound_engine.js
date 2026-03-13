
/**
 * BranchAndBoundEngine class:
 * - This class implements a Branch and Bound algorithm to find optimal combinations of SKUs that fit within a given truck size while adhering to various constraints.
 * 
 * Overview:
 * The `BranchAndBoundEngine` class is designed to determine the best way to load a truck with bundles of SKUs (Stock Keeping Units) based on predefined constraints. 
 * The class uses the Branch and Bound method, a popular algorithm in combinatorial optimization, to explore all possible combinations of SKUs and select the optimal one.
 * 
 * Branch and Bound Method:
 * The Branch and Bound algorithm is a tree-based search method that is used to solve optimization problems. It systematically explores branches of a decision tree, 
 * pruning branches that do not lead to optimal solutions, thus reducing the number of potential solutions that need to be evaluated. This makes the algorithm 
 * particularly effective for problems like load optimization, where there are numerous possible combinations to consider.
 * 
 * Description:
 * - The `BranchAndBoundEngine` class takes in a set of SKUs, each with specific constraints, and attempts to find the best combination of SKUs that fit within 
 *   the truck's capacity.
 * - The class is designed to be compatible with older browsers, so it uses older JavaScript syntax (e.g., `var` instead of `const` and `let`).
 * - Only two methods, `bestSolution` and `updateAll`, are intended to be called from outside the class. The rest of the methods are internal and marked with 
 *   an underscore (`_`) to indicate that they are private.
 * - An important consideration is the scenario where no valid solution is found. In this case, the class will revert to the last valid solution and display an 
 *   alert. It is expected that the user interface (UI) will handle this scenario appropriately, as the alert alone may not be sufficient.
 * 
 * Example Usage:
 * 
 * const skus = {
 *     sku1: { skuId: 'sku1', SKU: 'Pipe A', sticksPerBundle: 10, popularityScore: 5 },
 *     sku2: { skuId: 'sku2', SKU: 'Pipe B', sticksPerBundle: 20, popularityScore: 3 },
 * };
 * 
 * const engine = new BranchAndBoundEngine(skus, 1000, new RatiosCalculator());
 * const bestSolution = engine.bestSolution();
 * 
 * Output:
 * - The best combination of SKUs that fits within the truck's capacity.
 * 
 * Date: 2024-07-11
 * Author: Stephen Johns

 * bestSolution method:
 * - This public method initiates the process of finding the optimal solution based on the given SKUs and constraints.
 * 
 * Overview:
 * The `bestSolution` method is the primary entry point for users to find the best combination of SKUs that can be loaded onto a truck. 
 * It uses the Branch and Bound algorithm to explore all possible combinations, evaluates them based on predefined constraints and popularity scores, 
 * and returns the most optimal solution.
 * 
 * Description:
 * This method calls internal methods to generate and evaluate possible solutions. It filters and selects the solution with the highest popularity score 
 * that meets all the constraints. If no valid solution is found, the method will revert to the last valid solution and alert the user.
 * 
 * Variables:
 * - None directly in this method. It relies on the SKUs, constraints, and other properties initialized in the class.
 * 
 * Methods:
 * 
 * 1. _findAllSolutions:
 *    - Explores all possible combinations of SKUs to find valid solutions.
 * 
 * 2. _findOptimalSolution:
 *    - Filters and selects the most optimal solution based on the popularity score.
 * 
 * Example Usage:
 * 
 * const engine = new BranchAndBoundEngine(skus, 1000, new RatiosCalculator());
 * const bestSolution = engine.bestSolution();
 * 
 * Output:
 * - Returns the most optimal solution that fits within the truck's capacity.

 * updateAll method:
 * - This public method updates constraints for a specific SKU, recalculates the best solution, and updates the UI.
 * 
 * Overview:
 * The `updateAll` method allows users to modify constraints for a specific SKU and immediately see the effects on the best solution. 
 * It is designed to be called from outside the class, typically in response to user interactions in the UI.
 * 
 * Description:
 * This method updates the constraints for the specified SKU based on user input, recalculates the optimal solution, and updates the UI 
 * (including buttons and other relevant elements). If no valid solution is found after the update, the method will revert to the last valid solution 
 * and display an alert, signaling that further handling may be required in the UI.
 * 
 * Variables:
 * - skuId: The identifier for the SKU being updated.
 * - action: The action being performed (e.g., 'increase', 'decrease').
 * - bundles: The new number of bundles for the SKU.
 * 
 * Methods:
 * 
 * 1. _updateConstraints:
 *    - Updates the constraints for the specified SKU based on the provided action and bundles.
 * 
 * 2. bestSolution:
 *    - Recalculates and returns the best solution based on the updated constraints.
 * 
 * 3. _updateButtonStates:
 *    - Updates the UI elements (like buttons) to reflect the new constraints and solution.
 * 
 * Example Usage:
 * 
 * const engine = new BranchAndBoundEngine(skus, 1000, new RatiosCalculator());
 * engine.updateAll('sku1', 'increase', 5);
 * 
 * Output:
 * - Updates the constraints for 'sku1' and recalculates the best solution.

 * _initializeConstraints method:
 * - This internal method sets up the initial constraints based on the SKUs provided.
 * 
 * Overview:
 * The `_initializeConstraints` method is responsible for setting up the initial state of the constraints for each SKU. It checks if all SKUs 
 * have divisible bundles, calculates the truck size constraints, and sets up initial and last states for bundle and bundle count constraints.
 * 
 * Description:
 * This method is called once during the construction of the `BranchAndBoundEngine` class to prepare the initial constraints. It checks if each SKU's 
 * calculated bundles per truckload are divisible by a given modulus size (`MOD_SIZE`). Based on this, it sets the truck size constraints and stores 
 * the initial and last states of the constraints for future reference.
 * 
 * Variables:
 * - None directly, but it relies on the SKUs and other properties initialized in the class.
 * 
 * Methods:
 * 
 * 1. _setTruckSizeConstraints:
 *    - Sets the minimum and maximum truck size constraints based on the fractions provided.
 * 
 * Example Usage:
 * - This method is called internally by the constructor and does not require direct usage.
 * 
 * Output:
 * - Initializes the constraints for the SKUs.

 * _findAllSolutions method:
 * - This internal method explores all possible SKU combinations to find valid solutions.
 * 
 * Overview:
 * The `_findAllSolutions` method systematically explores all possible combinations of SKUs to find solutions that meet the constraints. 
 * It generates combinations using recursion and stores the valid solutions for further evaluation.
 * 
 * Description:
 * This method generates and evaluates possible solutions by recursively calling `_findSKUCombinations`. It filters the solutions based on their size 
 * and stores them for further evaluation. If no valid solution is found, it reverts to the last valid solution and displays an alert.
 * 
 * Variables:
 * - None directly in this method. It uses the SKUs and constraints initialized in the class.
 * 
 * Methods:
 * 
 * 1. _findSKUCombinations:
 *    - Generates combinations of SKUs to evaluate.
 * 
 * Example Usage:
 * - This method is called internally by `bestSolution` and does not require direct usage.
 * 
 * Output:
 * - A set of valid solutions that meet the constraints.

 * _findSKUCombinations method:
 * - This internal recursive method generates combinations of SKUs to evaluate.
 * 
 * Overview:
 * The `_findSKUCombinations` method generates all possible combinations of SKUs and evaluates them against the constraints. 
 * It uses recursion to explore different branches of possible solutions.
 * 
 * Description:
 * This method is the core of the Branch and Bound algorithm, where different combinations of SKUs are generated and checked to see 
 * if they fit within the truck's constraints. If a combination meets the constraints, it is stored for further evaluation.
 * 
 * Variables:
 * - SKUs: The list of SKUs to consider for combinations.
 * - solution: The current combination being evaluated.
 * - totalSize: The current total size of the combination.
 * 
 * Methods:
 * 
 * 1. _isValidSolution:
 *    - Checks if the current combination meets all constraints.
 * 
 * Example Usage:
 * - This method is called internally by `_findAllSolutions` and does not require direct usage.
 * 
 * Output:
 * - A valid combination of SKUs that meets the constraints.

 * _isValidSolution method:
 * - This internal method checks if a given solution meets all the constraints.
 * 
 * Overview:
 * The `_isValidSolution` method evaluates whether a given solution (a combination of SKUs) adheres to all predefined constraints, 
 * such as minimum and maximum truck size, and bundle constraints.
 * 
 * Description:
 * This method is called to ensure that the current solution being evaluated meets all the required constraints before it is considered 
 * for further evaluation or selection as the best solution.
 * 
 * Variables:
 * - solution: The current solution being evaluated.
 * - totalSize: The total size of the solution.
 * 
 * Methods:
 * 
 * 1. _checkBundlesPerSKUConstraints:
 *    - Verifies that the number of bundles per SKU in the solution adheres to the constraints.
 * 
 * Example Usage:
 * - This method is called internally by `_findSKUCombinations` and does not require direct usage.
 * 
 * Output:
 * - Returns `true` if the solution meets all constraints, `false` otherwise.

 * _calculateTruckSize method:
 * - This internal method calculates the total size of a solution to ensure it fits within the truck's capacity.
 * 
 * Overview:
 * The `_calculateTruckSize` method sums up the total size of all SKUs in the current solution to determine if it fits within the truck's capacity.
 * 
 * Description:
 * This method is used to calculate the total size of the current solution, ensuring that it does not exceed the truck's capacity. It iterates 
 * through each SKU in the solution, multiplies the number of bundles by the SKU's bundle size, and sums the results.
 * 
 * Variables:
 * - solution: The current solution for which the truck size is being calculated.
 * 
 * Methods:
 * 
 * - None, as this method is a utility function within the class.
 * 
 * Example Usage:
 * - This method is called internally by `_findSKUCombinations` and does not require direct usage.
 * 
 * Output:
 * - The total size of the solution in terms of truck capacity.

 * _updateConstraints method:
 * - This internal method updates the constraints for a specific SKU based on user actions.
 * 
 * Overview:
 * The `_updateConstraints` method modifies the constraints for a specific SKU according to the user's action (e.g., increasing or decreasing the number of bundles). 
 * It ensures that the constraints remain valid and within the initial limits set for each SKU.
 * 
 * Description:
 * This method is called to update the constraints for a specific SKU when the user interacts with the UI (e.g., by increasing or decreasing the number of bundles). 
 * It adjusts the constraints accordingly and ensures that they do not exceed the initial or last known valid constraints.
 * 
 * Variables:
 * - skuId: The identifier for the SKU being updated.
 * - action: The action being performed (e.g., 'increase', 'decrease').
 * - numberOfBundles: The new number of bundles for the SKU.
 * 
 * Methods:
 * 
 * - None, as this method directly manipulates the constraints.
 * 
 * Example Usage:
 * - This method is called internally by `updateAll` and does not require direct usage.
 * 
 * Output:
 * - Updates the constraints for the specified SKU.

 * _updateButtonStates method:
 * - This internal method updates the UI elements (like buttons) based on the current state of the SKUs.
 * 
 * Overview:
 * The `_updateButtonStates` method adjusts the state of UI elements such as buttons based on the current constraints and solution. 
 * It ensures that the buttons accurately reflect whether actions (e.g., increasing or decreasing bundles) are possible.
 * 
 * Description:
 * This method is used to update the state of UI elements (e.g., disabling or enabling buttons) to reflect the current constraints and 
 * the state of the SKUs. It ensures that users can only perform valid actions based on the current state.
 * 
 * Variables:
 * - None directly, but it relies on the current state of the SKUs and constraints.
 * 
 * Methods:
 * 
 * - None, as this method interacts with the DOM to update UI elements.
 * 
 * Example Usage:
 * - This method is called internally by `updateAll` and does not require direct usage.
 * 
 * Output:
 * - Updated UI elements that accurately reflect the current state of the SKUs.

 * _deepClone method:
 * - This internal utility method creates a deep copy of an object.
 * 
 * Overview:
 * The `_deepClone` method creates a deep copy of the provided object, ensuring that changes to the copy do not affect the original object.
 * 
 * Description:
 * This method is used whenever a deep copy of an object is required, such as when storing the initial and last known valid states of constraints. 
 * It ensures that the original object remains unchanged when modifications are made to the copy.
 * 
 * Variables:
 * - obj: The object to be deep cloned.
 * 
 * Methods:
 * - None, as this is a utility function.
 * 
 * Example Usage:
 * - This method is called internally by several methods and does not require direct usage.
 * 
 * Output:
 * - A deep copy of the provided object.

 * _handleError method:
 * - This internal method handles errors that occur within the class.
 * 
 * Overview:
 * The `_handleError` method provides a consistent way to handle errors that occur during the execution of the class methods. 
 * It logs the error and throws a new error with a descriptive message.
 * 
 * Description:
 * This method is called whenever an error occurs within the class. It logs the error to the console and throws a new error with a 
 * message that describes what went wrong, ensuring that errors are handled in a consistent manner.
 * 
 * Variables:
 * - message: A descriptive message about the error.
 * - error: The original error object that was caught.
 * 
 * Methods:
 * - None, as this is a utility function.
 * 
 * Example Usage:
 * - This method is called internally by several methods and does not require direct usage.
 * 
 * Output:
 * - Throws a new error with a descriptive message.

 * _findOptimalSolution method:
 * - This internal method selects the best solution from the set of valid solutions.
 * 
 * Overview:
 * The `_findOptimalSolution` method evaluates all valid solutions and selects the one with the highest popularity score. 
 * If multiple solutions have the same score, it selects the one with the highest total sticks.
 * 
 * Description:
 * This method filters and selects the optimal solution from the set of valid solutions based on predefined criteria. 
 * It first looks for the solution with the highest popularity score, and if there are ties, it selects the one with the highest total sticks.
 * 
 * Variables:
 * - None directly, but it uses the set of valid solutions generated by `_findAllSolutions`.
 * 
 * Methods:
 * - None, as this method is the final step in the solution selection process.
 * 
 * Example Usage:
 * - This method is called internally by `bestSolution` and does not require direct usage.
 * 
 * Output:
 * - Returns the most optimal solution based on the criteria.
 */


class BranchAndBoundEngine {
    constructor(SKUs, lcmValue, ratiosCalculator) {
        // Initialize properties for SKUs, constraints, and solution tracking
        this.SKUs = SKUs;
        this.previousSolutions = [];
        this.fullTruckSize = lcmValue;
        this.minTruckSize = 1;
        this.MOD_SIZE = 6;
        this.minFractionWhereSKUsNotDivisiable = 0.95;
        this.maxFractionWhereSKUsNotDivisiable = 0.98;
        this.bundleConstraints = {};
        this.initialBundleConstraints = {};
        this.lastBundleConstraints = {};
        this.truckSizeConstraints = {};
        this.ratiosCalculator = ratiosCalculator;
        this.solutions = [];
        this.currentMaxTruckSize = 0;
		this.initialCalculation = true;

        // Initialize constraints based on the SKUs provided
        this._initializeConstraints();
    }

    _initializeConstraints() {
        // Set truck size constraints and bundle constraints based on SKUs
        console.log('fulltruckSize :', this.fullTruckSize);
        
        if (Object.keys(this.SKUs).length === 1) {
            const singleSKU = Object.values(this.SKUs)[0];
            this.truckSizeConstraints = { minTruckSize: this.fullTruckSize, maxTruckSize: this.fullTruckSize };
            console.log('1 SKU');
            console.log('truckSizeConstraints:', this.truckSizeConstraints);
        } else {
            const allSKUsHaveDivisibleBundles = Object.values(this.SKUs).every(sku => {
                const calculatedBundlesPerTruckload = parseInt(sku.calculatedBundlesPerTruckload, 10);
                console.log('calculatedBundlesPerTruckload:', calculatedBundlesPerTruckload);
                console.log(sku.calculatedBundlesPerTruckload / this.MOD_SIZE);
                const isDivisible = calculatedBundlesPerTruckload % this.MOD_SIZE === 0;
                console.log(`isDivisible: ${isDivisible}`);
                return isDivisible;
            });

            console.log('allSKUsHaveDivisibleBundles: ', allSKUsHaveDivisibleBundles);

            if (allSKUsHaveDivisibleBundles) {
                this.truckSizeConstraints = { minTruckSize: this.fullTruckSize, maxTruckSize: this.fullTruckSize };
                console.log('SKU by 6');
                console.log('truckSizeConstraints :', this.truckSizeConstraints);
            } else {
                this._setTruckSizeConstraints(this.minFractionWhereSKUsNotDivisiable, this.maxFractionWhereSKUsNotDivisiable);
                console.log('SKU not by 6');
                console.log('truckSizeConstraints :', this.truckSizeConstraints);
            }
        }

        try {
            Object.values(this.SKUs).forEach(sku => {
                this.bundleConstraints[sku.skuId] = {
                    minNumberOfBundles: 1,
                    maxNumberOfBundles: sku.calculatedBundlesPerTruckload
                };
            });

            this.initialBundleConstraints = this._deepClone(this.bundleConstraints);
            this.lastBundleConstraints = this._deepClone(this.bundleConstraints);
        } catch (error) {
            this._handleError('Error calculating bundle constraints', error);
        }
//        console.log('initialBundleConstraints :', this.initialBundleConstraints);
//        console.log('lastBundleConstraints :', this.lastBundleConstraints);
//		console.log('bundleConstraints :', this.bundleConstraints);
    }
    
    _setTruckSizeConstraints(minFraction, maxFraction) {
        // Set the minimum and maximum truck size constraints based on the fractions provided
        const minTruckSize = Math.floor(this.fullTruckSize * minFraction);
        const maxTruckSize = Math.floor(this.fullTruckSize * maxFraction);
        this.truckSizeConstraints = { minTruckSize, maxTruckSize };
    }

    _checkBundlesPerSKUConstraints(solution) {
        // Validate that the number of bundles per SKU in the solution meets the constraints
        try {
            const SKUBundles = this._countBundlesPerSKU(solution);

            for (const [skuId, count] of Object.entries(SKUBundles)) {
                const constraints = this.bundleConstraints[skuId];
                if (count < constraints.minNumberOfBundles || count > constraints.maxNumberOfBundles) {
                    return false;
                }
            }

            return true;
        } catch (error) {
            this._handleError('Error checking number of bundles per size', error);
        }
    }

    _countBundlesPerSKU(solution) {
        // Count the number of bundles per SKU in the given solution
        const sizeBundlesCount = {};
        solution.forEach(item => {
            const sku = this.SKUs[item.skuId];
            if (!sizeBundlesCount[sku.skuId]) {
                sizeBundlesCount[sku.skuId] = 0;
            }
            sizeBundlesCount[sku.skuId] += item.numberOfBundles;

            this._validateBundleConstraints(item);
        });
        return sizeBundlesCount;
    }

    _validateBundleConstraints(item) {
        // Ensure the number of bundles for an SKU in the solution is within its defined constraints
        const bundleConstraints = this.bundleConstraints[item.skuId];
        if (item.numberOfBundles < bundleConstraints.minNumberOfBundles || item.numberOfBundles > bundleConstraints.maxNumberOfBundles) {
            throw new Error(`Number of bundles for skuId ${item.skuId} is out of bounds.`);
        }
    }

    _findAllSolutions() {
        // Generate all possible valid solutions based on the SKU constraints
        try {
            this.solutions = [];
            this.currentMaxTruckSize = 0;
            const allSKUs = Object.keys(this.bundleConstraints);
            this._findSKUCombinations(allSKUs, [], 0);
            this.solutions = this.solutions.filter(solution => solution.totalSize >= this.currentMaxTruckSize);

            if (this.solutions.length < 1) {
				if (!this.initialCalculation )
				{
                this.bundleConstraints = this._deepClone(this.lastBundleConstraints);
                alert('No possible solutions for last modification. The last modification has been reversed.');
				this.bestSolution();
                return;
				}
            }

            return this.solutions;
        } catch (error) {
            this._handleError('Error finding all solutions', error);
        }
    }

    _findSKUCombinations(SKUs, solution, totalSize) {
        // Recursively explore different combinations of SKUs to find valid solutions
        if (SKUs.length === 0) {
            if (totalSize < this.currentMaxTruckSize) {
                return;
            }
            this.currentMaxTruckSize = totalSize;
            if (this._isValidSolution(solution, totalSize)) {
                this.solutions.push({ solution: [...solution], totalSize });
            }
            this.solutions = this.solutions.filter(sol => sol.totalSize >= this.currentMaxTruckSize);

            return;
        }

        const [skuId, ...remainingSKUs] = SKUs;
        const constraints = this.bundleConstraints[skuId];
        const skuInfo = this.SKUs[skuId];

        for (let numberOfBundles = constraints.minNumberOfBundles; numberOfBundles <= constraints.maxNumberOfBundles; numberOfBundles++) {
            const newSize = totalSize + numberOfBundles * skuInfo.calculatedBundleSize;

            if (newSize > this.truckSizeConstraints.maxTruckSize) break;

            solution.push({ skuId, numberOfBundles });
            this._findSKUCombinations(remainingSKUs, solution, newSize);
            solution.pop();
        }
    }

    calculateTruckSize(solution) {
        // Calculate the total truck size for a given solution
        return solution.reduce((totalTruckSize, item) => {
            const skuData = this.SKUs[item.skuId];
            if (skuData === undefined) {
                console.error(`Undefined SKU data for skuId: ${item.skuId}`);
                return totalTruckSize;
            }
            const skuSize = skuData.calculatedBundleSize;
            return totalTruckSize + (skuSize * item.numberOfBundles);
        }, 0);
    }

    _isValidSolution(solution, totalSize) {
        // Check if the solution meets all constraints, including truck size and bundle counts
        return this._checkBundlesPerSKUConstraints(solution) &&
            totalSize >= this.truckSizeConstraints.minTruckSize &&
            totalSize <= this.truckSizeConstraints.maxTruckSize;
    }

    bestSolution() {
        // Public method to find the best solution based on the constraints
        this._findAllSolutions();
//		console.log('solutions: ',this.solutions);
        const optimalSolutions = this._findOptimalSolution();
        const optimalSolution = optimalSolutions.solution;
//		console.log('optimalSolution: ',optimalSolution);
		this.lastBundleConstraints = this._deepClone(this.bundleConstraints);
//		console.log('initialCalculation: ',this.initialCalculation);
		this.initialCalculation = false;
//		console.log('initialCalculation: ',this.initialCalculation);

        return optimalSolution;

    }
  
    _deepClone(obj) {
        // Utility method to create a deep clone of an object
        return JSON.parse(JSON.stringify(obj));
    }

    _handleError(message, error) {
        // Handle errors consistently across the class
        console.error(message, error);
        throw new Error(message);
    }

    _updateConstraints(skuId, action, numberOfBundles) {
        // Update the constraints for a specific SKU based on user actions
        const minNumberOfBundlesInitial = this.initialBundleConstraints[skuId].minNumberOfBundles;
        const maxNumberOfBundlesInitial = this.initialBundleConstraints[skuId].maxNumberOfBundles;
		const minNumberOfBundlesLast = this.lastBundleConstraints[skuId].minNumberOfBundles;
        const maxNumberOfBundlesLast = this.lastBundleConstraints[skuId].maxNumberOfBundles;
		const minNumberOfBundles = this.bundleConstraints[skuId].minNumberOfBundles;
        const maxNumberOfBundles = this.bundleConstraints[skuId].maxNumberOfBundles;
		console.log('skuId: ', skuId);

		const correctAmountCheckbox = document.querySelector(`#orderTableDataCorrectAmountId${skuId}`);
		console.log('correctAmountCheckbox: ',correctAmountCheckbox);
		if (correctAmountCheckbox) {
    console.log('correctAmountCheckbox found: ', correctAmountCheckbox);
} else {
    console.log('correctAmountCheckbox not found for skuId: ', skuId);
}

		console.log('action: ',action);
        switch (action) {
            case 'correctAmount':
                this.bundleConstraints[skuId].minNumberOfBundles = numberOfBundles;
                this.bundleConstraints[skuId].maxNumberOfBundles = numberOfBundles;
				console.log('after UpdateAll initialBundleConstraints :', this.initialBundleConstraints);
				console.log('after updateAll lastBundleConstraints :', this.lastBundleConstraints);
				console.log('after updateAll bundleConstraints :', this.bundleConstraints);
				console.log('Checkbox before:', correctAmountCheckbox.checked);
//orrectAmountCheckbox.checked = true;


				correctAmountCheckbox.checked = true;
				console.log('Checkbox after:', correctAmountCheckbox.checked);
                break;
            case 'notCorrectAmount':
                this.bundleConstraints[skuId].minNumberOfBundles = minNumberOfBundlesLast;
                this.bundleConstraints[skuId].maxNumberOfBundles = maxNumberOfBundlesLast;
//				correctAmountCheckbox.checked = false;
                break;
            case 'increase':
//				console.log('increase');
                if (numberOfBundles < maxNumberOfBundlesInitial) {
                    const newNumberOfBundles = Math.max(0, parseInt(numberOfBundles) + 1);
//					console.log('newNumberOfBundles: ',newNumberOfBundles);
                    this.bundleConstraints[skuId].minNumberOfBundles = newNumberOfBundles;
					this.bundleConstraints[skuId].maxNumberOfBundles = maxNumberOfBundlesInitial;
                }
				console.log('after UpdateAll initialBundleConstraints :', this.initialBundleConstraints);
				console.log('after updateAll lastBundleConstraints :', this.lastBundleConstraints);
				console.log('after updateAll bundleConstraints :', this.bundleConstraints);
                break;
            case 'decrease':
//				console.log('decrease');
                if (numberOfBundles > minNumberOfBundlesInitial) {
                    const newNumberOfBundles = Math.max(0, parseInt(numberOfBundles) - 1);
					console.log('newNumberOfBundles: ',newNumberOfBundles);
                    this.bundleConstraints[skuId].maxNumberOfBundles = newNumberOfBundles;
					this.bundleConstraints[skuId].minNumberOfBundles = minNumberOfBundlesInitial;
                }
				console.log('after UpdateAll decrease initialBundleConstraints :', this.initialBundleConstraints);
				console.log('after updateAll decrease lastBundleConstraints :', this.lastBundleConstraints);
				console.log('after updateAll decreasebundleConstraints :', this.bundleConstraints);
                break;
            default:
                throw new Error(`Unknown action: ${action}`);
        }
    }

    updateButtonStates() {
        // Update the state of UI buttons based on the current constraints and SKU states
        Object.keys(this.SKUs).forEach(skuId => {
            const numberOfBundles = parseInt(document.querySelector(`#orderTableDataRowId${skuId}`).getAttribute('data-total-bundles'));

            const minNumberOfBundles = this.initialBundleConstraints[skuId].minNumberOfBundles;
            const maxNumberOfBundles = this.initialBundleConstraints[skuId].maxNumberOfBundles;

            const increaseButton = document.querySelector(`#orderTableDataIncreaseAmountId${skuId}`);
            const decreaseButton = document.querySelector(`#orderTableDataDecreaseAmountId${skuId}`);
            const correctAmountCheckbox = document.querySelector(`#orderTableDataCorrectAmountId${skuId}`);
			        console.log(`Checkbox for SKU ID ${skuId}:`, correctAmountCheckbox);
        console.log(`Checkbox Checked State for SKU ID ${skuId}:`, correctAmountCheckbox ? correctAmountCheckbox.checked : 'Checkbox not found');


            increaseButton.disabled = numberOfBundles >= maxNumberOfBundles;
            decreaseButton.disabled = numberOfBundles <= minNumberOfBundles;
//            correctAmountCheckbox.checked = false;
        });
		
    }

    updateAll(skuId, action, bundles) {
        // Update all constraints, recalculate the best solution, and update the UI
//		console.log('updateAll');
//		console.log('skuId: ', skuId);
//		console.log('action: ', action);
//		console.log('bundles: ', bundles);
        bundles = parseInt(bundles, 10); // Convert to integer, base 10
        this._updateConstraints(skuId, action, bundles);
        const bestSolution = this.bestSolution();
        orderTable = new OrderTable(this.SKUs, bestSolution, branchAndBoundEngine);
        this.updateButtonStates();
		
//		console.log('bundleConstraints :', this.bundleConstraints);
    }

    _findOptimalSolution() { 
        // Find the optimal solution from the generated solutions
        console.log('_findAOptimaSolution - Solutions: ', this.solutions);
    
        if (this.solutions.length === 0) {
            throw new Error("No solutions available");
        } 

        if (this.solutions.length === 1) {
            console.log('1 solution: ', this.solutions[0]);
            return this.solutions[0];
        }
                
        let minDifference = Infinity;

        this.solutions.forEach(solution => {
            const { differenceSum, totalSticks } = this.ratiosCalculator.popularityScoreDifference(solution);

            solution.differenceSum = differenceSum;
            solution.totalSticks = totalSticks;

//            console.log('solution.differenceSum: ', solution.differenceSum);
            
            if (solution.differenceSum < minDifference) {
                minDifference = solution.differenceSum;
            }
        });
        
        console.log('minDifference: ', minDifference);
        this.solutions = this.solutions.filter(solution => solution.differenceSum === minDifference);

        if (this.solutions.length === 1) {
			this.lastBestSolution = this.solutions[0];
            return this.solutions[0];
        }
      
        let maxTotalSticks = -Infinity;
      
        this.solutions.forEach(solution => {
            if (solution.totalSticks > maxTotalSticks) {
                maxTotalSticks = solution.totalSticks;
            }
        });
        
        this.solutions = this.solutions.filter(solution => solution.totalSticks === maxTotalSticks);           
        console.log('end solutions: ', this.solutions);

        if (this.solutions.length === 0) {
            throw new Error("No solutions available");
        } 

        return this.solutions[0];
    }
}
