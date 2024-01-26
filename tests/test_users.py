from fastapi.testclient import TestClient


def test_create_users_201(client: TestClient):
    user_data = {
        "email": "test@test.com",
        "password": "pass123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
