from fastapi import APIRouter, status, HTTPException
from typing import List
from app.services.user import UserService
from app.schemas.user import User, UserCreate, UserUpdate, StatusUpdate

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()

@router.get("/", response_model=List[User])
def list_users():
    users = user_service.get_all_users()
    return users 

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    return user_service.create_user(user)

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    user = user_service.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.patch("/{user_id}/status", response_model=User)
def update_status(user_id: int, status_update: StatusUpdate):
    is_active = status_update.is_active  
    result = user_service.update_user_status(user_id, is_active)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if result == "already_set":
        status_text = "active" if is_active else "inactive" 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User is already {status_text}"
        )
    return result

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")