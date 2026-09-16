from typing import Optional
from passlib.context import CryptContext
from app.shared.domain.models.configs import HasherConfig
from app.shared.domain.interfaces.security import IPasswordHasher

class PasswordHasher(IPasswordHasher):
    """
    Servicio de infraestructura encargado de hashear y verificar contraseñas
    utilizando algoritmos criptográficos robustos, salt automático y pepper
    externo para mitigar compromisos de base de datos.
    """

    def __init__(self, hasher_config: HasherConfig) -> None:
        self.hasher_config = hasher_config
        self._context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

    def hash(
        self, 
        password: str,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> str:
        return self._context.hash(
            password + self.hasher_config.hash_password_pepper
        )

    def verify(
        self, 
        password: str, 
        password_hash: str,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> bool:
        return self._context.verify(
            password + self.hasher_config.hash_password_pepper, password_hash
        )