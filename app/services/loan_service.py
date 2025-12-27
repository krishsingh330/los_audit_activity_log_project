from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.loan_repository import LoanRepository


def fetch_all_loans(db: Session):
    """
    Service layer wrapper for fetching all loans.
    """

    return LoanRepository.get_all_loans(db)


def fetch_loan_by_id(db: Session, loan_id: int):
    """
    Fetch a loan by ID, validating its existence.
    
    Raises:
        HTTPException: 404 if loan not found.
    """

    loan = LoanRepository.get_loan_by_id(db, loan_id)

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    return loan


def create_loan(db: Session, user_id: int, payload):
    """
    Business logic for creating a loan.
    
    Validates:
    - user_id is provided and corresponds to a valid user.
    
    Args:
        db (Session): Database session.
        user_id (int): ID of the creating user.
        payload (LoanCreateSchema): Loan application data.
        
    Returns:
        Loan: The created loan.
    """

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id required")

    user = LoanRepository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid employee")

    loan_data = {
        "customer_name": payload.customer_name,
        "loan_amount": payload.loan_amount,
        "tenure_months": payload.tenure_months,
        "interest_rate": payload.interest_rate,
        "created_by": user_id
    }

    loan = LoanRepository.create_loan(db, loan_data)
    return loan


def update_loan(db: Session, loan_id: int, user_id: int, payload):
    """
    Business logic for updating a loan.
    
    Validates:
    - user_id is present.
    - loan exists.
    
    Args:
        db (Session): Database session.
        loan_id (int): ID of the loan to update.
        user_id (int): ID of the user performing update.
        payload (LoanUpdateSchema): Fields to update.
        
    Returns:
        Loan: The updated loan.
    """

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id required")

    loan = LoanRepository.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    update_data = payload.dict(exclude_unset=True)

    loan = LoanRepository.update_loan(db, loan, update_data)
    return loan


def delete_loan(db: Session, loan_id: int, user_id: int):
    """
    Business logic for deleting a loan.
    """

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id required")

    loan = LoanRepository.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    LoanRepository.delete_loan(db, loan)
