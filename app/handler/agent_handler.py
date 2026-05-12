from fastapi import APIRouter

from app.model.agent import AgentRunRequest, AgentRunResponse
from app.service.agent_service import AgentService

router = APIRouter(prefix="/api/agent", tags=["agent"])
_service = AgentService()


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(payload: AgentRunRequest) -> AgentRunResponse:
    return await _service.run(payload)
