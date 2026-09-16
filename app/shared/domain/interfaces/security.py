from typing import Protocol, runtime_checkable, Optional

@runtime_checkable
class IPasswordHasher(Protocol):
    """
    Servicio de infraestructura encargado de hashear y verificar contraseñas
    utilizando algoritmos criptográficos robustos, salt automático y pepper
    externo para mitigar compromisos de base de datos.
    """
    def hash(
        self, 
        password: str, 
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None
    ) -> str:
        ...

    def verify(
        self, 
        password: str, 
        password_hash: str,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> bool:
        ...