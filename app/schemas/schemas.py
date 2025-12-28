from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# AUTH
class UserRegisterSchema(BaseModel):
    """
    Schema for user registration.
    
    Attributes:
        email (EmailStr): Valid email address.
        password (str): Plain text password (will be hashed).
        role (str): Role of the user (admin, officer, etc.).
    """
    email: EmailStr
    password: str
    role: str


class UserLoginSchema(BaseModel):
    """
    Schema for user login.
    
    Attributes:
        email (EmailStr): User's email.
        password (str): User's password.
    """
    email: EmailStr
    password: str


# LOAN
class LoanCreateSchema(BaseModel):
    """
    Schema for creating a new loan application.
    
    Attributes:
        customer_name (str): Name of the applicant.
        loan_amount (float): Desired loan amount.
        tenure_months (int): Duration in months.
        interest_rate (float, optional): Proposed interest rate.
    """
    customer_name: str
    loan_amount: float
    tenure_months: int
    interest_rate: Optional[float] = None


class LoanUpdateSchema(BaseModel):
    """
    Schema for updating an existing loan.
    All fields are optional to allow partial updates.
    
    Attributes:
        loan_amount (float): Revised loan amount.
        interest_rate (float): Revised interest rate.
        status (str): New status (e.g., APPROVED, REJECTED).
        tenure_months (int): Revised tenure (must be > 0).
    """
    loan_amount: Optional[float] = None
    interest_rate: Optional[float] = None
    status: Optional[str] = None
    tenure_months: Optional[int] = Field(None, gt=0)


# PAYMENT
class PaymentCreate(BaseModel):
    """
    Schema for recording a new payment.
    
    Attributes:
        amount (float): Payment amount.
        payment_mode (str): Mode of payment (CASH, CARD, UPI).
    """
    amount: float
    payment_mode: str


class PaymentUpdate(BaseModel):
    """
    Schema for updating a payment record.
    
    Attributes:
        amount (float): Updated amount.
        status (str): Updated status (e.g., COMPLETED, FAILED).
    """
    amount: Optional[float] = None
    status: Optional[str] = None
