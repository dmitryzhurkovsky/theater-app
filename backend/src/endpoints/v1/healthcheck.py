import structlog
from fastapi import APIRouter

from src.core.schemas import MessageResponseSchema

router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])

LOG = structlog.get_logger()


@router.get("/", summary="Healthcheck", response_model=MessageResponseSchema)
async def healthcheck():
    return MessageResponseSchema(message="success!")
