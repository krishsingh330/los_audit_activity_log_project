from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import AuditLog


class AuditRepository:
    """
    Repository for accessing AuditLog data.
    """

    @staticmethod
    async def get_audit_logs(
        session: AsyncSession,
        table_name=None,
        record_id=None,
        action=None,
        limit=100
    ):
        """
        Retrieves audit logs with optional filters.
        
        Repository layer is responsible only for database interaction.
        No validation, no request handling, no business rules.
        
        Args:
            session (AsyncSession): Database session.
            table_name (str, optional): Filter by table name.
            record_id (int, optional): Filter by record ID.
            action (str, optional): Filter by action type (CREATE, UPDATE, DELETE).
            limit (int): Maximum number of records to return.
            
        Returns:
            list[AuditLog]: A list of matching audit log entries.
        """
        try:
            # Initialize base query on AuditLog table
            # At this stage, query represents:
            # SELECT * FROM audit_logs
            statement = select(AuditLog)

            # Apply table name filter if provided
            # This restricts logs to a specific database table
            if table_name:
                statement = statement.where(AuditLog.table_name == table_name)

            # Apply record ID filter if provided
            # This fetches audit history of a specific row
            if record_id is not None:
                statement = statement.where(AuditLog.record_id == record_id)

            # Apply action filter if provided
            # Action is normalized to uppercase to match DB values
            if action:
                statement = statement.where(AuditLog.action == action.upper())

            # Sort records by creation time in descending order
            # Limit is applied to protect database from heavy queries
            statement = statement.order_by(AuditLog.created_at.desc()).limit(limit)

            result = await session.exec(statement)
            
            # Return list of audit log records
            return result.all()

        except Exception as e:
            raise e
