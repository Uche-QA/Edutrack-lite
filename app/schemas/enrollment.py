from pydantic import BaseModel
from datetime import date

class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int
    enrolled_date: date 
    completed: bool = False

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    user_id: int | None = None
    course_id: int | None = None
    enrolled_date: date | None = None
    completed: bool | None = None

class Enrollment(EnrollmentBase):
    id: int

class Config:
        from_attributes = True 

class Config:
    from_attributes = True
