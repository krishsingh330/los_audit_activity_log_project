from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from app.services.activity_service import ActivityService
from app.dependencies import get_db
from app.core.logger import logger

router = APIRouter(prefix="/activity-logs", tags=["Activity Logs"])

@router.get("/")
def get_activity_logs(
    user_id: int = None,
    entity: str = None,
    entity_id: int = None,
    action: str = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all activity logs with optional filtering.
    
    Args:
        user_id (int, optional): Filter by user ID.
        entity (str, optional): Filter by entity name (e.g., 'LOAN', 'PAYMENT').
        entity_id (int, optional): Filter by specific entity ID.
        action (str, optional): Filter by action type.
        limit (int): Limit number of records (default 100).
        db (Session): Database session.
        
    Returns:
        list[ActivityLog]: List of system activity logs matching criteria.
    """
    
    return ActivityService.get_activity_logs(
        db,
        user_id=user_id,
        entity=entity,
        entity_id=entity_id,
        action=action,
        limit=limit
    )
