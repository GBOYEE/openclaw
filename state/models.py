"""SQLAlchemy models for OpenClaw persistence and audit."""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Text, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import enum

Base = declarative_base()

class EventType(str, enum.Enum):
    task_received = "task_received"
    planned = "planned"
    executed = "executed"
    approval_requested = "approval_requested"
    approval_granted = "approval_granted"
    approval_rejected = "approval_rejected"
    error = "error"

class Event(Base):
    __tablename__ = "events"
    event_id = Column(String, primary_key=True)
    type = Column(SQLEnum(EventType), nullable=False)
    task_id = Column(String, nullable=True, index=True)
    payload = Column(JSON, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    source = Column(String, nullable=True)

class Approval(Base):
    __tablename__ = "approvals"
    approval_id = Column(String, primary_key=True)
    task_id = Column(String, nullable=False, index=True)
    step = Column(Integer, nullable=False)
    tool = Column(String, nullable=False)
    args = Column(JSON, nullable=False)
    requested_by = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    granted_by = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)

class Decision(Base):
    __tablename__ = "decisions"
    decision_id = Column(String, primary_key=True)
    task_id = Column(String, nullable=False, index=True)
    agent = Column(String, nullable=False)
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=False)
    confidence = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    log_id = Column(String, primary_key=True)
    user = Column(String, nullable=True)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

def init_db(database_url: str):
    engine = create_engine(database_url, echo=False, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session
