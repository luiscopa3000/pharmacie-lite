from fastapi import APIRouter
from .auth_router import auth_router
from .users_router import users_router
from .roles_router import roles_router

def include_identity_routers(router: APIRouter) -> None:
    router.include_router(auth_router)
    router.include_router(users_router)
    router.include_router(roles_router)
