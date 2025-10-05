from datetime import date

# Auto-increment counters
user_id_counter = 4
course_id_counter = 4
enrollment_id_counter = 4

# In-memory "tables"
users_db = [
    {"id": 1, "name": "Temitope Adeyemi", "email": "temitopeadeyemi@email.com", "is_active": True},
    {"id": 2, "name": "Ngozi Maduekwe", "email": "ngozimaduekwe@email.com", "is_active": True},
    {"id": 3, "name": "Hassan Dogo", "email": "hassandogo@email.com", "is_active": False},
]

courses_db = [
    {"id": 1, "title": "Python Basics", "description": "Learn Python", "is_open": True},
    {"id": 2, "title": "FastAPI Fundamentals", "description": "Learn FastAPI", "is_open": True},
    {"id": 3, "title": "Data Structures", "description": "Learn DS", "is_open": False},
]

enrollments_db = [
    {"id": 1, "user_id": 1, "course_id": 1, "enrolled_date": "2025-09-16", "completed": False},
    {"id": 2, "user_id": 2, "course_id": 1, "enrolled_date": "2025-09-17", "completed": False},
    {"id": 3, "user_id": 1, "course_id": 2, "enrolled_date": "2025-09-18", "completed": True},
]
