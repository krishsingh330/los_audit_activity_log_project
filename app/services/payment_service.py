from fastapi import HTTPException
from sqlmodel import Session

from app.models import Payment
from app.repositories.payment_repository import PaymentRepository
from app.schemas.schemas import PaymentCreate, PaymentUpdate


class PaymentService:
    """
    Service logic for handling payments.
    """

    @staticmethod
    def create_payment(
        session: Session,
        payload: PaymentCreate,
        user_id: int
    ):
        """
        Create a new payment record.
        
        Args:
            session (Session): Database session.
            payload (PaymentCreate): Payment data.
            user_id (int): User creating the payment (unused but kept for consistency/extensions).
            
        Returns:
            Payment: Created payment object.
        """
        payment = Payment(**payload.dict())
        return PaymentRepository.create(session, payment)

    @staticmethod
    def update_payment(
        session: Session,
        payment_id: int,
        payload: PaymentUpdate,
        user_id: int
    ):
        """
        Update an existing payment.
        
        Args:
            session (Session): Database session.
            payment_id (int): ID of the payment to update.
            payload (PaymentUpdate): Data to update.
            user_id (int): User performing the update.
            
        Returns:
            Payment: Updated payment object.
            
        Raises:
            HTTPException: 404 if payment not found.
        """
        payment = PaymentRepository.get_by_id(session, payment_id)

        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        for key, value in payload.dict(exclude_unset=True).items():
            setattr(payment, key, value)

        PaymentRepository.update(session, payment)
        return payment
