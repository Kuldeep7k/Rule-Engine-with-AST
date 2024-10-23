# Rule Engine with Abstract Syntax Tree (AST)

## Overview

This project implements a 3-tier rule engine designed to determine user eligibility based on various attributes like age, department, income, and experience. The core of the system is built around an Abstract Syntax Tree (AST) that represents conditional rules, allowing for the dynamic creation, combination, and evaluation of rules. It features a user-friendly web interface, RESTful API endpoints, and a backend data storage mechanism powered by SQLite.

## Features

- **Create Rules**: Dynamically create rules from string representations, converting them into AST nodes.
- **Combine Rules**: Combine multiple rules into a single AST for optimized and efficient evaluation.
- **Evaluate Rules**: Evaluate the combined AST against provided user data to determine eligibility.
- **User Interface**: A simple web-based interface for inputting rules and displaying results.
- **Error Handling**: Comprehensive error handling for invalid rule formats and data inputs.
- **Data Storage**: Persistent storage of rules in an SQLite database.

## Screenshots

### UI

![Home](https://github.com/user-attachments/assets/4bb5336f-2112-4cce-8674-9b861f5673dc)

### Create Rule

![create rule](https://github.com/user-attachments/assets/6259c4ba-8c41-459b-a668-9fc8af6c7ff7)

### Combine Rules

![combined rule](https://github.com/user-attachments/assets/3064aa0b-7746-44c2-b339-46d586d4a1ac)

### Evaluate Rule

![evaluate rule](https://github.com/user-attachments/assets/e09bbce8-9aea-4033-af66-b84dd58fe1ad)

---

## Tech Stack

- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Libraries**:
  - Flask for the web framework
  - SQLite3 for database interactions
  - Regex for Rule parsing and validation

## Project Structure

    Rule_Engine_Project/
    ├── rule_engine/
    │ ├── init.py
    │ ├── rule_engine.py
    │ ├── database.py
    │ └── models.py
    ├── templates/
    │ ├── index.html
    │ └── result.html
    ├── static/
    │ ├── script.js
    │ └── style.css
    ├── app.py
    ├── requirements.txt
    └── README.md

### Key Files

- `app.py`: The main Flask application file that handles routing and API endpoints.
- `rule_engine/rule_engine.py`: Contains logic for creating, combining, and evaluating rules using the AST structure.
- `rule_engine/database.py`: Handles database connections and operations for storing rules.
- `static/script.js`: Contains JavaScript functions for managing frontend interactions.
- `static/style.css`: Contains CSS Styles for frontend.
- `templates/index.html`: The main HTML file for the user interface.
- `requirements.txt`: A list of Python packages required for the project.

## Installation

### Prerequisites

Make sure you have Python 3.6 or higher installed on your system.

### Steps to Set Up the Project

1.  Clone the repository:

    ```git
    git clone <repository-url>
    ```

    ```cmd
    cd Rule_Engine_Project
    ```

2.  Create and Activate a Virtual Environment:

    ```python
    python3 -m venv ProjectEnv

    source ProjectEnv/bin/activate  # On Windows: ProjectEnv\Scripts\activate
    ```

3.  Install required packages:
    ```python
    pip install -r requirements.txt
    ```
4.  Run the Flask application:
    ```python
    python app.py
    ````
    The SQLite database (rules.db) will be created automatically when the application is run for the first time.

Open your web browser and navigate to http://127.0.0.1:5000.

### Usage

- Creating a Rule:

  - Input a rule string in the provided text box.
  - Click the "Create Rule" button to convert it into an AST.

- Combining Rules:

  - Enter multiple rule strings, each on a new line.
  - Click the "Combine Rules" button to combine them into a single AST.

- Evaluating a Rule:
  - Provide the AST JSON and user data in the respective input fields.
  - Click the "Evaluate Rule" button to check eligibility.

## API Endpoints

### Create Rule

- Endpoint: /create_rule
- Method: POST
- Request Body:

  ```Json
  {
    "rule_string": "age > 30"
  }
  ```

- Response: Returns the AST representation of the rule.

### Combine Rules

- Endpoint: /combine_rules
- Method: POST
- Request Body:

  ```json
  {
  "rules": [
      "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
  ]}
  ```

- Response: Returns the combined AST.

### Evaluate Rule

- Endpoint: /evaluate_rule
- Method: POST
- Request Body:

  AST JSON:
  ```Json
  {"node_type": "operator", "value": "AND", "left": {"node_type": "operand", "value": "age > 30"}, "right": {"node_type": "operand", "value": "salary > 50000"}}
  ```
  Data JSON:
  ```Json
  {"age": 35, "salary": 60000}
  ```
- Response: 
  
  Status Code: 200 OK

  ```json
  {
    "result": true
  }
  ```

## Database Schema

### Table: rules

  - id (INTEGER PRIMARY KEY):
      This column represents the unique identifier for each rule stored in the database.
      It is an INTEGER and serves as the primary key, meaning it auto-increments for every new rule.
  - rule_string (TEXT NOT NULL):
      This column holds the actual rule in string format.
      The data type is TEXT, and it is required (NOT NULL), meaning every record must have a rule string associated with it.

### Test Cases

## Testing

- Unit tests are provided to ensure the project runs as expected. These tests cover weather data fetching, summary calculations, and alert storage.

  Run the Tests:

      python -m unittest tests/tests.py

### Tests include:

#### TestRuleEngine

1. **test_rule1**: Evaluates a complex rule with `AND` and `OR` operators.
2. **test_rule2**: Tests a simpler rule involving conditions on age, department, salary, and experience.
3. **test_combined_rules**: Evaluates combined rules using multiple conditions.
4. **test_edge_cases**: Checks for proper handling of missing data fields.
5. **test_rule_evaluation_with_strings**: Tests rule evaluation with string values.

#### TestNode

1. **test_node_creation**: Verifies creation of a Node object.
2. **test_node_children**: Tests assignment and retrieval of Node children.
3. **test_node_evaluation**: Checks evaluation logic of Node objects.

## Contact Information

If you have any questions or feedback about the project, feel free to contact me:

<a href="mailto:your_email@example.com">
    <img src="https://skillicons.dev/icons?i=gmail" alt="Gmail" style="width: 34px; height: 34px; margin-right: 10px;">
</a>
<a href="https://www.linkedin.com/in/yourprofile">
    <img src="https://skillicons.dev/icons?i=linkedin" alt="LinkedIn" style="width: 37px; height: 34px;">
</a>
