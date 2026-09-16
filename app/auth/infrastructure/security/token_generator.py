import jwt
from uuid import uuid4
from typing import Any, Dict
from datetime import datetime, timedelta, timezone

from app.auth.domain.models.token_config import TokenConfig
from app.auth.domain.interfaces.token_generator import ITokenGenerator


class TokenGenerator(ITokenGenerator):
    """
    Servicio de infraestructura encargado de generar tokens de acceso firmados
    para procesos de autenticación.

    El token generado cumple con la especificación JWT (RFC 7519) e incluye
    claims estándar de seguridad para identificar al usuario autenticado,
    validar el emisor, restringir el uso del token, controlar su vigencia
    y prevenir ataques de reutilización.
    """

    def __init__(self, token_config: TokenConfig) -> None:
        """
        Inicializa el generador de tokens con los parámetros de seguridad
        necesarios para la firma y validación del JWT.
        """
        self.token_config = token_config

    def generate(self, subject: str, extra_payload: Dict[str, Any] | None = None) -> str:
        """
        Genera un token de acceso firmado para un sujeto autenticado.

        El parámetro `subject` representa el identificador único e inmutable
        del usuario autenticado dentro del sistema. Este valor se asigna al
        claim `sub` del JWT y se utiliza como referencia principal para
        identificar al usuario en cada solicitud autenticada.

        El token incluye los siguientes claims estándar:
        - sub: Identificador único del usuario autenticado.
        - iss: Emisor del token.
        - aud: Audiencia autorizada a consumir el token.
        - iat: Fecha y hora de emisión del token.
        - nbf: Fecha y hora a partir de la cual el token es válido.
        - exp: Fecha y hora de expiración del token.
        - jti: Identificador único del token para prevenir reutilización.

        :param subject: Identificador único del usuario autenticado.
        :param extra_payload: Información adicional opcional a incluir en el token.
        :return: Token JWT firmado y codificado.
        """
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "iss": self.token_config.issuer,
            "aud": self.token_config.audience,
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=self.token_config.expiration_minutes),
            "jti": str(uuid4()),
        }

        if extra_payload:
            payload.update(extra_payload)

        return jwt.encode(
            payload,
            self.token_config.secret_key,
            algorithm=self.token_config.algorithm,
        )