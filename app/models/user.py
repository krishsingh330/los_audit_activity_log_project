from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    """
    Represents a user in the system (e.g., admin, loan officer).
    
    Attributes:
        id (int): Unique identifier for the user.
        email (str): User's email address (must be unique).
        password (str): Hashed password.
        role (str): Role of the user in the system.
        created_at (datetime): Timestamp when the user was created.
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)
    role: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
