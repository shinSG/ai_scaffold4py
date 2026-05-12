import pytest

from integrations.nacos.registrar import NacosRegistrar


@pytest.mark.asyncio
async def test_nacos_lifecycle_stub() -> None:
    registrar = NacosRegistrar()
    await registrar.register()
    await registrar.deregister()
