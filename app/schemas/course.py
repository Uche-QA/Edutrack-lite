from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    description: str
    is_open: bool = True

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_open: bool | None = None

class Course(CourseBase):
    id: int

class Config:
    from_attributes = True

