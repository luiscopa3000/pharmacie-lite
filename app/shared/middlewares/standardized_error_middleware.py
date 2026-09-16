import uuid
from fastapi import Request
from fastapi.responses import JSONResponse

from app.shared.api.schemas import ErrorResponse, ErrorData
from app.shared.domain.models.errors.standardized_error import StandardizedError
from app.shared.bootstraps import get_logger


async def standardized_error_middleware(request: Request, call_next):
    logger = get_logger()

    host = request.client.host if request.client else "unknown"
    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())

    request.state.request_id = request_id

    content_type = request.headers.get("content-type", "-")

    body_info = "-"
    if request.method in {"POST", "PUT", "PATCH"}:
        try:
            body = await request.body()
            # Mostramos el contenido del body para depurar
            body_info = body.decode("utf-8")
        except Exception:
            body_info = "unreadable"

    logger.info(
        f"Incoming request | method={request.method} | "
        f"path={request.url.path} | "
        f"query={request.url.query or '-'} | "
        f"content-type={content_type} | "
        f"body={body_info}",
        request_id=request_id,
        host=host,
    )

    try:
        return await call_next(request)

    except StandardizedError as exc:
        logger.error(
            f"{exc.error} | method={request.method} | path={request.url.path}",
            request_id=request_id,
            host=host,
        )

        return JSONResponse(
            status_code=exc.http_status,
            content=ErrorResponse(
                message=exc.user_message,
                data=ErrorData(
                    code=exc.error_code,
                    type=exc.error_type,
                    details=exc.data
                ),
            ).model_dump(),
        )

    except Exception as exc:
        import traceback
        logger.error(
            f"Unhandled exception={exc}\n{traceback.format_exc()} | method={request.method} | path={request.url.path}",
            request_id=request_id,
            host=host,
        )

        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                message="Error interno del servidor",
                data=ErrorData(
                    type="internal_error",
                    code="INTERNAL_ERROR",
                    details={"error": str(exc)},
                ),
            ).model_dump(),
        )