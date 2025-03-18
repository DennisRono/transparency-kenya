from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.controllers import auth_controller
from app.auth.jwt import get_current_active_user
from app.db.session import get_db
from app.schemas import auth_schema
from app.models.employee import UserAccount

router = APIRouter()

@router.post("/login", response_model=auth_schema.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await auth_controller.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is locked"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    access_token = auth_controller.create_user_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/password-change", response_model=auth_schema.User)
async def change_password(
    password_data: auth_schema.PasswordChange,
    current_user: UserAccount = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change the current user's password.
    """
    # Verify current password
    if not auth_controller.verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Change password
    user = await auth_controller.change_password(db, current_user.id, password_data.new_password)
    return user

@router.get("/me", response_model=auth_schema.User)
async def read_users_me(current_user: UserAccount = Depends(get_current_active_user)):
    """
    Get current user information.
    """
    return current_user

