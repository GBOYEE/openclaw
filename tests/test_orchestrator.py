import pytest
from unittest.mock import MagicMock
from polish.openclaw.core.orchestrator import Orchestrator

@pytest.fixture
def mock_db_factory():
    def mock_session():
        session = MagicMock()
        session.add = MagicMock()
        session.commit = MagicMock()
        session.close = MagicMock()
        return session
    return lambda: mock_session()

@pytest.fixture
def permissions():
    return {
        "tools": {
            "shell": {"risk": "high", "require_approval": True},
            "disk_clean": {"risk": "low", "auto_execute": True},
        }
    }

def test_receive_task(mock_db_factory, permissions):
    orch = Orchestrator(db_session_factory=mock_db_factory, permissions=permissions)
    task_id = orch.receive_task("test", {"description": "do something"})
    assert task_id is not None
    assert orch.metrics["tasks_received"] == 1

def test_plan_task(mock_db_factory, permissions):
    orch = Orchestrator(db_session_factory=mock_db_factory, permissions=permissions)
    task_id = orch.receive_task("test", {"desc": "x"})
    plan = orch.plan_task(task_id, "test plan")
    assert "steps" in plan
    assert len(plan["steps"]) >= 1

def test_execute_plan_low_risk_success(mock_db_factory, permissions):
    orch = Orchestrator(db_session_factory=mock_db_factory, permissions=permissions)
    task_id = orch.receive_task("test", {})
    plan = {"steps": [{"step": 1, "action": "disk_clean", "args": {"limit_mb": 500}}]}
    result = orch.execute_plan(task_id, plan)
    assert result["payload"]["success"] is True
    assert orch.metrics["tasks_executed"] == 1
    assert orch.metrics["tasks_succeeded"] == 1

def test_execute_plan_high_risk_requires_approval(mock_db_factory, permissions):
    orch = Orchestrator(db_session_factory=mock_db_factory, permissions=permissions)
    task_id = orch.receive_task("test", {})
    plan = {"steps": [{"step": 1, "action": "shell", "args": {"cmd": "whoami"}}]}
    result = orch.execute_plan(task_id, plan)
    assert result["payload"]["success"] is False
    events = result["payload"]["results"]
    assert any(r.get("status") == "awaiting_approval" for r in events)
    assert orch.metrics["approvals_requested"] == 1

def test_assess_risk(mock_db_factory, permissions):
    orch = Orchestrator(db_session_factory=mock_db_factory, permissions=permissions)
    assert orch._assess_risk("disk_clean", {}) == "low"
    assert orch._assess_risk("shell", {}) == "high"
    assert orch._assess_risk("unknown", {}) == "medium"
