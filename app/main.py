from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import setup_exception_handlers
from app.core.logging import logger
from app.middlewares import (
    RateLimitMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
    RolePermissionMiddleware,
)
from app.db.session import get_db
from sqlalchemy.orm import Session

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_STR}/docs1",
    redoc_url=None,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
if settings.ENVIRONMENT == "production":
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RolePermissionMiddleware)

# Set up exception handlers
setup_exception_handlers(app)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=["Home"])
async def root():
    return {
        "message": "Transparency Kenya Api",
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "documentation": "api/v1/docs",
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}


def run_daily():
    pass


@asynccontextmanager
async def lifespan():
    scheduler = AsyncIOScheduler(timezone="Africa/Nairobi")
    scheduler.add_job(
        func=run_daily, trigger="interval", seconds=60 * 60 * 24
    )  # run daily
    scheduler.start()
    yield


main_app_lifespan = app.router.lifespan_context


@asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    logger.info("Application started")
    async with main_app_lifespan(app) as maybe_state:
        yield maybe_state
    logger.info("Application shutting down")


app.router.lifespan_context = lifespan_wrapper
