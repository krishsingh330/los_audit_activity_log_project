from sqlalchemy.orm import Session
from app.models import Loan
from app.models import User


class LoanRepository:
    """
    Repository for managing Loan persistence.
    """

    @staticmethod
    def get_all_loans(db: Session):
        """
        Repository function to fetch all loan records.
        No filters, no validation, no business rules.
        
        Args:
            db (Session): Database session.
            
        Returns:
            list[Loan]: List of all loans.
        """
        loans = db.query(Loan).all()
        return loans

    @staticmethod
    def get_loan_by_id(db: Session, loan_id: int):
        """
        Fetch a single loan by primary key.
        
        Args:
            db (Session): Database session.
            loan_id (int): The ID of the loan to fetch.
            
        Returns:
            Loan | None: The loan object if found, else None.
        """
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        return loan

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """
        Fetch user/employee who performs the action.
        Used to validate created_by / updated_by.
        
        Args:
            db (Session): Database session.
            user_id (int): The ID of the user.
            
        Returns:
            User | None: The user object if found, else None.
        """
        user = db.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def create_loan(db: Session, loan_data: dict):
        """
        Create and persist a new loan record.
        Assumes data is already validated by service layer.
        
        Args:
            db (Session): Database session.
            loan_data (dict): Dictionary containing valid loan data.
            
        Returns:
            Loan: The created loan object.
        """
        loan = Loan(**loan_data)

        db.add(loan)
        db.commit()
        db.refresh(loan)

        return loan

    @staticmethod
    def update_loan(db: Session, loan: Loan, update_data: dict):
        """
        Update existing loan object with new values.
        
        Args:
            db (Session): Database session.
            loan (Loan): The existing loan object to update.
            update_data (dict): Dictionary of fields to update.
            
        Returns:
            Loan: The updated loan object.
        """
        for key, value in update_data.items():
            setattr(loan, key, value)

        db.commit()
        db.refresh(loan)

        return loan

    @staticmethod
    def delete_loan(db: Session, loan: Loan):
        """
        Delete loan record from database.
        
        Args:
            db (Session): Database session.
            loan (Loan): The loan object to delete.
        """
        db.delete(loan)
        db.commit()
