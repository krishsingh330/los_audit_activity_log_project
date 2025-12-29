from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.activity_repository import ActivityRepository
from fastapi import HTTPException
from app.core.logger import logger

class ActivityService:
    """
    Service layer for handling activity logs.
    """

    @staticmethod
    async def get_activity_logs(
        session: AsyncSession,
        user_id: int = None,
        entity: str = None,
        entity_id: int = None,
        action: str = None,
        limit: int = 100
    ):
        """
        Retrieves activity logs from the repository with filters.
    
        Args:
            session (AsyncSession): Database session.
            user_id (int, optional): Filter by user ID.
            entity (str, optional): Filter by entity name.
            entity_id (int, optional): Filter by entity ID.
            action (str, optional): Filter by action type.
            limit (int): Max records (capped at 500).
            
        Returns:
            list[ActivityLog]: List of application activity logs.
        """
        try:
            if limit > 500:
                limit = 500
                
            return await ActivityRepository.get_all(
                session=session,
                user_id=user_id,
                entity=entity,
                entity_id=entity_id,
                action=action,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Error fetching activity logs: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
