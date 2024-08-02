from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.deps import get_performance_service
from src.core.schemas import (
    MessageResponseSchema,
    PerformanceCreate,
    PerformanceRead,
    PerformanceUpdate,
)
from src.services import PerformanceService

router = APIRouter(prefix="/performances", tags=["Performances"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PerformanceRead)
async def create_performance(
    performance: PerformanceCreate, service: PerformanceService = Depends(get_performance_service)
):
    return await service.create_performance(performance)


@router.get("/{performance_id}", response_model=PerformanceRead)
async def get_performance_by_id(performance_id: UUID, service: PerformanceService = Depends(get_performance_service)):
    return await service.retrieve_performance(performance_id)


@router.patch("/{performance_id}", response_model=PerformanceRead)
async def update_performance(
    performance_id: UUID, performance: PerformanceUpdate, service: PerformanceService = Depends(get_performance_service)
):
    return await service.update_performance(performance_id=performance_id, performance=performance)


@router.delete("/{performance_id}", response_model=MessageResponseSchema)
async def delete_performance(performance_id: UUID, service: PerformanceService = Depends(get_performance_service)):
    return await service.delete_performance(performance_id)
