import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import database


@pytest.fixture(scope="function")
def client():
    """Fixture that provides a TestClient for making requests to the API"""
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def reset_database():
    """
    Automatically reset the in-memory database before each test.
    This ensures test isolation and prevents test interference.
    """
    # Store original state
    original_courses = database.courses_db.copy()
    original_enrollments = database.enrollments_db.copy()
    original_users = database.users_db.copy()
    original_course_counter = database.course_id_counter
    original_user_counter = database.user_id_counter
    original_enrollment_counter = database.enrollment_id_counter
    
    # Reset to initial state
    database.courses_db.clear()
    database.courses_db.extend([
        {"id": 1, "title": "Python Basics", "description": "Learn Python", "is_open": True},
        {"id": 2, "title": "FastAPI Fundamentals", "description": "Learn FastAPI", "is_open": True},
        {"id": 3, "title": "Data Structures", "description": "Learn DS", "is_open": False},
    ])
    
    database.enrollments_db.clear()
    database.enrollments_db.extend([
        {"id": 1, "user_id": 1, "course_id": 1, "enrolled_date": "2025-09-16", "completed": False},
        {"id": 2, "user_id": 2, "course_id": 1, "enrolled_date": "2025-09-17", "completed": False},
        {"id": 3, "user_id": 1, "course_id": 2, "enrolled_date": "2025-09-18", "completed": True},
    ])
    
    database.users_db.clear()
    database.users_db.extend([
        {"id": 1, "name": "Temitope Adeyemi", "email": "temitopeadeyemi@email.com", "is_active": True},
        {"id": 2, "name": "Ngozi Maduekwe", "email": "ngozimaduekwe@email.com", "is_active": True},
        {"id": 3, "name": "Hassan Dogo", "email": "hassandogo@email.com", "is_active": False},
    ])
    
    # Reset counters
    database.course_id_counter = 4
    database.user_id_counter = 4
    database.enrollment_id_counter = 4
    
    yield
    
    # Cleanup after test (restore original state)
    database.courses_db.clear()
    database.courses_db.extend(original_courses)
    database.enrollments_db.clear()
    database.enrollments_db.extend(original_enrollments)
    database.users_db.clear()
    database.users_db.extend(original_users)
    database.course_id_counter = original_course_counter
    database.user_id_counter = original_user_counter
    database.enrollment_id_counter = original_enrollment_counter


@pytest.fixture
def sample_course():
    """Fixture providing a sample course dictionary"""
    return {
        "id": 1,
        "title": "Python Basics",
        "description": "Learn Python",
        "is_open": True
    }


@pytest.fixture
def sample_user():
    """Fixture providing a sample user dictionary"""
    return {
        "id": 1,
        "name": "Temitope Adeyemi",
        "email": "temitopeadeyemi@email.com",
        "is_active": True
    }


@pytest.fixture
def sample_enrollment():
    """Fixture providing a sample enrollment dictionary"""
    return {
        "id": 1,
        "user_id": 1,
        "course_id": 1,
        "enrolled_date": "2025-09-16",
        "completed": False
    }


@pytest.fixture
def course_create_data():
    """Fixture providing valid data for creating a course"""
    return {
        "title": "Advanced Python",
        "description": "Master Python programming",
        "is_open": True
    }


@pytest.fixture
def course_update_data():
    """Fixture providing valid data for updating a course"""
    return {
        "title": "Python Basics - Updated",
        "description": "Learn Python from scratch",
        "is_open": True
    }


@pytest.fixture
def user_create_data():
    """Fixture providing valid data for creating a user"""
    return {
        "name": "John Doe",
        "email": "johndoe@email.com",
        "is_active": True
    }


@pytest.fixture
def user_update_data():
    """Fixture providing valid data for updating a user"""
    return {
        "name": "John Doe Updated",
        "email": "johndoe.updated@email.com",
        "is_active": False
    }


@pytest.fixture
def enrollment_create_data():
    """Fixture providing valid data for creating an enrollment"""
    return {
        "user_id": 2,
        "course_id": 2,
        "enrolled_date": "2025-10-01"
    }


# Pytest configuration
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )


# Custom assertions (optional)
@pytest.fixture
def assert_course_structure():
    """Fixture providing a function to assert course structure"""
    def _assert(course_dict):
        assert "id" in course_dict
        assert "title" in course_dict
        assert "description" in course_dict
        assert "is_open" in course_dict
        assert isinstance(course_dict["id"], int)
        assert isinstance(course_dict["title"], str)
        assert isinstance(course_dict["description"], str)
        assert isinstance(course_dict["is_open"], bool)
    return _assert


@pytest.fixture
def assert_user_structure():
    """Fixture providing a function to assert user structure"""
    def _assert(user_dict):
        assert "id" in user_dict
        assert "name" in user_dict
        assert "email" in user_dict
        assert "is_active" in user_dict
        assert isinstance(user_dict["id"], int)
        assert isinstance(user_dict["name"], str)
        assert isinstance(user_dict["email"], str)
        assert isinstance(user_dict["is_active"], bool)
    return _assert


@pytest.fixture
def assert_enrollment_structure():
    """Fixture providing a function to assert enrollment structure"""
    def _assert(enrollment_dict):
        assert "id" in enrollment_dict
        assert "user_id" in enrollment_dict
        assert "course_id" in enrollment_dict
        assert "enrolled_date" in enrollment_dict
        assert "completed" in enrollment_dict
        assert isinstance(enrollment_dict["id"], int)
        assert isinstance(enrollment_dict["user_id"], int)
        assert isinstance(enrollment_dict["course_id"], int)
        assert isinstance(enrollment_dict["enrolled_date"], str)
        assert isinstance(enrollment_dict["completed"], bool)
    return _assert