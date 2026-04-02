# OpenClaw Gateway — Production Guide

Production deployment, observability, and safety guidelines for the OpenClaw Gateway service.

---

## Architecture Overview

The Gateway is a FastAPI application that provides:

- **HTTP API** — robust endpoints for task creation, event retrieval, approvals
- **Orchestrator** — explicit plan → execute → observe cycle
- **State persistence** — PostgreSQL for audit trail (events, approvals, decisions)
- **Safety layer** — tool permissions, risk-based auto/approval/block
- **Observability** — structured JSON logs, `/metrics`, request IDs

The system is designed for controlled autonomy: AI can suggest and execute low-risk actions, but medium/high-risk actions require explicit human approval.

---

## Deployment

### Docker Compose (recommended)

```bash
cd polish/openclaw
docker-compose up -d
```

Services:

| Service | Port | Description |
|---------|------|-------------|
| `gateway` | 8080 | FastAPI application |
| `postgres` | 5432 | PostgreSQL database |

Data volumes:

- `postgres_data` — persisted DB data
- `./logs` — host logs directory mounted into container for persistence

Environment variables can be set in `.env` or directly in `docker-compose.yml`.

---

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCLAW_ENV` | `production` | `development` enables auto-reload |
| `OPENCLAW_PORT` | `8080` | HTTP port |
| `OPENCLAW_SECRET` | `change-me` | HMAC secret for webhook verification |
| `OPENCLAW_DATABASE_URL` | `sqlite:///openclaw.db` | PostgreSQL URL recommended |
| `OPENCLAW_PERMISSIONS` | `polish/openclaw/config/permissions.yaml` | Path to YAML permissions |
| `OPENCLAW_LOG_LEVEL` | `INFO` | Logging level |
| `OPENCLAW_LOG_FORMAT` | `json` | `json` or `text` |
| `OPENCLAW_RATE_LIMIT` | `60` | Requests per minute per IP |
| `OPENCLAW_ENABLE_APPROVAL` | `true` | Enable approval workflow for medium/high risk tools |

---

## Observability

### Health Check

`GET /health` returns:

```json
{
  "status": "ok",
  "timestamp": 1712101234.567,
  "version": "1.2.0",
  "environment": "production",
  "database": "connected"
}
```

### Metrics

`GET /metrics` returns JSON counters:

```json
{
  "requests_total": 1234,
  "requests_failed": 5,
  "rate_limited": 2,
  "webhooks_received": 10,
  "tasks_received": 100,
  "tasks_planned": 100,
  "tasks_executed": 95,
  "tasks_succeeded": 90,
  "tasks_failed": 5,
  "approvals_requested": 3,
  "approvals_granted": 2,
  "approvals_rejected": 1
}
```

### Logs

Logs are JSON lines if `OPENCLAW_LOG_FORMAT=json`. They include fields:

- `timestamp`
- `level`
- `name` (logger name)
- `message`
- `request_id` (for HTTP requests)
- `task_id` (when within a task lifecycle)

Log files are written to `logs/` (if directory mounted).

---

## Safety & Permissions

Edit `config/permissions.yaml` to adjust tool policies. Example:

```yaml
tools:
  shell:
    risk: high
    require_approval: true
    allowed_roles: [admin]
    allowed_commands: ["ls", "cat", "pwd", "systemctl"]
  file_write:
    risk: medium
    require_approval: true
    allowed_roles: [admin, operator]
  disk_clean:
    risk: low
    auto_execute: true
    allowed_roles: [admin, operator]
```

After changing the file, restart the gateway (or mount read-only to prevent runtime changes).

---

## Approval Workflow

When an agent attempts a medium/high-risk action:

1. Action is blocked, an `Approval` record is created in PostgreSQL with status `pending`
2. The orchestrator returns a response with `status: awaiting_approval` and an `approval_id`
3. Human operator reviews via dashboard or API:
   - `POST /approvals/{id}/approve` with header `X-User-ID: alice`
   - `POST /approvals/{id}/reject` with header `X-User-ID: alice`
4. Approved actions are executed automatically by the next cycle (or via webhook trigger).
5. All decisions are logged in `events` table.

---

## Database Schema

The gateway uses SQLAlchemy ORM. Tables:

- **events** — every lifecycle event (task_received, planned, executed, approval_*)
- **approvals** — pending and completed approvals
- **decisions** — AI decisions (future)
- **audit_logs** — administrative actions (future)

For production, use PostgreSQL. SQLite fallback is for development only.

To initialize:

```bash
# If using Docker Compose, DB is auto-initialized.
# For manual PostgreSQL:
createdb openclaw -U postgres
psql openclaw -c "CREATE USER openclaw WITH PASSWORD 'openclaw'; GRANT ALL PRIVILEGES ON DATABASE openclaw TO openclaw;"
```

---

## Monitoring & Alerts

Use any of these methods:

- **Prometheus** — scrape `/metrics` endpoint (convert counters to Prometheus format)
- **Cron health check** — `curl -f http://localhost:8080/health || echo 'OpenClaw down' | mail admin@example.com`
- **Log monitoring** — watch for `"level": "error"` events
- **Approval backlog** — alert if `GET /approvals/pending` returns > N items

---

## Backup & Restore

PostgreSQL backups:

```bash
# Backup
docker exec openclaw-pg pg_dump -U openclaw openclaw > backup_$(date +%F).sql

# Restore
cat backup_2026-04-02.sql | docker exec -i openclaw-pg psql -U openclaw openclaw
```

Also back up `logs/` directory if you need historical JSON logs.

---

## Upgrading

1. Pull latest code
2. Rebuild and restart: `docker-compose pull && docker-compose up -d --force-recreate`
3. Run migrations if needed (currently schema is auto-created on startup)

---

## Security Considerations

- Change `OPENCLAW_SECRET` to a strong random value in production
- Use network policies to restrict gateway access to trusted IPs
- Enable TLS (terminate at reverse proxy like nginx)
- Limit `allowed_commands` in `permissions.yaml` to safe subset
- Keep PostgreSQL behind firewall; use strong passwords

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|----------|--------------|-----|
| 500 errors, DB connection refused | PostgreSQL not running | `docker-compose up postgres` |
| High approval backlog | Too many high-risk tool calls | Review agent prompts, reduce tool usage |
| Metrics not updating | Wrong DB URL / permissions | Check `OPENCLAW_DATABASE_URL` and ORM init |
| Container crashes on start | Missing `config/permissions.yaml` | Ensure file exists or path configured |

---

## Next Steps

- Add a Streamlit dashboard for approvals and real-time logs ([docs](docs/dashboard.md))
- Integrate with Slack for approval notifications
- Implement AI model router with cost tracking
- Add support for OAuth2 authentication on API

---

*Built with GSD. Production-grade from day one.*
