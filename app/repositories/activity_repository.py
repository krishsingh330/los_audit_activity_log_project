from sqlmodel import Session, select
from app.models import ActivityLog


class ActivityRepository:
    """
    Repository for accessing ActivityLog data.
    """

    @staticmethod
    def get_all(
        session: Session,
        user_id: int = None,
        entity: str = None,
        entity_id: int = None,
        action: str = None,
        limit: int = 100
    ):
        """
        Retrieves activity logs from the database with optional filters.
        
        Args:
            session (Session): The database session.
            user_id (int, optional): Filter by user ID.
            entity (str, optional): Filter by entity name.
            entity_id (int, optional): Filter by entity ID.
            action (str, optional): Filter by action type.
            limit (int): Max records to return.
            
        Returns:
            list[ActivityLog]: A list of filtered activity logs.
        """
        statement = select(ActivityLog)

        if user_id:
            statement = statement.where(ActivityLog.user_id == user_id)
        if entity:
            statement = statement.where(ActivityLog.entity == entity)
        if entity_id:
            statement = statement.where(ActivityLog.entity_id == entity_id)
        if action:
            statement = statement.where(ActivityLog.action == action)

        statement = statement.limit(limit)
        
        return session.exec(statement).all()
