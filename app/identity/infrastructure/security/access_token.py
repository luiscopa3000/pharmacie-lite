from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from app.identity.domain.interfaces.token_service import IAccessTokenService
from app.identity.domain.models.token import AccessTokenClaims, IssuedAccessToken, TokenConfig


class InvalidAccessToken(Exception):
    pass


class AccessTokenService(IAccessTokenService):
    """Genera y verifica JWT. Los roles/permisos NO se confían al JWT."""

    def __init__(self, config: TokenConfig) -> None:
        self.config = config

    def issue(self, subject: int) -> IssuedAccessToken:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=self.config.expiration_minutes)
        session_id = str(uuid4())
        payload = {
            "sub": str(subject),
            "jti": session_id,
            "typ": "access",
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "iat": now,
            "nbf": now,
            "exp": expires_at,
        }
        token = jwt.encode(payload, self.config.secret_key, algorithm=self.config.algorithm)
        return IssuedAccessToken(
            token=token,
            session_id=session_id,
            subject=subject,
            expires_at=expires_at,
        )

    def verify(self, token: str) -> AccessTokenClaims:
        try:
            payload = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm],
                issuer=self.config.issuer,
                audience=self.config.audience,
                options={"require": ["sub", "jti", "iss", "aud", "iat", "nbf", "exp"]},
            )
            if payload.get("typ") != "access":
                raise InvalidAccessToken("Tipo de token inválido")
            subject = int(payload["sub"])
            session_id = str(payload["jti"])
            expires_at_raw = payload["exp"]
            expires_at = datetime.fromtimestamp(float(expires_at_raw), tz=timezone.utc)
            return AccessTokenClaims(subject=subject, session_id=session_id, expires_at=expires_at)
        except (jwt.PyJWTError, ValueError, TypeError, KeyError) as exc:
            raise InvalidAccessToken("Token inválido o expirado") from exc
