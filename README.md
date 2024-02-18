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

## API Routes Overview

After launching the API, you can access the Swagger UI documentation at `/docs` to explore the available routes, including:

-   **/init-db**: Executes all necessary DDL commands to set up the database schema, including tables, indexes, stored procedures, views, and materialized views.

### ETL Routes

-   **Extract Routes**: For extracting data from the specified sources.
-   **Clean Routes**: For cleaning the extracted data.
-   **Load Routes**: For loading the cleaned data into the database.

### API Data Access Routes

-   Routes to **get datasets**, including detailed information and statistics.

## Database Backup

Included in the project is a backup file to directly fill your database with initial data. Follow the instructions specific to your database management system to import this backup.

---
