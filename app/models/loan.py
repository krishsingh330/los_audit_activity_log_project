from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

from app.models.audit import AuditableBase


class Loan(AuditableBase, SQLModel, table=True):
    """
    Represents a loan application.
    
    Inherits from AuditableBase to support audit trails.
    
    Attributes:
        id (int): Unique identifier for the loan.
        customer_name (str): Name of the customer applying for the loan.
        loan_amount (float): Amount requested.
        tenure_months (int): Duration of the loan in months.
        interest_rate (float): Applied interest rate.
        status (str): Current status of the loan (e.g., pending, approved).
        created_by (int): ID of the user who created the application.
        approved_by (int): ID of the user who approved the application (optional).
        created_at (datetime): Timestamp of creation.
        approved_at (datetime): Timestamp of approval (optional).
    """
    __tablename__ = "loans"

    id: Optional[int] = Field(default=None, primary_key=True)

    customer_name: str = Field(nullable=False)

    loan_amount: float = Field(nullable=False)

    tenure_months: int = Field(nullable=False)

    interest_rate: Optional[float] = Field(default=None)

    status: str = Field(default="pending", nullable=False)

    created_by: int = Field(
        foreign_key="users.id",
        nullable=False
    )

    approved_by: Optional[int] = Field(
        default=None,
        foreign_key="users.id"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    approved_at: Optional[datetime] = Field(default=None)
