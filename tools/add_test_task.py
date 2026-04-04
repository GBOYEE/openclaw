#!/usr/bin/env python3
"""Quick test of autonomous task queue."""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/polish/openclaw')

from core.autonomy import TaskQueue

# Initialize queue (uses default /data/tasks.db)
q = TaskQueue()

# Add a test task
q.add(
    task_id="demo_001",
    title="Generate autonomous test report",
    priority=1,
    run_at=None  # immediate
)

print("✅ Task added to queue. Start the autonomous service to execute.")
print("Run: source .venv/bin/activate && python -m core.autonomy.autonomous_service")
