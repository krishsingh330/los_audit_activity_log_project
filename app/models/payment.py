from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

from app.models.audit import AuditableBase

class Payment(AuditableBase, SQLModel, table=True):
    """
    Represents a payment transaction.
    
    Inherits from AuditableBase to support audit trails.
    
    Attributes:
        id (int): Unique identifier for the payment.
        amount (float): Payment amount.
        payment_mode (str): Method of payment (CASH, UPI, CARD).
        status (str): Status of the payment (e.g., PENDING, COMPLETED).
        created_at (datetime): Timestamp when the payment was recorded.
    """
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)

    amount: float = Field(nullable=False)

    payment_mode: str = Field(nullable=False)  # CASH / UPI / CARD

    status: str = Field(default="PENDING", nullable=False)

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
