from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.loan_repository import LoanRepository
from app.core.logger import logger


async def fetch_all_loans(session: AsyncSession):
    """
    Service layer wrapper for fetching all loans.
    """
    try:
        return await LoanRepository.get_all_loans(session)
    except Exception as e:
        logger.error(f"Error fetching loans: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def fetch_loan_by_id( session: AsyncSession, loan_id: int):
    """
    Fetch a loan by ID, validating its existence.
    
    Raises:
        HTTPException: 404 if loan not found.
    """
    try:
        loan = await LoanRepository.get_loan_by_id(session, loan_id)

        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        return loan
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching loan {loan_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def create_loan(session: AsyncSession, user_id: int, payload):
    """
    Business logic for creating a loan.
    
    Validates:
    - user_id is provided and corresponds to a valid user.
    
    Args:
        db (AsyncSession): Database session.
        user_id (int): ID of the creating user.
        payload (LoanCreateSchema): Loan application data.
        
    Returns:
        Loan: The created loan.
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id required")

        user = await LoanRepository.get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid employee")

        loan_data = {
            "customer_name": payload.customer_name,
            "loan_amount": payload.loan_amount,
            "tenure_months": payload.tenure_months,
            "interest_rate": payload.interest_rate,
            "created_by": user_id
        }

        loan = await LoanRepository.create_loan(session, loan_data)
        return loan
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating loan: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def update_loan(session: AsyncSession, loan_id: int, user_id: int, payload):
    """
    Business logic for updating a loan.
    
    Validates:
    - user_id is present.
    - loan exists.
    
    Args:
        db (AsyncSession): Database session.
        loan_id (int): ID of the loan to update.
        user_id (int): ID of the user performing update.
        payload (LoanUpdateSchema): Fields to update.
        
    Returns:
        Loan: The updated loan.
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id required")

        loan = await LoanRepository.get_loan_by_id(session, loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        update_data = payload.dict(exclude_unset=True)

        loan = await LoanRepository.update_loan(session, loan, update_data)
        return loan
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating loan {loan_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def delete_loan(session: AsyncSession, loan_id: int, user_id: int):
    """
    Business logic for deleting a loan.
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id required")

        loan = await LoanRepository.get_loan_by_id(session, loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        await LoanRepository.delete_loan(session, loan)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting loan {loan_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
