# 01-03: Integrate Twilio SMS & Localization

**Epic:** Data Ingestion & Alerts

## Goal

Send real SMS to farmers in their language using Twilio.

## Acceptance

- Twilio account with phone number (buy number for Nigeria/Kenya)
- `send_sms(phone, message)` uses Twilio REST API
- L10n: message templates in Hausa, Swahili, Bengali (select based on farmer pref)
- Opt‑out handling (STOP keyword)
- Delivery status callbacks logged

## Tasks

1. Sign up Twilio; enable SMS; get ACCOUNT_SID, AUTH_TOKEN
2. Write Twilio client wrapper; handle errors (rate limits, invalid numbers)
3. Create translation files `locales/{lang}.yaml` with message templates
4. Add farmer profile table with `language` field
5. Test sending to personal phone (sandbox mode if available)

## Dependencies

01-02

## Time

6 hours
