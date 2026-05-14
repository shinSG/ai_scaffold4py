from functools import lru_cache
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="agent-scaffold4py", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    app_env: str = Field(default="dev", alias="APP_ENV")
    host: str = Field(default="0.0.0.0", alias="APP_HOST")
    port: int = Field(default=8000, alias="APP_PORT")

    http_server_enabled: bool = Field(default=True, alias="HTTP_SERVER_ENABLED")
    mcp_server_enabled: bool = Field(default=True, alias="MCP_SERVER_ENABLED")
    a2a_server_enabled: bool = Field(default=True, alias="A2A_SERVER_ENABLED")
    acp_server_enabled: bool = Field(default=True, alias="ACP_SERVER_ENABLED")

    nacos_server_addr: str = Field(default="127.0.0.1:8848", alias="NACOS_SERVER_ADDR")
    nacos_namespace: str = Field(default="public", alias="NACOS_NAMESPACE")
    nacos_group: str = Field(default="DEFAULT_GROUP", alias="NACOS_GROUP")
    nacos_service_name: str = Field(default="agent-scaffold4py", alias="NACOS_SERVICE_NAME")
    nacos_enabled: bool = Field(default=True, alias="NACOS_ENABLED")
    nacos_service_ip: str | None = Field(default=None, alias="NACOS_SERVICE_IP")
    nacos_cluster_name: str = Field(default="DEFAULT", alias="NACOS_CLUSTER_NAME")
    nacos_weight: float = Field(default=1.0, alias="NACOS_WEIGHT")
    nacos_ephemeral: bool = Field(default=True, alias="NACOS_EPHEMERAL")
    nacos_timeout_seconds: float = Field(default=2.0, alias="NACOS_TIMEOUT_SECONDS")
    nacos_fail_fast: bool = Field(default=False, alias="NACOS_FAIL_FAST")
    nacos_metadata: dict[str, Any] = Field(default_factory=dict, alias="NACOS_METADATA")
    nacos_register_http_enabled: bool = Field(default=True, alias="NACOS_REGISTER_HTTP_ENABLED")
    nacos_register_mcp_enabled: bool = Field(default=True, alias="NACOS_REGISTER_MCP_ENABLED")
    nacos_register_a2a_enabled: bool = Field(default=True, alias="NACOS_REGISTER_A2A_ENABLED")
    nacos_register_acp_enabled: bool = Field(default=True, alias="NACOS_REGISTER_ACP_ENABLED")
    nacos_http_service_name: str | None = Field(default=None, alias="NACOS_HTTP_SERVICE_NAME")
    nacos_mcp_service_name: str | None = Field(default=None, alias="NACOS_MCP_SERVICE_NAME")
    nacos_a2a_service_name: str | None = Field(default=None, alias="NACOS_A2A_SERVICE_NAME")
    nacos_acp_service_name: str | None = Field(default=None, alias="NACOS_ACP_SERVICE_NAME")

    mq_backend: str = Field(default="rabbitmq", alias="MQ_BACKEND")
    rabbitmq_url: str = Field(default="amqp://guest:guest@127.0.0.1:5672/", alias="RABBITMQ_URL")
    rocketmq_namesrv_addr: str = Field(default="127.0.0.1:9876", alias="ROCKETMQ_NAMESRV_ADDR")

    llm_provider: str = Field(default="echo", alias="LLM_PROVIDER")
    llm_model: str = Field(default="echo", alias="LLM_MODEL")
    llm_base_url: str | None = Field(default=None, alias="LLM_BASE_URL")
    llm_api_key: str | None = Field(default=None, alias="LLM_API_KEY")
    llm_timeout_seconds: float = Field(default=30.0, alias="LLM_TIMEOUT_SECONDS")
    llm_temperature: float = Field(default=0.7, alias="LLM_TEMPERATURE")
    llm_top_p: float = Field(default=1.0, alias="LLM_TOP_P")
    llm_top_k: int = Field(default=0, alias="LLM_TOP_K")
    llm_max_tokens: int = Field(default=1024, alias="LLM_MAX_TOKENS")
    llm_enable_thinking: bool = Field(default=False, alias="LLM_ENABLE_THINKING")
    llm_show_reasoning: bool = Field(default=False, alias="LLM_SHOW_REASONING")

    embedding_provider: str = Field(default="local", alias="EMBEDDING_PROVIDER")
    embedding_model: str = Field(default="text-embedding-ada-002", alias="EMBEDDING_MODEL")
    embedding_base_url: str | None = Field(default=None, alias="EMBEDDING_BASE_URL")
    embedding_dimension: int = Field(default=384, alias="EMBEDDING_DIMENSION")

    vectorstore_backend: str = Field(default="memory", alias="VECTORSTORE_BACKEND")
    vectorstore_endpoint: str = Field(default="http://127.0.0.1:8000", alias="VECTORSTORE_ENDPOINT")
    vectorstore_collection: str = Field(default="default", alias="VECTORSTORE_COLLECTION")

    cache_backend: str = Field(default="memory", alias="CACHE_BACKEND")
    cache_redis_url: str = Field(default="redis://127.0.0.1:6379/0", alias="CACHE_REDIS_URL")

    rag_backend: str = Field(default="stub", alias="RAG_BACKEND")
    rag_endpoint: str = Field(default="http://127.0.0.1:9000", alias="RAG_ENDPOINT")

    db_url: str = Field(default="sqlite+aiosqlite:///./agent_scaffold.db", alias="DB_URL")
    db_echo: bool = Field(default=False, alias="DB_ECHO")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
