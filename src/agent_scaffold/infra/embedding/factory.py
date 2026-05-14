from agent_scaffold.core.config import get_settings
from agent_scaffold.infra.embedding.ports import EmbeddingProvider


def get_embedding_provider() -> EmbeddingProvider:
    settings = get_settings()
    provider = settings.embedding_provider.lower()

    if provider == "openai":
        from agent_scaffold.infra.embedding.openai_provider import OpenAIEmbeddingProvider
        return OpenAIEmbeddingProvider(settings)

    from agent_scaffold.infra.embedding.local_provider import LocalEmbeddingProvider
    return LocalEmbeddingProvider(dimension=settings.embedding_dimension)
