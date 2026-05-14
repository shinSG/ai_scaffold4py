from dataclasses import dataclass, field
from typing import Any

from agent_scaffold.core.config import Settings, get_settings


@dataclass(frozen=True)
class ServerDefinition:
    name: str
    protocol: str
    endpoint: str
    service_name: str
    enabled: bool
    nacos_register_enabled: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def should_register(self) -> bool:
        return self.enabled and self.nacos_register_enabled


class HTTPServer:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def definition(self) -> ServerDefinition:
        return ServerDefinition(
            name="http-server",
            protocol="http",
            endpoint="/",
            service_name=self._settings.nacos_http_service_name or self._settings.nacos_service_name,
            enabled=self._settings.http_server_enabled,
            nacos_register_enabled=self._settings.nacos_register_http_enabled,
            metadata={"routes": "/health,/api/agent/run,/api/stream/sse,/api/stream/ws"},
        )


class MCPServer:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def definition(self) -> ServerDefinition:
        return ServerDefinition(
            name="mcp-server",
            protocol="mcp",
            endpoint="/api/protocol/mcp",
            service_name=self._settings.nacos_mcp_service_name or f"{self._settings.nacos_service_name}-mcp",
            enabled=self._settings.mcp_server_enabled,
            nacos_register_enabled=self._settings.nacos_register_mcp_enabled,
        )


class A2AServer:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def definition(self) -> ServerDefinition:
        return ServerDefinition(
            name="a2a-server",
            protocol="a2a",
            endpoint="/api/protocol/a2a",
            service_name=self._settings.nacos_a2a_service_name or f"{self._settings.nacos_service_name}-a2a",
            enabled=self._settings.a2a_server_enabled,
            nacos_register_enabled=self._settings.nacos_register_a2a_enabled,
        )


class ACPServer:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def definition(self) -> ServerDefinition:
        return ServerDefinition(
            name="acp-server",
            protocol="acp",
            endpoint="/api/protocol/acp",
            service_name=self._settings.nacos_acp_service_name or f"{self._settings.nacos_service_name}-acp",
            enabled=self._settings.acp_server_enabled,
            nacos_register_enabled=self._settings.nacos_register_acp_enabled,
        )


def get_app_servers(settings: Settings | None = None) -> list[ServerDefinition]:
    resolved_settings = settings or get_settings()
    return [
        HTTPServer(resolved_settings).definition(),
        MCPServer(resolved_settings).definition(),
        A2AServer(resolved_settings).definition(),
        ACPServer(resolved_settings).definition(),
    ]


def get_enabled_protocols(settings: Settings | None = None) -> set[str]:
    return {server.protocol for server in get_app_servers(settings) if server.enabled}


def get_nacos_registrations(settings: Settings | None = None) -> list[ServerDefinition]:
    return [server for server in get_app_servers(settings) if server.should_register]
