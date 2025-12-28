from sqlalchemy.orm import Session
from app.models import AuditLog


class AuditRepository:
    """
    Repository for accessing AuditLog data.
    """

    @staticmethod
    def get_audit_logs(
        db: Session,
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
            db (Session): Database session.
            table_name (str, optional): Filter by table name.
            record_id (int, optional): Filter by record ID.
            action (str, optional): Filter by action type (CREATE, UPDATE, DELETE).
            limit (int): Maximum number of records to return.
            
        Returns:
            list[AuditLog]: A list of matching audit log entries.
        """
        # Initialize base query on AuditLog table
        # At this stage, query represents:
        # SELECT * FROM audit_logs
        query = db.query(AuditLog)

        # Apply table name filter if provided
        # This restricts logs to a specific database table
        if table_name:
            query = query.filter(AuditLog.table_name == table_name)

        # Apply record ID filter if provided
        # This fetches audit history of a specific row
        if record_id is not None:
            query = query.filter(AuditLog.record_id == record_id)

        # Apply action filter if provided
        # Action is normalized to uppercase to match DB values
        if action:
            query = query.filter(AuditLog.action == action.upper())

        # Sort records by creation time in descending order
        # Limit is applied to protect database from heavy queries
        logs = (
            query
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()
        )

        # Return list of audit log records
        return logs
