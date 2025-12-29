from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.audit_repository import AuditRepository
from fastapi import HTTPException
from app.core.logger import logger


async def fetch_audit_logs(
    session: AsyncSession,
    table_name=None,
    record_id=None,
    action=None,
    limit=100
):
    """
    Service layer acts as the business logic layer.
    It decides how data should be processed
    before and after repository access.
    
    Args:
        db (AsyncSession): Database session.
        table_name (str, optional): Filter by table name.
        record_id (int, optional): Filter by record ID.
        action (str, optional): Filter by action type.
        limit (int): Max records (capped at 500).
        
    Returns:
        list[AuditLog]: Filtered audit logs.
    """
    try:
        # Enforce maximum limit to avoid accidental heavy DB queries
        # This rule lives in service, not in router or repository
        if limit > 500:
            limit = 500

        # Call repository function to fetch audit logs
        logs = await AuditRepository.get_audit_logs(
            session=session,
            table_name=table_name,
            record_id=record_id,
            action=action,
            limit=limit
        )

        # Service can transform or enrich data here if required
        # For now, logs are returned as-is
        return logs
    except Exception as e:
        logger.error(f"Error fetching audit logs: {e}")
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
