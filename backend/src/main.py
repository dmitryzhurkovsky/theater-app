import logging.config

from fastapi import FastAPI

from backend.src.core.config.settings import get_settings
from backend.src.utils.logging_config import config

logging.config.dictConfig(config.LOGGING_CONFIG)
settings = get_settings()

# initializing FastAPI app
app = FastAPI(
    title="Theater App",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    debug=settings.DEBUG,
    version=settings.VERSION,
)

# adding routers
# app.include_router()
