from fastapi import APIRouter

from src.endpoints.v1 import healthcheck
from src.endpoints.v1 import users

router = APIRouter()

router.include_router(healthcheck.router)
router.include_router(users.router)
