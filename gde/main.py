from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI  #, Request
# from fastapi.responses import RedirectResponse, Response

from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware

from .views import router as root_router
from .settings import get_settings
from .logging import configure_logging
from .app_init import app_init, app_cleanup


here = Path(__file__).parent.absolute()
static_path = here.parent.absolute() / 'static'
configure_logging()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    "Code that runs before application startup and shutdown"
    app_init()

    yield

    # clean up app globals
    app_cleanup()


app = FastAPI(title="Graph Data Explorer", debug=settings.debug, lifespan=lifespan)
app.mount('/static', StaticFiles(directory=static_path), name="static")
# app.add_middleware(SessionMiddleware, secret_key=settings.middleware_secret_key)


# @app.exception_handler(RequiresLoginException)
# async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
#     response = RedirectResponse(url=request.url_for('login'))
#     response.set_cookie(key="sh_redirect_url", value=request.url.path)

#     return response


app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
# include_app_routers(app)
