from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class UserCreateRequest:
    username: str
    password: str
    role_code: str
    first_name: str
    last_name: Optional[str] = None
    record_status: str = "ACTIVE"
    must_change_password: bool = True


@dataclass(slots=True)
class UserUpdateRequest:
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
