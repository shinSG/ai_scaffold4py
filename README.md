# Agent Scaffold for Python

[English](README.md) | [简体中文](README.zh-CN.md)

A baseline Agent service scaffold built with FastAPI.

## Features

- FastAPI app with layered structure (src layout)
- Agent orchestration with tools and callbacks
- Service endpoints and adapters for MCP, A2A and ACP
- Optional HTTP, MCP, A2A and ACP servers with independent Nacos registration
- LLM provider abstraction with echo, OpenAI-compatible and Ollama providers
- MQ abstractions for RocketMQ and RabbitMQ
- Streaming endpoints with SSE and WebSocket
- RAG / Prompt / Memory extension points
- Project generation script

## Quick Start

```bash
pip install -e .
cp .env.example .env
uvicorn agent_scaffold.api.main:app --reload --host 0.0.0.0 --port 8000
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

## Project Structure

```text
src/agent_scaffold/           # Main package (src layout)
├── core/                    # Config, exceptions, logging, events
├── agent/                   # Agent abstractions, tools, callbacks, orchestration
│   ├── abstractions/        # BaseAgent, AgentContext
│   ├── agents/              # EchoAgent, LLMAgent
│   ├── tools/               # Tool system (BaseTool, ToolRegistry, builtins)
│   ├── callbacks/           # Callback hooks (BaseCallback, CallbackManager)
│   ├── orchestrator/        # AgentOrchestrator
│   └── registry/            # AgentRegistry
├── protocols/               # MCP, A2A, ACP adapters, contracts, handlers
├── infra/                   # LLM, MQ, Nacos, RAG adapters
├── memory/                  # Session and long-term memory
├── prompts/                 # Prompt registry and loader
├── streaming/               # SSE and WebSocket streaming
└── api/                     # FastAPI application layer
    ├── handlers/            # HTTP route handlers
    ├── models/              # Request/response models
    ├── services/            # Business logic services
    ├── middleware/           # Error handler, request ID
    ├── main.py              # FastAPI app entry point
    ├── servers.py           # Server definitions and switches
    └── lifespan.py          # Startup/shutdown lifecycle
tests/                       # Unit, integration, and contract tests
scripts/                     # Project generation script and templates
```

## Service development model

The application uses a layered FastAPI structure. New business services should follow this flow:

1. Define request/response models in `src/agent_scaffold/api/models/` or protocol contracts in `protocols/<protocol>/contracts.py`.
2. Implement protocol or business logic in `src/agent_scaffold/api/services/` or `protocols/<protocol>/adapter.py`.
3. Expose HTTP routes in `src/agent_scaffold/api/handlers/`.
4. Export routers from `src/agent_scaffold/api/handlers/__init__.py`.
5. Mount routers in `src/agent_scaffold/api/main.py`, usually controlled by server switches from `src/agent_scaffold/api/servers.py`.

## LLM Provider

Agents use `LLM_PROVIDER` to select the model provider. The default is `echo` for local development and tests.

| Environment variable | Default | Effect |
| --- | --- | --- |
| `LLM_PROVIDER` | `echo` | Provider name: `echo`, `openai`, `openai-compatible`, `deepseek`, `qwen`, `dashscope`, `ollama` |
| `LLM_MODEL` | `echo` | Model name |
| `LLM_BASE_URL` | empty | Provider API base URL |
| `LLM_API_KEY` | empty | API key for OpenAI-compatible providers |
| `LLM_TEMPERATURE` | `0.7` | Sampling temperature |
| `LLM_MAX_TOKENS` | `1024` | Maximum output tokens |

## Generate project template

```bash
python scripts/create_project.py --project-name my-agent-app --target-dir ./dist/my-agent-app
```
