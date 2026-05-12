import json
import logging
from typing import Any
from urllib.parse import urlparse

import httpx

from core.config import Settings, get_settings
from integrations.nacos.ports import NacosPort


class NacosClient(NacosPort):
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._logger = logging.getLogger(__name__)
        self._base_url = self._build_base_url(self._settings.nacos_server_addr)

    async def register(self, metadata: dict[str, Any] | None = None, service_name: str | None = None) -> None:
        if not self._settings.nacos_enabled:
            self._logger.info("nacos register skipped because nacos is disabled")
            return

        params = self._instance_params(metadata=metadata, service_name=service_name)
        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=self._settings.nacos_timeout_seconds) as client:
                response = await client.post("/nacos/v1/ns/instance", params=params)
                response.raise_for_status()
            self._logger.info(
                "nacos registered service %s at %s:%s",
                params["serviceName"],
                params["ip"],
                params["port"],
            )
        except Exception:
            self._logger.exception("nacos register failed")
            if self._settings.nacos_fail_fast:
                raise

    async def deregister(self, service_name: str | None = None) -> None:
        if not self._settings.nacos_enabled:
            self._logger.info("nacos deregister skipped because nacos is disabled")
            return

        params = self._instance_params(service_name=service_name)
        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=self._settings.nacos_timeout_seconds) as client:
                response = await client.delete("/nacos/v1/ns/instance", params=params)
                response.raise_for_status()
            self._logger.info(
                "nacos deregistered service %s at %s:%s",
                params["serviceName"],
                params["ip"],
                params["port"],
            )
        except Exception:
            self._logger.exception("nacos deregister failed")
            if self._settings.nacos_fail_fast:
                raise

    async def discover(self, service_name: str) -> list[dict]:
        if not self._settings.nacos_enabled:
            self._logger.info("nacos discover skipped because nacos is disabled")
            return []

        params: dict[str, Any] = {
            "serviceName": service_name,
            "namespaceId": self._settings.nacos_namespace,
            "groupName": self._settings.nacos_group,
        }
        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=self._settings.nacos_timeout_seconds) as client:
                response = await client.get("/nacos/v1/ns/instance/list", params=params)
                response.raise_for_status()
                payload = response.json()
            return payload.get("hosts", [])
        except Exception:
            self._logger.exception("nacos discover failed for %s", service_name)
            if self._settings.nacos_fail_fast:
                raise
            return []

    def _instance_params(self, metadata: dict[str, Any] | None = None, service_name: str | None = None) -> dict[str, Any]:
        merged_metadata = {
            "app_name": self._settings.app_name,
            "app_version": self._settings.app_version,
            "app_env": self._settings.app_env,
            **self._settings.nacos_metadata,
            **(metadata or {}),
        }
        return {
            "serviceName": service_name or self._settings.nacos_service_name,
            "ip": self._service_ip(),
            "port": self._settings.port,
            "namespaceId": self._settings.nacos_namespace,
            "groupName": self._settings.nacos_group,
            "clusterName": self._settings.nacos_cluster_name,
            "weight": self._settings.nacos_weight,
            "enabled": True,
            "healthy": True,
            "ephemeral": self._settings.nacos_ephemeral,
            "metadata": json.dumps(merged_metadata, ensure_ascii=False),
        }

    def _service_ip(self) -> str:
        if self._settings.nacos_service_ip:
            return self._settings.nacos_service_ip
        if self._settings.host in {"0.0.0.0", "::"}:
            return "127.0.0.1"
        return self._settings.host

    @staticmethod
    def _build_base_url(server_addr: str) -> str:
        parsed = urlparse(server_addr)
        if parsed.scheme:
            return server_addr.rstrip("/")
        return f"http://{server_addr.rstrip('/')}"
