from fastapi import FastAPI

from src.core.config.settings import settings
from src.endpoints.v1 import router as v1_router


def add_routes(app: FastAPI) -> None:
    app.include_router(v1_router, prefix=f"{settings.ENDPOINTS_SERVICE_PREFIX}/v1")
