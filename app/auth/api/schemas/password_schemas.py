from pydantic import BaseModel, Field, model_validator, field_validator
from pydantic_core import PydanticCustomError
from typing import Optional, ClassVar, Pattern
import re

class AuthResponse(BaseModel):
    """
    Modelo de respuesta para la autenticación.
    Contiene el token JWT generado tras una autenticación exitosa.
    """

    token: str = Field(..., description="Token JWT generado tras la autenticación")


class AuthPassword(BaseModel):
    """
    Modelo de autenticación que permite usar usuario o email, pero nunca ambos.
    La contraseña es obligatoria y solo acepta caracteres seguros.
    """

    username: Optional[str] = Field(default=None, min_length=3, max_length=50, alias="usuario")
    password: str = Field(..., min_length=6, max_length=64, alias="contrasena")

    _safe_pattern: ClassVar[Pattern[str]] = re.compile(r"^[a-zA-Z0-9._@-]+$")

    @field_validator("username" , "password")
    @classmethod
    def validate_safe_characters(cls, value: Optional[str]):
        if value is None:
            return value

        if not cls._safe_pattern.match(value):
            raise PydanticCustomError(
                "invalid_characters",
                "El campo contiene caracteres no permitidos"
            )

        return value

    @model_validator(mode="after")
    def validate_identity(self):
        if not self.username:
            raise PydanticCustomError(
                "identity_missing",
                "Debe proporcionar usuario"
            )

        return self