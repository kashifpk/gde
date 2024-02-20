"""Views that render non-json responses. Usually HTML responses are returned."""

from typing import Optional
import importlib.metadata
from fastapi import Depends, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
# from sqlalchemy import text

# from .singletons import sh
# from .db import get_db, Session
from .template_config import templates
# from .auth.depends import is_user_logged_in


router = APIRouter()


@router.get('/', response_class=HTMLResponse, include_in_schema=False)
def main(request: Request):
    "Homepage"

    return templates.TemplateResponse(
        'gde-main.html',
        {"request": request}
    )


@router.get('/detail', response_class=HTMLResponse, include_in_schema=False)
def detail(request: Request):
    "Node/Edge detail page"

    return templates.TemplateResponse(
        'gde-detail.html',
        {"request": request, "item_key": ""}
    )

@router.get('/detail/{item_key}', response_class=HTMLResponse, include_in_schema=False)
def detail_with_item(request: Request, item_key: str ):
    "Node/Edge detail page"

    return templates.TemplateResponse(
        'gde-detail.html',
        {"request": request, "item_key": item_key}
    )






@router.get('/test', response_class=HTMLResponse, include_in_schema=False)
def test_page(request: Request):
    "Test page for experimentation"

    return templates.TemplateResponse(
        'test.html',
        {"request": request}
    )
