# Xander Autonomous System (OpenClaw Orchestrator)

This module turns OpenClaw into a true autonomous operator that runs tasks without prompting and delivers results automatically.

## Components

- **TaskQueue** (`task_queue.py`) — SQLite-backed persistent queue with priority and scheduled execution
- **Finalizer** (`finalizer.py`) — Auto-delivers results via Telegram and logs proof
- **OperatorClient** (`operator_client.py`) — Calls xander-operator and enforces completion contract
- **AutonomousService** (`autonomous_service.py`) — Main orchestrator loop

## Operator Contract

Xander Operator must return:

```json
{
  "status": "completed",
  "task": "task description",
  "output_path": "/absolute/path/to/output",
  "summary": "human readable summary"
}
```

## Usage

### Start the service

```bash
# Set Telegram credentials
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_DEFAULT_CHAT_ID="your_chat_id"

# Activate OpenClaw venv
source polish/openclaw/.venv/bin/activate

# Run orchestrator loop
python -m core.autonomy.autonomous_service
```

Or enable systemd unit:

```bash
sudo cp deploy/xander-autonomous.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now xander-autonomous
```

### Add tasks

```python
from core.autonomy import TaskQueue

q = TaskQueue()
q.add(
    task_id="my_task_001",
    title="Generate trading performance report",
    priority=1,
    run_at=None  # or ISO datetime to schedule
)
```

### Task lifecycle

1. Task added to queue (status: pending or scheduled)
2. Orchestrator picks next task → marks running
3. Operator executes and returns contract
4. Finalizer:
   - Sends output file to Telegram
   - Sends summary message
   - Appends to `/logs/history.json`
   - Marks task completed
5. Loop continues

### Definition of DONE

A task is DONE only when:
- File successfully sent to Telegram
- Summary message sent
- Entry written to history log
- Task status = completed in queue

If any step fails, finalizer retries up to 3 times.

---

## Configuration

Environment variables:

- `TELEGRAM_BOT_TOKEN` — Bot token from @BotFather
- `TELEGRAM_DEFAULT_CHAT_ID` — Destination chat ID
- `OPERATOR_MODE` — `cli` (default) or `api`
- `OPERATOR_API_URL` — if mode=api, URL of operator server
- `TASK_QUEUE_PATH` — SQLite DB path (default: `/data/tasks.db`)

---

## File organization

```
polish/openclaw/
├── core/
│   └── autonomy/
│       ├── task_queue.py
│       ├── finalizer.py
│       ├── operator_client.py
│       ├── autonomous_service.py
│       └── __init__.py
├── deploy/
│   └── xander-autonomous.service
└── .env.autonomous
```

---

## Monitoring

- Task queue: `sqlite3 /data/tasks.db "SELECT * FROM tasks ORDER BY created_at DESC LIMIT 10;"`
- History log: `cat /logs/history.json`
- System logs: `journalctl -u xander-autonomous -f`
