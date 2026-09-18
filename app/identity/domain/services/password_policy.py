import re

from app.shared.domain.models.errors import StandardizedError


class PasswordPolicy:
    """Política central del backend para contraseñas nuevas o temporales."""

    def __init__(self, min_length: int = 8, max_length: int = 128) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password: str) -> None:
        valid = (
            self.min_length <= len(password) <= self.max_length
            and re.search(r"[a-z]", password) is not None
            and re.search(r"[A-Z]", password) is not None
            and re.search(r"\d", password) is not None
            and re.search(r"[^A-Za-z0-9]", password) is not None
        )
        if not valid:
            raise StandardizedError(
                error="PASSWORD_POLICY",
                error_code="BAD_REQUEST",
                error_type="VALIDATION_ERROR",
                user_message=(
                    f"La contraseña debe tener entre {self.min_length} y {self.max_length} caracteres, "
                    "incluyendo mayúscula, minúscula, número y carácter especial."
                ),
                http_status=400,
            )
