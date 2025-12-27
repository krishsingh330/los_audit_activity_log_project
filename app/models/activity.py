from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON


class ActivityLog(SQLModel, table=True):
    """
    Represents an activity log for HTTP requests/actions.
    
    Attributes:
        id (int): Unique identifier.
        user_id (int): ID of the user performing the request (optional).
        action (str): Description of the action (e.g., "GET /api/v1/users").
        entity (str): Affected entity name but often used for logical grouping.
        entity_id (int): ID of the affected entity.
        method (str): HTTP method (GET, POST, etc.).
        endpoint (str): API endpoint accessed.
        ip_address (str): IP address of the client.
        status (str): Outcome of the request (SUCCESS, FAILED).
        status_code (int): HTTP status code returned.
        extra_data (Dict): Additional context or payload data.
        created_at (datetime): Timestamp of the request.
    """
    __tablename__ = "activity_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None)

    action: str = Field(nullable=False)

    entity: Optional[str] = Field(default=None)

    entity_id: Optional[int] = Field(default=None)

    method: str = Field(nullable=False)

    endpoint: str = Field(nullable=False)

    ip_address: Optional[str] = Field(default=None)

    status: str = Field(default="SUCCESS", nullable=False)

    status_code: Optional[int] = Field(default=None)

    # Stores flexible JSON data for extra context
    extra_data: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
