from typing import Any
from pydantic import BaseModel, Field


class LoginRequestSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=256)


class ChangePasswordSchema(BaseModel):
    current_password: str = Field(..., min_length=1, max_length=256)
    new_password: str = Field(..., min_length=8, max_length=128)


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: Any
    must_change_password: bool = False
    user: dict[str, Any] = {}
    permissions: list[Any] = []
