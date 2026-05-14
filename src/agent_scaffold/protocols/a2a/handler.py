from fastapi import APIRouter

from agent_scaffold.protocols.a2a.contracts import A2ARequest, A2AResponse

router = APIRouter(prefix="/api/protocol", tags=["protocol"])


@router.post("/a2a", response_model=A2AResponse)
async def handle_a2a(payload: A2ARequest) -> A2AResponse:
    from agent_scaffold.api.services.protocol_service import ProtocolService
    service = ProtocolService()
    return await service.handle_a2a(payload)
