from fastapi import APIRouter, Depends, Request, status

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_session
from app.identity.api.schemas.auth_schemas import ChangePasswordSchema, LoginRequestSchema
from app.identity.application.dto import ChangePasswordRequest, LoginRequest
from app.identity.bootstraps import bootstrap_change_password, bootstrap_login, bootstrap_logout
from app.identity.domain.models.session_context import SessionContext


auth_router = APIRouter(prefix="/auth", tags=["Identity - Auth"])


@auth_router.post("/login", response_model=ResponseMessage[dict], status_code=status.HTTP_200_OK)
def login(request: Request, data: LoginRequestSchema) -> ResponseMessage:
    result = bootstrap_login(get_logger()).execute(
        LoginRequest(**data.model_dump()),
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return ResponseMessage(message="Autenticación realizada correctamente", data=result)


@auth_router.post("/logout", response_model=ResponseMessage[dict], status_code=status.HTTP_200_OK)
def logout(request: Request, session: SessionContext = Depends(require_session)) -> ResponseMessage:
    result = bootstrap_logout(get_logger()).execute(
        session.user_id,
        session.session_id,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Sesión cerrada correctamente", data=result)


@auth_router.post("/change-password", response_model=ResponseMessage[dict], status_code=status.HTTP_200_OK)
def change_password(
    request: Request,
    data: ChangePasswordSchema,
    session: SessionContext = Depends(require_session),
) -> ResponseMessage:
    result = bootstrap_change_password(get_logger()).execute(
        session.user_id,
        ChangePasswordRequest(**data.model_dump()),
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(
        message="Contraseña actualizada correctamente. Debe iniciar sesión nuevamente.",
        data=result,
    )
