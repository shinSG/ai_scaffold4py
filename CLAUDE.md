# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Scaffold for Python — a FastAPI-based baseline for building agent services with multi-protocol support (HTTP, MCP, A2A, ACP), Nacos service registration, LLM provider abstraction, and streaming endpoints (SSE/WebSocket). Uses src layout with `agent_scaffold` as the main package.

## Commands

```bash
# Install in editable mode
pip install -e .

# Run the server
uvicorn agent_scaffold.api.main:app --reload --host 0.0.0.0 --port 8000

# Run all tests
pytest

# Run a single test file
pytest tests/unit/test_config.py

# Lint and format
ruff check .
black .
mypy .
```

## Architecture

**Layered structure** — `core/` → `agent/` → `protocols/` → `infra/` → `api/`

All source lives under `src/agent_scaffold/`:

- **core/**: Cross-cutting — config (pydantic-settings from `.env`), logging, exceptions, events bus
- **agent/**: Agent orchestration and capabilities
  - `abstractions/`: `BaseAgent` ABC, `AgentContext`
  - `agents/`: Built-in agent implementations (`EchoAgent`, `LLMAgent`)
  - `tools/`: Tool system — `BaseTool` ABC, `ToolRegistry`, built-in tools (echo, http)
  - `callbacks/`: Callback hooks — `BaseCallback` ABC, `CallbackManager`, `LoggingCallback`
  - `orchestrator/`: `AgentOrchestrator` dispatches requests to agents
  - `registry/`: `AgentRegistry` maps agent names to instances
- **protocols/**: MCP, A2A, ACP — each with `adapter.py`, `contracts.py`, `handler.py`
  - `base.py`: `ProtocolAdapter` ABC
- **infra/**: Infrastructure adapters
  - `llm/`: LLM provider abstraction (`ports.py` = ABC, `factory.py` = factory). Built-in: echo, openai-compatible, ollama
  - `embedding/`: Embedding provider abstraction. Built-in: local (hash-based), OpenAI-compatible
  - `vectorstore/`: Vector store abstraction. Built-in: in-memory (cosine similarity), Chroma
  - `loader/`: Document loader abstraction. Built-in: text, PDF (pypdf), web (BeautifulSoup)
  - `cache/`: Cache abstraction. Built-in: in-memory (with TTL), Redis
  - `db/`: Database ORM abstraction (SQLAlchemy async). Built-in: SQLite (aiosqlite). Includes `BaseModel` with UUID PK + timestamps, `SQLAlchemyRepository` for generic CRUD
  - `nacos/`: Nacos client, registrar, discovery
  - `mq/`: RocketMQ and RabbitMQ abstractions
  - `rag/`: RAG adapter (integrates embedding + vector store)
- **memory/**: Session and long-term memory stores
- **streaming/**: SSE/WebSocket event streaming
- **prompts/**: Prompt registry and loader
- **api/**: FastAPI application layer
  - `main.py`: Creates app, mounts routers conditionally based on server switches
  - `servers.py`: `ServerDefinition` for each protocol; controls enablement and Nacos registration
  - `handlers/`: Route handlers (health, agent, stream, protocol)
  - `models/`: Pydantic request/response models (merged from old model/ and schemas/)
  - `services/`: Business logic (protocol dispatch, health, agent, stream)
  - `middleware/`: Request ID injection, error handling
  - `lifespan.py`: Startup/shutdown hooks including Nacos registration/deregistration

## Key Patterns

**Server switches**: Each protocol server (HTTP/MCP/A2A/ACP) can be independently enabled/disabled via env vars (`HTTP_SERVER_ENABLED`, `MCP_SERVER_ENABLED`, etc.). Disabled servers don't mount routes or register to Nacos.

**LLM provider factory**: `infra/llm/factory.py` creates providers based on `LLM_PROVIDER` env var. Default is `echo` (local dev). Supports `openai`, `openai-compatible`, `deepseek`, `qwen`, `dashscope`, `ollama`.

**Tool system**: Implement `BaseTool` in `agent/tools/`, register in `ToolRegistry`. Built-in tools in `agent/tools/builtins/`.

**Callback hooks**: Implement `BaseCallback` in `agent/callbacks/`, add to `CallbackManager` for lifecycle events (agent start/end, tool start/end, LLM start/end, errors).

**Adding a new protocol**: Add a package under `protocols/` with `adapter.py` + `contracts.py` + `handler.py`, add a server definition in `api/servers.py`, and mount the router in `api/main.py`.

**Adding a new agent**: Implement `BaseAgent` in `agent/abstractions/`, create the agent class in `agent/agents/`, register in `AgentRegistry`, and select via `metadata.agent` in the run request.

## Testing

Tests live under `tests/` with subdirectories `unit/`, `integration/`, and `contract/`. The `conftest.py` inserts `src/` into `sys.path` and provides a `client` fixture wrapping `TestClient(app)`.

## Configuration

All settings come from environment variables or `.env` file via pydantic-settings (`core/config.py`). Copy `.env.example` to `.env` before running. The settings object is cached via `@lru_cache`.
