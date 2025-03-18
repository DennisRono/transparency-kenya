from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import json
import inspect

from app.db.session import get_db
from app.models.employee import UserAccount, Role
from app.core.config import settings

security = HTTPBearer()

class RolePermissionMiddleware(BaseHTTPMiddleware):
    """
    Middleware for route-based role and permission authorization.
    """
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for certain paths
        if request.url.path in [
            f"{settings.API_V1_STR}/auth/login",
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
        ]:
            return await call_next(request)
        
        try:
            # Extract token from header
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return await call_next(request)  # Let the endpoint handle auth
            
            scheme, credentials = auth_header.split()
            if scheme.lower() != "bearer":
                return await call_next(request)
            
            token = credentials
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = int(payload["sub"])
            except JWTError:
                return await call_next(request)  # Let the endpoint handle invalid token
            
            # Get user and permissions
            db = next(get_db())
            user = db.query(UserAccount).filter(UserAccount.id == user_id).first()
            if not user:
                return await call_next(request)
            
            # Check if user is active and not locked
            if not user.is_active or user.is_locked:
                return await call_next(request)
            
            # Parse permissions
            role = db.query(Role).filter(Role.id == user.role_id).first()
            if not role:
                return await call_next(request)
            
            try:
                permissions = json.loads(role.permissions)
            except:
                permissions = []
            
            # Attach user and permissions to request state
            request.state.user = user
            request.state.permissions = permissions
            
            # Continue with the request
            return await call_next(request)
            
        except Exception as e:
            # For any errors, let the endpoint handle auth
            return await call_next(request)

