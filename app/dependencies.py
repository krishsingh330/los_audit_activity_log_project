from fastapi import Request
from sqlalchemy.orm import Session

def get_db(request: Request) -> Session:
    """
    Retrieves the database session from the request state.
    
    This dependency is used by routers to access the database.
    The session is initialized and attached to the request by the ActivityLoggerMiddleware.
    
    Args:
        request (Request): The incoming HTTP request.
        
    Returns:
        Session: The SQLAlchemy database session.
    """

    # Extract the session from request state
    db: Session = request.state.db

    # Return active session to router/service
    return db
