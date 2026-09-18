from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.identity.domain.models.token import TokenConfig

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent


class TokenSetting(BaseSettings):
    secret_key: str = Field(..., validation_alias=AliasChoices("JWT_SECRET_KEY"))
    issuer: str = Field(..., validation_alias=AliasChoices("JWT_ISSUER"))
    audience: str = Field(..., validation_alias=AliasChoices("JWT_AUDIENCE"))
    algorithm: str = Field(..., validation_alias=AliasChoices("JWT_ALGORITHM"))
    expiration_minutes: int = Field(
        ..., ge=1, le=1440, validation_alias=AliasChoices("JWT_EXPIRATION_MINUTES")
    )

    model_config = SettingsConfigDict(
        env_file=str(_BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


@lru_cache()
def get_token_config() -> TokenConfig:
    settings = TokenSetting()
    return TokenConfig(
        secret_key=settings.secret_key,
        issuer=settings.issuer,
        audience=settings.audience,
        algorithm=settings.algorithm,
        expiration_minutes=settings.expiration_minutes,
    )
