import json
import psycopg2
from typing import Any, Optional
from app.shared.domain.interfaces.database import ISqlDatabase
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.models.errors import StandardizedError
from app.shared.decorators import (
    generic_error_handler,
    postgres_error_handler,
)


class PostgresDatabase(ISqlDatabase):
    """
    Implementación PostgreSQL de ISqlDatabase.
    Maneja ejecución de queries directas y dinámicas vía funciones SQL.
    """

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        logger: ILogger,
    ) -> None:
        if not all([host, database, user, password]):
            raise StandardizedError(
                error="Missing database credentials",
                user_message="Error interno en la base de datos.",
                http_status=500,
                error_type="DATABASE",
            )

        self.logger = logger
        self._host = host
        self._database = database
        self._user = user
        self._password = password


    def _get_connection(self):
        return psycopg2.connect(
            host=self._host,
            database=self._database,
            user=self._user,
            password=self._password,
        )

    @generic_error_handler()
    @postgres_error_handler()
    def execute_query_string(
        self,
        query_string: str,
        params: tuple | None = None,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        current_user_id: Optional[str] = None,
    ) -> Any:
        """
        Ejecuta una query SQL directa.
        Retorna resultados si existen, caso contrario None.
        """

        params = params or ()

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                if current_user_id is not None:
                    cursor.execute("SET LOCAL app.current_user_id = %s;", (current_user_id,))
                
                cursor.execute(query_string, params)

                try:
                    return cursor.fetchall()
                except psycopg2.ProgrammingError:
                    return None

    @generic_error_handler()
    @postgres_error_handler()
    def execute_query_dynamic(
        self,
        query_name: str,
        obj: Any,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        current_user_id: Optional[str] = None,
    ) -> list[Any]:
        """
        Ejecuta una función PostgreSQL que recibe un JSONB.
        """

        if obj is None:
            raise StandardizedError(
                error="Missing payload",
                user_message="No se proporcionaron datos para ejecutar la consulta.",
                http_status=400,
                error_type="VALIDATION",
            )

        parameters = self._normalize_payload(obj)

        payload_json = json.dumps(
            parameters,
            ensure_ascii=False,
            separators=(",", ":"),
            default=str,
        )

        sql = f"SELECT {query_name}(%s::jsonb);"

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                if current_user_id is not None:
                    cursor.execute("SET LOCAL app.current_user_id = %s;", (current_user_id,))
                    
                cursor.execute(sql, (payload_json,))
                return cursor.fetchall()

    @staticmethod
    def _normalize_payload(obj: Any) -> dict:
        if isinstance(obj, dict):
            return obj

        if hasattr(obj, "parameters"):
            return obj.parameters

        if hasattr(obj, "dict") and callable(obj.dict):
            return obj.dict()

        if hasattr(obj, "__dict__"):
            return vars(obj)

        raise StandardizedError(
            error="Invalid payload type",
            user_message="Los datos enviados no son válidos.",
            http_status=400,
            error_type="VALIDATION",
        )