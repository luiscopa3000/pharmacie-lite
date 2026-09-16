from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class PharmaciesDbConfig:
    pharmacies_db_host: str
    pharmacies_db_name: str
    pharmacies_db_user: str
    pharmacies_db_password: str