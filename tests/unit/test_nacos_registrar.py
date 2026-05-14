import pytest

from agent_scaffold.api.servers import ServerDefinition
from agent_scaffold.infra.nacos.registrar import NacosRegistrar


class FakeNacosClient:
    def __init__(self) -> None:
        self.registered: list[tuple[str | None, dict | None]] = []
        self.deregistered: list[str | None] = []

    async def register(self, metadata: dict | None = None, service_name: str | None = None) -> None:
        self.registered.append((service_name, metadata))

    async def deregister(self, service_name: str | None = None) -> None:
        self.deregistered.append(service_name)


@pytest.mark.asyncio
async def test_nacos_registrar_registers_and_deregisters_multiple_services() -> None:
    client = FakeNacosClient()
    registrar = NacosRegistrar(client=client)  # type: ignore[arg-type]
    services = [
        ServerDefinition(
            name="mcp-server",
            protocol="mcp",
            endpoint="/api/protocol/mcp",
            service_name="demo-mcp",
            enabled=True,
            nacos_register_enabled=True,
        ),
        ServerDefinition(
            name="a2a-server",
            protocol="a2a",
            endpoint="/api/protocol/a2a",
            service_name="demo-a2a",
            enabled=True,
            nacos_register_enabled=True,
        ),
    ]

    await registrar.register_services(services)
    await registrar.deregister_services(services)

    assert [item[0] for item in client.registered] == ["demo-mcp", "demo-a2a"]
    assert client.registered[0][1]["protocol"] == "mcp"
    assert client.registered[0][1]["endpoint"] == "/api/protocol/mcp"
    assert client.deregistered == ["demo-a2a", "demo-mcp"]
