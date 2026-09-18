from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class TokenConfig:
    secret_key: str
    issuer: str
    audience: str
    algorithm: str
    expiration_minutes: int


@dataclass(slots=True, frozen=True)
class IssuedAccessToken:
    token: str
    session_id: str
    subject: int
    expires_at: datetime


@dataclass(slots=True, frozen=True)
class AccessTokenClaims:
    subject: int
    session_id: str
    expires_at: datetime
