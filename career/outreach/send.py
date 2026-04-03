#!/usr/bin/env python3
"""
Outreach sender — read target list, render templates, send emails or print to stdout.
"""

import os
import sys
import smtplib
import yaml
from email.message import EmailMessage
from pathlib import Path
from string import Template

TEMPLATES_DIR = Path(__file__).parent.parent / "materials"
TARGETS_FILE = Path(__file__).parent.parent / "materials" / "02-01-target-companies.yaml"
OUTPUT_DIR = Path(__file__).parent / "sent_log"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_targets():
    with open(TARGETS_FILE) as f:
        return yaml.safe_load(f)

def load_template(name: str) -> Template:
    path = TEMPLATES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Template {name} not found")
    return Template(path.read_text())

def render(template: Template, context: dict) -> str:
    return template.safe_substitute(**context)

def send_email(to_addr, subject, body, smtp_cfg):
    msg = EmailMessage()
    msg["To"] = to_addr
    msg["From"] = smtp_cfg["from"]
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL(smtp_cfg["host"], smtp_cfg["port"]) as s:
        s.login(smtp_cfg["username"], smtp_cfg["password"])
        s.send_message(msg)

def main():
    dry_run = os.getenv("OUTREACH_DRY_RUN", "1") == "1"
    smtp_cfg = {
        "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "465")),
        "username": os.getenv("SMTP_USER"),
        "password": os.getenv("SMTP_PASS"),
        "from": os.getenv("OUTREACH_FROM"),
    }
    targets = load_targets()
    email_tpl = load_template("outreach-templates.md").split("## 2. Direct Email")[1].split("## 3.")[0].strip()
    # The above is hacky; better to store separate files. For now, just use a simple version.
    # Let's instead define a minimal direct email template inline.
    email_tpl = """Hi $name,

I'm an AI Automation Engineer who builds production-grade systems using GSD. I noticed $company is doing $reason — it aligns with my work on agent-core and automation-engine.

I'd love to connect and explore if my skills could help your team. Open to roles or consulting.

Briefly, I've delivered:
- agent-core: intelligent agent framework
- automation-engine: secure scheduler + webhook
- trading-lab: backtesting & optimization

Happy to share more if interesting.

Cheers,
GBOYEE
GitHub: https://github.com/GBOYEE
Portfolio: https://gboyee.com
"""
    email_tpl = Template(email_tpl)

    sent = 0
    for t in targets[:5]:  # limit for safety
        name = t.get("contact") or "Hiring Manager"
        company = t["company"]
        reason = t["reason"]
        body = email_tpl.substitute(name=name, company=company, reason=reason)
        subject = f"AI automation expertise that could help {company}"
        if dry_run:
            print(f"\n[DRY RUN] Would send to {company}:\nSubject: {subject}\nBody:\n{body}\n")
            (OUTPUT_DIR / f"{company}.txt").write_text(f"Subject: {subject}\n\n{body}")
            sent += 1
        else:
            try:
                send_email(t.get("contact_email", "hello@gboyee.com"), subject, body, smtp_cfg)
                sent += 1
                print(f"Sent to {company}")
            except Exception as e:
                print(f"Failed {company}: {e}")

    print(f"Total: {sent} messages processed (dry_run={dry_run})")

if __name__ == "__main__":
    main()