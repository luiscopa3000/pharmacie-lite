from typing import Optional

from app.shared.decorators import generic_error_handler
from app.shared.domain.models.errors import StandardizedError
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.database import ISqlDatabase

from app.auth.domain.constants.db_operations import DbOperations
from app.auth.domain.interfaces.repositories import IRegisterUserRepository


class RegisterUserRepository(IRegisterUserRepository):
    def __init__(self, logger: ILogger, database: ISqlDatabase) -> None:
        self.logger = logger
        self.database = database

    @generic_error_handler()
    def execute(
        self,
        role_id: int,
        username: str,
        email: str,
        password_hash: str,
        full_name: str,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        current_user_id: Optional[str] = None,
    ) -> int:
        payload = {
            "role_id": role_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "full_name": full_name
        }

        raw = self.database.execute_query_dynamic(
            query_name=DbOperations.REGISTER_USER.value,
            obj=payload,
            request_id=request_id,
            host=host,
            current_user_id=current_user_id,
        )

        if not raw or not raw[0]:
            raise StandardizedError(
                error="DB_ERROR",
                error_code="INTERNAL_SERVER_ERROR",
                error_type="DATABASE_ERROR",
                user_message="Error al registrar el usuario en la base de datos.",
                http_status=500,
            )

        row = raw[0][0]
        if not row or not isinstance(row, dict) or not row.get("success"):
            raise StandardizedError(
                error="DB_ERROR",
                error_code="INTERNAL_SERVER_ERROR",
                error_type="DATABASE_ERROR",
                user_message="La base de datos retornó un estado de fallo.",
                http_status=500,
            )

        data = row.get("data", {})
        id_user = data.get("id_user")
        
        if id_user is None:
            raise StandardizedError(
                error="DB_ERROR",
                error_code="INTERNAL_SERVER_ERROR",
                error_type="DATABASE_ERROR",
                user_message="No se pudo obtener el ID del usuario creado.",
                http_status=500,
            )
            
        return int(id_user)
