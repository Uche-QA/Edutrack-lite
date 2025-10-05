# EduTrack Lite

cc

---

## 🚀 Features

- Manage users (create, update, deactivate, delete)
- Manage courses (open/close enrollment, update details)
- Enroll users into courses
- Mark enrollments as completed
- Includes **pytest** test coverage with reusable fixtures

---

## 🛠️ Tech Stack

- **FastAPI** — Web framework for building APIs  
- **Pydantic** — Data validation and settings management  
- **Uvicorn** — ASGI server for running FastAPI apps  
- **Pytest** — Testing framework  
- **HTTPX** — Used for test client requests  

---

### Project Structure
edutrack-lite/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point of the FastAPI app
│   ├── database.py             # In-memory mock database
│   │
│   ├── routers/                # API routes
│   │   ├── __init__.py
│   │   ├── user_router.py
│   │   ├── course_router.py
│   │   └── enrollment_router.py
│   │
│   ├── schemas/                # Pydantic models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── course.py
│   │   └── enrollment.py
│   │
│   └── services/               # Business logic
│       ├── __init__.py
│       ├── user.py
│       ├── course.py
│       └── enrollment.py
│
├── tests/                      # Test directory
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_users.py
│   ├── test_courses.py
│   └── test_enrollments.py
│
├── requirements.txt
└── README.md

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

git clone https://github.com/<your-username>/edutrack-lite.git
cd edutrack-lite

### 2 Create Virtual Environment:
python -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate

### 3 Install Dependencies:
pip install -r requirements.txt

### 4 Run the App:
uvicorn app.main:app --reload

Once the server starts, open your browser at:
👉 http://127.0.0.1:8000/docs
 (for Swagger UI)
👉 http://127.0.0.1:8000/redoc
 (for ReDoc)

---

# Running Tests

Run all tests:
pytest -v

Run a specific test file:
pytest tests/test_users.py -v

---

# Example Endpoints
| Method   | Endpoint        | Description               |
| -------- | --------------- | ------------------------- |
| **GET**  | `/users/`       | Get all users             |
| **POST** | `/users/`       | Create a new user         |
| **GET**  | `/courses/`     | Get all courses           |
| **POST** | `/enrollments/` | Enroll a user in a course |


For full documentation, visit Swagger UI

# Contact
Uchenna Agwunobi
Github: Uche-QA