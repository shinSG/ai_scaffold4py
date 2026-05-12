# Agent Scaffold for Python 使用说明

本文档说明如何使用本脚手架开发、运行、配置和扩展一个 Agent 服务，包括 HTTP/MCP/A2A/ACP 服务开发方式、Nacos 注册机制、流式接口、项目生成和测试流程。

## 1. 脚手架定位

本项目是一个基于 FastAPI 的 Python Agent 服务脚手架，提供以下基础能力：

- FastAPI Web 服务结构
- Agent 编排骨架
- HTTP 业务接口
- MCP/A2A/ACP 协议服务接口
- SSE/WebSocket 流式输出
- Nacos 服务注册、注销和发现抽象
- MQ 抽象，预留 RabbitMQ/RocketMQ 扩展点
- LLM Provider 抽象，内置 echo、OpenAI 兼容接口和 Ollama
- RAG、Prompt、Memory 扩展点
- 项目生成脚本
- 单元测试与集成测试结构

## 2. 目录结构说明

```text
agent/                  Agent 抽象、注册与编排
app/                    FastAPI 应用层
  handler/              HTTP Router / Handler
  service/              应用服务层
  model/                API 请求响应模型
  middleware/           中间件
  lifespan.py           应用启动/关闭生命周期
  main.py               FastAPI 应用入口
  servers.py            HTTP/MCP/A2A/ACP server 定义与开关
core/                   配置、异常、日志、容器等核心模块
integrations/           外部集成
  nacos/                Nacos 注册、注销、发现
  mq/                   MQ 抽象与实现占位
  rag/                  RAG 抽象与实现占位
memory/                 会话记忆和长期记忆占位
prompts/                Prompt 加载和注册
protocols/              MCP/A2A/ACP 协议契约与 adapter
streaming/              SSE/WebSocket 流式能力
tests/                  测试目录
scripts/                项目生成脚本与模板
requirements/           分环境依赖
```

## 3. 环境准备

建议使用 Python 3.11+。

安装基础依赖：

```bash
pip install -r requirements/base.txt
```

安装测试依赖：

```bash
pip install -r requirements/test.txt
```

安装开发依赖：

```bash
pip install -r requirements/dev.txt
```

复制环境变量文件：

```bash
cp .env.example .env
```

## 4. 启动服务

开发模式启动：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问健康检查：

```bash
curl http://127.0.0.1:8000/health
```

默认端口由 `APP_PORT` 控制，但实际启动端口仍以 `uvicorn --port` 为准。建议两者保持一致，便于 Nacos 注册正确端口。

## 5. 内置接口

| 类型 | 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| HTTP | GET | `/health` | 健康检查 |
| HTTP | POST | `/api/agent/run` | Agent 执行入口 |
| MCP | POST | `/api/protocol/mcp` | MCP 协议服务入口 |
| A2A | POST | `/api/protocol/a2a` | A2A 协议服务入口 |
| ACP | POST | `/api/protocol/acp` | ACP 协议服务入口 |
| Stream | GET | `/api/stream/sse` | SSE 流式接口 |
| Stream | WS | `/api/stream/ws` | WebSocket 流式接口 |

## 6. 服务开发方式

本脚手架采用分层开发模式：

```text
请求 -> Handler -> Service -> Adapter / Orchestrator -> Response
```

### 6.1 新增 HTTP 业务接口

推荐步骤：

1. 在 `app/model/` 定义请求和响应模型。
2. 在 `app/service/` 实现业务逻辑。
3. 在 `app/handler/` 创建路由。
4. 在 `app/handler/__init__.py` 导出 router。
5. 在 `app/main.py` 挂载 router。

示例开发路径：

```text
app/model/example.py
app/service/example_service.py
app/handler/example_handler.py
```

### 6.2 新增协议服务

MCP/A2A/ACP 都按协议包开发：

```text
protocols/<protocol>/contracts.py   协议请求/响应模型
protocols/<protocol>/adapter.py     协议适配与处理逻辑
```

当前已有：

```text
protocols/mcp/
protocols/a2a/
protocols/acp/
```

协议请求由 `app/service/protocol_service.py` 分发到对应 adapter，再由 `app/handler/protocol_handler.py` 暴露为 FastAPI 路由。

新增协议时，需要同时：

1. 新增 `protocols/<new_protocol>/contracts.py`。
2. 新增 `protocols/<new_protocol>/adapter.py`。
3. 在 `app/service/protocol_service.py` 增加分发方法。
4. 在 `app/handler/protocol_handler.py` 增加 router。
5. 在 `app/servers.py` 增加 server 定义。
6. 在 `app/main.py` 根据开关挂载 router。

## 7. Server 开关机制

当前 HTTP/MCP/A2A/ACP 都被建模为独立 server，定义在 `app/servers.py`。

每个 server 都有两个层面的开关：

1. 是否启用服务本身。
2. 是否向 Nacos 注册。

### 7.1 服务启用开关

| 环境变量 | 默认值 | 作用 |
| --- | --- | --- |
| `HTTP_SERVER_ENABLED` | `true` | 启用 HTTP 业务接口和流式接口 |
| `MCP_SERVER_ENABLED` | `true` | 启用 MCP 路由 `/api/protocol/mcp` |
| `A2A_SERVER_ENABLED` | `true` | 启用 A2A 路由 `/api/protocol/a2a` |
| `ACP_SERVER_ENABLED` | `true` | 启用 ACP 路由 `/api/protocol/acp` |

服务关闭后：

- 对应路由不会挂载。
- 对应服务不会注册到 Nacos。
- 即使对应 `NACOS_REGISTER_*_ENABLED=true`，也不会注册。

### 7.2 Nacos 注册开关

| 环境变量 | 默认值 | 作用 |
| --- | --- | --- |
| `NACOS_REGISTER_HTTP_ENABLED` | `true` | 注册 HTTP server |
| `NACOS_REGISTER_MCP_ENABLED` | `true` | 注册 MCP server |
| `NACOS_REGISTER_A2A_ENABLED` | `true` | 注册 A2A server |
| `NACOS_REGISTER_ACP_ENABLED` | `true` | 注册 ACP server |

这些开关只控制是否注册到 Nacos，不影响本地路由是否挂载。

## 8. Nacos 注册机制

### 8.1 注册流程

应用启动时：

1. FastAPI 执行 `app/lifespan.py` 中的 `app_lifespan()`。
2. `get_nacos_registrations()` 从 `app/servers.py` 获取需要注册的 server。
3. 只有同时满足以下条件的 server 才会进入注册列表：
   - server 自身启用。
   - 对应 Nacos 注册开关启用。
4. `NacosRegistrar.register_services()` 逐个注册服务。
5. `NacosClient.register()` 调用 Nacos OpenAPI：`POST /nacos/v1/ns/instance`。

应用关闭时：

1. `NacosRegistrar.deregister_services()` 按注册列表反向注销。
2. `NacosClient.deregister()` 调用 Nacos OpenAPI：`DELETE /nacos/v1/ns/instance`。

### 8.2 全局 Nacos 配置

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| `NACOS_ENABLED` | `true` | 是否启用 Nacos 集成 |
| `NACOS_SERVER_ADDR` | `127.0.0.1:8848` | Nacos 地址 |
| `NACOS_NAMESPACE` | `public` | Nacos namespace |
| `NACOS_GROUP` | `DEFAULT_GROUP` | Nacos group |
| `NACOS_SERVICE_NAME` | `agent-scaffold4py` | 基础服务名 |
| `NACOS_SERVICE_IP` | `127.0.0.1` | 注册到 Nacos 的实例 IP |
| `NACOS_CLUSTER_NAME` | `DEFAULT` | Nacos cluster |
| `NACOS_WEIGHT` | `1.0` | 实例权重 |
| `NACOS_EPHEMERAL` | `true` | 是否临时实例 |
| `NACOS_TIMEOUT_SECONDS` | `2.0` | Nacos 请求超时时间 |
| `NACOS_FAIL_FAST` | `false` | 注册失败时是否中断应用启动 |
| `NACOS_METADATA` | `{}` | 追加到所有注册实例的 metadata |

`NACOS_ENABLED=false` 时，不执行注册、注销和发现请求。

### 8.3 独立服务名

每个 server 会作为独立 Nacos service 注册。

| Server | serviceName 配置 | 未配置时默认值 |
| --- | --- | --- |
| HTTP | `NACOS_HTTP_SERVICE_NAME` | `NACOS_SERVICE_NAME` |
| MCP | `NACOS_MCP_SERVICE_NAME` | `{NACOS_SERVICE_NAME}-mcp` |
| A2A | `NACOS_A2A_SERVICE_NAME` | `{NACOS_SERVICE_NAME}-a2a` |
| ACP | `NACOS_ACP_SERVICE_NAME` | `{NACOS_SERVICE_NAME}-acp` |

### 8.4 注册 metadata

每个实例注册时会写入 metadata。公共字段包括：

| 字段 | 说明 |
| --- | --- |
| `app_name` | 应用名称 |
| `app_version` | 应用版本 |
| `app_env` | 运行环境 |
| `server_name` | server 内部名称 |
| `protocol` | 协议类型：`http`、`mcp`、`a2a`、`acp` |
| `endpoint` | server 主入口路径 |
| `routes` | HTTP server 的路由摘要 |

`NACOS_METADATA` 中的字段会合并进 metadata。

## 9. 常见配置场景

### 9.1 只启动 HTTP 服务，不注册 Nacos

```env
HTTP_SERVER_ENABLED=true
MCP_SERVER_ENABLED=false
A2A_SERVER_ENABLED=false
ACP_SERVER_ENABLED=false

NACOS_ENABLED=false
```

### 9.2 启动全部服务，但只注册 MCP

```env
HTTP_SERVER_ENABLED=true
MCP_SERVER_ENABLED=true
A2A_SERVER_ENABLED=true
ACP_SERVER_ENABLED=true

NACOS_ENABLED=true
NACOS_REGISTER_HTTP_ENABLED=false
NACOS_REGISTER_MCP_ENABLED=true
NACOS_REGISTER_A2A_ENABLED=false
NACOS_REGISTER_ACP_ENABLED=false
NACOS_MCP_SERVICE_NAME=my-agent-mcp
```

### 9.3 只启动和注册 ACP

```env
HTTP_SERVER_ENABLED=false
MCP_SERVER_ENABLED=false
A2A_SERVER_ENABLED=false
ACP_SERVER_ENABLED=true

NACOS_ENABLED=true
NACOS_REGISTER_ACP_ENABLED=true
NACOS_ACP_SERVICE_NAME=my-agent-acp
```

### 9.4 启动全部服务并全部注册

```env
HTTP_SERVER_ENABLED=true
MCP_SERVER_ENABLED=true
A2A_SERVER_ENABLED=true
ACP_SERVER_ENABLED=true

NACOS_ENABLED=true
NACOS_REGISTER_HTTP_ENABLED=true
NACOS_REGISTER_MCP_ENABLED=true
NACOS_REGISTER_A2A_ENABLED=true
NACOS_REGISTER_ACP_ENABLED=true
```

## 10. Agent 开发方式

Agent 执行入口是：

```text
POST /api/agent/run
```

调用链：

```text
app/handler/agent_handler.py
-> app/service/agent_service.py
-> agent/orchestrator/agent_orchestrator.py
```

推荐扩展方式：

1. 在 `agent/abstractions/base_agent.py` 基于抽象定义 Agent 能力。
2. 在 `agent/registry/agent_registry.py` 注册具体 Agent。
3. 在 `agent/orchestrator/agent_orchestrator.py` 编排 Agent 执行流程。
4. 在 `app/model/agent.py` 扩展请求和响应字段。

## 11. 流式服务开发

脚手架提供两类流式接口：

- SSE：`GET /api/stream/sse`
- WebSocket：`WS /api/stream/ws`

调用链：

```text
app/handler/stream_handler.py
-> app/service/stream_service.py
-> streaming/sse/emitter.py
-> streaming/websocket/connection_manager.py
```

适合用于：

- Agent token 流式输出
- 长任务进度推送
- 多 Agent 协作过程事件推送

## 12. Prompt、Memory、RAG 扩展

### 12.1 Prompt

Prompt 模板目录：

```text
prompts/templates/
```

加载和注册逻辑：

```text
prompts/loader.py
prompts/registry.py
```

### 12.2 Memory

记忆模块位置：

```text
memory/session_memory.py
memory/long_term_memory.py
memory/store.py
```

可用于接入 Redis、数据库或向量存储。

### 12.3 RAG

RAG 抽象和 stub：

```text
integrations/rag/ports.py
integrations/rag/retriever_stub.py
integrations/rag/adapter.py
```

可替换为真实向量库、知识库或检索服务。

### 12.4 LLM Provider

LLM 抽象位于：

```text
integrations/llm/ports.py
integrations/llm/factory.py
integrations/llm/echo_provider.py
integrations/llm/openai_compatible_provider.py
integrations/llm/ollama_provider.py
```

默认 agent 使用 `LLM_PROVIDER` 创建 provider。未配置时使用 `echo`，不会请求外部服务。

支持的 provider：

- `echo`：本地回显，用于开发和测试。
- `openai` / `openai-compatible` / `qwen` / `dashscope`：调用 OpenAI Chat Completions 兼容接口。
- `deepseek`：默认 base URL 为 `https://api.deepseek.com/v1`。
- `ollama`：调用本地 Ollama `/api/generate`。

通用配置：

```env
LLM_PROVIDER=echo
LLM_MODEL=echo
LLM_BASE_URL=
LLM_API_KEY=
LLM_TIMEOUT_SECONDS=30
LLM_TEMPERATURE=0.7
LLM_TOP_P=1.0
LLM_TOP_K=0
LLM_MAX_TOKENS=1024
LLM_ENABLE_THINKING=false
LLM_SHOW_REASONING=false
```

参数说明：

- `LLM_TOP_P` 会传给 OpenAI 兼容接口和 Ollama。
- `LLM_TOP_K` 大于 `0` 时才会传给 provider；标准 OpenAI 接口不支持时可保持 `0`。
- `LLM_ENABLE_THINKING=true` 时会向 OpenAI 兼容接口传递 `enable_thinking=true`，适用于支持该字段的模型服务。
- `LLM_SHOW_REASONING=true` 时，如果 provider 返回 `reasoning_content` 或 `reasoning`，响应会包含该内容；默认关闭。

OpenAI 兼容接口示例：

```env
LLM_PROVIDER=openai-compatible
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your-api-key
LLM_TOP_P=0.9
LLM_TOP_K=0
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

调用 `/api/agent/run` 时，可通过 `metadata` 控制 agent 和 system prompt：

```json
{
  "session_id": "demo",
  "user_input": "你好",
  "metadata": {
    "agent": "llm",
    "system_prompt": "你是一个简洁的助手"
  }
}
```

## 13. MQ 扩展

MQ 抽象位于：

```text
integrations/mq/ports.py
integrations/mq/factory.py
```

当前预留实现目录：

```text
integrations/mq/rabbitmq/
integrations/mq/rocketmq/
```

通过环境变量选择后端：

```env
MQ_BACKEND=rabbitmq
RABBITMQ_URL=amqp://guest:guest@127.0.0.1:5672/
ROCKETMQ_NAMESRV_ADDR=127.0.0.1:9876
```

## 14. 生成新项目

脚手架提供项目生成脚本：

```bash
python scripts/create_project.py --project-name my-agent-app --target-dir ./dist/my-agent-app
```

强制覆盖目标目录：

```bash
python scripts/create_project.py --project-name my-agent-app --target-dir ./dist/my-agent-app --force
```

预览生成内容：

```bash
python scripts/create_project.py --project-name my-agent-app --target-dir ./dist/my-agent-app --dry-run
```

模板目录：

```text
scripts/templates/project/
```

## 15. 测试

运行全部测试：

```bash
pytest -q
```

当前测试覆盖：

- 协议 adapter 合约测试
- protocol service 分发测试
- Nacos client 参数构造测试
- Nacos registrar 批量注册注销测试
- server 开关和注册筛选测试
- streaming 集成测试
- config 基础测试

## 16. 代码检查

如果安装了开发依赖，可以运行：

```bash
ruff check .
black .
mypy .
```

也可以先做 Python 语法编译检查：

```bash
python -m compileall app core integrations protocols tests
```

## 17. 推荐开发流程

1. 从 `.env.example` 复制 `.env`。
2. 根据需要启用或关闭 HTTP/MCP/A2A/ACP server。
3. 根据部署环境配置 Nacos。
4. 在 `app/model/` 定义业务模型。
5. 在 `app/service/` 实现业务逻辑。
6. 在 `app/handler/` 暴露接口。
7. 如果是协议能力，在 `protocols/` 中实现契约和 adapter。
8. 如需服务发现，在 `app/servers.py` 中补充 server 定义和 metadata。
9. 增加测试。
10. 运行 `pytest -q` 验证。

## 18. 部署注意事项

- `APP_PORT` 应与实际启动端口一致，否则 Nacos 注册端口可能不正确。
- `NACOS_SERVICE_IP` 应设置为其他服务可访问的地址，不建议生产环境使用 `127.0.0.1`。
- 如果应用绑定 `0.0.0.0` 且未设置 `NACOS_SERVICE_IP`，注册逻辑会回退为 `127.0.0.1`。
- 生产环境建议设置明确的 `NACOS_HTTP_SERVICE_NAME`、`NACOS_MCP_SERVICE_NAME`、`NACOS_A2A_SERVICE_NAME`、`NACOS_ACP_SERVICE_NAME`。
- 如果希望 Nacos 注册失败时阻止应用启动，设置 `NACOS_FAIL_FAST=true`。
- 如果只做本地开发，可以设置 `NACOS_ENABLED=false`。

## 19. 快速排查

### 路由不存在

检查对应 server 是否开启：

```env
MCP_SERVER_ENABLED=true
A2A_SERVER_ENABLED=true
ACP_SERVER_ENABLED=true
```

### 服务没有注册到 Nacos

依次检查：

1. `NACOS_ENABLED=true`
2. 对应 server 是否启用。
3. 对应 `NACOS_REGISTER_*_ENABLED=true`。
4. `NACOS_SERVER_ADDR` 是否可访问。
5. `NACOS_SERVICE_IP` 和 `APP_PORT` 是否正确。

### 注册成功但调用不到服务

通常是实例地址或端口不可访问。检查：

- `NACOS_SERVICE_IP`
- `APP_PORT`
- `uvicorn --host`
- `uvicorn --port`
- 防火墙或容器端口映射

## 20. 最小可用配置

本地开发最小配置：

```env
APP_NAME=agent-scaffold4py
APP_HOST=0.0.0.0
APP_PORT=8000

HTTP_SERVER_ENABLED=true
MCP_SERVER_ENABLED=true
A2A_SERVER_ENABLED=true
ACP_SERVER_ENABLED=true

NACOS_ENABLED=false
```

生产注册示例：

```env
APP_NAME=agent-scaffold4py
APP_ENV=prod
APP_HOST=0.0.0.0
APP_PORT=8000

NACOS_ENABLED=true
NACOS_SERVER_ADDR=nacos.example.com:8848
NACOS_NAMESPACE=public
NACOS_GROUP=DEFAULT_GROUP
NACOS_SERVICE_IP=10.0.1.23
NACOS_FAIL_FAST=true

NACOS_HTTP_SERVICE_NAME=agent-scaffold4py
NACOS_MCP_SERVICE_NAME=agent-scaffold4py-mcp
NACOS_A2A_SERVICE_NAME=agent-scaffold4py-a2a
NACOS_ACP_SERVICE_NAME=agent-scaffold4py-acp
```