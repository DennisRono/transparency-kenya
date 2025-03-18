from typing import Optional
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
import uuid

from app.models.employee import UserAccount, Role, Employee
from app.auth.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.schemas import auth_schema

def get_user_by_username(db: Session, username: str) -> Optional[UserAccount]:
    """
    Get a user by username.
    """
    return db.query(UserAccount).filter(UserAccount.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[UserAccount]:
    """
    Get a user by email.
    """
    return db.query(UserAccount).filter(UserAccount.email == email).first()

def create_user(db: Session, user: auth_schema.UserCreate, employee_id: int, role_id: int) -> UserAccount:
    """
    Create a new user account.
    """
    hashed_password = get_password_hash(user.password)
    
    db_user = UserAccount(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        is_active=True,
        is_locked=False,
        password_reset_required=True,
        failed_login_attempts=0,
        employee_id=employee_id,
        role_id=role_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate(db: Session, username: str, password: str) -> Optional[UserAccount]:
    """
    Authenticate a user.
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        # Increment failed login attempts
        user.failed_login_attempts += 1
        
        # Lock the account if too many failed attempts
        if user.failed_login_attempts >= 5:
            user.is_locked = True
            user.lock_reason = "Too many failed login attempts"
        
        db.commit()
        return None
    
    # Reset failed login attempts on successful login
    if user.failed_login_attempts > 0:
        user.failed_login_attempts = 0
        db.commit()
    
    return user

def create_user_token(user_id: int) -> str:
    """
    Create an access token for a user.
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(subject=user_id, expires_delta=access_token_expires)

def change_password(db: Session, user_id: int, new_password: str) -> UserAccount:
    """
    Change a user's password.
    """
    user = db.query(UserAccount).filter(UserAccount.id == user_id).first()
    if not user:
        return None
    
    user.password_hash = get_password_hash(new_password)
    user.password_reset_required = False
    user.last_password_change = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    return user

def update_user_role(db: Session, user_id: int, role_id: int) -> UserAccount:
    """
    Update a user's role.
    """
    user = db.query(UserAccount).filter(UserAccount.id == user_id).first()
    if not user:
        return None
    
    user.role_id = role_id
    
    db.commit()
    db.refresh(user)
    return user

def lock_user(db: Session, user_id: int, reason: str) -> UserAccount:
    """
    Lock a user account.
    """
    user = db.query(UserAccount).filter(UserAccount.id == user_id).first()
    if not user:
        return None
    
    user.is_locked = True
    user.lock_reason = reason
    
    db.commit()
    db.refresh(user)
    return user

def unlock_user(db: Session, user_id: int) -> UserAccount:
    """
    Unlock a user account.
    """
    user = db.query(UserAccount).filter(UserAccount.id == user_id).first()
    if not user:
        return None
    
    user.is_locked = False
    user.lock_reason = None
    user.failed_login_attempts = 0
    
    db.commit()
    db.refresh(user)
    return user

