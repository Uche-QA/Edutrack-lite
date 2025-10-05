from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.enrollment import Enrollment, EnrollmentCreate, EnrollmentUpdate
from app.services.enrollment import enrollment_service  

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.get("/", response_model=List[Enrollment])
def list_enrollments():
    return enrollment_service.get_all_enrollments()

@router.get("/{enrollment_id}", response_model=Enrollment)
def get_enrollment(enrollment_id: int):
    e = enrollment_service.get_enrollment_by_id(enrollment_id) 
    if not e:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return e

@router.get("/user/{user_id}", response_model=List[Enrollment])
def get_enrollments_for_user(user_id: int):
    return enrollment_service.get_enrollments_for_user(user_id)

@router.post("/", response_model=Enrollment, status_code=201)
def create_enrollment(enrollment: EnrollmentCreate):
    try:
        return enrollment_service.create_enrollment(enrollment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    
@router.put("/{enrollment_id}", response_model=Enrollment)
def update_enrollment(enrollment_id: int, enrollment_update: EnrollmentUpdate):
    e = enrollment_service.update_enrollment(enrollment_id, enrollment_update)
    if not e:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return e

@router.patch("/{enrollment_id}/complete", response_model=Enrollment)
def mark_completed(enrollment_id: int):
    e = enrollment_service.mark_completed(enrollment_id)
    if not e:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return e


@router.delete("/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int):
    ok = enrollment_service.delete_enrollment(enrollment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
