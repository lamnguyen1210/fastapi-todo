def test_register_creates_user(client):
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # never expose the hash


def test_register_duplicate_email_returns_400(client):
    payload = {"email": "user@example.com", "password": "password123"}
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_login_returns_jwt_token(client):
    client.post("/auth/register", json={"email": "user@example.com", "password": "password123"})
    response = client.post("/auth/login", json={"email": "user@example.com", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password_returns_401(client):
    client.post("/auth/register", json={"email": "user@example.com", "password": "password123"})
    response = client.post("/auth/login", json={"email": "user@example.com", "password": "wrongpassword"})
    assert response.status_code == 401


def test_login_unknown_email_returns_401(client):
    response = client.post("/auth/login", json={"email": "ghost@example.com", "password": "password123"})
    assert response.status_code == 401
