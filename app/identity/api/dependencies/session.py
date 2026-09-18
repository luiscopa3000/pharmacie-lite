from collections.abc import Callable

from fastapi import Depends, Header, Request

from app.shared.bootstraps import get_logger
from app.shared.domain.models.errors import StandardizedError
from app.identity.bootstraps import bootstrap_session_validate
from app.identity.domain.models.session_context import SessionContext


def require_session(
    request: Request,
    authorization: str | None = Header(default=None),
) -> SessionContext:
    if not authorization or not authorization.startswith("Bearer "):
        raise StandardizedError(
            error="AUTH_REQUIRED",
            error_code="UNAUTHORIZED",
            error_type="AUTH_ERROR",
            user_message="Autenticación requerida.",
            http_status=401,
        )
    token = authorization[7:].strip()
    if not token:
        raise StandardizedError(
            error="AUTH_REQUIRED",
            error_code="UNAUTHORIZED",
            error_type="AUTH_ERROR",
            user_message="Autenticación requerida.",
            http_status=401,
        )

    session = bootstrap_session_validate(get_logger()).execute(
        token,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    request.state.user_id = session.user_id
    request.state.permissions = session.permissions
    request.state.session_id = session.session_id
    return session


def require_ready_session(session: SessionContext = Depends(require_session)) -> SessionContext:
    if session.must_change_password:
        raise StandardizedError(
            error="PASSWORD_CHANGE_REQUIRED",
            error_code="FORBIDDEN",
            error_type="AUTH_ERROR",
            user_message="Debe cambiar su contraseña antes de continuar.",
            http_status=403,
        )
    return session


def _permission_codes(session: SessionContext) -> set[str]:
    result: set[str] = set()
    for item in session.permissions:
        if isinstance(item, str):
            result.add(item)
        elif isinstance(item, dict):
            code = item.get("permission_code") or item.get("code")
            if code:
                result.add(str(code))
    return result


def require_permission(permission_code: str) -> Callable:
    def dependency(session: SessionContext = Depends(require_ready_session)) -> SessionContext:
        if permission_code not in _permission_codes(session):
            raise StandardizedError(
                error="FORBIDDEN",
                error_code="FORBIDDEN",
                error_type="AUTHORIZATION_ERROR",
                user_message="No tiene permisos para realizar esta operación.",
                http_status=403,
            )
        return session

    return dependency
