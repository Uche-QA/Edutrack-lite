import pytest
from fastapi import status


# -----------------------------
# GET /enrollments/
# -----------------------------

def test_list_enrollments_returns_200(client):
    response = client.get("/enrollments/")
    assert response.status_code == status.HTTP_200_OK


def test_list_enrollments_returns_list(client):
    response = client.get("/enrollments/")
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_list_enrollments_has_expected_fields(client):
    response = client.get("/enrollments/")
    enrollments = response.json()

    for enrollment in enrollments:
        assert "id" in enrollment
        assert "user_id" in enrollment
        assert "course_id" in enrollment
        assert "enrolled_date" in enrollment
        assert "completed" in enrollment


# -----------------------------
# GET /enrollments/{id}
# -----------------------------

def test_get_enrollment_by_id_returns_200(client):
    response = client.get("/enrollments/1")
    assert response.status_code == status.HTTP_200_OK


def test_get_enrollment_returns_correct_data(client, sample_enrollment):
    response = client.get("/enrollments/1")
    enrollment = response.json()

    assert enrollment["id"] == sample_enrollment["id"]
    assert enrollment["user_id"] == sample_enrollment["user_id"]
    assert enrollment["course_id"] == sample_enrollment["course_id"]


def test_get_enrollment_not_found_returns_404(client):
    response = client.get("/enrollments/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# -----------------------------
# GET /enrollments/user/{user_id}
# -----------------------------

def test_get_enrollments_for_user_returns_200(client):
    response = client.get("/enrollments/user/1")
    assert response.status_code == status.HTTP_200_OK


def test_get_enrollments_for_user_returns_list(client):
    response = client.get("/enrollments/user/1")
    data = response.json()

    assert isinstance(data, list)
    for enrollment in data:
        assert "user_id" in enrollment
        assert enrollment["user_id"] == 1


# -----------------------------
# POST /enrollments/
# -----------------------------

def test_create_enrollment_returns_201(client, enrollment_create_data):
    response = client.post("/enrollments/", json=enrollment_create_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_enrollment_returns_enrollment_with_id(client, enrollment_create_data):
    response = client.post("/enrollments/", json=enrollment_create_data)
    created = response.json()

    assert "id" in created
    assert created["user_id"] == enrollment_create_data["user_id"]
    assert created["course_id"] == enrollment_create_data["course_id"]


def test_create_enrollment_saves_correct_data(client):
    new_enrollment = {
        "user_id": 2,
        "course_id": 2,
        "enrolled_date": "2025-10-05"
    }

    response = client.post("/enrollments/", json=new_enrollment)
    created = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert created["user_id"] == 2
    assert created["course_id"] == 2


def test_create_enrollment_missing_field_fails(client):
    incomplete = {"user_id": 1}
    response = client.post("/enrollments/", json=incomplete)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    


# -----------------------------
# DELETE /enrollments/{id}
# -----------------------------

def test_delete_enrollment_returns_204(client):
    response = client.delete("/enrollments/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_enrollment_removes_from_database(client):
    client.delete("/enrollments/1")
    response = client.get("/enrollments/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_enrollment_returns_404(client):
    response = client.delete("/enrollments/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_reduces_enrollment_count(client):
    response = client.get("/enrollments/")
    initial_count = len(response.json())

    client.delete("/enrollments/1")

    response = client.get("/enrollments/")
    new_count = len(response.json())

    assert new_count == initial_count - 1
