from fastapi import APIRouter

from agent_scaffold.protocols.mcp.contracts import MCPRequest, MCPResponse

router = APIRouter(prefix="/api/protocol", tags=["protocol"])


@router.post("/mcp", response_model=MCPResponse)
async def handle_mcp(payload: MCPRequest) -> MCPResponse:
    from agent_scaffold.api.services.protocol_service import ProtocolService
    service = ProtocolService()
    return await service.handle_mcp(payload)
