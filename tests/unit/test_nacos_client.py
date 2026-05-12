import json

from core.config import Settings
from integrations.nacos.client import NacosClient


def test_nacos_client_builds_instance_params() -> None:
    settings = Settings(
        APP_NAME="demo-agent",
        APP_VERSION="1.2.3",
        APP_ENV="test",
        APP_HOST="0.0.0.0",
        APP_PORT=9000,
        NACOS_SERVICE_NAME="demo-service",
        NACOS_METADATA={"owner": "ai"},
    )
    client = NacosClient(settings=settings)

    params = client._instance_params(metadata={"protocols": "mcp,a2a,acp"})
    metadata = json.loads(params["metadata"])

    assert params["serviceName"] == "demo-service"
    assert params["ip"] == "127.0.0.1"
    assert params["port"] == 9000
    assert metadata["app_name"] == "demo-agent"
    assert metadata["protocols"] == "mcp,a2a,acp"
    assert metadata["owner"] == "ai"


def test_nacos_client_accepts_service_name_override() -> None:
    settings = Settings(NACOS_SERVICE_NAME="demo-service")
    client = NacosClient(settings=settings)

    params = client._instance_params(service_name="demo-service-mcp")

    assert params["serviceName"] == "demo-service-mcp"
