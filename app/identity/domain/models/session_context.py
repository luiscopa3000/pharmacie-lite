from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SessionContext:
    """Contexto autenticado obtenido después de validar JWT + sesión en BD."""

    user_id: int
    session_id: str
    user: dict[str, Any]
    permissions: list[Any]
    must_change_password: bool = False
