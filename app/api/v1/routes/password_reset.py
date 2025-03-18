from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.auth.password_reset import generate_password_reset_token, reset_password
from app.db.session import get_db
from app.schemas import auth_schema

router = APIRouter()

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

@router.post("/request-reset")
def request_password_reset(
    reset_request: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Request a password reset token.
    """
    token = generate_password_reset_token(db, reset_request.email)
    
    # TODO: send an email to the user
    
    return {
        "message": "If your email is registered, you will receive a password reset link."
    }

@router.post("/reset-password", response_model=auth_schema.User)
def confirm_password_reset(
    reset_confirm: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """
    Reset password using a token.
    """
    user = reset_password(db, reset_confirm.token, reset_confirm.new_password)
    return user

