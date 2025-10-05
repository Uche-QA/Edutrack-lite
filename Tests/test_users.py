import pytest
from fastapi import status


# -----------------------------
# GET /users/
# -----------------------------

def test_get_all_users_returns_200(client):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK


def test_get_all_users_returns_list(client):
    response = client.get("/users/")
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 3


def test_get_all_users_has_correct_names(client):
    response = client.get("/users/")
    users = response.json()

    names = [user["name"] for user in users]
    assert "Temitope Adeyemi" in names
    assert "Ngozi Maduekwe" in names
    assert "Hassan Dogo" in names


# -----------------------------
# GET /users/{id}
# -----------------------------

def test_get_user_by_id_returns_200(client):
    response = client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK


def test_get_user_returns_correct_user(client, sample_user):
    response = client.get("/users/1")
    user = response.json()

    assert user["id"] == sample_user["id"]
    assert user["name"] == sample_user["name"]
    assert user["email"] == sample_user["email"]


def test_get_nonexistent_user_returns_404(client):
    response = client.get("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


# -----------------------------
# POST /users/
# -----------------------------

def test_create_user_returns_201(client, user_create_data):
    response = client.post("/users/", json=user_create_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_user_returns_user_with_id(client, user_create_data):
    response = client.post("/users/", json=user_create_data)
    created_user = response.json()

    assert "id" in created_user
    assert created_user["id"] == 4


def test_create_user_saves_correct_data(client):
    new_user = {
        "name": "Jane Doe",
        "email": "janedoe@email.com",
        "is_active": True,
    }
    response = client.post("/users/", json=new_user)
    created_user = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert created_user["name"] == "Jane Doe"
    assert created_user["email"] == "janedoe@email.com"
    assert created_user["is_active"] is True


def test_create_user_without_name_fails(client):
    incomplete_user = {"email": "test@email.com"}
    response = client.post("/users/", json=incomplete_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_user_with_bad_email_fails(client):
    bad_user = {"name": "Bad Email User", "email": "not-an-email"}
    response = client.post("/users/", json=bad_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# -----------------------------
# PUT /users/{id}
# -----------------------------

def test_update_user_returns_200(client):
    updates = {"name": "Updated Name", "email": "updated@email.com"}
    response = client.put("/users/1", json=updates)
    assert response.status_code == status.HTTP_200_OK


def test_update_user_changes_name(client):
    updates = {"name": "New Name"}
    response = client.put("/users/1", json=updates)
    updated_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert updated_user["name"] == "New Name"


def test_update_user_changes_email(client):
    updates = {"email": "newemail@email.com"}
    response = client.put("/users/1", json=updates)
    updated_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert updated_user["email"] == "newemail@email.com"


def test_update_nonexistent_user_returns_404(client):
    updates = {"name": "Ghost"}
    response = client.put("/users/999", json=updates)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_keeps_same_id(client):
    updates = {"name": "Changed Name"}
    response = client.put("/users/1", json=updates)
    updated_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert updated_user["id"] == 1


# -----------------------------
# PATCH /users/{id}/status
# -----------------------------

def test_deactivate_active_user_returns_200(client):
    status_change = {"is_active": False}
    response = client.patch("/users/1/status", json=status_change)
    assert response.status_code == status.HTTP_200_OK


def test_deactivate_user_changes_status(client):
    status_change = {"is_active": False}
    response = client.patch("/users/1/status", json=status_change)
    user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert user["is_active"] is False


def test_activate_inactive_user_works(client):
    status_change = {"is_active": True}
    response = client.patch("/users/3/status", json=status_change)
    user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert user["is_active"] is True


def test_deactivate_already_inactive_user_fails(client):
    status_change = {"is_active": False}
    response = client.patch("/users/3/status", json=status_change)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already inactive" in response.json()["detail"].lower()


def test_activate_already_active_user_fails(client):
    status_change = {"is_active": True}
    response = client.patch("/users/1/status", json=status_change)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already active" in response.json()["detail"].lower()


# -----------------------------
# DELETE /users/{id}
# -----------------------------

def test_delete_user_returns_204(client):
    response = client.delete("/users/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user_removes_from_database(client):
    client.delete("/users/1")
    response = client.get("/users/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_user_returns_404(client):
    response = client.delete("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_reduces_user_count(client):
    response = client.get("/users/")
    initial_count = len(response.json())

    client.delete("/users/1")

    response = client.get("/users/")
    new_count = len(response.json())

    assert new_count == initial_count - 1
