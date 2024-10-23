import sqlite3

def create_database():
    """
    Create a database with a table for storing rules.

    This function establishes a connection to the 'rules.db' database and creates a table named 'rules'
    with two columns: 'id' as the primary key and 'rule_string' as a non-null text field.

    Returns:
        None
    """
    with sqlite3.connect('rules.db') as connection:
        cursor = connection.cursor()
        
        # Create a table for rules
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY,
                rule_string TEXT NOT NULL
            )
        ''')
        
        connection.commit()

def add_rule(rule_string):
    """
    Add a rule to the database.

    Args:
        rule_string (str): The rule as a string.

    Returns:
        None
    """
    try:
        with sqlite3.connect('rules.db') as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO rules (rule_string) VALUES (?)', (rule_string,))
            connection.commit()
            print("Rule added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while adding the rule: {e}")

def get_rules():
    """
    Retrieve all rules from the database.

    Returns:
        A list of tuples, where each tuple contains the id and rule_string.
    """
    try:
        with sqlite3.connect('rules.db') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM rules')
            return cursor.fetchall()  # Returns a list of tuples (id, rule_string)
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving rules: {e}")
        return []
