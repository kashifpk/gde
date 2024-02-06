"""Views that render non-json responses. Usually HTML responses are returned."""

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
        {"request": request}
    )

