import pytest
from fastapi.testclient import TestClient
from test_auth import test_login_for_access_token


@pytest.fixture
def post_data() -> dict:
    return {"title": "Example", "content": "Lorem Ipsum"}


def test_create_post_201(client: TestClient, post_data: dict, user_data: dict):
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    assert response.json()["title"] == post_data["title"]
    assert response.json()["content"] == post_data["content"]


def test_create_post_not_logged_in_401(client: TestClient, post_data: dict):
    response = client.post("/posts", json=post_data)
    assert response.status_code == 401


def test_get_post_200(client: TestClient, post_data: dict, user_data: dict):
    # Create post
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    post_id = response.json()["id"]
    # Get post
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    post = response.json()
    assert post["title"] == post_data["title"]
    assert post["votes"] == 0
    assert post["owner"] == user_data["email"]


def test_get_post_not_found_404(client: TestClient):
    response = client.get("/posts/1")
    assert response.status_code == 404


def test_get_posts_200(client: TestClient, user_data: dict):
    # Create posts
    post_count = 10
    token = test_login_for_access_token(client, user_data)
    for i in range(1, post_count + 1):
        post_data = {"title": str(i), "content": "Lorem Ipsum"}
        response = client.post(
            "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
        )
        assert response.status_code == 201
    # Get posts
    response = client.get("/posts")
    assert response.status_code == 200
    posts = response.json()
    # All posts were returned and are in correct order
    for i in range(post_count):
        assert posts[i]["title"] == str(post_count - i)


def test_get_posts_limit_200(client: TestClient, user_data: dict):
    # Create posts
    post_count = 10
    token = test_login_for_access_token(client, user_data)
    for i in range(1, post_count + 1):
        post_data = {"title": str(i), "content": "Lorem Ipsum"}
        response = client.post(
            "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
        )
        assert response.status_code == 201
    # Get posts
    limit = 3
    response = client.get("/posts", params={"limit": limit})
    assert response.status_code == 200
    posts = response.json()
    # Correct posts were returned
    for i in range(limit):
        assert posts[i]["title"] == str(post_count - i)


def test_get_posts_offset_200(client: TestClient, user_data: dict):
    # Create posts
    post_count = 5
    token = test_login_for_access_token(client, user_data)
    for i in range(1, post_count + 1):
        post_data = {"title": str(i), "content": "Lorem Ipsum"}
        response = client.post(
            "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
        )
        assert response.status_code == 201
    # Get posts
    offset = 3
    response = client.get("/posts", params={"offset": offset})
    assert response.status_code == 200
    # Correct posts were returned
    posts = response.json()
    for i in range(post_count - offset):
        assert posts[i]["title"] == str(post_count - offset - i)


def test_update_post_200(client: TestClient, post_data: dict, user_data: dict):
    # Create post
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    post_id = response.json()["id"]
    # Update post
    updated_post_data = {"title": post_data["title"], "content": "updated content"}
    response = client.put(
        f"/posts/{post_id}",
        json=updated_post_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["content"] == updated_post_data["content"]
    # Post was updated
    response = client.get(f"/posts/{post_id}")
    assert response.json()["content"] == updated_post_data["content"]


def test_update_post_not_logged_in_401(client: TestClient, post_data: dict):
    response = client.put("/posts/1", json=post_data)
    assert response.status_code == 401


def test_update_post_not_found_404(
    client: TestClient, post_data: dict, user_data: dict
):
    token = test_login_for_access_token(client, user_data)
    response = client.put(
        "/posts/1", json=post_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_update_post_not_owner_403(
    client: TestClient, post_data: dict, user_data: dict
):
    # Create post
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    post_id = response.json()["id"]
    # Create another user
    user_data_2 = {"email": "other_user@test.com", "password": "pass123"}
    token_2 = test_login_for_access_token(client, user_data_2)
    # Update post
    response = client.put(
        f"/posts/{post_id}",
        json=post_data,
        headers={"Authorization": f"Bearer {token_2}"},
    )
    assert response.status_code == 403


def test_delete_post_204(client: TestClient, post_data: dict, user_data: dict):
    # Create post
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    post_id = response.json()["id"]
    # Delete post
    response = client.delete(
        f"/posts/{post_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
    # Post was deleted
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404


def test_delete_post_not_found_404(client: TestClient, user_data: dict):
    token = test_login_for_access_token(client, user_data)
    response = client.delete("/posts/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_delete_post_not_logged_in_401(client: TestClient):
    response = client.delete("/posts/1")
    assert response.status_code == 401


def test_delete_post_not_owner_403(
    client: TestClient, post_data: dict, user_data: dict
):
    # Create post
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    post_id = response.json()["id"]
    # Create another user
    user_data_2 = {"email": "other_user@test.com", "password": "pass123"}
    token_2 = test_login_for_access_token(client, user_data_2)
    # Delete post
    response = client.delete(
        f"/posts/{post_id}", headers={"Authorization": f"Bearer {token_2}"}
    )
    assert response.status_code == 403


def test_vote_post_201(client: TestClient, post_data: dict, user_data: dict):
    # Create post
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    post_id = response.json()["id"]
    # Vote
    response = client.post(
        f"/posts/{post_id}/vote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    # Vote was added
    response = client.get(f"/posts/{post_id}")
    assert response.json()["votes"] == 1


def test_vote_post_already_voted_400(
    client: TestClient, post_data: dict, user_data: dict
):
    # Create post
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    post_id = response.json()["id"]
    # Vote
    response = client.post(
        f"/posts/{post_id}/vote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    # Vote again
    response = client.post(
        f"/posts/{post_id}/vote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400


def test_vote_post_not_logged_in_401(client: TestClient):
    response = client.post("/posts/1/vote")
    response.status_code == 401


def test_vote_post_not_found_404(client: TestClient, user_data: dict):
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts/1/vote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_unvote_post_200(client: TestClient, post_data: dict, user_data: dict):
    # Create post
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    post_id = response.json()["id"]
    # Vote
    response = client.post(
        f"/posts/{post_id}/vote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    # Unvote
    response = client.post(
        f"/posts/{post_id}/unvote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    # Vote was removed
    response = client.get(f"/posts/{post_id}")
    assert response.json()["votes"] == 0


def test_unvote_post_no_vote_400(client: TestClient, post_data: dict, user_data: dict):
    # Create post
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts", headers={"Authorization": f"Bearer {token}"}, json=post_data
    )
    assert response.status_code == 201
    post_id = response.json()["id"]
    # Vote
    response = client.post(
        f"/posts/{post_id}/vote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    # Unvote
    response = client.post(
        f"/posts/{post_id}/unvote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    # Unvote again
    response = client.post(
        f"/posts/{post_id}/unvote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400


def test_unvote_post_not_found_404(
    client: TestClient, post_data: dict, user_data: dict
):
    token = test_login_for_access_token(client, user_data)
    response = client.post(
        "/posts/1/unvote", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_unvote_post_not_logged_in_401(client: TestClient):
    response = client.post("/posts/1/unvote")
    response.status_code == 401
