import logging.config

from fastapi import FastAPI

from backend.src.core.config.settings import get_settings
from backend.src.utils.logging_config import config

logging.config.dictConfig(config.LOGGING_CONFIG)
settings = get_settings()

# initializing FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    swagger_ui_parameters=settings.SWAGGER_UI_PARAMETERS,
    debug=settings.DEBUG,
    version=settings.VERSION,
)

# adding routers
# app.include_router()
