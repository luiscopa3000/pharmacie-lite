from typing import Literal
from pydantic import BaseModel, Field


class RoleAssignSchema(BaseModel):
    role_code: Literal["ADMINISTRADOR", "VENDEDOR_CAJA", "ALMACEN"]


class PermissionCheckSchema(BaseModel):
    permission_code: str = Field(..., min_length=1, max_length=100)
