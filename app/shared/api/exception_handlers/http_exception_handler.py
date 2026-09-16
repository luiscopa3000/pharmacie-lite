from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.shared.api.schemas import ErrorResponse, ErrorData

async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", None)

    # Mapeo más completo de errores de HTTP que ocurren dentro del endpoint o en Depends/Security
    code_map = {
        401: ("UNAUTHORIZED", "AUTH_ERROR", "No autorizado"),
        403: ("FORBIDDEN", "AUTH_ERROR", "Prohibido"),
        405: ("METHOD_NOT_ALLOWED", "HTTP_ERROR", "Método no permitido"),
        409: ("CONFLICT", "HTTP_ERROR", "Conflicto en la solicitud"),
        429: ("TOO_MANY_REQUESTS", "HTTP_ERROR", "Demasiadas solicitudes"),
    }

    code, type_, msg = code_map.get(
        exc.status_code,
        (f"HTTP_{exc.status_code}", "HTTP_ERROR", str(exc.detail)),
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=msg,
            data=ErrorData(
                code=code,
                type=type_,
                details={"request_id": request_id},
            ),
        ).model_dump(),
    )