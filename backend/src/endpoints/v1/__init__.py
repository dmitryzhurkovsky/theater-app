from fastapi import APIRouter

from src.endpoints.v1 import healthcheck

router = APIRouter()

router.include_router(healthcheck.router)
