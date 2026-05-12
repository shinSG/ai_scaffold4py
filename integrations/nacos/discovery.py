from integrations.nacos.client import NacosClient


class NacosDiscovery:
    def __init__(self, client: NacosClient | None = None) -> None:
        self._client = client or NacosClient()

    async def list_instances(self, service_name: str) -> list[dict]:
        return await self._client.discover(service_name)
