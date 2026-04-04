"""Autonomous Service — Xander Orchestrator (Main Loop)."""

import time
import logging
from typing import Optional

from .task_queue import TaskQueue
from .finalizer import Finalizer
from .operator_client import OperatorClient
from ..config.settings import settings

logger = logging.getLogger(__name__)

class AutonomousService:
    """
    Orchestrator loop:
    - Fetch next task from queue (handles scheduled tasks automatically)
    - Execute via Operator client
    - Finalize on completion
    """
    def __init__(self):
        self.task_queue = TaskQueue(settings.task_queue_path)
        self.finalizer = Finalizer(self.task_queue)
        self.operator = OperatorClient(
            mode=settings.operator_mode,
            api_url=settings.operator_api_url
        )
        self.running = False

    def start(self):
        """Start the orchestrator loop (blocking)."""
        self.running = True
        logger.info("Autonomous service starting...")

        while self.running:
            try:
                task = self.task_queue.next()
                if task:
                    self._execute_task(task)
                else:
                    # No tasks; optional: sleep or do maintenance
                    time.sleep(5)
            except KeyboardInterrupt:
                logger.info("Shutting down autonomous service")
                break
            except Exception as e:
                logger.exception(f"Loop error: {e}")
                time.sleep(5)

    def _execute_task(self, task: dict):
        task_id = task["id"]
        title = task["title"]
        logger.info(f"Executing task: {task_id} - {title}")

        try:
            result = self.operator.execute(title)
            status = result.get("status")

            if status == "completed":
                output_path = result.get("output_path")
                summary = result.get("summary", "")
                success = self.finalizer.safe_finalize(task_id, title, output_path, summary)
                if success:
                    logger.info(f"Task {task_id} finalized successfully")
                else:
                    logger.error(f"Task {task_id} finalize failed; marking as 'completed_with_issues'")
                    self.task_queue.update(task_id, status="completed_with_issues")
            else:
                # Execution failed
                logger.error(f"Task {task_id} execution failed: {result.get('summary')}")
                self.task_queue.update(task_id, status="failed")

        except Exception as e:
            logger.exception(f"Task {task_id} execution exception")
            self.task_queue.update(task_id, status="failed")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    service = AutonomousService()
    service.start()

if __name__ == "__main__":
    main()
