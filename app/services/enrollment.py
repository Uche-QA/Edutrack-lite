from app import database
from app.schemas.enrollment import  EnrollmentUpdate
from datetime import date

class EnrollmentService:
    def get_all_enrollments(self):
        return database.enrollments_db

    def get_enrollment_by_id(self, enrollment_id):
        for e in database.enrollments_db:
            if e["id"] == enrollment_id:
                return e
        return None

    def create_enrollment(self, enrollment_data):
       
        user = next((u for u in database.users_db if u["id"] == enrollment_data.user_id), None)
        if not user:
            raise ValueError("User does not exist")
        if not user["is_active"]:
            raise ValueError("User is not active")

        course = next((c for c in database.courses_db if c["id"] == enrollment_data.course_id), None)
        if not course:
            raise ValueError("Course does not exist")
        if not course["is_open"]:
            raise ValueError("Course is closed for enrollment")

        if any(e for e in database.enrollments_db if e["user_id"] == enrollment_data.user_id and e["course_id"] == enrollment_data.course_id):
            raise ValueError("User already enrolled in this course")

        new_id = max((e["id"] for e in database.enrollments_db), default=0) + 1
        new_enrollment = {
            "id": new_id,
            "user_id": enrollment_data.user_id,
            "course_id": enrollment_data.course_id,
            "enrolled_date": date.today().isoformat(),
            "completed": False
        }
        database.enrollments_db.append(new_enrollment)
        return new_enrollment

    def mark_completed(self, enrollment_id):
        for e in database.enrollments_db:
            if e["id"] == enrollment_id:
                if e.get("completed"):
                    return e
                e["completed"] = True
                return e
        return None

    def update_enrollment(self, enrollment_id: int, update_data: EnrollmentUpdate):
        enrollment = self.get_enrollment_by_id(int(enrollment_id))
        if not enrollment:
             return None
        for key, value in update_data.model_dump(exclude_unset=True).items():
            enrollment[key] = value
            return enrollment

    def get_enrollments_for_user(self, user_id):
        return [e for e in database.enrollments_db if e["user_id"] == user_id]
    
    def delete_enrollment(self, enrollment_id):
        for i, e in enumerate(database.enrollments_db):
            if e["id"] == enrollment_id:
                del database.enrollments_db[i]
                return True
        return False


enrollment_service = EnrollmentService()
