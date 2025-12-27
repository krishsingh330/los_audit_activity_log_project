from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from app.services.auth_service import AuthService
from app.schemas.schemas import UserRegisterSchema, UserLoginSchema
from app.dependencies import get_db
router = APIRouter(prefix="/auth", tags=["Auth"])


# def get_db(request: Request) -> Session:
#     """Dependency: Extract database session from request state."""
#     return request.state.db


@router.post("/register")
def register_user(
    data: UserRegisterSchema,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        data (UserRegisterSchema): User registration details.
        
    Returns:
        dict: Success message and user info.
    """
    user = AuthService.register_user(db, data)
    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "role": user.role
    }


@router.post("/login")
def login_user(
    data: UserLoginSchema,
    db: Session = Depends(get_db)
):
    """
    Login a user.
    
    Args:
        data (UserLoginSchema): User login credentials.
        
    Returns:
        dict: Success message and user info.
    """
    user = AuthService.login_user(db, data)
    return {
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }
