from sqlmodel import Session, select
from app.models import Payment


class PaymentRepository:
    """
    Repository for managing Payment persistence.
    """

    @staticmethod
    def create(session: Session, payment: Payment):
        """
        Persists a new payment record.
        
        Args:
            session (Session): Database session.
            payment (Payment): The payment object to save.
            
        Returns:
            Payment: The refreshed payment object with ID.
        """
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment

    @staticmethod
    def get_by_id(session: Session, payment_id: int):
        """
        Retrieves a payment by its ID.
        
        Args:
            session (Session): Database session.
            payment_id (int): The ID of the payment.
            
        Returns:
            Payment | None: The payment object if found, else None.
        """
        statement = select(Payment).where(Payment.id == payment_id)
        return session.exec(statement).first()

    @staticmethod
    def update(session: Session, payment: Payment):
        """
        Updates an existing payment record.
        
        Args:
            session (Session): Database session.
            payment (Payment): The modified payment object.
            
        Returns:
            Payment: The updated payment object.
        """
        session.add(payment)
        session.commit()
        return payment
