from typing import Any, Dict, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class BaseAPIException(Exception):
    """Base API exception class."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        self.headers = headers


class DatabaseError(BaseAPIException):
    """Database error exception."""

    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR",
        )


class NotFoundError(BaseAPIException):
    """Resource not found exception."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail, error_code="NOT_FOUND"
        )


class AuthenticationError(BaseAPIException):
    """Authentication error exception."""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTHENTICATION_ERROR",
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(BaseAPIException):
    """Authorization error exception."""

    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTHORIZATION_ERROR",
        )


class RateLimitExceededError(BaseAPIException):
    """Rate limit exceeded exception."""

    def __init__(self, detail: str = "Rate limit exceeded. Please try again later."):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="RATE_LIMIT_EXCEEDED",
        )


class ValidationError(BaseAPIException):
    """Validation error exception."""

    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR",
        )


class PaymentRequiredError(BaseAPIException):
    """Payment required exception."""

    def __init__(self, detail: str = "Payment required to access this resource"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
            error_code="PAYMENT_REQUIRED",
        )


class ResourceLimitExceededError(BaseAPIException):
    """Resource limit exceeded exception."""

    def __init__(self, detail: str = "Resource limit exceeded"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="RESOURCE_LIMIT_EXCEEDED",
        )


class DeploymentError(BaseAPIException):
    """Deployment error exception."""

    def __init__(self, detail: str = "Deployment failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DEPLOYMENT_ERROR",
        )


class IntegrationError(BaseAPIException):
    """Integration error exception."""

    def __init__(self, detail: str = "Integration error"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail,
            error_code="INTEGRATION_ERROR",
        )


def setup_exception_handlers(app: FastAPI) -> None:
    """Set up exception handlers for the application."""

    @app.exception_handler(BaseAPIException)
    async def handle_base_api_exception(
        request: Request, exc: BaseAPIException
    ) -> JSONResponse:
        """Handle base API exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.error_code, "message": exc.detail}},
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle validation errors."""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation error",
                    "details": exc.errors(),
                }
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def handle_sqlalchemy_error(
        request: Request, exc: SQLAlchemyError
    ) -> JSONResponse:
        """Handle SQLAlchemy errors."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": "Database error occurred",
                }
            },
        )

    @app.exception_handler(Exception)
    async def handle_general_exception(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle general exceptions."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                }
            },
        )
