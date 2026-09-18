from fastapi import APIRouter
from .routers import sales_router


sales_api = APIRouter()
sales_api.include_router(sales_router, prefix="/sales")