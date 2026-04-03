# 04-02: Build Multi-Tenant Architecture

**Epic**: Productization

## Goal

Adapt automation-engine (or agent-core) to serve multiple customers with isolation and usage tracking.

## Acceptance Criteria

- Tenants have isolated configs, schedules, webhook endpoints
- Database schema: tenants, tasks, usage (rows inserted), API keys per tenant
- Middleware in FastAPI to identify tenant via API key
- Admin panel (simple) to view per-tenant metrics
- Logging structured with tenant_id

## Tasks

1. Design data model (SQLite → PostgreSQL maybe later)
2. Implement tenant-aware config loader (loads from /data/tenants/{id}/config.yaml)
3. Add API key authentication (HS256)
4. Modify runner/scheduler to operate within tenant context
5. Implement usage counter (tasks executed per month)

## Dependencies

04-01

## Time Estimate

20 hours
