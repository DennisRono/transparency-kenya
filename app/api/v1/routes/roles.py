from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import json

from app.auth.jwt import has_permission
from app.db.session import get_db
from app.models.employee import Role, UserAccount
from app.schemas import role_schema
from app.auth.permissions import ADMIN_PERMISSIONS, MANAGER_PERMISSIONS, OFFICER_PERMISSIONS, PUBLIC_PERMISSIONS, Permissions

router = APIRouter()

@router.get("/", response_model=List[role_schema.Role])
def get_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.ROLE_READ))
):
    """
    Retrieve all roles.
    """
    roles = db.query(Role).filter(Role.is_deleted == False).offset(skip).limit(limit).all()
    return roles

@router.post("/", response_model=role_schema.Role, status_code=status.HTTP_201_CREATED)
def create_role(
    role: role_schema.RoleCreate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.ROLE_CREATE))
):
    """
    Create a new role.
    """
    # Check if role name already exists
    db_role = db.query(Role).filter(Role.name == role.name).first()
    if db_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this name already exists"
        )
    
    # Create role
    permissions_json = json.dumps(role.permissions)
    db_role = Role(
        name=role.name,
        description=role.description,
        permissions=permissions_json,
        is_system_role=role.is_system_role,
        is_active=role.is_active
    )
    
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/{role_id}", response_model=role_schema.Role)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.ROLE_READ))
):
    """
    Get a specific role by ID.
    """
    role = db.query(Role).filter(Role.id == role_id, Role.is_deleted == False).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role

@router.put("/{role_id}", response_model=role_schema.Role)
def update_role(
    role_id: int,
    role_update: role_schema.RoleUpdate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.ROLE_UPDATE))
):
    """
    Update a role.
    """
    db_role = db.query(Role).filter(Role.id == role_id, Role.is_deleted == False).first()
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Update attributes
    update_data = role_update.dict(exclude_unset=True)
    if "permissions" in update_data:
        update_data["permissions"] = json.dumps(update_data["permissions"])
    
    for key, value in update_data.items():
        setattr(db_role, key, value)
    
    db.commit()
    db.refresh(db_role)
    return db_role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(has_permission(Permissions.ROLE_DELETE))
):
    """
    Delete a role (soft delete).
    """
    db_role = db.query(Role).filter(Role.id == role_id, Role.is_deleted == False).first()
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Check if role is in use
    users_with_role = db.query(UserAccount).filter(UserAccount.role_id == role_id).count()
    if users_with_role > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role is in use by {users_with_role} users and cannot be deleted"
        )
    
    db_role.is_deleted = True
    db.commit()
    return None

@router.get("/templates/admin", response_model=List[str])
def get_admin_permissions(
    current_user: UserAccount = Depends(has_permission(Permissions.ROLE_READ))
):
    """
    Get the admin permissions template.
    """
    return ADMIN_PERMISSIONS

@router.get("/templates/manager", response_model=List[str])
def get_manager_permissions(
    current_user: UserAccount = Depends(has_permission(Permissions.ROLE_READ))
):
    """
    Get the manager permissions template.
    """
    return MANAGER_PERMISSIONS

@router.get("/templates/officer", response_model=List[str])
def get_officer_permissions(
    current_user: UserAccount = Depends(has_permission(Permissions.ROLE_READ))
):
    """
    Get the officer permissions template.
    """
    return OFFICER_PERMISSIONS

@router.get("/templates/public", response_model=List[str])
def get_public_permissions(
    current_user: UserAccount = Depends(has_permission(Permissions.ROLE_READ))
):
    """
    Get the public permissions template.
    """
    return PUBLIC_PERMISSIONS

