from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.servers import get_nacos_registrations
from integrations.nacos.registrar import NacosRegistrar


@asynccontextmanager
async def app_lifespan(_: FastAPI) -> AsyncIterator[None]:
    registrar = NacosRegistrar()
    services = get_nacos_registrations()
    await registrar.register_services(services)
    try:
        yield
    finally:
        await registrar.deregister_services(services)
