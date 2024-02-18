from fastapi.testclient import TestClient
from main import app


# Dependency override function for testing


client = TestClient(app)


def test_get_datasets():
    response = client.get("/datasets")
    assert response.status_code == 200
    # Add more assertions here based on your expected output


def test_get_dataset_details_existing_id():
    # You need to ensure that there is a dataset with id=1 in your test setup
    response = client.get("/datasets/1")
    assert response.status_code == 200
    # Add more assertions here


if __name__ == "__main__":
    import pytest
    pytest.main()
