from agent_scaffold.core.config import Settings
from agent_scaffold.api.servers import get_app_servers, get_enabled_protocols, get_nacos_registrations


def test_app_servers_can_be_enabled_and_registered_independently() -> None:
    settings = Settings(
        NACOS_SERVICE_NAME="demo-agent",
        HTTP_SERVER_ENABLED=True,
        MCP_SERVER_ENABLED=False,
        A2A_SERVER_ENABLED=True,
        ACP_SERVER_ENABLED=True,
        NACOS_REGISTER_HTTP_ENABLED=False,
        NACOS_REGISTER_MCP_ENABLED=True,
        NACOS_REGISTER_A2A_ENABLED=True,
        NACOS_REGISTER_ACP_ENABLED=False,
    )

    servers = {server.protocol: server for server in get_app_servers(settings)}
    enabled_protocols = get_enabled_protocols(settings)
    registrations = {server.protocol: server for server in get_nacos_registrations(settings)}

    assert enabled_protocols == {"http", "a2a", "acp"}
    assert servers["http"].service_name == "demo-agent"
    assert servers["mcp"].service_name == "demo-agent-mcp"
    assert servers["a2a"].service_name == "demo-agent-a2a"
    assert servers["acp"].service_name == "demo-agent-acp"
    assert set(registrations) == {"a2a"}


def test_app_servers_accept_custom_nacos_service_names() -> None:
    settings = Settings(
        NACOS_SERVICE_NAME="demo-agent",
        NACOS_HTTP_SERVICE_NAME="custom-http",
        NACOS_MCP_SERVICE_NAME="custom-mcp",
        NACOS_A2A_SERVICE_NAME="custom-a2a",
        NACOS_ACP_SERVICE_NAME="custom-acp",
    )

    servers = {server.protocol: server for server in get_app_servers(settings)}

    assert servers["http"].service_name == "custom-http"
    assert servers["mcp"].service_name == "custom-mcp"
    assert servers["a2a"].service_name == "custom-a2a"
    assert servers["acp"].service_name == "custom-acp"
