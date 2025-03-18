from fastapi import APIRouter

from app.api.v1.routes import (docs)

api_router = APIRouter()

api_router.include_router(docs.router, prefix="/docs", tags=["Rapi Docs"])