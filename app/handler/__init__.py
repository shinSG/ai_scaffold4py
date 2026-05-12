from .agent_handler import router as agent_router
from .health_handler import router as health_router
from .protocol_handler import a2a_router, acp_router, mcp_router, router as protocol_router
from .stream_handler import router as stream_router

__all__ = ["health_router", "agent_router", "stream_router", "protocol_router", "mcp_router", "a2a_router", "acp_router"]
