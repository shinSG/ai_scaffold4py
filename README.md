# Agent Scaffold for Python

[English](README.md) | [简体中文](README.zh-CN.md)

A baseline Agent service scaffold built with FastAPI.

## Features

- FastAPI app with layered structure
- Agent orchestration skeleton
- Service endpoints and adapters for MCP, A2A and ACP
- Optional HTTP, MCP, A2A and ACP servers with independent Nacos registration
- MQ abstractions for RocketMQ and RabbitMQ
- Streaming endpoints with SSE and WebSocket
- RAG / Prompt / Memory extension points
- Project generation script

## Quick Start

```bash
pip install -r requirements/base.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Full usage guide

See [docs/USAGE.md](docs/USAGE.md) for the complete scaffold usage guide, including service development, server switches, Nacos registration, streaming, extension points, testing and deployment notes.

## Endpoints

- GET /health
- POST /api/agent/run
- POST /api/protocol/mcp
- POST /api/protocol/a2a
- POST /api/protocol/acp
- GET /api/stream/sse
- WS /api/stream/ws

## Service development model

The application uses a layered FastAPI structure. New business services should follow this flow:

1. Define request/response models in `app/model/` or protocol contracts in `protocols/<protocol>/contracts.py`.
2. Implement protocol or business logic in `app/service/` or `protocols/<protocol>/adapter.py`.
3. Expose HTTP routes in `app/handler/`.
4. Export routers from `app/handler/__init__.py`.
5. Mount routers in `app/main.py`, usually controlled by server switches from `app/servers.py`.

Current built-in services:

| Server | Purpose | Route | Implementation entry |
| --- | --- | --- | --- |
| HTTP | Health, agent run, SSE and WebSocket APIs | `/health`, `/api/agent/run`, `/api/stream/*` | `app/handler/*_handler.py` |
| MCP | MCP protocol request handling | `/api/protocol/mcp` | `protocols/mcp/adapter.py` |
| A2A | A2A protocol request handling | `/api/protocol/a2a` | `protocols/a2a/adapter.py` |
| ACP | ACP protocol request handling | `/api/protocol/acp` | `protocols/acp/adapter.py` |

### Protocol service development

MCP, A2A and ACP are implemented as independent protocol servers over the same FastAPI runtime:

- Protocol contracts live in `protocols/<protocol>/contracts.py`.
- Protocol adapters live in `protocols/<protocol>/adapter.py`.
- `app/service/protocol_service.py` dispatches requests to each protocol adapter.
- `app/handler/protocol_handler.py` exposes separate routers for MCP, A2A and ACP.
- `app/main.py` mounts each protocol router only when the corresponding server is enabled.

To add a new protocol service, add a new protocol package under `protocols/`, add a service dispatch method, create a router in `app/handler/`, then add a server definition in `app/servers.py` so it can be enabled and registered independently.

### Server switches

Each server can be enabled or disabled independently. Disabled servers do not mount their routes and are not registered to Nacos.

| Environment variable | Default | Effect |
| --- | --- | --- |
| `HTTP_SERVER_ENABLED` | `true` | Enables HTTP business routes such as agent and stream APIs |
| `MCP_SERVER_ENABLED` | `true` | Enables `/api/protocol/mcp` |
| `A2A_SERVER_ENABLED` | `true` | Enables `/api/protocol/a2a` |
| `ACP_SERVER_ENABLED` | `true` | Enables `/api/protocol/acp` |

## Nacos registration

The FastAPI lifespan automatically registers enabled services to Nacos on startup and deregisters them on shutdown.

Registration flow:

1. `app/lifespan.py` calls `get_nacos_registrations()` during startup.
2. `app/servers.py` returns all server definitions whose server switch and Nacos registration switch are both enabled.
3. `NacosRegistrar.register_services()` registers each server as an independent Nacos service.
4. `NacosClient.register()` sends `POST /nacos/v1/ns/instance` to Nacos.
5. During shutdown, `NacosRegistrar.deregister_services()` deregisters the services in reverse order with `DELETE /nacos/v1/ns/instance`.

Global Nacos configuration:

- `NACOS_ENABLED=true`
- `NACOS_SERVER_ADDR=127.0.0.1:8848`
- `NACOS_SERVICE_NAME=agent-scaffold4py`
- `NACOS_SERVICE_IP=127.0.0.1`
- `APP_PORT=8000`

Set `NACOS_FAIL_FAST=true` if startup should fail when Nacos registration fails.

Each server can also be registered to Nacos independently:

- `NACOS_REGISTER_HTTP_ENABLED=true` registers `NACOS_HTTP_SERVICE_NAME` or `NACOS_SERVICE_NAME`
- `NACOS_REGISTER_MCP_ENABLED=true` registers `NACOS_MCP_SERVICE_NAME` or `{NACOS_SERVICE_NAME}-mcp`
- `NACOS_REGISTER_A2A_ENABLED=true` registers `NACOS_A2A_SERVICE_NAME` or `{NACOS_SERVICE_NAME}-a2a`
- `NACOS_REGISTER_ACP_ENABLED=true` registers `NACOS_ACP_SERVICE_NAME` or `{NACOS_SERVICE_NAME}-acp`

If a server is disabled, its route is not mounted and it is not registered even when the corresponding Nacos registration switch is enabled.

### Nacos service names

Each server is registered as a separate Nacos service. You can override every service name explicitly:

| Server | Service name variable | Default when unset |
| --- | --- | --- |
| HTTP | `NACOS_HTTP_SERVICE_NAME` | `NACOS_SERVICE_NAME` |
| MCP | `NACOS_MCP_SERVICE_NAME` | `{NACOS_SERVICE_NAME}-mcp` |
| A2A | `NACOS_A2A_SERVICE_NAME` | `{NACOS_SERVICE_NAME}-a2a` |
| ACP | `NACOS_ACP_SERVICE_NAME` | `{NACOS_SERVICE_NAME}-acp` |

### Nacos registration metadata

Every registered instance includes common metadata from `NACOS_METADATA` plus generated server metadata:

| Metadata key | Meaning |
| --- | --- |
| `app_name` | Application name from `APP_NAME` |
| `app_version` | Application version from `APP_VERSION` |
| `app_env` | Runtime environment from `APP_ENV` |
| `server_name` | Internal server name, for example `mcp-server` |
| `protocol` | Registered protocol: `http`, `mcp`, `a2a` or `acp` |
| `endpoint` | Main endpoint for this server |
| `routes` | HTTP server route summary, only for the HTTP server |

### Registration examples

Register only the MCP protocol service:

```env
HTTP_SERVER_ENABLED=false
MCP_SERVER_ENABLED=true
A2A_SERVER_ENABLED=false
ACP_SERVER_ENABLED=false

NACOS_ENABLED=true
NACOS_REGISTER_MCP_ENABLED=true
NACOS_MCP_SERVICE_NAME=my-agent-mcp
```

Expose all routes locally, but register only HTTP and ACP to Nacos:

```env
HTTP_SERVER_ENABLED=true
MCP_SERVER_ENABLED=true
A2A_SERVER_ENABLED=true
ACP_SERVER_ENABLED=true

NACOS_REGISTER_HTTP_ENABLED=true
NACOS_REGISTER_MCP_ENABLED=false
NACOS_REGISTER_A2A_ENABLED=false
NACOS_REGISTER_ACP_ENABLED=true
```

Disable all Nacos registration while keeping local routes available:

```env
NACOS_ENABLED=false
```

## Generate project template

```bash
python scripts/create_project.py --project-name my-agent-app --target-dir ./dist/my-agent-app
```
