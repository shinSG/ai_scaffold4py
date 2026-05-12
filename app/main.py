from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.handler import a2a_router, acp_router, agent_router, health_router, mcp_router, stream_router
from app.lifespan import app_lifespan
from app.middleware.error_handler import app_error_handler, generic_error_handler
from app.middleware.request_id import RequestIdMiddleware
from app.servers import get_enabled_protocols
from core.config import get_settings
from core.exceptions import AppError

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=app_lifespan)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, generic_error_handler)

app.include_router(health_router)
enabled_protocols = get_enabled_protocols(settings)
if "http" in enabled_protocols:
    app.include_router(agent_router)
    app.include_router(stream_router)
if "mcp" in enabled_protocols:
    app.include_router(mcp_router)
if "a2a" in enabled_protocols:
    app.include_router(a2a_router)
if "acp" in enabled_protocols:
    app.include_router(acp_router)
