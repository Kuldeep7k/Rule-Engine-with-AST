/**
 * Submits a rule string to the server to be created and displays the
 * resulting AST in the "output" div.
 *
 * @returns {Promise<void>}
 */
async function createRule() {
    const ruleString = document.getElementById("ruleInput").value.trim();

    if (!ruleString) {
        alert("Please enter a rule.");
        return;
    }

    try {
        const response = await fetch('/create_rule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rule_string: ruleString }),
        });

        const data = await handleResponse(response);
        displayResult("output", data);
    } catch (error) {
        displayError("output", error);
    }
}

/**
 * Submits an array of rule strings to the server to be combined and displays
 * the resulting AST in the "combinedOutput" div.
 *
 * @returns {Promise<void>}
 */
async function combineRules() {
    const rules = document.getElementById("combineRulesInput").value
        .split("\n")
        .map(rule => rule.trim())
        .filter(rule => rule);

    if (rules.length === 0) {
        alert("Please enter at least one rule.");
        return;
    }

    try {
        const response = await fetch('/combine_rules', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rules: rules }),
        });

        const data = await handleResponse(response);
        displayResult("combinedOutput", data);
    } catch (error) {
        displayError("combinedOutput", error);
    }
}

/**
 * Submits a rule AST and data to the server to be evaluated and displays
 * the result in the "evaluationResult" div.
 *
 * @returns {Promise<void>}
 */
async function evaluateRule() {
    try {
        const ruleASTInput = document.getElementById("evaluateASTInput").value;
        const dataInput = document.getElementById("evaluateDataInput").value;

        // Ensure valid JSON format
        const ruleAST = JSON.parse(ruleASTInput);
        const data = JSON.parse(dataInput);

        const response = await fetch('/evaluate_rule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ast: ruleAST, data: data }),
        });

        const result = await handleResponse(response);
        displayResult("evaluationResult", result);
    } catch (error) {
        displayError("evaluationResult", error);
    }
}

/**
 * Handles an HTTP response from the server, throwing an error if the response was not successful.
 *
 * @param {Response} response The HTTP response to handle
 * @returns {Promise<*>} A promise that resolves to the parsed JSON response or rejects with an error.
 */
async function handleResponse(response) {
    if (!response.ok) {
        const errorText = await response.text(); // Get the raw text of the response
        throw new Error(`HTTP error! Status: ${response.status}, Response: ${errorText}`);
    }
    return response.json(); // Parse the JSON if the response is OK
}

/**
 * Updates the specified HTML element with the stringified representation of the provided data.
 */
function displayResult(elementId, data) {
    const outputElement = document.getElementById(elementId);
    outputElement.innerText = JSON.stringify(data, null, 2);
}

/**
 * Updates the specified HTML element with an error message and logs the error to the console.
 *
 * @param {string} elementId - The ID of the HTML element to update with the error message.
 * @param {Error} error - The error object containing the error message to display.
 */
function displayError(elementId, error) {
    const outputElement = document.getElementById(elementId);
    outputElement.innerText = `Error: ${error.message || 'An error occurred'}`;
    console.error(error); // Log the error to the console for debugging
}
