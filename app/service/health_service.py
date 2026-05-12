from app.model.common import HealthResponse
from core.config import get_settings


class HealthService:
    async def get_health(self) -> HealthResponse:
        settings = get_settings()
        return HealthResponse(status="ok", service=settings.app_name, version=settings.app_version)
