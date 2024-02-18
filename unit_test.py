from fastapi.testclient import TestClient
from main import app
from psycopg2 import OperationalError, ProgrammingError
from app.db_config import run_query
import os
from dotenv import load_dotenv
import pytest
# Dependency override function for testing

client = TestClient(app)


def test_get_datasets():
    response = client.get("/datasets")
    assert response.status_code == 200
    print("test_get_datasets passed: /datasets endpoint is working as expected.")
    # Add more assertions here based on your expected output


def test_get_dataset_details_existing_id():
    # You need to ensure that there is a dataset with id=1 in your test setup
    response = client.get("/datasets/1")
    assert response.status_code == 200
    print("test_get_dataset_details_existing_id passed: Details for dataset with id=1 retrieved successfully.")
    # Add more assertions here


def test_sources_stats():
    response = client.get("/stats/sources")
    assert response.status_code == 200
    print("test_sources_stats passed: /stats/sources endpoint is working as expected.")


def test_tags_stats():
    response = client.get("/stats/tags")
    assert response.status_code == 200
    print("test_tags_stats passed: /stats/tags endpoint is working as expected.")

# db connection test


@pytest.fixture(scope="session")
def setup_test_env():
    # Backup the original environment variables
    original_db_name = os.getenv("DB_NAME")
    original_db_username = os.getenv("DB_USERNAME")
    original_db_password = os.getenv("DB_PASSWORD")
    original_host = os.getenv("HOST")
    original_port = os.getenv("PORT")

    # Set environment variables for the test database
    # Replace with your test database name
    os.environ["DB_NAME"] = "test_db_name"
    # Replace with your test database username
    os.environ["DB_USERNAME"] = "test_username"
    # Replace with your test database password
    os.environ["DB_PASSWORD"] = "test_password"
    # Adjust if your test DB is hosted differently
    os.environ["HOST"] = "localhost"
    os.environ["PORT"] = "5432"  # Default PostgreSQL port; adjust if necessary

    # Reload dotenv to apply the test environment variables
    load_dotenv()

    yield  # Provide control back to the test function

    # Restore the original environment variables after tests are done
    if original_db_name:
        os.environ["DB_NAME"] = original_db_name
    if original_db_username:
        os.environ["DB_USERNAME"] = original_db_username
    if original_db_password:
        os.environ["DB_PASSWORD"] = original_db_password
    if original_host:
        os.environ["HOST"] = original_host
    if original_port:
        os.environ["PORT"] = original_port


def test_connection_error_handling(monkeypatch, setup_test_env):
    # Usage monkeypatch to simulate a connection error
    def mock_connect(**kwargs):
        raise OperationalError("Could not connect to database")
    monkeypatch.setattr("psycopg2.connect", mock_connect)
    with pytest.raises(OperationalError):
        result = run_query("SELECT 1;")

    print("test_connection_error_handling passed: Connection error handled successfully.")


def test_query_error_handling(setup_test_env):
    # Deliberately cause a syntax error in the SQL
    sql = "SELEC * FROM nonexistent_table;"
    with pytest.raises(ProgrammingError):
        run_query(sql)

    result = run_query("SELECT 1;")

    print("test_query_error_handling passed: Query error handled successfully.")


if __name__ == "__main__":
    import pytest
    # The "-s" option is used here to allow print statements to be visible.
    pytest.main(["-s"])
