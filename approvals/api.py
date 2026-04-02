"""Approval API endpoints with proper dependency injection, auth, and role checks."""
import os
import yaml
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from datetime import datetime
import uuid

from sqlalchemy.orm import Session

from ..state.models import Approval, init_db, Event, EventType
from ..config.settings import settings

router = APIRouter(prefix="/approvals", tags=["approvals"])

# Load permissions once
with open(settings.permissions.path) as f:
    PERMISSIONS = yaml.safe_load(f)

def get_user_role(x_user_id: str) -> str:
    """Map user ID to role via env whitelists."""
    admins = os.getenv("OPENCLAW_ADMIN_USERS", "").split(",")
    operators = os.getenv("OPENCLAW_OPERATORS", "").split(",")
    if x_user_id in admins:
        return "admin"
    if x_user_id in operators:
        return "operator"
    return "viewer"

def get_db_session():
    SessionFactory = init_db(settings.database.url)
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

def require_user_id(x_user_id: str = Header(..., alias="X-User-ID")):
    """Ensure user identifier is provided."""
    return x_user_id

@router.get("/pending")
def list_pending(db: Session = Depends(get_db_session)):
    approvals = db.query(Approval).filter(Approval.status == "pending").all()
    return [
        {
            "approval_id": a.approval_id,
            "task_id": a.task_id,
            "step": a.step,
            "tool": a.tool,
            "args": a.args,
            "requested_by": a.requested_by,
            "created_at": a.created_at.isoformat(),
        }
        for a in approvals
    ]

@router.post("/{approval_id}/approve")
def approve(
    approval_id: str,
    request: Request,
    db: Session = Depends(get_db_session),
    x_user_id: str = Depends(require_user_id),
):
    approval = db.query(Approval).filter(Approval.approval_id == approval_id).first()
    if not approval or approval.status != "pending":
        raise HTTPException(status_code=404, detail="Approval not found or already processed")

    # Role check
    user_role = get_user_role(x_user_id)
    allowed_roles = PERMISSIONS.get("tools", {}).get(approval.tool, {}).get("allowed_roles", [])
    if user_role not in allowed_roles:
        raise HTTPException(status_code=403, detail=f"User role {user_role} not allowed for tool {approval.tool}")

    approval.status = "granted"
    approval.granted_by = x_user_id
    approval.decided_at = datetime.utcnow()
    db.commit()

    event = Event(
        event_id=str(uuid.uuid4()),
        type=EventType.approval_granted,
        task_id=approval.task_id,
        payload={"approval_id": approval_id, "tool": approval.tool, "args": approval.args},
        timestamp=datetime.utcnow(),
        source="approvals",
    )
    db.add(event)
    db.commit()
    return {"status": "ok", "action": "approved"}

@router.post("/{approval_id}/reject")
def reject(
    approval_id: str,
    request: Request,
    db: Session = Depends(get_db_session),
    x_user_id: str = Depends(require_user_id),
):
    approval = db.query(Approval).filter(Approval.approval_id == approval_id).first()
    if not approval or approval.status != "pending":
        raise HTTPException(status_code=404, detail="Approval not found or already processed")

    # Role check (rejection also requires permission)
    user_role = get_user_role(x_user_id)
    allowed_roles = PERMISSIONS.get("tools", {}).get(approval.tool, {}).get("allowed_roles", [])
    if user_role not in allowed_roles:
        raise HTTPException(status_code=403, detail=f"User role {user_role} not allowed for tool {approval.tool}")

    approval.status = "rejected"
    approval.granted_by = x_user_id
    approval.decided_at = datetime.utcnow()
    db.commit()

    event = Event(
        event_id=str(uuid.uuid4()),
        type=EventType.approval_rejected,
        task_id=approval.task_id,
        payload={"approval_id": approval_id},
        timestamp=datetime.utcnow(),
        source="approvals",
    )
    db.add(event)
    db.commit()
    return {"status": "ok", "action": "rejected"}
