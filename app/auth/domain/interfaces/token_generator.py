from typing import Any, Dict, Protocol, runtime_checkable


@runtime_checkable
class ITokenGenerator(Protocol):
    """
    Servicio de infraestructura encargado de generar tokens de acceso firmados
    con claims estándar de seguridad para autenticación y control de sesión.
    """

    def generate(self, subject: str, extra_payload: Dict[str, Any] | None = None) -> str:
        ...