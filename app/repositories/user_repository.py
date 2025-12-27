from sqlmodel import Session, select
from app.models import User


class UserRepository:
    """
    Repository for managing User persistence.
    """

    @staticmethod
    def get_by_email(session: Session, email: str):
        """
        Retrieves a user by their email address.
        
        Args:
            session (Session): Database session.
            email (str): The email to search for.
            
        Returns:
            User | None: The user object if found, else None.
        """
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def create(session: Session, user: User):
        """
        Persists a new user record.
        
        Args:
            session (Session): Database session.
            user (User): The user object to save.
            
        Returns:
            User: The refreshed user object with ID.
        """
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
