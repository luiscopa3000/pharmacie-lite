from typing import Optional
from dataclasses import dataclass

@dataclass(slots=True)
class LoginRequest:
    password: str
    user: Optional[str] = None
    email: Optional[str] = None