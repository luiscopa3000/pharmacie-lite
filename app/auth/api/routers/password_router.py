from fastapi import APIRouter, status, Request

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger

from app.auth.api.schemas.password_schemas import (
    AuthResponse,
    AuthPassword,
)
from app.auth.application.dto import LoginRequest
from app.auth.bootstraps import (
    bootstrap_auth_by_password,
)

# Tag del router hijo; el padre no define tag para que la documentación OpenAPI muestre solo esta sección (Auth).
password_router = APIRouter(
    tags=["Password"],
    prefix="/password",
)

@password_router.post(
    "/login",
    response_model=ResponseMessage[AuthResponse],
    status_code=status.HTTP_200_OK
)
def login_by_password(
    request: Request,
    data: AuthPassword
) -> ResponseMessage:
    """
    Autentica a un usuario mediante usuario o email y contraseña.
    Retorna un mensaje de confirmación cuando las credenciales son válidas.
    """
    
    logger = get_logger()
    logger.info(
        f"Intento de autenticación por contraseña | has_usuario={bool(data.username)} ",
        request_id=request.state.request_id,
        host=request.client.host,
    )

    auth_by_password_use_case = bootstrap_auth_by_password(logger)
    token = auth_by_password_use_case.execute(
        LoginRequest(**data.__dict__),
        request_id=request.state.request_id,
        host=request.client.host
    )

    return ResponseMessage(
        message="Autenticación realizada correctamente",
        data={"token": token}
    )