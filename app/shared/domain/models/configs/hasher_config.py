from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class HasherConfig:
    hash_password_pepper: str