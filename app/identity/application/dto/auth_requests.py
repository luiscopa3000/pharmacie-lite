from dataclasses import dataclass


@dataclass(slots=True)
class LoginRequest:
    username: str
    password: str


@dataclass(slots=True)
class ChangePasswordRequest:
    current_password: str
    new_password: str
