import functools
import inspect
import psycopg2
from typing import Any, Dict
from app.shared.domain.models.errors import StandardizedError

POSTGRES_ERROR_MAP: Dict[str, dict] = {
    "23505": {
        "message": "Ya existe un registro con la información proporcionada.",
        "http_status": 409,
        "type": "INTEGRITY"
    },
    "23503": {
        "message": "No es posible completar la operación porque uno de los datos no existe.",
        "http_status": 409,
        "type": "INTEGRITY"
    },
    "23502": {
        "message": "Faltan datos obligatorios para completar la operación.",
        "http_status": 400,
        "type": "VALIDATION"
    },
    "23514": {
        "message": "La información ingresada no cumple con los requisitos establecidos.",
        "http_status": 400,
        "type": "VALIDATION"
    },
    "22001": {
        "message": "Uno de los datos ingresados supera el límite permitido.",
        "http_status": 400,
        "type": "VALIDATION"
    },
    "22003": {
        "message": "Uno de los valores ingresados no es válido.",
        "http_status": 400,
        "type": "VALIDATION"
    },
    "22P02": {
        "message": "El formato de la información ingresada no es válido.",
        "http_status": 400,
        "type": "VALIDATION"
    },
    "22007": {
        "message": "El formato de fecha u hora ingresado no es válido.",
        "http_status": 400,
        "type": "VALIDATION"
    },
    "22012": {
        "message": "No fue posible procesar la operación solicitada.",
        "http_status": 400,
        "type": "LOGIC"
    },
    "40001": {
        "message": "La operación no pudo completarse. Por favor, intente nuevamente.",
        "http_status": 409,
        "type": "TRANSACTION"
    },
    "40P01": {
        "message": "La operación no pudo completarse en este momento. Intente nuevamente.",
        "http_status": 409,
        "type": "TRANSACTION"
    },
    "42501": {
        "message": "No cuenta con autorización para realizar esta operación.",
        "http_status": 403,
        "type": "SECURITY"
    },
    "28P01": {
        "message": "No fue posible validar las credenciales de acceso.",
        "http_status": 401,
        "type": "SECURITY"
    },
    "42601": {
        "message": "Ocurrió un error al procesar la solicitud.",
        "http_status": 500,
        "type": "INTERNAL"
    },
    "42883": {
        "message": "La operación solicitada no está disponible.",
        "http_status": 400,
        "type": "LOGIC"
    },
    "42P01": {
        "message": "El recurso solicitado no se encuentra disponible.",
        "http_status": 404,
        "type": "NOT_FOUND"
    },
    "42703": {
        "message": "La información solicitada no es válida.",
        "http_status": 400,
        "type": "LOGIC"
    },
    "08001": {
        "message": "No fue posible conectarse al sistema en este momento. Intente más tarde.",
        "http_status": 503,
        "type": "AVAILABILITY"
    },
    "08006": {
        "message": "Se perdió la conexión durante la operación. Intente nuevamente.",
        "http_status": 503,
        "type": "AVAILABILITY"
    },
    "53300": {
        "message": "El sistema se encuentra temporalmente indisponible. Intente más tarde.",
        "http_status": 503,
        "type": "AVAILABILITY"
    },
    "P0001": {
        "message": "No es posible completar la operación solicitada.",
        "http_status": 400,
        "type": "BUSINESS"
    },
    "XXXXX": {
        "message": "Ocurrió un error inesperado. Por favor, intente más tarde.",
        "http_status": 500,
        "type": "INTERNAL"
    }
}


SENSITIVE_KEYS = {"password", "passwd", "secret", "token", "api_key"}


def _sanitize_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Oculta valores sensibles antes de loguear."""
    sanitized = {}
    for k, v in params.items():
        if k.lower() in SENSITIVE_KEYS:
            sanitized[k] = "***"
        else:
            sanitized[k] = v
    return sanitized


def _parse_postgres_error(exc: psycopg2.Error) -> StandardizedError:
    pgcode = getattr(exc, "pgcode", None)

    error_cfg = POSTGRES_ERROR_MAP.get(pgcode)
    if error_cfg:
        user_message = error_cfg["message"]
        http_status = error_cfg["http_status"]
    else:
        user_message = "Ocurrió un error interno en la base de datos."
        http_status = 500

    return StandardizedError(
        error=str(exc),
        user_message=user_message,
        http_status=http_status,
        error_type="DATABASE",
        error_code=pgcode,
    )


def postgres_error_handler():
    """
    Traduce errores de PostgreSQL a StandardizedError.
    NO maneja conexiones (eso lo hace el método con `with`).
    """

    def decorator(func):
        sig = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()

            self_obj = bound.arguments.get("self")
            logger = getattr(self_obj, "logger", None)

            try:
                return func(*args, **kwargs)

            except psycopg2.Error as exc:
                method_name = func.__name__
                parameters = {
                    k: v for k, v in bound.arguments.items()
                    if k != "self"
                }
                safe_params = _sanitize_params(parameters)

                if logger:
                    logger.error(
                        message=(
                            f"PostgreSQL error in {method_name} | "
                            f"SQLSTATE={getattr(exc, 'pgcode', None)} | "
                            f"ERROR={getattr(exc, 'pgerror', str(exc))} | "
                            f"PARAMS={safe_params}"
                        ),
                        request_id=bound.arguments.get("request_id"),
                        host=bound.arguments.get("client_host"),
                    )

                raise _parse_postgres_error(exc) from exc

        return wrapper

    return decorator