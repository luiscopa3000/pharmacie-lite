from fastapi import APIRouter

from .routers import stock_router, movements_router, lots_router


inventory_api = APIRouter(prefix="/inventory")
inventory_api.include_router(stock_router)
inventory_api.include_router(movements_router)
inventory_api.include_router(lots_router)
