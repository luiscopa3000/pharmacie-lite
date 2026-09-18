from fastapi import APIRouter
from app.identity.api.routers import include_identity_routers

identity_api = APIRouter(prefix="/identity")
include_identity_routers(identity_api)
