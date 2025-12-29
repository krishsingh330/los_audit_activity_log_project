from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.logger import logger

from app.models import Payment
from app.repositories.payment_repository import PaymentRepository
from app.schemas.schemas import PaymentCreate, PaymentUpdate


class PaymentService:
    """
    Service logic for handling payments.
    """

    @staticmethod
    async def create_payment(
        session: AsyncSession,
        payload: PaymentCreate,
        user_id: int
    ):
        """
        Create a new payment record.
        
        Args:
            session (AsyncSession): Database session.
            payload (PaymentCreate): Payment data.
            user_id (int): User creating the payment (unused but kept for consistency/extensions).
            
        Returns:
            Payment: Created payment object.
        """
        try:
            payment = Payment(**payload.dict())
            return await PaymentRepository.create(session, payment)
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    async def update_payment(
        session: AsyncSession,
        payment_id: int,
        payload: PaymentUpdate,
        user_id: int
    ):
        """
        Update an existing payment.
        
        Args:
            session (AsyncSession): Database session.
            payment_id (int): ID of the payment to update.
            payload (PaymentUpdate): Data to update.
            user_id (int): User performing the update.
            
        Returns:
            Payment: Updated payment object.
            
        Raises:
            HTTPException: 404 if payment not found.
        """
        try:
            payment = await PaymentRepository.get_by_id(session, payment_id)

            if not payment:
                raise HTTPException(status_code=404, detail="Payment not found")

            for key, value in payload.dict(exclude_unset=True).items():
                setattr(payment, key, value)

            payment = await PaymentRepository.update(session, payment)
            return payment
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error updating payment {payment_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
