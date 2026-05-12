from fastapi import APIRouter

from app.model.common import HealthResponse
from app.service.health_service import HealthService

router = APIRouter(tags=["health"])
_service = HealthService()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return await _service.get_health()
