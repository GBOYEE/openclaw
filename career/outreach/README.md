# Outreach Automation

Simple Python script to send consulting outreach emails to target companies.

## Setup

1. Fill `.env` with your SMTP credentials (see `.env.example`)
2. Edit `target-companies.yaml` to customize list
3. Optionally edit the email template in `send.py` (currently hardcoded)

## Run

```bash
cd career/outreach
cp .env.example .env
# edit .env with real values
python send.py
```

First run will be dry‑run (writes messages to `sent_log/`). Set `OUTREACH_DRY_RUN=0` to actually send.

## Tracking

After sending, fill `materials/outreach-tracker.md` with dates and responses.

---