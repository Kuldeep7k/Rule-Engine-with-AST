from flask import Flask, request, jsonify, render_template
import json
import logging

from rule_engine.rule_engine import create_rule, combine_rules, evaluate_rule, Node
from rule_engine.database import create_database

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    """Displays the home page of the application."""
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule_route():
    """
    Creates a rule from a given rule string.

    :param rule_string: The rule as a string (e.g. "age > 30")
    :return: The root node of the abstract syntax tree, or an error message
    """
    try:
        rule_string = request.json.get('rule_string')
        if not rule_string:
            return jsonify({"error": "rule_string is required"}), 400
        
        ast = create_rule(rule_string)
        return jsonify(ast.to_dict()), 200
    except ValueError as e:
        logging.error("Error creating rule: %s", str(e))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error("Unexpected error while creating rule: %s", str(e))
        return jsonify({"error": "An unexpected error occurred while creating the rule."}), 500


@app.route('/combine_rules', methods=['POST'])
def api_combine_rules():
    """
    Combines multiple rules into a single abstract syntax tree (AST) using the
    logical "OR" operator.

    :param rules: A list of rule strings to be combined
    :return: The root node of the combined abstract syntax tree, or an error message
    """
    try:
        rules = request.json.get('rules')
        if not rules or not isinstance(rules, list) or len(rules) == 0:
            return jsonify({"error": "A non-empty list of rules is required."}), 400

        combined_ast = combine_rules(rules)
        return jsonify(combined_ast.to_dict()), 200
    except ValueError as e:
        logging.error("Invalid rule format: %s", str(e))
        return jsonify({"error": "Invalid rule format. Please check your input."}), 400
    except Exception as e:
        logging.error("Unexpected error while combining rules: %s", str(e))
        return jsonify({"error": "An unexpected error occurred while combining rules."}), 500

@app.route('/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    """
    Evaluates a rule Abstract Syntax Tree (AST) against provided user data.

    This endpoint takes a JSON payload containing an AST and user data, evaluates
    the AST against the data, and returns the result of the evaluation.

    Request Body:
        - data: A dictionary of user data against which the AST will be evaluated.
        - ast: A dictionary representing the AST to be evaluated, which must include
               'node_type' and 'value' keys.

    Returns:
        - JSON response with the evaluation result (True or False) if successful.
        - JSON error message with a 400 status code if required fields are missing
          or if the AST structure is invalid.
        - JSON error message with a 500 status code if an unexpected error occurs.
    """
    try:
        data = request.json.get('data')
        ast_data = request.json.get('ast')
        
        if not data or not ast_data:
            return jsonify({"error": "data and ast are required"}), 400
        
        if 'node_type' not in ast_data or 'value' not in ast_data:
            return jsonify({"error": "Invalid AST structure. 'node_type' and 'value' are required."}), 400

        ast = json_to_node(ast_data)
        result = evaluate_rule(ast, data)
        return jsonify({"result": result}), 200
    except ValueError as e:
        logging.error("Error evaluating rule: %s", str(e))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error("Unexpected error during rule evaluation: %s", str(e))
        return jsonify({"error": "An unexpected error occurred during rule evaluation."}), 500

def json_to_node(data):
    """
    Recursively converts a JSON-serializable dictionary into an AST Node.

    :param data: A dictionary representing the AST Node to be created, which must
                 include 'node_type' and 'value' keys.
    :return: The root Node of the constructed AST
    """
    if 'node_type' not in data or 'value' not in data:
        raise ValueError("Invalid AST data: 'node_type' and 'value' are required")

    left_node = json_to_node(data['left']) if data.get('left') else None
    right_node = json_to_node(data['right']) if data.get('right') else None

    return Node(node_type=data['node_type'], value=data['value'], left=left_node, right=right_node)

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
