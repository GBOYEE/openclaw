# 04-01: Choose MVP Product — Decision

**Chosen MVP:** automation-engine SaaS

**Rationale:**
- Clear market need: small businesses/indie hackers want reliable task scheduling + webhooks without managing servers.
- Mature codebase: automation-engine already v1.0.0 with security, retries, metrics, dashboard.
- Easy to multi‑tenant: config files are per-tenant; runners are stateless.
- Pricing: $29/mo (Basic: 100 tasks/mo), $99/mo (Pro: 1000 tasks + alerts), $299/mo (Business: custom).
- Competition: n8n, Zapier, cron-job.org — but we offer tighter control, cheaper, self‑hostable option.
- Leverages existing assets; minimal new code (just multitenancy + billing).

**Alternatives considered:**
- agent-core Cloud API: more abstract, harder to sell to non‑technical.
- trading-lab SaaS: niche (traders), regulatory considerations.
- claw-ui NPM package: smaller market.

**Decision:** Build automation-engine SaaS first. Target launch in 8 weeks (Month 4 of GSD plan).

**Next:** 04-02 Build multi‑tenant architecture.
