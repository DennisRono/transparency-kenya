from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.auth.security import verify_password
from app.db.session import get_db
from app.models.employee import UserAccount, Role
from app.schemas.auth_schema import TokenPayload
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def authenticate_user(db: Session, username: str, password: str) -> Optional[UserAccount]:
    """
    Authenticate a user by username and password.
    """
    user = db.query(UserAccount).filter(UserAccount.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserAccount:
    """
    Get the current authenticated user.
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
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    
    return user

def check_user_permissions(required_permissions: list, user: UserAccount = Depends(get_current_user)) -> bool:
    """
    Check if the user has the required permissions.
    """
    user_permissions = user.role.permissions
    # Assuming permissions is a JSON string that needs to be parsed
    import json
    user_permissions = json.loads(user_permissions)
    
    for permission in required_permissions:
        if permission not in user_permissions:
            return False
    return True

def get_admin_user(
    current_user: UserAccount = Depends(get_current_user),
) -> UserAccount:
    """
    Check if the user is an admin.
    """
    # Assuming the role with id=1 is the admin role
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
