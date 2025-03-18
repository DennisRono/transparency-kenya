from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.controllers import auth_controller
from app.auth.jwt import get_current_active_user, has_permission, is_admin
from app.db.session import get_db
from app.schemas import auth_schema
from app.models.employee import UserAccount, Employee, Role
from app.auth.permissions import Permissions

router = APIRouter()

@router.get("/", response_model=List[auth_schema.User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.USER_READ))
):
    """
    Retrieve all users.
    """
    users = db.query(UserAccount).filter(UserAccount.is_deleted == False).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=auth_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: auth_schema.UserCreate,
    employee_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.USER_CREATE))
):
    """
    Create a new user.
    """
    # Check if username already exists
    db_user = auth_controller.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    db_user = auth_controller.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if employee exists
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee not found"
        )
    
    # Check if role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not found"
        )
    
    # Create user
    return auth_controller.create_user(db, user, employee_id, role_id)

@router.get("/{user_id}", response_model=auth_schema.User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.USER_READ))
):
    """
    Get a specific user by ID.
    """
    user = db.query(UserAccount).filter(UserAccount.id == user_id, UserAccount.is_deleted == False).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}/lock", response_model=auth_schema.User)
def lock_user(
    user_id: int,
    reason: str,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.USER_UPDATE))
):
    """
    Lock a user account.
    """
    user = auth_controller.lock_user(db, user_id, reason)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}/unlock", response_model=auth_schema.User)
def unlock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.USER_UPDATE))
):
    """
    Unlock a user account.
    """
    user = auth_controller.unlock_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}/role", response_model=auth_schema.User)
def update_user_role(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.USER_UPDATE))
):
    """
    Update a user's role.
    """
    # Check if role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not found"
        )
    
    user = auth_controller.update_user_role(db, user_id, role_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

