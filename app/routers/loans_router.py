from fastapi import APIRouter, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.schemas import LoanCreateSchema, LoanUpdateSchema
from app.services import loan_service
from app.dependencies import get_db

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.get("")
async def get_loans(session: AsyncSession = Depends(get_db)):
    """
    Fetch all loan applications.
    
    Args:
        session (AsyncSession): Database session.
        
    Returns:
        list[Loan]: List of all loans.
    """
    return await loan_service.fetch_all_loans(session)


@router.get("/{loan_id}")
async def get_loan(loan_id: int, session: AsyncSession = Depends(get_db)):
    """
    Fetch a single loan by ID.
    
    Args:
        loan_id (int): Primary key of the loan.
        session (AsyncSession): Database session.
        
    Returns:
        Loan: Loan object if found.
    """
    return await loan_service.fetch_loan_by_id(session, loan_id)


@router.post("")
async def create_loan(
    request: Request,
    user_id: int,
    data: LoanCreateSchema,
    session: AsyncSession = Depends(get_db)
):
    """
    Create a new loan application.
    
    Args:
        user_id (int): ID of the employee creating the loan.
        data (LoanCreateSchema): Loan details.
        
    Returns:
        dict: Confirmation message and created loan details.
    """
    loan = await loan_service.create_loan(session, user_id, data)

    return {
        "message": "Loan created successfully",
        "loan_id": loan.id,
        "customer_name": loan.customer_name,
        "loan_amount": loan.loan_amount,
        "status": loan.status
    }


@router.put("/{loan_id}")
async def update_loan(
    request: Request,
    loan_id: int,
    user_id: int,
    payload: LoanUpdateSchema,
    session: AsyncSession = Depends(get_db)
):
    """
    Update an existing loan.
    
    Args:
        loan_id (int): ID of the loan to update.
        user_id (int): ID of the user performing the update.
        payload (LoanUpdateSchema): Fields to update.
        
    Returns:
        dict: Confirmation message.
    """
    loan = await loan_service.update_loan(session, loan_id, user_id, payload)

    return {
        "message": "Loan updated successfully",
        "loan_id": loan.id
    }


@router.delete("/{loan_id}")
async def delete_loan(
    request: Request,
    loan_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    """
    Delete a loan application.
    
    Args:
        loan_id (int): ID of the loan to delete.
        user_id (int): ID of the user performing the deletion.
        
    Returns:
        dict: Confirmation message.
    """
    await loan_service.delete_loan(session, loan_id, user_id)

    return {
        "message": "Loan deleted successfully",
        "loan_id": loan_id
    }
