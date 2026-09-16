from fastapi import APIRouter
from .password_router import password_router
from .register_router import register_router

def include_auth_routers(router: APIRouter) -> None:
    router.include_router(password_router)
    router.include_router(register_router)