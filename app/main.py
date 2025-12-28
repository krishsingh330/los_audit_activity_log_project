from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routers import api_router
from app.middleware.logging_middleware import loguru_logging_middleware
from app.middleware import ActivityLoggerMiddleware
from app.core.logger import setup_logger

# Create FastAPI app instance
# Title and version will appear in the Swagger UI
app = FastAPI(
    title="Loan Management System with Automatic Audit",
    version="1.0.0"
)

# Initialize Database
# This command ensures that all tables defined in SQLModel models are created
# in the database if they do not already exist.
SQLModel.metadata.create_all(engine)

# Initialize Application Logging
# Sets up Loguru logger for console and file output
setup_logger()

# Register middleware
# ActivityLoggerMiddleware captures user actions for audit trails
app.add_middleware(ActivityLoggerMiddleware)
# loguru_logging_middleware logs detailed HTTP request and response information
app.middleware("http")(loguru_logging_middleware)

# Register API routes
# Include all routes from the api_router with the prefix /api/v1
app.include_router(api_router, prefix="/api/v1")


@app.get("/api/v1")
def root():
    """
    Root endpoint for the API.
    
    Returns:
        dict: A welcome message indicating the service is running.
    """
    return {
        "message": "Loan Management System with Automatic Audit",
    }

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Status of the application, used by monitoring systems.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    # Allow running the file directly for development purposes
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
