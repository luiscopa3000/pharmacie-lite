from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TokenConfig:
    secret_key: str
    issuer: str
    audience: str
    algorithm: str
    expiration_minutes: int