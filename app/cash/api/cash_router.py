from fastapi import APIRouter
from .routers import cash_router

cash_api = APIRouter(prefix="/cash")
cash_api.include_router(cash_router)
