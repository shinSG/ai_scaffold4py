from fastapi import APIRouter

from agent_scaffold.api.services.protocol_service import ProtocolService
from agent_scaffold.protocols.a2a.contracts import A2ARequest, A2AResponse
from agent_scaffold.protocols.acp.contracts import ACPRequest, ACPResponse
from agent_scaffold.protocols.mcp.contracts import MCPRequest, MCPResponse

mcp_router = APIRouter(prefix="/api/protocol", tags=["protocol"])
a2a_router = APIRouter(prefix="/api/protocol", tags=["protocol"])
acp_router = APIRouter(prefix="/api/protocol", tags=["protocol"])
router = APIRouter()
_service = ProtocolService()


@mcp_router.post("/mcp", response_model=MCPResponse)
async def handle_mcp(payload: MCPRequest) -> MCPResponse:
    return await _service.handle_mcp(payload)


@a2a_router.post("/a2a", response_model=A2AResponse)
async def handle_a2a(payload: A2ARequest) -> A2AResponse:
    return await _service.handle_a2a(payload)


@acp_router.post("/acp", response_model=ACPResponse)
async def handle_acp(payload: ACPRequest) -> ACPResponse:
    return await _service.handle_acp(payload)


router.include_router(mcp_router)
router.include_router(a2a_router)
router.include_router(acp_router)
