from agent_scaffold.core.config import get_settings
from agent_scaffold.infra.llm.echo_provider import EchoLLMProvider
from agent_scaffold.infra.llm.ollama_provider import OllamaProvider
from agent_scaffold.infra.llm.openai_compatible_provider import OpenAICompatibleProvider
from agent_scaffold.infra.llm.ports import LLMProvider


def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    provider = settings.llm_provider.lower()

    if provider == "ollama":
        return OllamaProvider(settings)
    if provider == "deepseek":
        return OpenAICompatibleProvider(settings, base_url=settings.llm_base_url or "https://api.deepseek.com/v1")
    if provider in {"openai", "openai-compatible", "qwen", "dashscope"}:
        return OpenAICompatibleProvider(settings)
    return EchoLLMProvider()
