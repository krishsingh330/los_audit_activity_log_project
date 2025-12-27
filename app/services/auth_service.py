from fastapi import HTTPException
from sqlmodel import Session

from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.schemas import UserRegisterSchema, UserLoginSchema


class AuthService:
    """
    Service for checking user credentials and managing registration.
    """

    @staticmethod
    def register_user(session: Session, data: UserRegisterSchema):
        """
        Registers a new user in the system.
        
        Checks if email already exists before creating.
        
        Args:
            session (Session): Database session.
            data (UserRegisterSchema): Registration data.
            
        Returns:
            User: The created user.
            
        Raises:
            HTTPException: If email is already registered.
        """
        existing_user = UserRepository.get_by_email(session, data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            email=data.email,
            password=data.password,
            role=data.role
        )

        return UserRepository.create(session, user)

    @staticmethod
    def login_user(session: Session, data: UserLoginSchema):
        """
        Authenticates a user.
        
        Args:
            session (Session): Database session.
            data (UserLoginSchema): Login credentials.
            
        Returns:
            User: The authenticated user.
            
        Raises:
            HTTPException: If credentials are invalid.
        """
        user = UserRepository.get_by_email(session, data.email)

        if not user or user.password != data.password:
            raise HTTPException(status_code=400, detail="Invalid email or password")

        return user
