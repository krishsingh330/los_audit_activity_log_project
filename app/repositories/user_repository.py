from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import User


class UserRepository:
    """
    Repository for managing User persistence.
    """

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str):
        """
        Retrieves a user by their email address.
        
        Args:
            session (AsyncSession): Database session.
            email (str): The email to search for.
            
        Returns:
            User | None: The user object if found, else None.
        """
        try:
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            return result.first()
        except Exception as e:
            raise e

    @staticmethod
    async def create(session: AsyncSession, user: User):
        """
        Persists a new user record.
        
        Args:
            session (AsyncSession): Database session.
            user (User): The user object to save.
            
        Returns:
            User: The refreshed user object with ID.
        """
        try:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        except Exception as e:
            raise e
