def test_get_me_returns_current_user(auth_client):
    client, token, user_data = auth_client
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "hashed_password" not in data


def test_get_me_without_token_returns_401(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_get_me_with_invalid_token_returns_401(client):
    response = client.get("/users/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
