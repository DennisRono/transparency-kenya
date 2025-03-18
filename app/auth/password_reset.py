from datetime import datetime, timedelta
import secrets
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.employee import UserAccount
from app.auth.security import get_password_hash
from app.core.config import settings

def generate_password_reset_token(db: Session, email: str) -> str:
    """
    Generate a password reset token for a user.
    """
    user = db.query(UserAccount).filter(UserAccount.email == email).first()
    if not user:
        # Don't reveal that the user doesn't exist
        return None
    
    if not user.is_active:
        # Don't allow password reset for inactive users
        return None
    
    # Generate a secure token
    token = secrets.token_urlsafe(32)
    
    # Set token expiry (24 hours)
    expiry = datetime.utcnow() + timedelta(hours=24)
    
    # Save token to user
    user.activation_token = token
    user.activation_token_expiry = expiry
    
    db.commit()
    
    return token

def verify_password_reset_token(db: Session, token: str) -> Optional[UserAccount]:
    """
    Verify a password reset token.
    """
    user = db.query(UserAccount).filter(UserAccount.activation_token == token).first()
    if not user:
        return None
    
    # Check if token is expired
    if not user.activation_token_expiry or user.activation_token_expiry < datetime.utcnow():
        return None
    
    return user

def reset_password(db: Session, token: str, new_password: str) -> UserAccount:
    """
    Reset a user's password using a token.
    """
    user = verify_password_reset_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    # Update password
    user.password_hash = get_password_hash(new_password)
    user.activation_token = None
    user.activation_token_expiry = None
    user.password_reset_required = False
    user.last_password_change = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    return user

