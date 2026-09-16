from pydantic import BaseModel, Field
from typing import ClassVar, Pattern
import re
from pydantic_core import PydanticCustomError

class RegisterUserResponse(BaseModel):
    """
    Modelo de respuesta para la creación de usuario.
    """
    id_user: int = Field(..., description="ID del usuario creado")


class RegisterUserRequest(BaseModel):
    """
    Modelo de petición para la creación de un nuevo usuario.
    """
    role_id: int = Field(..., description="ID del rol a asignar")
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6, max_length=64)
    full_name: str = Field(..., min_length=3, max_length=150)

    _safe_pattern: ClassVar[Pattern[str]] = re.compile(r"^[a-zA-Z0-9._@-]+$")

    @classmethod
    def validate_safe_characters(cls, value: str):
        if not cls._safe_pattern.match(value):
            raise PydanticCustomError(
                "invalid_characters",
                "El campo contiene caracteres no permitidos"
            )
        return value
