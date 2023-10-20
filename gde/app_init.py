"""
Application wide initialization logic.

This is used by both api and non api processes like celery tasks, cli commands etc.
"""

# from .singletons import sh
# from .apps import get_app_globals

from .logging import configure_logging


# def app_globals_init():
#     # ag = get_app_globals()
#     # sh.app_globals = ag
#     # load app globals

#     for attr_name in dir(sh.app_globals):
#         if attr_name.startswith("_"):
#             continue

#         getattr(sh.app_globals, attr_name).load()


# def app_globals_cleanup():
#     for attr_name in dir(sh.app_globals):
#         if attr_name.startswith("_"):
#             continue

#         getattr(sh.app_globals, attr_name).cleanup()


def app_init():
    configure_logging()
    # app_globals_init()


def app_cleanup():
    # app_globals_cleanup()
    pass
