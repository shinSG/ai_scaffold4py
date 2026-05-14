from fastapi import APIRouter

from agent_scaffold.api.models.common import HealthResponse
from agent_scaffold.api.services.health_service import HealthService

router = APIRouter(tags=["health"])
_service = HealthService()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return await _service.get_health()
