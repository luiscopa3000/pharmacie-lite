from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.shared.api.schemas import ErrorResponse, ErrorData


def _sanitize_errors(errors: list) -> list:
    """Convierte la lista de errores a estructuras JSON-serializables (sin objetos excepción en ctx)."""
    out = []
    for err in errors:
        if not isinstance(err, dict):
            out.append({"msg": str(err)})
            continue
        sanitized = {}
        for key, value in err.items():
            if key == "ctx" and value is not None and isinstance(value, dict):
                sanitized[key] = {
                    k: (v if isinstance(v, (str, int, float, bool, type(None))) else str(v))
                    for k, v in value.items()
                }
            elif isinstance(value, (str, int, float, bool, type(None), list, dict)):
                sanitized[key] = value
            else:
                sanitized[key] = str(value)
        out.append(sanitized)
    return out


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", None)
    errors = _sanitize_errors(exc.errors())

    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            message="Error de validación",
            data=ErrorData(
                code="INVALID_REQUEST",
                type="VALIDATION_ERROR",
                details={
                    "errors": errors,
                    "request_id": request_id,
                },
            ),
        ).model_dump(),
    )