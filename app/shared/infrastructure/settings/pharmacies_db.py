from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.shared.domain.models.configs import PharmaciesDbConfig

# .env en la raíz de pharmacie-backend (independiente del cwd)
_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent


class PharmaciesDbSetting(BaseSettings):
    pharmacies_db_host: str = Field(
        ..., validation_alias=AliasChoices("PHARMACIES_DB_HOST")
    )
    pharmacies_db_name: str = Field(
        ..., validation_alias=AliasChoices("PHARMACIES_DB_NAME")
    )
    pharmacies_db_user: str = Field(
        ..., validation_alias=AliasChoices("PHARMACIES_DB_USER")
    )
    pharmacies_db_password: str = Field(
        ..., validation_alias=AliasChoices("PHARMACIES_DB_PASSWORD")
    )

    model_config = SettingsConfigDict(
        env_file=str(_BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache()
def get_pharmacies_db_config() -> PharmaciesDbConfig:
    s = PharmaciesDbSetting()

    return PharmaciesDbConfig(
        pharmacies_db_host=s.pharmacies_db_host,
        pharmacies_db_name=s.pharmacies_db_name,
        pharmacies_db_user=s.pharmacies_db_user,
        pharmacies_db_password=s.pharmacies_db_password
    )