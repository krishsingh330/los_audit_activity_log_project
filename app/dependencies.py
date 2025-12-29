from fastapi import Request
from sqlmodel.ext.asyncio.session import AsyncSession

def get_db(request: Request) -> AsyncSession:
    """
    Retrieves the database session from the request state.
    
    This dependency is used by routers to access the database.
    The session is initialized and attached to the request by the ActivityLoggerMiddleware.
    
    Args:
        request (Request): The incoming HTTP request.
        
    Returns:
        AsyncSession: The SQLAlchemy database session.
    """

    # Extract the session from request state
    db: AsyncSession = request.state.db

    # Return active session to router/service
    return db
