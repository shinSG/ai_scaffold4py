# Agent Scaffold for Python

[English](README.md) | [简体中文](README.zh-CN.md)

一个基于 FastAPI 构建的 Agent 服务脚手架。

## 功能特性

- 基于 FastAPI 的分层应用结构
- Agent 编排骨架
- MCP、A2A、ACP 协议服务端点与适配器
- 可选的 HTTP、MCP、A2A、ACP 独立 server，并支持分别向 Nacos 注册
- LLM Provider 抽象，内置 echo、OpenAI 兼容接口和 Ollama
- RocketMQ / RabbitMQ 的 MQ 抽象
- SSE / WebSocket 流式接口
- RAG / Prompt / Memory 扩展点
- 项目生成脚本

## 快速开始

```bash
pip install -r requirements/base.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 完整使用文档

完整脚手架使用说明请查看 [docs/USAGE.md](docs/USAGE.md)，包含服务开发、server 开关、Nacos 注册、流式接口、扩展点、测试与部署说明。

## 接口列表

- GET /health
- POST /api/agent/run
- POST /api/protocol/mcp
- POST /api/protocol/a2a
- POST /api/protocol/acp
- GET /api/stream/sse
- WS /api/stream/ws

## 服务开发模型

应用采用分层结构。新增业务服务建议遵循以下流程：

1. 在 `app/model/` 定义请求/响应模型，或在 `protocols/<protocol>/contracts.py` 定义协议契约。
2. 在 `app/service/` 或 `protocols/<protocol>/adapter.py` 实现业务逻辑。
3. 在 `app/handler/` 暴露 HTTP 路由。
4. 在 `app/handler/__init__.py` 导出 router。
5. 在 `app/main.py` 挂载 router，通常由 `app/servers.py` 中的 server 开关控制。

当前内置服务：

| Server | 用途 | 路径 | 实现入口 |
| --- | --- | --- | --- |
| HTTP | 健康检查、Agent 执行、SSE、WebSocket | `/health`, `/api/agent/run`, `/api/stream/*` | `app/handler/*_handler.py` |
| MCP | MCP 协议请求处理 | `/api/protocol/mcp` | `protocols/mcp/adapter.py` |
| A2A | A2A 协议请求处理 | `/api/protocol/a2a` | `protocols/a2a/adapter.py` |
| ACP | ACP 协议请求处理 | `/api/protocol/acp` | `protocols/acp/adapter.py` |

### 协议服务开发

MCP、A2A、ACP 以独立协议 server 形式运行在同一个 FastAPI 应用内：

- 协议契约位于 `protocols/<protocol>/contracts.py`
- 协议适配器位于 `protocols/<protocol>/adapter.py`
- `app/service/protocol_service.py` 负责分发请求到对应协议 adapter
- `app/handler/protocol_handler.py` 提供 MCP/A2A/ACP 独立 router
- `app/main.py` 仅在对应 server 启用时挂载对应协议 router

新增协议服务建议步骤：

1. 在 `protocols/` 下新增协议目录与 `contracts.py`、`adapter.py`。
2. 在 `app/service/protocol_service.py` 增加分发方法。
3. 在 `app/handler/protocol_handler.py` 增加新协议 router。
4. 在 `app/servers.py` 增加 server 定义，以支持独立开关和注册。

### Server 开关

每个 server 都可以独立启用/禁用。server 禁用后，其路由不会挂载，也不会注册到 Nacos。

| 环境变量 | 默认值 | 作用 |
| --- | --- | --- |
| `HTTP_SERVER_ENABLED` | `true` | 启用 HTTP 业务路由（含 agent / stream） |
| `MCP_SERVER_ENABLED` | `true` | 启用 `/api/protocol/mcp` |
| `A2A_SERVER_ENABLED` | `true` | 启用 `/api/protocol/a2a` |
| `ACP_SERVER_ENABLED` | `true` | 启用 `/api/protocol/acp` |

## Nacos 注册机制

FastAPI 生命周期会在启动时自动注册已启用服务，在关闭时自动注销。

注册流程：

1. `app/lifespan.py` 在启动时调用 `get_nacos_registrations()`。
2. `app/servers.py` 依据 server 开关与 Nacos 注册开关筛选可注册服务。
3. `NacosRegistrar.register_services()` 将每个 server 作为独立 Nacos service 注册。
4. `NacosClient.register()` 调用 `POST /nacos/v1/ns/instance`。
5. 应用关闭时，`NacosRegistrar.deregister_services()` 反向注销服务，调用 `DELETE /nacos/v1/ns/instance`。

全局 Nacos 配置：

- `NACOS_ENABLED=true`
- `NACOS_SERVER_ADDR=127.0.0.1:8848`
- `NACOS_SERVICE_NAME=agent-scaffold4py`
- `NACOS_SERVICE_IP=127.0.0.1`
- `APP_PORT=8000`

如果希望注册失败即启动失败，设置：

- `NACOS_FAIL_FAST=true`

每个 server 可分别控制是否注册：

- `NACOS_REGISTER_HTTP_ENABLED=true` 使用 `NACOS_HTTP_SERVICE_NAME` 或 `NACOS_SERVICE_NAME`
- `NACOS_REGISTER_MCP_ENABLED=true` 使用 `NACOS_MCP_SERVICE_NAME` 或 `{NACOS_SERVICE_NAME}-mcp`
- `NACOS_REGISTER_A2A_ENABLED=true` 使用 `NACOS_A2A_SERVICE_NAME` 或 `{NACOS_SERVICE_NAME}-a2a`
- `NACOS_REGISTER_ACP_ENABLED=true` 使用 `NACOS_ACP_SERVICE_NAME` 或 `{NACOS_SERVICE_NAME}-acp`

当某个 server 被禁用时，即使对应 `NACOS_REGISTER_*_ENABLED=true` 也不会注册。

## LLM Provider

Agent 默认通过 `LLM_PROVIDER` 选择模型提供方。未配置时使用 `echo`，方便本地开发和测试。

| 环境变量 | 默认值 | 作用 |
| --- | --- | --- |
| `LLM_PROVIDER` | `echo` | Provider 名称：`echo`、`openai`、`openai-compatible`、`deepseek`、`qwen`、`dashscope`、`ollama` |
| `LLM_MODEL` | `echo` | 模型名称 |
| `LLM_BASE_URL` | 空 | Provider API 地址，OpenAI 兼容接口默认使用 `https://api.openai.com/v1`，Ollama 默认使用 `http://127.0.0.1:11434` |
| `LLM_API_KEY` | 空 | OpenAI 兼容接口鉴权密钥 |
| `LLM_TIMEOUT_SECONDS` | `30` | 请求超时时间 |
| `LLM_TEMPERATURE` | `0.7` | 采样温度 |
| `LLM_TOP_P` | `1.0` | nucleus sampling 参数 |
| `LLM_TOP_K` | `0` | top-k 采样参数，`0` 表示不传该参数 |
| `LLM_MAX_TOKENS` | `1024` | 最大输出 token 数 |
| `LLM_ENABLE_THINKING` | `false` | 是否向兼容接口传递 `enable_thinking=true` |
| `LLM_SHOW_REASONING` | `false` | 是否在响应中展示 provider 返回的 `reasoning_content` / `reasoning` |

OpenAI 兼容接口示例：

```env
LLM_PROVIDER=openai-compatible
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your-api-key
LLM_TOP_P=0.9
LLM_TOP_K=40
LLM_ENABLE_THINKING=false
LLM_SHOW_REASONING=false
```

Ollama 示例：

```env
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:7b
LLM_BASE_URL=http://127.0.0.1:11434
LLM_TOP_P=0.9
LLM_TOP_K=40
```

调用 `/api/agent/run` 时，可以在 `metadata` 中传入 `system_prompt`，也可以通过 `agent` 指定 `llm` 或 `echo`。

### Nacos 服务名

每个 server 都是独立 Nacos service，可单独配置服务名：

| Server | 服务名变量 | 未设置时默认值 |
| --- | --- | --- |
| HTTP | `NACOS_HTTP_SERVICE_NAME` | `NACOS_SERVICE_NAME` |
| MCP | `NACOS_MCP_SERVICE_NAME` | `{NACOS_SERVICE_NAME}-mcp` |
| A2A | `NACOS_A2A_SERVICE_NAME` | `{NACOS_SERVICE_NAME}-a2a` |
| ACP | `NACOS_ACP_SERVICE_NAME` | `{NACOS_SERVICE_NAME}-acp` |

### Nacos 注册 metadata

每个注册实例包含 `NACOS_METADATA` 的公共信息以及自动生成的 server 元信息：

| 字段 | 含义 |
| --- | --- |
| `app_name` | 来自 `APP_NAME` |
| `app_version` | 来自 `APP_VERSION` |
| `app_env` | 来自 `APP_ENV` |
| `server_name` | server 内部名称，例如 `mcp-server` |
| `protocol` | 协议类型：`http`、`mcp`、`a2a`、`acp` |
| `endpoint` | server 主入口路径 |
| `routes` | HTTP server 路由摘要（仅 HTTP server） |

## 注册示例

仅注册 MCP 服务：

```env
HTTP_SERVER_ENABLED=false
MCP_SERVER_ENABLED=true
A2A_SERVER_ENABLED=false
ACP_SERVER_ENABLED=false

NACOS_ENABLED=true
NACOS_REGISTER_MCP_ENABLED=true
NACOS_MCP_SERVICE_NAME=my-agent-mcp
```

本地启用全部路由，但只向 Nacos 注册 HTTP 与 ACP：

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

关闭 Nacos 注册，但保留本地路由：

```env
NACOS_ENABLED=false
```

## 生成新项目模板

```bash
python scripts/create_project.py --project-name my-agent-app --target-dir ./dist/my-agent-app
```