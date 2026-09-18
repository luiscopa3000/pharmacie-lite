from typing import Literal, Optional
from pydantic import BaseModel, Field

RoleCode = Literal["ADMINISTRADOR", "VENDEDOR_CAJA", "ALMACEN"]
RecordStatus = Literal["ACTIVE", "INACTIVE"]


class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)
    role_code: RoleCode
    first_name: str = Field(..., min_length=1, max_length=120)
    last_name: Optional[str] = Field(default=None, max_length=120)
    record_status: RecordStatus = "ACTIVE"
    must_change_password: bool = True


class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=100)
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    last_name: Optional[str] = Field(default=None, max_length=120)


class UserStatusSchema(BaseModel):
    record_status: RecordStatus


class PasswordResetSchema(BaseModel):
    temporary_password: str = Field(..., min_length=8, max_length=128)
