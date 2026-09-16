from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.shared.domain.models.configs import HasherConfig

# .env en la raíz de pharmacie-backend (independiente del cwd)
_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent


class HasherSetting(BaseSettings):
    hash_password_pepper: str = Field(
        ..., validation_alias=AliasChoices("HASH_PASSWORD_PEPPER")
    )

    model_config = SettingsConfigDict(
        env_file=str(_BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

def get_hasher_config() -> HasherConfig:
    s = HasherSetting()

    return HasherConfig(
        hash_password_pepper=s.hash_password_pepper
    )