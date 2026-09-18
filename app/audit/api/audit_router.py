from fastapi import APIRouter
from .routers import audit_router
audit_api=APIRouter(prefix="/audit")
audit_api.include_router(audit_router)
