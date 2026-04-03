import pytest
from fastapi.testclient import TestClient
from polish.openclaw.approvals.api import router, get_db_session
from polish.openclaw.state.models import Base, Approval
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

@pytest.fixture
def client_with_temp_db(tmp_path, monkeypatch):
    # Set admin users for role checks
    monkeypatch.setenv("OPENCLAW_ADMIN_USERS", "admin,superadmin")
    db_file = tmp_path / "test.db"
    db_url = f"sqlite:///{db_file}"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    from fastapi import FastAPI
    app = FastAPI()
    app.dependency_overrides[get_db_session] = lambda: Session()
    app.include_router(router)
    client = TestClient(app)
    return client, engine

def test_list_pending_empty(client_with_temp_db):
    client, _ = client_with_temp_db
    resp = client.get("/approvals/pending")
    assert resp.status_code == 200
    assert resp.json() == []

def test_approval_flow(client_with_temp_db):
    client, engine = client_with_temp_db
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        approval = Approval(
            approval_id="test_id",
            task_id="task_123",
            step=1,
            tool="shell",
            args={"cmd": "test"},
            status="pending",
            requested_by="tester",
            created_at=datetime.utcnow(),
        )
        session.add(approval)
        session.commit()
    finally:
        session.close()

    verify = Session()
    try:
        assert verify.query(Approval).count() == 1
    finally:
        verify.close()

    # Approve with proper headers (auth not enforced in test because env var not set)
    resp = client.post("/approvals/test_id/approve", headers={"X-User-ID": "admin"})
    assert resp.status_code == 200
    assert resp.json()["action"] == "approved"

    # Pending empty
    resp = client.get("/approvals/pending")
    assert resp.status_code == 200
    assert resp.json() == []
