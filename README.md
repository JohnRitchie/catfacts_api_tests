# Random Facts API Test Suite

## Overview
This project is a Python-based test automation suite designed to test the Cat Facts API. It validates the API's behavior, response structure, and functionality under various conditions. The suite also uses Allure for reporting.

## Project Structure
```
.
├── requirements.txt
├── session.py
├── conftest.py
├── tests
│   ├── tests_random_facts
│   │   ├── random_facts_models.py
│   │   └── test_random_facts.py   # Test cases for the /random endpoint
```

## Prerequisites
Before running the tests, ensure you have the following installed:
- Python 3.10+
- pip (Python package manager)

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Tests
1. Execute the tests with Pytest:
   ```bash
   pytest --alluredir=allure-results
   ```

2. To generate and view the Allure report:
   ```bash
   allure serve allure-results
   ```

## Key Features
- Response validation against Pydantic models.
- Logging and reporting of request and response details using Allure.
- Includes tests for status codes, response structure, data correctness, and parallel request handling.

## Contribution
Feel free to submit issues or pull requests to improve this project. Contributions are welcome!