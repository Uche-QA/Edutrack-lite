from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class User(UserBase):
    id: int

class StatusUpdate(BaseModel):
    is_active: bool

class Config:
    from_attributes = True


