from fastapi import APIRouter

from app.api.v1.routes import (
    docs,
    auth,
    ministries,
    departments,
    employees,
    budgets,
    complaints,
    police,
    crime_reports,
    auth,
    users,
    roles,
    password_reset,
)

api_router = APIRouter()

api_router.include_router(docs.router, prefix="/docs", tags=["Rapi Docs"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentification"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(password_reset.router, prefix="/password-reset", tags=["authentication"])
api_router.include_router(ministries.router, prefix="/ministries", tags=["ministries"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(complaints.router, prefix="/complaints", tags=["complaints"])
api_router.include_router(police.router, prefix="/police", tags=["police"])
api_router.include_router(crime_reports.router, prefix="/crime-reports", tags=["crime-reports"])
