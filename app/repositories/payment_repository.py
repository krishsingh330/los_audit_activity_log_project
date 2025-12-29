from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import Payment


class PaymentRepository:
    """
    Repository for managing Payment persistence.
    """

    @staticmethod
    async def create(session: AsyncSession, payment: Payment):
        """
        Persists a new payment record.
        
        Args:
            session (AsyncSession): Database session.
            payment (Payment): The payment object to save.
            
        Returns:
            Payment: The refreshed payment object with ID.
        """
        try:
            session.add(payment)
            await session.commit()
            await session.refresh(payment)
            return payment
        except Exception as e:
            raise e

    @staticmethod
    async def get_by_id(session: AsyncSession, payment_id: int):
        """
        Retrieves a payment by its ID.
        
        Args:
            session (AsyncSession): Database session.
            payment_id (int): The ID of the payment.
            
        Returns:
            Payment | None: The payment object if found, else None.
        """
        try:
            statement = select(Payment).where(Payment.id == payment_id)
            result = await session.exec(statement)
            return result.first()
        except Exception as e:
            raise e

    @staticmethod
    async def update(session: AsyncSession, payment: Payment):
        """
        Updates an existing payment record.
        
        Args:
            session (AsyncSession): Database session.
            payment (Payment): The modified payment object.
            
        Returns:
            Payment: The updated payment object.
        """
        try:
            session.add(payment)
            await session.commit()
            await session.refresh(payment)
            return payment
        except Exception as e:
            raise e
