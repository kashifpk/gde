from pathlib import Path

import jinja2
from fastapi.templating import Jinja2Templates
# import fastapi_vite

from .settings import get_settings
# from .apps import get_apps
# from .filters import custom_filters

settings = get_settings()

here = Path(__file__).parent.absolute()
templates_path = here / 'templates'

# Set according to environment (development or production)
# if settings.environment == 'development':
#     fastapi_vite.settings.hot_reload = True

loaders = [jinja2.FileSystemLoader(templates_path)]

# for app in get_apps():
#     loaders.append(jinja2.FileSystemLoader(here / app / "templates"))

loader = jinja2.ChoiceLoader(loaders)

templates = Jinja2Templates(directory=templates_path, loader=loader)
# templates.env.globals['vite_hmr_client'] = fastapi_vite.vite_hmr_client
# templates.env.globals['vite_asset'] = fastapi_vite.vite_asset

# load custom filters
# templates.env.filters.update(custom_filters)
