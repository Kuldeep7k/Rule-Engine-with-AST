import unittest
from rule_engine.rule_engine import create_rule, combine_rules, evaluate_rule
from rule_engine.rule_engine import Node

class TestRuleEngine(unittest.TestCase):
    def print_ast(self, node, level=0):
        """
        Prints a human-readable representation of an abstract syntax tree (AST) starting from the given node.

        :param node: The root node of the AST to be printed.
        :param level: An integer indicating the level of indentation to use.

        :return: None
        """
        indent = "  " * level
        if node.node_type == "operand":
            print(f"{indent}Operand: {node.value}")
        else:
            print(f"{indent}Operator: {node.value}")
            if node.left:
                self.print_ast(node.left, level + 1)
            if node.right:
                self.print_ast(node.right, level + 1)

    def test_rule1(self):
        """
        Tests the evaluation of a rule that combines multiple AND and OR
        operators.

        The rule is as follows:

        ((age > 30 AND department == 'Sales') OR (age < 25 AND department == 'Marketing'))
        AND (salary > 50000 OR experience > 5)

        The test checks the evaluation of this rule for 3 different sets of
        data.
        """
        rule1 = "((age > 30 AND department == 'Sales') OR (age < 25 AND department == 'Marketing')) AND (salary > 50000 OR experience > 5)"
        ast = create_rule(rule1)

        data1 = {"age": 35, "department": "Sales", "salary": 60000, "experience": 6}
        data2 = {'age': 35, 'department': 'Sales', 'salary': 50000, 'experience': 6}
        data3 = {"age": 29, "department": "Sales", "salary": 40000, "experience": 3}

        self.assertEqual(evaluate_rule(ast, data1), True) 
        self.assertEqual(evaluate_rule(ast, data2), True)  
        self.assertEqual(evaluate_rule(ast, data3), False)  

    def test_rule2(self):
        """
        Tests the evaluation of a rule that involves a combination of AND 
        and OR operators with conditions on age, department, salary, and 
        experience.

        The rule is as follows:

        ((age > 30 AND department == 'Marketing')) AND 
        (salary > 20000 OR experience > 5)

        The test checks the evaluation of this rule for 2 different sets 
        of data.
        """
        rule2 = "((age > 30 AND department == 'Marketing')) AND (salary > 20000 OR experience > 5)"
        ast = create_rule(rule2)
        data1 = {"age": 32, "department": "Marketing", "salary": 25000, "experience": 6}
        data2 = {"age": 31, "department": "Marketing", "salary": 15000, "experience": 3}

        self.assertEqual(evaluate_rule(ast, data1), True) 
        self.assertEqual(evaluate_rule(ast, data2), False)  

    def test_combined_rules(self):
        """
        Tests the evaluation of a combined rule that involves a combination of AND 
        and OR operators with conditions on age, salary, experience, and department.

        The combined rule is as follows:

        (age > 30 AND salary > 40000) OR (experience > 5 OR department == 'Sales')

        The test checks the evaluation of this rule for 3 different sets of data.
        """
        rules = [
            "age > 30 AND salary > 40000",
            "experience > 5 OR department == 'Sales'"
        ]
        combined_ast = combine_rules(rules)
        data1 = {"age": 35, "salary": 50000, "experience": 4, "department": "Sales"}
        data2 = {"age": 25, "salary": 30000, "experience": 6, "department": "IT"}
        data3 = {"age": 28, "salary": 30000, "experience": 2, "department": "Marketing"}

        self.assertEqual(evaluate_rule(combined_ast, data1), True)  
        self.assertEqual(evaluate_rule(combined_ast, data2), True)  
        self.assertEqual(evaluate_rule(combined_ast, data3), False) 

    def test_edge_cases(self):
        """
        Tests the evaluation of a rule with missing data fields.

        The rule is as follows:
        
        age > 30 AND salary > 50000

        The test checks the evaluation of this rule with datasets that 
        are missing either the 'age' or 'salary' field, ensuring that 
        a ValueError is raised in both cases.
        """
        rule = "age > 30 AND salary > 50000"
        ast = create_rule(rule)
        data_missing_age = {"salary": 60000}
        data_missing_salary = {"age": 35}

        with self.assertRaises(ValueError):
            evaluate_rule(ast, data_missing_age)

        with self.assertRaises(ValueError):
            evaluate_rule(ast, data_missing_salary)

    def test_rule_evaluation_with_strings(self):
        """
        Tests the evaluation of a rule with string values.

        The rule is as follows:

        department == 'Sales' AND region == 'North'

        The test checks the evaluation of this rule with 3 different datasets
        to ensure that the rule is correctly evaluated when strings are involved.
        """
        rule = "department == 'Sales' AND region == 'North'"
        ast = create_rule(rule)
        data1 = {"department": "Sales", "region": "North"}
        data2 = {"department": "Sales", "region": "South"}
        data3 = {"department": "IT", "region": "North"}

        self.assertEqual(evaluate_rule(ast, data1), True)  
        self.assertEqual(evaluate_rule(ast, data2), False) 
        self.assertEqual(evaluate_rule(ast, data3), False)  

class TestNode(unittest.TestCase):

    def test_node_creation(self):
        """
        Tests the creation of a Node object.

        Verifies that the correct value is assigned to the Node, and that the
        left and right children are None when no children are provided.
        """
        node = Node(node_type='operator', value='AND', left=None, right=None)
        self.assertEqual(node.value, 'AND')
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_node_children(self):
        """
        Tests the creation of a Node with children.

        Verifies that the correct left and right children are assigned to the
        parent Node, and that the children are correctly retrieved by the
        'left' and 'right' properties.
        """
        left_child = Node(node_type='operand', value='age > 30')
        right_child = Node(node_type='operand', value='salary > 50000')
        parent = Node(node_type='operator', value='AND', left=left_child, right=right_child)

        self.assertEqual(parent.left.value, 'age > 30')
        self.assertEqual(parent.right.value, 'salary > 50000')

    def test_node_evaluation(self):
        """
        Tests the evaluation of a Node object.

        Verifies that the correct value is returned when evaluating a Node with
        children, and that the correct values are used when evaluating operands
        with different values.
        """
        def mock_evaluate(node, data):
            if node.value == 'AND':
                return node.left.evaluate(data) and node.right.evaluate(data)
            if node.value == 'age > 30':
                return data.get('age', 0) > 30
            if node.value == 'salary > 50000':
                return data.get('salary', 0) > 50000
            return False
        
        # Patching Node's evaluate method for test purpose
        Node.evaluate = mock_evaluate

        left_child = Node(node_type='operand', value='age > 30')
        right_child = Node(node_type='operand', value='salary > 50000')
        parent = Node(node_type='operator', value='AND', left=left_child, right=right_child)

        self.assertTrue(parent.evaluate({'age': 35, 'salary': 60000})) 
        self.assertFalse(parent.evaluate({'age': 25, 'salary': 60000})) 
        self.assertFalse(parent.evaluate({'age': 35, 'salary': 40000})) 


if __name__ == '__main__':
    unittest.main()
