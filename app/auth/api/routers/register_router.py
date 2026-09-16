from fastapi import APIRouter, status, Request

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger

from app.auth.api.schemas.register_schemas import (
    RegisterUserRequest,
    RegisterUserResponse,
)
from app.auth.application.dto.register_request import RegisterRequest as RegisterRequestDTO
from app.auth.bootstraps import bootstrap_register_user


register_router = APIRouter(
    tags=["Register"],
    prefix="/register",
)

@register_router.post(
    "",
    response_model=ResponseMessage[RegisterUserResponse],
    status_code=status.HTTP_201_CREATED
)
def register_user(
    request: Request,
    data: RegisterUserRequest
) -> ResponseMessage:
    """
    Registra un nuevo usuario en el sistema.
    """
    
    logger = get_logger()
    logger.info(
        f"Intento de registro de usuario | username={data.username} | email={data.email}",
        request_id=request.state.request_id,
        host=request.client.host,
    )

    # In a real scenario, the current_user_id might come from auth middleware
    # current_user_id = getattr(request.state, "user_id", None)
    current_user_id = None

    register_use_case = bootstrap_register_user(logger)
    user_id = register_use_case.execute(
        RegisterRequestDTO(**data.__dict__),
        request_id=request.state.request_id,
        host=request.client.host,
        current_user_id=current_user_id
    )

    return ResponseMessage(
        message="Usuario creado correctamente",
        data={"id_user": user_id}
    )
