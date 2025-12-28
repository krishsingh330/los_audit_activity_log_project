from sqlmodel import Session
from app.repositories.activity_repository import ActivityRepository


class ActivityService:
    """
    Service layer for handling activity logs.
    """

    @staticmethod
    def get_activity_logs(
        session: Session,
        user_id: int = None,
        entity: str = None,
        entity_id: int = None,
        action: str = None,
        limit: int = 100
    ):
        """
        Retrieves activity logs from the repository with filters.
    
        Args:
            session (Session): Database session.
            user_id (int, optional): Filter by user ID.
            entity (str, optional): Filter by entity name.
            entity_id (int, optional): Filter by entity ID.
            action (str, optional): Filter by action type.
            limit (int): Max records (capped at 500).
            
        Returns:
            list[ActivityLog]: List of application activity logs.
        """
        if limit > 500:
            limit = 500
            
        return ActivityRepository.get_all(
            session=session,
            user_id=user_id,
            entity=entity,
            entity_id=entity_id,
            action=action,
            limit=limit
        )
