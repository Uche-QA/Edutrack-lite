import pytest
from fastapi import status


# -----------------------------
# GET /courses/
# -----------------------------

def test_get_all_courses_returns_200(client):
    response = client.get("/courses/")
    assert response.status_code == status.HTTP_200_OK


def test_get_all_courses_returns_list(client):
    response = client.get("/courses/")
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_get_all_courses_has_expected_fields(client):
    response = client.get("/courses/")
    courses = response.json()

    for course in courses:
        assert "id" in course
        assert "title" in course
        assert "description" in course


# -----------------------------
# GET /courses/{id}
# -----------------------------

def test_get_course_by_id_returns_200(client):
    response = client.get("/courses/1")
    assert response.status_code == status.HTTP_200_OK


def test_get_course_returns_correct_course(client, sample_course):
    response = client.get("/courses/1")
    course = response.json()

    assert course["id"] == sample_course["id"]
    assert course["title"] == sample_course["title"]
    assert course["description"] == sample_course["description"]


def test_get_nonexistent_course_returns_404(client):
    response = client.get("/courses/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


# -----------------------------
# POST /courses/
# -----------------------------

def test_create_course_returns_201(client, course_create_data):
    response = client.post("/courses/", json=course_create_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_course_returns_course_with_id(client, course_create_data):
    response = client.post("/courses/", json=course_create_data)
    created_course = response.json()

    assert "id" in created_course
    assert created_course["title"] == course_create_data["title"]


def test_create_course_saves_correct_data(client):
    new_course = {
        "title": "Advanced Data Structures",
        "description": "In-depth coverage of data structures and algorithms.",
    }
    response = client.post("/courses/", json=new_course)
    created_course = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert created_course["title"] == "Advanced Data Structures"
    assert created_course["description"].startswith("In-depth coverage")


def test_create_course_without_title_fails(client):
    incomplete_course = {"description": "Missing title field"}
    response = client.post("/courses/", json=incomplete_course)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# -----------------------------
# PUT /courses/{id}
# -----------------------------

def test_update_course_returns_200(client):
    updates = {"title": "Updated Course", "description": "Updated content"}
    response = client.put("/courses/1", json=updates)

    assert response.status_code == status.HTTP_200_OK


def test_update_course_changes_title(client):
    updates = {"title": "New Course Title"}
    response = client.put("/courses/1", json=updates)
    updated_course = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert updated_course["title"] == "New Course Title"


def test_update_nonexistent_course_returns_404(client):
    updates = {"title": "Ghost Course"}
    response = client.put("/courses/999", json=updates)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_keeps_same_id(client):
    updates = {"title": "Retitled Course"}
    response = client.put("/courses/1", json=updates)
    updated_course = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert updated_course["id"] == 1


# -----------------------------
# DELETE /courses/{id}
# -----------------------------

def test_delete_course_returns_204(client):
    response = client.delete("/courses/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_course_removes_from_database(client):
    client.delete("/courses/1")
    response = client.get("/courses/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_course_returns_404(client):
    response = client.delete("/courses/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_reduces_course_count(client):
    response = client.get("/courses/")
    initial_count = len(response.json())

    client.delete("/courses/1")

    response = client.get("/courses/")
    new_count = len(response.json())

    assert new_count == initial_count - 1
