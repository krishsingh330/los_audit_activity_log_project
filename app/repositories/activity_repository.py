from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import ActivityLog


class ActivityRepository:
    """
    Repository for accessing ActivityLog data.
    """

    @staticmethod
    async def get_all(
        session: AsyncSession,
        user_id: int = None,
        entity: str = None,
        entity_id: int = None,
        action: str = None,
        limit: int = 100
    ):
        """
        Retrieves activity logs from the database with optional filters.
        """
        try:
            statement = select(ActivityLog)

            if user_id:
                statement = statement.where(ActivityLog.user_id == user_id)
            if entity:
                statement = statement.where(ActivityLog.entity == entity)
            if entity_id:
                statement = statement.where(ActivityLog.entity_id == entity_id)
            if action:
                statement = statement.where(ActivityLog.action == action.upper())

            statement = statement.limit(limit)

            result = await session.exec(statement)
            return result.all()

        except Exception as e:
            raise e
