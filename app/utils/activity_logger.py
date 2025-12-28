from fastapi import Request
from sqlmodel import Session
from typing import Optional, Dict, Any

from app.models.activity import ActivityLog


def create_log_activity(
    db: Session,
    request: Request,
    action: str,
    entity: Optional[str] = None,
    entity_id: Optional[int] = None,
    status: str = "SUCCESS",
    status_code: Optional[int] = None,
    extra_data: Optional[Dict[str, Any]] = None
):
    """
    Creates and persists a new ActivityLog entry.
    
    Args:
        db (Session): Database session.
        request (Request): HTTP request object.
        action (str): Action performed (CREATE, UPDATE, etc.).
        entity (str, optional): Entity affected.
        entity_id (int, optional): ID of the entity.
        status (str): Outcome (SUCCESS/FAILED).
        status_code (int): HTTP status.
        extra_data (dict): Additional context (encrypted).
    """


    activity = ActivityLog(
        user_id=getattr(request.state, "user_id", None),
        action=action,
        entity=entity,
        entity_id=entity_id,
        method=request.method,
        endpoint=request.url.path,
        ip_address=request.client.host if request.client else None,
        status=status,
        status_code=status_code,
        extra_data=extra_data
    )

    db.add(activity)
    db.commit()

   
