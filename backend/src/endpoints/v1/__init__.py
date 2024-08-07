from fastapi import APIRouter

from src.endpoints.v1 import healthcheck, performance, performance_role, users
from src.endpoints.v1.auth import jwt_auth
from src.endpoints.v1.auth.oauth import google

router = APIRouter()

router.include_router(healthcheck.router)
router.include_router(users.router)
router.include_router(jwt_auth.router)
router.include_router(google.router)
router.include_router(performance.router)
router.include_router(performance_role.router)
