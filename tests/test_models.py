import pytest
from datetime import datetime
from polish.openclaw.state.models import Event, Approval, AuditLog, EventType

def test_event_crud(db_session):
    event = Event(
        event_id="evt_123",
        type=EventType.task_received,
        task_id="task_456",
        payload={"test": "data"},
        timestamp=datetime.utcnow(),
        source="gateway",
    )
    db_session.add(event)
    db_session.commit()
    fetched = db_session.query(Event).filter_by(event_id="evt_123").first()
    assert fetched is not None
    assert fetched.payload["test"] == "data"

def test_approval_crud(db_session):
    approval = Approval(
        approval_id="app_123",
        task_id="task_456",
        step=1,
        tool="shell",
        args={"cmd": "test"},
        requested_by="user1",
        status="pending",
        created_at=datetime.utcnow(),
    )
    db_session.add(approval)
    db_session.commit()
    fetched = db_session.query(Approval).filter_by(approval_id="app_123").first()
    assert fetched.tool == "shell"
    assert fetched.status == "pending"

def test_audit_log_crud(db_session):
    log = AuditLog(
        log_id="log_123",
        user="admin",
        action="approve",
        resource="approval",
        details={"approval_id": "app_123"},
        timestamp=datetime.utcnow(),
    )
    db_session.add(log)
    db_session.commit()
    fetched = db_session.query(AuditLog).filter_by(log_id="log_123").first()
    assert fetched.action == "approve"
