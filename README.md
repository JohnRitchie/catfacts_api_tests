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

## Test Cases Overview

### 1. **Basic Tests**
- **`test_status_code_ok`**: Verifies that the endpoint returns a 200 status code.
- **`test_non_empty_text`**: Ensures the `text` field in the response is not empty.
- **`test_response_contains_all_fields`**: Confirms that all required fields are present in the response.

### 2. **Parameter Validation**
- **`test_default_parameters`**: Validates the default behavior of the API.
- **`test_user_parameters`**: Checks that the API returns the expected type when a parameter (e.g., `animal_type`) is passed.
- **`test_unsupported_parameters`**: Ensures unsupported parameters do not break the API or affect the response.

### 3. **Advanced Tests**
- **`test_datetime_format`**: Validates the format of the `createdAt` and `updatedAt` fields.
- **`test_response_encoding`**: Confirms the response encoding is `UTF-8`.
- **`test_no_caching`**: Ensures the API does not cache responses between requests.

### 4. **Performance and Load Tests**
- **`test_unique_facts`**: Validates that multiple requests return unique facts.
- **`test_high_load`**: Tests the API's behavior under multiple parallel requests.

## Contribution
Feel free to submit issues or pull requests to improve this project. Contributions are welcome!