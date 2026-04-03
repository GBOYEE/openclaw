# 01-03: Verify Dry Run

**Epic:** Setup

## Goal

Run `python send.py` in dry‑run mode and confirm 5 email drafts appear in `sent_log/`.

## Steps

1. In `career/outreach/`, run: `python send.py`
2. It should print "Total: 5 messages processed (dry_run=1)"
3. Check `sent_log/` folder — 5 `.txt` files (one per company)
4. Open a few, verify content looks good (personalized with company name, reason)

If any errors: check `.env` values, ensure targets file exists.

## Acceptance

- `sent_log/` contains at least 5 draft files
- Content is personalized and error‑free

## Time

5 minutes
