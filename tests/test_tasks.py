def test_create_task(auth_client):
    client, token, _ = auth_client
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tasks", json={"title": "Buy milk"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["is_done"] is False
    assert "id" in data


def test_create_task_with_description(auth_client):
    client, token, _ = auth_client
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tasks", json={"title": "Buy milk", "description": "2% please"}, headers=headers)
    assert response.status_code == 201
    assert response.json()["description"] == "2% please"


def test_list_tasks_returns_only_own_tasks(auth_client):
    client, token, _ = auth_client
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/tasks", json={"title": "Task 1"}, headers=headers)
    client.post("/tasks", json={"title": "Task 2"}, headers=headers)
    response = client.get("/tasks", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id(auth_client):
    client, token, _ = auth_client
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/tasks", json={"title": "My task"}, headers=headers).json()
    response = client.get(f"/tasks/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "My task"


def test_get_nonexistent_task_returns_404(auth_client):
    client, token, _ = auth_client
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks/99999", headers=headers)
    assert response.status_code == 404


def test_update_task_mark_done(auth_client):
    client, token, _ = auth_client
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/tasks", json={"title": "My task"}, headers=headers).json()
    response = client.put(f"/tasks/{created['id']}", json={"is_done": True}, headers=headers)
    assert response.status_code == 200
    assert response.json()["is_done"] is True
    assert response.json()["title"] == "My task"  # title unchanged


def test_update_task_title(auth_client):
    client, token, _ = auth_client
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/tasks", json={"title": "Old title"}, headers=headers).json()
    response = client.put(f"/tasks/{created['id']}", json={"title": "New title"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_delete_task(auth_client):
    client, token, _ = auth_client
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/tasks", json={"title": "My task"}, headers=headers).json()
    delete_response = client.delete(f"/tasks/{created['id']}", headers=headers)
    assert delete_response.status_code == 204
    get_response = client.get(f"/tasks/{created['id']}", headers=headers)
    assert get_response.status_code == 404


def test_cannot_access_another_users_task(auth_client, client):
    client, token1, _ = auth_client

    # Register a second user
    client.post("/auth/register", json={"email": "other@example.com", "password": "password123"})
    login_resp = client.post("/auth/login", json={"email": "other@example.com", "password": "password123"})
    token2 = login_resp.json()["access_token"]

    # User 1 creates a task
    headers1 = {"Authorization": f"Bearer {token1}"}
    created = client.post("/tasks", json={"title": "Private task"}, headers=headers1).json()

    # User 2 tries to read it
    headers2 = {"Authorization": f"Bearer {token2}"}
    response = client.get(f"/tasks/{created['id']}", headers=headers2)
    assert response.status_code == 404  # 404, not 403 — don't reveal task exists


def test_cannot_update_another_users_task(auth_client, client):
    client, token1, _ = auth_client

    client.post("/auth/register", json={"email": "other@example.com", "password": "password123"})
    login_resp = client.post("/auth/login", json={"email": "other@example.com", "password": "password123"})
    token2 = login_resp.json()["access_token"]

    headers1 = {"Authorization": f"Bearer {token1}"}
    created = client.post("/tasks", json={"title": "Private task"}, headers=headers1).json()

    headers2 = {"Authorization": f"Bearer {token2}"}
    response = client.put(f"/tasks/{created['id']}", json={"title": "Hijacked"}, headers=headers2)
    assert response.status_code == 404  # 404, not 403 — don't reveal task exists


def test_cannot_delete_another_users_task(auth_client, client):
    client, token1, _ = auth_client

    client.post("/auth/register", json={"email": "other@example.com", "password": "password123"})
    login_resp = client.post("/auth/login", json={"email": "other@example.com", "password": "password123"})
    token2 = login_resp.json()["access_token"]

    headers1 = {"Authorization": f"Bearer {token1}"}
    created = client.post("/tasks", json={"title": "Private task"}, headers=headers1).json()

    headers2 = {"Authorization": f"Bearer {token2}"}
    response = client.delete(f"/tasks/{created['id']}", headers=headers2)
    assert response.status_code == 404
