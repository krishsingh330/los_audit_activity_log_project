from fastapi import APIRouter, Depends,Request
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services import audit_service
from app.dependencies import get_db

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("/")
async def get_audit_logs(
    table_name: str = None,
    record_id: int = None,
    action: str = None,
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
):
    """
    Retrieve audit logs with optional filtering.

    This endpoint delegates the data retrieval to the service layer,
    allowing filtering by table name, record ID, and action type.

    Args:
        table_name (str, optional): Name of the table to filter by.
        record_id (int, optional): ID of the specific record.
        action (str, optional): Action type (INSERT, UPDATE, DELETE).
        limit (int): Maximum number of records to return.
        db (AsyncSession): Database session.

    Returns:
        list[AuditLog]: A list of audit logs matching the criteria.
    """

    # Call service layer with request parameters
    logs = await audit_service.fetch_audit_logs(
        session=session,
        table_name=table_name,
        record_id=record_id,
        action=action,
        limit=limit
    )

    # Return response to client
    return logs
