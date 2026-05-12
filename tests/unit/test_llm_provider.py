import pytest

from core.config import get_settings
from core.exceptions import ConfigurationError
from integrations.llm.echo_provider import EchoLLMProvider
from integrations.llm.factory import get_llm_provider
from integrations.llm.ollama_provider import OllamaProvider
from integrations.llm.openai_compatible_provider import OpenAICompatibleProvider


def test_get_default_llm_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, EchoLLMProvider)
    get_settings.cache_clear()


def test_get_ollama_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, OllamaProvider)
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_openai_compatible_provider_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai-compatible")
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, OpenAICompatibleProvider)
    with pytest.raises(ConfigurationError):
        await provider.generate("hello")
    get_settings.cache_clear()


def test_openai_compatible_provider_builds_sampling_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai-compatible")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("LLM_TEMPERATURE", "0.2")
    monkeypatch.setenv("LLM_TOP_P", "0.8")
    monkeypatch.setenv("LLM_TOP_K", "50")
    monkeypatch.setenv("LLM_ENABLE_THINKING", "true")
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, OpenAICompatibleProvider)
    payload = provider._build_payload("hello", system_prompt="system")
    assert payload["model"] == "test-model"
    assert payload["temperature"] == 0.2
    assert payload["top_p"] == 0.8
    assert payload["top_k"] == 50
    assert payload["enable_thinking"] is True
    assert payload["messages"][0] == {"role": "system", "content": "system"}
    get_settings.cache_clear()


def test_openai_compatible_provider_can_show_reasoning(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai-compatible")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_SHOW_REASONING", "true")
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, OpenAICompatibleProvider)
    content = provider._extract_content(
        {
            "choices": [
                {
                    "message": {
                        "reasoning_content": "reasoning text",
                        "content": "final answer",
                    }
                }
            ]
        }
    )
    assert "reasoning text" in content
    assert "final answer" in content
    get_settings.cache_clear()