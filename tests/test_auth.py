from fastapi.testclient import TestClient


def test_login_for_access_token(client: TestClient, user_data: dict):
    # create user
    r_create = client.post("/users", json=user_data)
    assert r_create.status_code == 201
    # get token
    payload = {"username": user_data["email"], "password": user_data["password"]}
    r_token = client.post("/token", data=payload)
    assert r_token.status_code == 200
    token = r_token.json()["access_token"]
    assert token is not None
    # return token for use in other tests
    return token
