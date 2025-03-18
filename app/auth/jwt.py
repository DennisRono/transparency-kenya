from typing import List, Optional, Union, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
import json

from app.core.config import settings
from app.db.session import get_db
from app.models.employee import UserAccount, Role
from app.schemas.auth_schema import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> UserAccount:
    """
    Get the current authenticated user from JWT token.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(UserAccount).filter(UserAccount.id == token_data.sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_user(
    current_user: UserAccount = Depends(get_current_user),
) -> UserAccount:
    """
    Get the current active user.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    
    if current_user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is locked",
        )
    
    return current_user

def has_permission(required_permissions: Union[str, List[str]]):
    """
    Dependency to check if the current user has the required permissions.
    
    Usage:
    @app.get("/endpoint")
    def endpoint(current_user: UserAccount = Depends(has_permission(["permission1", "permission2"]))):
        ...
    """
    if isinstance(required_permissions, str):
        required_permissions = [required_permissions]
    
    def permission_checker(
        current_user: UserAccount = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> UserAccount:
        # Get user role
        role = db.query(Role).filter(Role.id == current_user.role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not found",
            )
        
        # Parse permissions
        try:
            user_permissions = json.loads(role.permissions)
        except:
            user_permissions = []
        
        # Check if user has all required permissions
        for permission in required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {permission} is required",
                )
        
        return current_user
    
    return permission_checker

def is_admin(
    current_user: UserAccount = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> UserAccount:
    """
    Check if the current user is an admin.
    """
    # Get user role
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or role.name != "Administrator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    
    return current_user
