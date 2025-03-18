from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings

router = APIRouter(include_in_schema=False)
directory = Path(__file__).parents[4].joinpath("static").resolve()
templates = Jinja2Templates(directory)


@router.get("/", response_class=HTMLResponse)
def view_documentations(request: Request):
    return templates.TemplateResponse(
        "/docs.html",
        {
            "request": request,
            "schema_url": f"{settings.API_V1_STR}/openapi.json",
            "title": str(settings.PROJECT_NAME),
        },
    )
