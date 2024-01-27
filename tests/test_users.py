from fastapi.testclient import TestClient
from test_auth import test_login_for_access_token


def test_create_user_201(client: TestClient, user_data: dict):
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["email"] == user_data["email"]
    assert "password" not in json_data
    

def test_create_user_user_already_exists_409(client: TestClient, user_data: dict):
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    response = client.post("/users", json=user_data)
    assert response.status_code == 409


def test_get_users_200(client: TestClient):
    user_count = 3
    for i in range(user_count):
        user_data = {
            "email": f"test{i}@test.com",
            "password": "pass123"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 201
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == user_count
    
        
def test_get_user_me_200(client: TestClient, user_data: dict):
    token = test_login_for_access_token(client, user_data)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    