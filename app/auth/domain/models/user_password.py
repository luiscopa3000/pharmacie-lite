from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class UserPassword:
    id_user: int
    id_user_password: int
    username: str
    email: str
    password_hash: str
    # Bloqueo por intentos (get_user_for_login)
    intentos_fallidos: int = 0
    bloqueado_hasta: Optional[datetime] = None
    max_intentos: int = 5
    bloqueo_minutos: int = 15