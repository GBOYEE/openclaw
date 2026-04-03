# 01-02: Fill `.env` with SMTP Credentials

**Epic:** Setup

## Goal

Create `.env` file with Xanderaicorp@gmail.com credentials.

## Steps

1. In `career/outreach/`, run: `cp .env.example .env`
2. Open `.env` in editor
3. Set:
   ```
   SMTP_USER=Xanderaicorp@gmail.com
   SMTP_PASS=the-16-char-app-password
   OUTREACH_FROM=Xanderaicorp@gmail.com
   ```
4. Save

## Acceptance

- `.env` file exists with correct values

## Time

2 minutes
