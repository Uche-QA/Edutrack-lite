from app import database

class CourseService:
    def get_all_courses(self):
        return database.courses_db

    def get_course_by_id(self, course_id: int):
        for c in database.courses_db:
            if c["id"] == course_id:
                return c
        return None
    
    def get_enrolled_users(self, course_id: int):
        # Check course exists
        course = self.get_course_by_id(course_id)
        if not course:
            return None
        # Find all enrollments for this course
        user_ids = [e["user_id"] for e in database.enrollments_db if e["course_id"] == course_id]
        # Get user dicts
        users = [u for u in database.users_db if u["id"] in user_ids]
        return users

    def create_course(self, course_data):
        new_course = course_data.model_dump()
        new_course["id"] = database.course_id_counter
        new_course.setdefault("is_open", True)
        database.courses_db.append(new_course)
        database.course_id_counter += 1
        return new_course

    
    def update_course(self, course_id: int, update_data):
        course = self.get_course_by_id(course_id)
        if not course:
            return None
        for key, value in update_data.model_dump(exclude_unset=True).items():
            course[key] = value
        return course
        
    def close_enrollment(self, course_id: int):
        course = self.get_course_by_id(course_id)
        if not course:
            return None
        if not course["is_open"]:
            return "already_closed"
        course["is_open"] = False
        return course
    
    def delete_course(self, course_id: int):
        course = self.get_course_by_id(course_id)
        if not course:
            return None
        database.courses_db.remove(course) 
        return True
    
