from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from sqlalchemy import event
from sqlmodel import Session

from app.utils.audit_utils import model_to_dict, get_changed_fields_from_history


class AuditLog(SQLModel, table=True):
    """
    Represents an audit log entry for tracking database changes.
    
    Attributes:
        id (int): Unique identifier for the log entry.
        table_name (str): Name of the table where the change occurred.
        record_id (int): ID of the record that was changed.
        action (str): Type of action (CREATE, UPDATE, DELETE).
        before_data (Dict): Data state before the change (snapshot).
        after_data (Dict): Data state after the change (snapshot).
        performed_by (int): ID of the user who performed the action.
        created_at (datetime): Timestamp of the action.
    """
    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    table_name: str = Field(nullable=False)

    record_id: int = Field(nullable=False)

    action: str = Field(nullable=False)

    # Stores JSON data representing the state before the change
    before_data: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )

    # Stores JSON data representing the state after the change
    after_data: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )

    performed_by: int = Field(nullable=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)


class AuditableBase(SQLModel, table=False):
    """
    Base class for models that require audit logging.
    Models inheriting from this will automatically trigger audit logs on changes.
    """
    pass


@event.listens_for(Session, "after_flush")
def after_flush(session, flush_context):
    """
    SQLAlchemy event listener triggered after a session flush.
    
    Inspects the session for modified objects (new, dirty, deleted) that inherit from AuditableBase
    and creates corresponding AuditLog entries.
    
    Args:
        session: The current database session.
        flush_context: Context of the flush operation.
    """
    # Retrieve user_id from session info (set by middleware/dependency)
    user_id = session.info.get("user_id")
    if user_id is None:
        return

    # Handle CREATE operations
    for obj in session.new:
        if isinstance(obj, AuditableBase) and hasattr(obj, "id") and obj.id is not None:
            session.add(
                AuditLog(
                    table_name=obj.__tablename__,
                    record_id=obj.id,
                    action="CREATE",
                    before_data=None,
                    after_data=model_to_dict(obj),
                    performed_by=user_id,
                )
            )

    # Handle UPDATE operations
    for obj in session.dirty:
        if isinstance(obj, AuditableBase) and obj.__tablename__ != "audit_logs":
            before_data, after_data = get_changed_fields_from_history(obj)
            # Only log if there are actual changes
            if before_data:
                session.add(
                    AuditLog(
                        table_name=obj.__tablename__,
                        record_id=obj.id,
                        action="UPDATE",
                        before_data=before_data,
                        after_data=after_data,
                        performed_by=user_id,
                    )
                )

    # Handle DELETE operations
    for obj in session.deleted:
        if isinstance(obj, AuditableBase):
            session.add(
                AuditLog(
                    table_name=obj.__tablename__,
                    record_id=obj.id,
                    action="DELETE",
                    before_data=model_to_dict(obj),
                    after_data=None,
                    performed_by=user_id,
                )
            )

