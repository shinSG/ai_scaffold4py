from core.config import get_settings
from integrations.llm.echo_provider import EchoLLMProvider
from integrations.llm.ollama_provider import OllamaProvider
from integrations.llm.openai_compatible_provider import OpenAICompatibleProvider
from integrations.llm.ports import LLMProvider


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