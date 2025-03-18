from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.controllers import employee_controller
from app.schemas import employee_schema
from app.auth.jwt import get_current_active_user, has_permission
from app.models.employee import UserAccount

router = APIRouter()

@router.get("/", response_model=List[employee_schema.Employee])
def get_employees(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    position_id: Optional[int] = None,
    ministry_id: Optional[int] = None,
    department_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission("employee:read"))
):
    """
    Retrieve all employees with optional filtering.
    """
    return employee_controller.get_employees(
        db, skip=skip, limit=limit, name=name, position_id=position_id,
        ministry_id=ministry_id, department_id=department_id, status=status
    )

@router.post("/", response_model=employee_schema.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: employee_schema.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission("employee:create"))
):
    """
    Create a new employee.
    """
    return employee_controller.create_employee(db, employee=employee)

@router.get("/{employee_id}", response_model=employee_schema.EmployeeDetail)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission("employee:read"))
):
    """
    Get detailed information about a specific employee.
    """
    db_employee = employee_controller.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}", response_model=employee_schema.Employee)
def update_employee(
    employee_id: int,
    employee: employee_schema.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission("employee:update"))
):
    """
    Update an employee.
    """
    db_employee = employee_controller.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_controller.update_employee(db, employee_id=employee_id, employee=employee)

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission("employee:delete"))
):
    """
    Delete an employee (soft delete).
    """
    db_employee = employee_controller.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee_controller.delete_employee(db, employee_id=employee_id)
    return None

@router.get("/{employee_id}/performance-reviews", response_model=List[employee_schema.PerformanceReview])
def get_employee_performance_reviews(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission("performance:read"))
):
    """
    Get all performance reviews for a specific employee.
    """
    db_employee = employee_controller.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_controller.get_employee_performance_reviews(db, employee_id=employee_id)

