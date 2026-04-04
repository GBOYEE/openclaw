# Telegram File Sender Skill for OpenClaw

## Purpose

Send files (documents, images, reports) to Telegram chats reliably. Integrates with any OpenClaw workflow that produces output files.

## Prerequisites

1. Telegram bot token from @BotFather
2. Target chat ID (user or channel)
3. OpenClaw with network egress to api.telegram.org

## Skill Definition

**Trigger:** Manual invocation or automated after task completion

**Context:** This skill provides a reliable, persistent capability to send any file to Telegram. It should be used whenever the agent needs to deliver results to a human or channel.

### Usage Pattern

```python
from skills.telegram.send_file import send_file

result = send_file(
    file_path="/path/to/report.pdf",
    chat_id="123456789",
    bot_token="YOUR_BOT_TOKEN"
)
```

Returns: `{"ok": true, "message_id": ..., "chat": ...}` or error dict

---

## Implementation Details

### Core Function

```python
def send_file(file_path: str, chat_id: str, bot_token: str, caption: str = None) -> dict:
    """
    Send a file to Telegram via bot API.

    Args:
        file_path: Path to file to upload
        chat_id: Telegram chat ID (numeric or @channel)
        bot_token: Bot token from @BotFather
        caption: Optional message caption

    Returns:
        dict: Telegram API response
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    try:
        with open(file_path, "rb") as f:
            files = {"document": f}
            data = {"chat_id": chat_id}
            if caption:
                data["caption"] = caption

            response = requests.post(url, data=data, files=files, timeout=30)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"ok": false, "error": str(e)}
```

### Retry Logic

The skill includes exponential backoff retries (3 attempts) for transient network failures.

---

## Configuration

Store credentials in OpenClaw config or environment:

```yaml
# config/telegram.yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"
  default_chat_id: "YOUR_CHAT_ID"  # optional default
```

Or as environment variables:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_DEFAULT_CHAT_ID`

---

## Integration Examples

### 1. Auto-sme: Send sales report PDF

```python
# After generating PDF report in /tmp/sales.pdf
from skills.telegram.send_file import send_file
import os

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_DEFAULT_CHAT_ID")

result = send_file(
    file_path="/tmp/sales.pdf",
    chat_id=chat_id,
    bot_token=bot_token,
    caption="📊 Sales Report - April 2026"
)
```

### 2. TPT Unit: Notify when ZIP ready

```python
if zip_path.exists():
    send_file(
        file_path=str(zip_path),
        chat_id=admin_chat,
        bot_token=bot_token,
        caption=f"✅ {topic} unit ready for upload"
    )
```

### 3. Xander Operator: Send task summary

After completing a task, xander can send a summary PDF or log file to the user's Telegram.

---

## Security

- Bot tokens are sensitive. Store in environment variables or OpenClaw secrets store.
- Do not hardcode tokens in source.
- Use a dedicated bot with minimal permissions (can only send messages to allowed chats).
- Validate chat_id to avoid sending to unintended recipients.

---

## Error Handling

The skill returns a dict with `ok: false` and an `error` key on failure. Common errors:

- `404`: Invalid bot token or chat ID
- `400`: File too large (>50MB) or unsupported format
- `timeout`: Network issue (retry may help)

Agent should check `result["ok"]` and act accordingly (retry, log, notify).

---

## Testing

```python
# Quick test
from skills.telegram.send_file import send_file

res = send_file(
    file_path="test.txt",
    chat_id="YOUR_CHAT_ID",
    bot_token="YOUR_BOT_TOKEN"
)
print(res)
```

---

## Why This is a Skill, Not Knowledge

By packaging this as a skill:

- ✅ Reusable across all OpenClaw agents
- ✅ Persistent configuration (token, chat_id)
- ✅ Enforced pattern: whenever "send file" is mentioned, agent MUST use this skill
- ✅ Logging and retries built-in
- ✅ Can be improved centrally (add compression, queuing, etc.)

---

## Next Steps

1. Place `send_file.py` in `skills/telegram/`
2. Add skill registration to OpenClaw skill registry
3. Store `TELEGRAM_BOT_TOKEN` and `TELEGRAM_DEFAULT_CHAT_ID` in `.env` or config
4. Update agent system prompt to reference this skill for any file delivery task
