from fastapi import APIRouter
from app.routers.loans_router import router as loan_router
from app.routers.auth_routes import router as auth_router
from app.routers.audit_router import router as audit_router
from app.routers.payment_routes import router as payment_router
from app.routers.activity_routes import router as activity_router
api_router = APIRouter()

api_router.include_router(loan_router)
api_router.include_router(auth_router)
api_router.include_router(audit_router)
api_router.include_router(payment_router)
api_router.include_router(activity_router)