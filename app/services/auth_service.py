from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.logger import logger

from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.schemas import UserRegisterSchema, UserLoginSchema


class AuthService:
    """
    Service for checking user credentials and managing registration.
    """

    @staticmethod
    async def register_user(session: AsyncSession, data: UserRegisterSchema):
        """
        Registers a new user in the system.
        
        Checks if email already exists before creating.
        
        Args:
            session (AsyncSession): Database session.
            data (UserRegisterSchema): Registration data.
            
        Returns:
            User: The created user.
            
        Raises:
            HTTPException: If email is already registered.
        """
        try:
            existing_user = await UserRepository.get_by_email(session, data.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")

            user = User(
                email=data.email,
                password=data.password,
                role=data.role
            )

            return await UserRepository.create(session, user)
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    async def login_user(session: AsyncSession, data: UserLoginSchema):
        """
        Authenticates a user.
        
        Args:
            session (AsyncSession): Database session.
            data (UserLoginSchema): Login credentials.
            
        Returns:
            User: The authenticated user.
            
        Raises:
            HTTPException: If credentials are invalid.
        """
        try:
            user = await UserRepository.get_by_email(session, data.email)

            if not user or user.password != data.password:
                raise HTTPException(status_code=400, detail="Invalid email or password")

            return user
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
