import re

class Node:
    def __init__(self, node_type, value, left=None, right=None):
        """
        Initializes a Node with the given type, value, and children (if any).

        :param node_type: The type of node (e.g. 'operand' or 'operator')
        :param value: The value of the node (e.g. 'age > 30' or 'AND')
        :param left: The left child of the node (default: None)
        :param right: The right child of the node (default: None)
        """
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):

        """
        Converts the Node to a dictionary.

        This method is intended to be used when serializing the Node to JSON.

        :return: A dictionary representation of the Node
        """
        node_dict = {
            "node_type": self.node_type,
            "value": self.value,
        }
        if self.left:
            node_dict["left"] = self.left.to_dict()
        if self.right:
            node_dict["right"] = self.right.to_dict()
        return node_dict


def create_rule(rule_string):
    """
    Creates an abstract syntax tree (AST) from a given rule string.

    :param rule_string: The rule string to parse (e.g. "age > 30")
    :return: The root node of the abstract syntax tree
    :raises ValueError: If there is an error parsing the rule string
    """
    if not rule_string:
        raise ValueError("rule_string must not be null or empty")
    
    tokens = tokenize(rule_string)
    if not tokens:
        raise ValueError("rule_string did not produce any tokens")
    
    try:
        ast = parse(tokens)
        if ast is None:
            raise ValueError("rule_string did not produce any abstract syntax tree")
    except ValueError as e:
        raise ValueError(f"Error parsing rule: {e}")
    
    return ast


def combine_rules(rules):
    """
    Combines multiple rule strings into a single abstract syntax tree (AST).

    This function takes a list of rule strings, parses each into an AST, and
    combines them using the logical "OR" operator into a single AST.

    :param rules: A list of rule strings to be combined.
    :return: The root node of the combined abstract syntax tree, or None if
             the input list is empty.
    """
    if not rules:
        return None
    
    combined_ast = None
    for rule in rules:
        try:
            rule_ast = create_rule(rule)
            if combined_ast is None:
                combined_ast = rule_ast
            else:
                combined_ast = Node("operator", value="OR", left=combined_ast, right=rule_ast)
        except ValueError as e:
            print(f"Error processing rule '{rule}': {str(e)}")
    
    return combined_ast


def tokenize(rule_string):
 
    """
    Tokenizes the given rule string into a list of tokens.

    :param rule_string: The rule string to tokenize
    :return: A list of tokens

    The tokenization is done using a regular expression that matches the following patterns:

    - Whitespaces
    - Keywords (AND, OR)
    - Comparison operators (>, <, =, !=, <=, >=)
    - Parentheses
    - Identifiers (e.g. age, department)
    - String literals (e.g. 'Sales', "Marketing")

    The tokens are then filtered to remove any empty strings (i.e. extra whitespace)
    """
    pattern = r'(\s+|AND|OR|[()<>!=]=?|[a-zA-Z_][a-zA-Z0-9_.]*|\'[^\']*\'|\"[^\"]*\")'
    tokens = [token for token in re.split(pattern, rule_string) if token.strip()]
    return tokens


def parse(tokens):
    """
    Parses the given list of tokens into an Abstract Syntax Tree (AST) node.

    The parser uses the Shunting-yard algorithm to handle operator precedence.

    :param tokens: A list of tokens as returned by tokenize
    :return: The root node of the parsed AST
    """
    output = []
    operators = []
    precedence = {'AND': 1, 'OR': 0}  # Operator precedence
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token == '(':
            operators.append(token)
            i += 1
        elif token == ')':
            # Handle closing parentheses by collapsing the operator stack
            while operators and operators[-1] != '(':
                if len(output) < 2:
                    raise ValueError("Incomplete expression before closing parenthesis")
                right = output.pop()
                left = output.pop()
                op = operators.pop()
                output.append(Node("operator", value=op, left=left, right=right))
            operators.pop()  # Pop the '('
            i += 1
        elif token in precedence:
            # Handle precedence of AND/OR operators
            while (operators and operators[-1] in precedence and precedence[operators[-1]] >= precedence[token]):
                if len(output) < 2:
                    raise ValueError("Incomplete expression during operator processing")
                right = output.pop()
                left = output.pop()
                op = operators.pop()
                output.append(Node("operator", value=op, left=left, right=right))
            operators.append(token)
            i += 1
        elif re.match(r"[a-zA-Z_][a-zA-Z0-9_.]*", token) and i + 2 < len(tokens) and re.match(r"[<>!=]+", tokens[i + 1]):
            # Parse binary operations like "field > 10"
            condition = f"{token} {tokens[i + 1]} {tokens[i + 2]}"
            output.append(Node("operand", value=condition))  # Store entire condition as a single operand node
            i += 3
        else:
            raise ValueError(f"Invalid token or incomplete expression: '{token}'")

    # Collapse remaining operators
    while operators:
        if len(output) < 2:
            raise ValueError("Incomplete expression at end of parsing")
        right = output.pop()
        left = output.pop()
        op = operators.pop()
        output.append(Node("operator", value=op, left=left, right=right))

    if len(output) != 1:
        raise ValueError("Invalid expression: check operator and operand count.")

    return output[0]


def evaluate_rule(ast, data):
   
    """
    Recursively evaluates a parsed Abstract Syntax Tree (AST) against the given data.

    :param ast: The root node of the parsed AST
    :param data: A dictionary of data to be evaluated against the AST
    :return: The result of evaluating the AST against the data
    """
    if ast is None or not isinstance(ast, Node):
        return False

    if ast.node_type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)

        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result

    elif ast.node_type == "operand":
        return evaluate_condition(ast.value, data)

    return False


def evaluate_condition(operand: str, data: dict) -> bool:
    """
    Evaluates a condition (operand) against the given data.

    The condition must be in the format of a field name, operator, and value, e.g.:
        age > 30
        salary >= 50000.00
        department == 'Sales'

    The condition is parsed and evaluated against the data, and the result is returned.

    :param operand: The condition string to be evaluated
    :param data: A dictionary of data to be evaluated against the condition
    :return: The result of evaluating the condition against the data
    :raises ValueError: If the condition is invalid or the field is not found in the data
    """
    pattern = r"([a-zA-Z_][a-zA-Z0-9_.]*)\s*([<>!=]=?)\s*(\d+(\.\d+)?|'.*?'|\".*?\")"
    match = re.match(pattern, operand)
    if not match:
        raise ValueError(f"Invalid condition: {operand}")

    field, operator, value = match.group(1), match.group(2), match.group(3)

    if field not in data:
        raise ValueError(f"Field '{field}' not found in data.")

    field_value = data[field]

    # Handle string values and numeric conversions
    if value.startswith(("'", "\"")) and value.endswith(("'", "\"")):
        value = value[1:-1]  # Remove quotes for strings

    # Type conversion based on field type
    if isinstance(field_value, (int, float)):
        value = float(value) if '.' in value else int(value)
    else:
        value = str(value)

    # Replace single '=' with '==' for consistency
    if operator == '=':
        operator = '=='

    # Mapping of operators to their respective lambdas
    operators = {
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '==': lambda x, y: x == y,
        '!=': lambda x, y: x != y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y
    }

    if operator in operators:
        result = operators[operator](field_value, value)
        return result
    else:
        raise ValueError(f"Unsupported operator: {operator}")
