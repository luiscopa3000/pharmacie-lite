from fastapi import APIRouter
from .routers import reports_router
reports_api=APIRouter(prefix="/reports")
reports_api.include_router(reports_router)
