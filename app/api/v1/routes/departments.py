from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.controllers import department_controller
from app.schemas import department_schema
from app.auth.jwt import get_current_active_user, has_permission
from app.models.employee import UserAccount

router = APIRouter()

@router.get("/", response_model=List[department_schema.Department])
def get_departments(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    ministry_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_active_user)
):
    """
    Retrieve all departments with optional filtering.
    """
    return department_controller.get_departments(
        db, skip=skip, limit=limit, name=name, ministry_id=ministry_id
    )

@router.post("/", response_model=department_schema.Department, status_code=status.HTTP_201_CREATED)
def create_department(
    department: department_schema.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission("department:create"))
):
    """
    Create a new department.
    """
    return department_controller.create_department(db, department=department)

@router.get("/{department_id}", response_model=department_schema.DepartmentDetail)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_active_user)
):
    """
    Get detailed information about a specific department.
    """
    db_department = department_controller.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@router.put("/{department_id}", response_model=department_schema.Department)
def update_department(
    department_id: int,
    department: department_schema.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission("department:update"))
):
    """
    Update a department.
    """
    db_department = department_controller.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department_controller.update_department(db, department_id=department_id, department=department)

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission("department:delete"))
):
    """
    Delete a department.
    """
    db_department = department_controller.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    department_controller.delete_department(db, department_id=department_id)
    return None

@router.get("/{department_id}/agencies", response_model=List[department_schema.Agency])
def get_department_agencies(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_active_user)
):
    """
    Get all agencies belonging to a specific department.
    """
    db_department = department_controller.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department_controller.get_department_agencies(db, department_id=department_id)

