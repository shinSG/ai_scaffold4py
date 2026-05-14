from typing import Any

from agent_scaffold.infra.nacos.client import NacosClient


class NacosRegistrar:
    def __init__(self, client: NacosClient | None = None) -> None:
        self._client = client or NacosClient()

    async def register(self, metadata: dict[str, Any] | None = None, service_name: str | None = None) -> None:
        await self._client.register(metadata=metadata, service_name=service_name)

    async def deregister(self, service_name: str | None = None) -> None:
        await self._client.deregister(service_name=service_name)

    async def register_services(self, services: list[Any]) -> None:
        for service in services:
            await self.register(metadata=self._metadata_for(service), service_name=service.service_name)

    async def deregister_services(self, services: list[Any]) -> None:
        for service in reversed(services):
            await self.deregister(service_name=service.service_name)

    @staticmethod
    def _metadata_for(service: Any) -> dict[str, Any]:
        return {
            "server_name": service.name,
            "protocol": service.protocol,
            "endpoint": service.endpoint,
            **service.metadata,
        }
