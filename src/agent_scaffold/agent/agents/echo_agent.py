from agent_scaffold.agent.abstractions.base_agent import BaseAgent
from agent_scaffold.agent.abstractions.context import AgentContext


class EchoAgent(BaseAgent):
    name = "echo"

    async def run(self, context: AgentContext) -> str:
        return f"Echo: {context.user_input}"
