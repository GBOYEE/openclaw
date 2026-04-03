# 01-02: Build Alert Generator

**Epic:** Data Ingestion & Alerts

## Goal

Create automation‑engine tasks that analyze data and produce SMS alerts.

## Acceptance

- Task: `check_irrigation` — if soil moisture < threshold + no rain forecast → send alert
- Task: `pest_risk` — if humidity + temperature in pest range → alert
- Task: `frost_warning` — if min temp near freezing → protect crops
- Alerts stored in DB with status (pending, sent, read)
- Mock SMS logging (later Twilio)

## Tasks

1. Write Python modules for each alert rule (pure functions)
2. Configure automation‑engine YAML with these tasks, daily schedule
3. Implement `send_sms(phone, message)` placeholder (log to file)
4. Add deduplication (don't spam same farmer)
5. Test with synthetic data

## Dependencies

01-01

## Time

6 hours
