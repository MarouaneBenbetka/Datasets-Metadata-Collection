# Datasets-Metadata-Collection

## Introduction

This project is a FastAPI application designed to simulate an ETL (Extract, Transform, Load) process by collecting data from four different sources: GitHub, Kaggle, Hugging Face, and the UCI Machine Learning Repository. It includes functionality for data extraction, cleaning, and loading into a PostgreSQL database, along with API routes to access datasets, detailed information about them, and some statistics about our data.

## Setup Instructions

### 1. Create and Activate a Virtual Environment

Before you start, ensure you have Python 3.8 or higher installed on your system. Follow these steps to set up your virtual environment:

**Step 1:** Clone the project repository to your local machine.

**Step 2:** Navigate to the project directory in your terminal.

**Step 3:** Create a virtual environment named `venv` by running:

```
python -m venv venv
```

**Step 4:** Activate the virtual environment:

-   On Windows:

```
.\venv\Scripts\activate
```

-   On macOS/Linux:

```
source venv/bin/activate
```

### 2. Install Dependencies

With the virtual environment activated, install the project dependencies by running:

```
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the `.env.example` file to a new file named `.env` and fill in the values:

```plaintext
# PostgreSQL database configuration
HOST=<your-db-host>
PORT=<your-db-port>
DB_NAME=<your-db-name>
DB_USERNAME=<your-db-username>
DB_PASSWORD=<your-db-password>

# Secret key for JWT token generation
JWT_SECRET=<your-jwt-secret>

# GitHub authentication token
GITHUB_AUTH_TOKEN=<your-github-auth-token>

# Kaggle API credentials
KAGGLE_USERNAME=<your-kaggle-username>
KAGGLE_KEY=<your-kaggle-key>
```

### 4. Launch the API

Run the FastAPI application with the following command:

```
uvicorn main:app --reload
```

This command starts the server with live reloading enabled.

---

## API Routes Overview

After launching the API, you can access the Swagger UI documentation at `/docs` to explore the available routes, including:

-   **/init-db**: Executes all necessary DDL commands to set up the database schema, including tables, indexes, stored procedures, views, and materialized views.

### ETL Routes

-   **Extract Routes**: For extracting data from the specified sources.
-   **Clean Routes**: For cleaning the extracted data.
-   **Load Routes**: For loading the cleaned data into the database.

### API Data Access Routes

-   Routes to **get datasets**, including detailed information and statistics.

## Database Backup and SQL Resources

Included in the project is a `sql` folder that contains various SQL resources for direct database interaction. This folder includes:

-   **Backup File**: A comprehensive backup file to directly fill your database with initial data.
-   **DDL Scripts**: Scripts for creating tables, indexes, stored procedures, views, and materialized views necessary for the application.
-   **Sample Queries**: Some sample queries for testing and verification purposes after the database setup.

---

## Unit Testing

This project includes a series of unit tests designed to ensure the reliability and functionality of the API endpoints and database interactions. The tests are contained in the `unit_test.py` file. To run these tests, follow the instructions below:

### Running the Unit Tests

Ensure you have pytest installed in your virtual environment. If not, you can install it using pip:

```
pip install pytest
```

With pytest installed, navigate to your project directory in the terminal and execute the tests by running:

```
pytest unit_test.py -s
```

The `-s` flag is used to enable the display of print statements from within the test cases, which can be helpful for debugging and verification purposes.

### Test Cases

The `unit_test.py` file includes tests for:

-   Validating the accessibility and functionality of the `/datasets`, `/datasets/{id}`, `/stats/sources`, and `/stats/tags` endpoints.
-   Testing database connection error handling and query error handling through dependency overrides and fixture setup for simulating different database states.

### Test Environment Configuration

A pytest fixture named `setup_test_env` is used to temporarily configure environment variables for testing against a test database. This ensures that your production or development database is unaffected by the test runs.

---

To utilize the backup for initializing your database, follow the instructions specific to your database management system to import the backup file found within the `sql` folder.
