from typing import Any

from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.database import ISqlDatabase
from app.shared.domain.models.errors import StandardizedError
from app.catalog.domain.constants import CatalogDbOperations
from app.catalog.domain.interfaces import ICatalogRepository

_SQLSTATE_HTTP = {
    "PH400": (400, "BAD_REQUEST"),
    "PH401": (401, "UNAUTHORIZED"),
    "PH403": (403, "FORBIDDEN"),
    "PH404": (404, "NOT_FOUND"),
    "PH409": (409, "CONFLICT"),
    "PH422": (422, "UNPROCESSABLE_ENTITY"),
}


def _extract_sqlstate(exc: Exception) -> str | None:
    for attr in ("sqlstate", "pgcode"):
        value = getattr(exc, attr, None)
        if value:
            return str(value)
    orig = getattr(exc, "orig", None)
    if orig is not None:
        for attr in ("sqlstate", "pgcode"):
            value = getattr(orig, attr, None)
            if value:
                return str(value)
    return None


def _first_json(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    current = raw
    for _ in range(4):
        if isinstance(current, (list, tuple)) and current:
            current = current[0]
            continue
        break
    if isinstance(current, dict):
        if len(current) == 1:
            only = next(iter(current.values()))
            if isinstance(only, dict):
                return only
        return current
    raise StandardizedError(
        error="DB_INVALID_RESPONSE",
        error_code="INTERNAL_SERVER_ERROR",
        error_type="DATABASE_ERROR",
        user_message="La base de datos devolvió una respuesta no válida.",
        http_status=500,
    )


class CatalogRepository(ICatalogRepository):
    def __init__(self, logger: ILogger, database: ISqlDatabase) -> None:
        self.logger = logger
        self.database = database

    def execute(
        self,
        operation: CatalogDbOperations,
        payload: dict[str, Any],
        *,
        request_id: str | None = None,
        host: str | None = None,
        current_user_id: str | None = None,
    ) -> dict[str, Any]:
        try:
            raw = self.database.execute_query_dynamic(
                query_name=operation.value,
                obj=payload,
                request_id=request_id,
                host=host,
                current_user_id=current_user_id,
            )
            return _first_json(raw)
        except StandardizedError:
            raise
        except Exception as exc:
            sqlstate = _extract_sqlstate(exc)
            if sqlstate in _SQLSTATE_HTTP:
                http_status, error_code = _SQLSTATE_HTTP[sqlstate]
                message = str(exc).split("\n", 1)[0] or "La operación fue rechazada."
                raise StandardizedError(
                    error=sqlstate,
                    error_code=error_code,
                    error_type="BUSINESS_RULE_ERROR",
                    user_message=message,
                    http_status=http_status,
                ) from exc
            raise StandardizedError(
                error="DB_ERROR",
                error_code="INTERNAL_SERVER_ERROR",
                error_type="DATABASE_ERROR",
                user_message="Ocurrió un error interno al ejecutar la operación.",
                http_status=500,
            ) from exc
