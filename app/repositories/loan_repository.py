from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import Loan
from app.models import User


class LoanRepository:
    """
    Repository for managing Loan persistence.
    """

    @staticmethod
    async def get_all_loans(session: AsyncSession):
        """
        Repository function to fetch all loan records.
        No filters, no validation, no business rules.
        
        Args:
            session (AsyncSession): Database session.
            
        Returns:
            list[Loan]: List of all loans.
        """
        try:
            statement = select(Loan)
            result = await session.exec(statement)
            return result.all()
        except Exception as e:
            raise e

    @staticmethod
    async def get_loan_by_id(session: AsyncSession, loan_id: int):
        """
        Fetch a single loan by primary key.
        
        Args:
            session (AsyncSession): Database session.
            loan_id (int): The ID of the loan to fetch.
            
        Returns:
            Loan | None: The loan object if found, else None.
        """
        try:
            statement = select(Loan).where(Loan.id == loan_id)
            result = await session.exec(statement)
            return result.first()
        except Exception as e:
            raise e

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int):
        """
        Fetch user/employee who performs the action.
        Used to validate created_by / updated_by.
        
        Args:
            session (AsyncSession): Database session.
            user_id (int): The ID of the user.
            
        Returns:
            User | None: The user object if found, else None.
        """
        try:
            statement = select(User).where(User.id == user_id)
            result = await session.exec(statement)
            return result.first()
        except Exception as e:
            raise e

    @staticmethod
    async def create_loan(session: AsyncSession, loan_data: dict):
        """
        Create and persist a new loan record.
        Assumes data is already validated by service layer.
        
        Args:
            session (AsyncSession): Database session.
            loan_data (dict): Dictionary containing valid loan data.
            
        Returns:
            Loan: The created loan object.
        """
        try:
            loan = Loan(**loan_data)

            session.add(loan)
            await session.commit()
            await session.refresh(loan)

            return loan
        except Exception as e:
            raise e

    @staticmethod
    async def update_loan(session: AsyncSession, loan: Loan, update_data: dict):
        """
        Update existing loan object with new values.
        
        Args:
            session (AsyncSession): Database session.
            loan (Loan): The existing loan object to update.
            update_data (dict): Dictionary of fields to update.
            
        Returns:
            Loan: The updated loan object.
        """
        try:
            for key, value in update_data.items():
                setattr(loan, key, value)

            session.add(loan)
            await session.commit()
            await session.refresh(loan)

            return loan
        except Exception as e:
            raise e

    @staticmethod
    async def delete_loan(session: AsyncSession, loan: Loan):
        """
        Delete loan record from database.
        
        Args:
            session (AsyncSession): Database session.
            loan (Loan): The loan object to delete.
        """
        try:
            await session.delete(loan)
            await session.commit()
        except Exception as e:
            raise e
