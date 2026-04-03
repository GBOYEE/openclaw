# Project: OpenClaw Gateway

## Project Reference

- Repository: GBOYEE/openclaw
- Branch: main
- Documentation: README.md, CONFIG.md

## Core Value

OpenClaw provides a secure, scalable gateway for AI agents with unified authentication, rate limiting, and runtime enforcement.

## Target Users

AI operators, autonomous agents, developers building agent systems.

## Requirements

### Functional
- Gateway API with HMAC validation
- Rate limiting per client
- Health check endpoint
- Runtime policy enforcement
- Plugin architecture for skills and products
- Submodule integration with xander-operator

### Non-Functional
- Secure key management
- Low latency (< 100ms for auth)
- High availability
- Observability (logs, metrics)
- Configurable policies

## Constraints

- Must run on Linux with Python 3.11+
- Configuration via environment variables and YAML
- No external database required (SQLite okay for persistence)

## Technical Stack

- Python 3.11, FastAPI
- Nginx for reverse proxy
- Optional: Uvicorn as ASGI server
- Subprocess spawning for agent runtimes

## Dependencies

- xander-operator (submodule at polish/xander-operator)
- Skills directory: `.claude/agents/`, `.claude/commands/`
- Products: `BOUNTY-SYSTEM/`, `products/`

## Interfaces

REST API endpoints:
- `POST /gateway/auth` — HMAC authentication
- `POST /gateway/execute` — execute skill/command
- `GET /health` — health check
- `GET /metrics` — Prometheus metrics (TODO)

## Acceptance Criteria

- All API endpoints return proper JSON with status codes
- Authentication fails with 401 on invalid HMAC
- Rate limiting returns 429 when exceeded
- Health endpoint returns 200 OK when gateway is healthy
- Submodule xander-operator loads and executes correctly

---

*Last updated: 2026-03-29*