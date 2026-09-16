from datetime import datetime
from typing import Optional

from app.shared.decorators import generic_error_handler
from app.shared.domain.models.errors import StandardizedError
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.database import ISqlDatabase

from app.auth.domain.constants.db_operations import DbOperations
from app.auth.domain.models.user_password import UserPassword
from app.auth.domain.interfaces.repositories import IAuthByPasswordRepository


def _parse_bloqueado_hasta(value) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return None
    return None


class AuthByPasswordRepository(IAuthByPasswordRepository):
    def __init__(self, logger: ILogger, database: ISqlDatabase) -> None:
        self.logger = logger
        self.database = database

    @generic_error_handler()
    def get_user_for_login(
        self,
        username: Optional[str] = None,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> Optional[UserPassword]:
        raw = self.database.execute_query_dynamic(
            query_name=DbOperations.AUTH_BY_PASSWORD.value,
            obj={"username": username},
            request_id=request_id,
            host=host,
        )
        if not raw or not raw[0]:
            return None

        row = raw[0][0]
        if not row or not isinstance(row, dict):
            return None

        id_user = row.get("id_usuario")
        id_user_password = row.get("id_usuario_password")
        if id_user is None or id_user_password is None:
            return None
            
        return UserPassword(
            id_user=int(id_user),
            id_user_password=int(id_user_password),
            username=row.get("username") or "",
            email=row.get("correo") or "",
            password_hash=row.get("password_hash") or "",
            intentos_fallidos=int(row.get("intentos_fallidos") or 0),
            bloqueado_hasta=_parse_bloqueado_hasta(row.get("bloqueado_hasta")),
            max_intentos=int(row.get("max_intentos") or 5),
            bloqueo_minutos=int(row.get("bloqueo_minutos") or 15),
        )

    @generic_error_handler()
    def execute(
        self,
        user: Optional[str] = None,
        email: Optional[str] = None,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> UserPassword:
        user_password = self.get_user_for_login(
            user=user, email=email, request_id=request_id, host=host
        )
        if not user_password:
            raise StandardizedError(
                error="INVALID_CREDENTIALS",
                error_code="UNAUTHORIZED",
                error_type="AUTH_ERROR",
                user_message="Credenciales inválidas",
                http_status=401,
            )
        return user_password