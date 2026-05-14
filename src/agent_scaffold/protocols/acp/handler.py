from fastapi import APIRouter

from agent_scaffold.protocols.acp.contracts import ACPRequest, ACPResponse

router = APIRouter(prefix="/api/protocol", tags=["protocol"])


@router.post("/acp", response_model=ACPResponse)
async def handle_acp(payload: ACPRequest) -> ACPResponse:
    from agent_scaffold.api.services.protocol_service import ProtocolService
    service = ProtocolService()
    return await service.handle_acp(payload)
