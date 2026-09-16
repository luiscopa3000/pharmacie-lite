from fastapi import APIRouter
from app.auth.api.routers import include_auth_routers

# Tag del padre desactivado: la documentación OpenAPI debe mostrar solo las secciones de los routers hijo (Auth, Users), evitando una sección genérica "Security Access" duplicada.
auth_api = APIRouter(
    prefix="/auth",
    # tags=["Security Access"],
)

include_auth_routers(auth_api)