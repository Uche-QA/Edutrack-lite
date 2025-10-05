from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.course import Course, CourseCreate, CourseUpdate
from app.schemas.user import User
from app.services.course import CourseService

router = APIRouter(prefix="/courses", tags=["Courses"])
course_service = CourseService()

# List all courses
@router.get("/", response_model=List[Course])
def list_courses():
    return course_service.get_all_courses()

# Get course by ID
@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Get users enrolled in a course
@router.get("/{course_id}/users", response_model=List[User])
def get_enrolled_users(course_id: int):
    users = course_service.get_enrolled_users(course_id)
    if users is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Course not found")
    if not users:
        raise HTTPException(status_code=404, detail="No users enrolled in this course")
    return users

# Create a course
@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    return course_service.create_course(course)


# Update a course
@router.put("/{course_id}", response_model=Course)
def update_course(course_id: int, course_update: CourseUpdate):
    course = course_service.update_course(course_id, course_update)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Close enrollment for a course
@router.patch("/{course_id}/close", response_model=Course)
def close_enrollment(course_id: int):
    result = course_service.close_enrollment(course_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if result == "already_closed":
        raise HTTPException(status_code=400, detail="Course enrollment is already closed")
    return result

# Delete a course
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    deleted_course = course_service.delete_course(course_id)
    if not deleted_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return None  

