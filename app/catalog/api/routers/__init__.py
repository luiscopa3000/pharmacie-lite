from fastapi import APIRouter
from .products_router import products_router
from .presentations_router import presentations_router
from .categories_router import categories_router
from .references_router import references_router


def include_catalog_routers(router: APIRouter) -> None:
    router.include_router(products_router)
    router.include_router(presentations_router)
    router.include_router(categories_router)
    router.include_router(references_router)
