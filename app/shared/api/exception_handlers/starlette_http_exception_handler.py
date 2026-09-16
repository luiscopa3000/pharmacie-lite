from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from app.shared.api.schemas import ErrorResponse, ErrorData

async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    request_id = getattr(request.state, "request_id", None)

    # Mapeo más completo de errores comunes de Starlette que ocurren antes del endpoint
    code_map = {
        404: ("ENDPOINT_NOT_FOUND", "NOT_FOUND", "Recurso no encontrado"),
        413: ("PAYLOAD_TOO_LARGE", "HTTP_ERROR", "Payload demasiado grande"),
        415: ("UNSUPPORTED_MEDIA_TYPE", "HTTP_ERROR", "Tipo de contenido no soportado"),
        400: ("BAD_REQUEST", "HTTP_ERROR", "Solicitud inválida"),
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