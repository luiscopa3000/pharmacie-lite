from fastapi import APIRouter
from app.catalog.api.routers import include_catalog_routers

catalog_api = APIRouter(prefix="/catalog")
include_catalog_routers(catalog_api)
