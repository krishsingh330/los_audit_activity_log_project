from fastapi import APIRouter, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.schemas import PaymentCreate, PaymentUpdate
from app.services.payment_service import PaymentService
from app.dependencies import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("")
async def create_payment(
    payload: PaymentCreate,
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    """
    Record a new payment.
    
    Args:
        payload (PaymentCreate): Payment details.
        user_id (int): ID of the user creating the payment.
        
    Returns:
        Payment: The created payment record.
    """
    return await PaymentService.create_payment(session, payload, user_id)


@router.put("/{payment_id}")
async def update_payment(
    payment_id: int,
    payload: PaymentUpdate,
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    """
    Update a payment status/amount.
    
    Args:
        payment_id (int): Payment ID.
        payload (PaymentUpdate): Data to update.
        user_id (int): User performing the update.
        
    Returns:
        dict: Success message.
    """
    await PaymentService.update_payment(session, payment_id, payload, user_id)
    return {"message": "Payment updated successfully"}
