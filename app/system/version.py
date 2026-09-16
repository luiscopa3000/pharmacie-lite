import asyncio
import os

from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field

from __version__ import __release_date__, __version__

version_router = APIRouter()

class VersionResponse(BaseModel):
    version: str = Field(
        ...,
        example=__version__,
        description="Versión semántica de la aplicación"
    )
    fecha_lanzamiento: str = Field(
        ...,
        example=__release_date__,
        description="Fecha de lanzamiento de la aplicación"
    )
    entorno: str = Field(
        ...,
        example="development",
        description="Entorno de ejecución de la aplicación"
    )

@version_router.get(
    "/version",
    tags=["version"],
    response_model=VersionResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener versión de la aplicación",
    description="Devuelve la versión de la aplicación, la fecha de lanzamiento y el entorno de ejecución"
)
async def version_command(request: Request):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, execute_version)

def execute_version() -> dict:
    return {
        "version": __version__,
        "fecha_lanzamiento": __release_date__,
        "entorno": os.environ.get("ENVIRONMENT", "development"),
    }