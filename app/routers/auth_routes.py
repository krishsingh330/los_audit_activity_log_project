from fastapi import APIRouter, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.auth_service import AuthService
from app.schemas.schemas import UserRegisterSchema, UserLoginSchema
from app.dependencies import get_db
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register_user(
    data: UserRegisterSchema,
    session: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        data (UserRegisterSchema): User registration details.
        
    Returns:
        dict: Success message and user info.
    """
    user = await AuthService.register_user(session, data)
    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "role": user.role
    }


@router.post("/login")
async def login_user(
    data: UserLoginSchema,
    session: AsyncSession = Depends(get_db)
):
    """
    Login a user.
    
    Args:
        data (UserLoginSchema): User login credentials.
        
    Returns:
        dict: Success message and user info.
    """
    user = await AuthService.login_user(session, data)
    return {
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }
