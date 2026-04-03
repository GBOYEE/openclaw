# 05-04: Managed Hosting Service

**Epic**: Passive Scale

## Goal

Offer "Automation-as-a-Service" where we host, monitor, and maintain automation-engine for clients ($299/mo).

## Acceptance Criteria

- Service page on site: "We run your automation. 99.9% uptime, alerts, support."
- Onboarding process: client provides config, we deploy to managed tenant
- Monitoring: health checks, log aggregation, backups
- Billing via Stripe subscriptions
- 5 managed customers within 6 months

## Tasks

1. Define scope: uptime SLA, support hours, config changes included
2. Build internal hosting platform (Docker Compose + Traefik + monitoring)
3. Create customer portal to view task runs, logs, metrics
4. Set up alerts (PagerDuty/Slack) for incidents
5. Pricing, TOS, privacy policy
6. Outreach to existing consulting clients → convert to retainer

## Dependencies

04-02, 04-03 (multi-tenancy + billing)

## Time Estimate

16 hours setup + ongoing ops
