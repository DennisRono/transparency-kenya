from datetime import datetime, timedelta
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status
from typing import Optional

from app.models.employee import UserAccount
from app.auth.security import get_password_hash
from app.core.config import settings

async def generate_password_reset_token(db: AsyncSession, email: str) -> Optional[str]:
    """
    Generate a password reset token for a user.
    """
    query = select(UserAccount).where(UserAccount.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
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
    
    await db.commit()
    
    return token

async def verify_password_reset_token(db: AsyncSession, token: str) -> Optional[UserAccount]:
    """
    Verify a password reset token.
    """
    query = select(UserAccount).where(UserAccount.activation_token == token)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    
    # Check if token is expired
    if not user.activation_token_expiry or user.activation_token_expiry < datetime.utcnow():
        return None
    
    return user

async def reset_password(db: AsyncSession, token: str, new_password: str) -> UserAccount:
    """
    Reset a user's password using a token.
    """
    user = await verify_password_reset_token(db, token)
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
    
    await db.commit()
    await db.refresh(user)
    
    return user

