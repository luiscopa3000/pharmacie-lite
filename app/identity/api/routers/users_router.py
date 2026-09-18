from fastapi import APIRouter, Depends, Query, Request, status

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.api.schemas.user_schemas import (
    PasswordResetSchema,
    UserCreateSchema,
    UserStatusSchema,
    UserUpdateSchema,
)
from app.identity.application.dto import UserCreateRequest, UserUpdateRequest
from app.identity.bootstraps import bootstrap_user_commands, bootstrap_user_queries
from app.identity.domain.models.session_context import SessionContext


users_router = APIRouter(prefix="/users", tags=["Identity - Users"])


@users_router.post("", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def create_user(
    request: Request,
    data: UserCreateSchema,
    session: SessionContext = Depends(require_permission("USERS_CREATE")),
) -> ResponseMessage:
    result = bootstrap_user_commands(get_logger()).create(
        session.user_id,
        UserCreateRequest(**data.model_dump()),
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Usuario creado correctamente", data=result)


@users_router.patch("/{user_id}", response_model=ResponseMessage[dict])
def update_user(
    user_id: int,
    request: Request,
    data: UserUpdateSchema,
    session: SessionContext = Depends(require_permission("USERS_UPDATE")),
) -> ResponseMessage:
    result = bootstrap_user_commands(get_logger()).update(
        session.user_id,
        UserUpdateRequest(user_id=user_id, **data.model_dump()),
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Usuario actualizado correctamente", data=result)


@users_router.get("", response_model=ResponseMessage[dict])
def list_users(
    request: Request,
    search: str | None = None,
    role_code: str | None = None,
    record_status: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("USERS_VIEW")),
) -> ResponseMessage:
    filters = {
        "search": search,
        "role_code": role_code,
        "record_status": record_status,
        "limit": limit,
        "offset": offset,
    }
    result = bootstrap_user_queries(get_logger()).list(
        session.user_id,
        filters,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Usuarios consultados correctamente", data=result)


@users_router.get("/{user_id}", response_model=ResponseMessage[dict])
def get_user(
    user_id: int,
    request: Request,
    session: SessionContext = Depends(require_permission("USERS_VIEW")),
) -> ResponseMessage:
    result = bootstrap_user_queries(get_logger()).get(
        session.user_id,
        user_id,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Usuario consultado correctamente", data=result)


@users_router.patch("/{user_id}/status", response_model=ResponseMessage[dict])
def set_user_status(
    user_id: int,
    request: Request,
    data: UserStatusSchema,
    session: SessionContext = Depends(require_permission("USERS_STATUS")),
) -> ResponseMessage:
    result = bootstrap_user_commands(get_logger()).set_status(
        session.user_id,
        user_id,
        data.record_status,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Estado del usuario actualizado correctamente", data=result)


@users_router.post("/{user_id}/reset-password", response_model=ResponseMessage[dict])
def reset_password(
    user_id: int,
    request: Request,
    data: PasswordResetSchema,
    session: SessionContext = Depends(require_permission("USERS_RESET_PASSWORD")),
) -> ResponseMessage:
    result = bootstrap_user_commands(get_logger()).reset_password(
        session.user_id,
        user_id,
        data.temporary_password,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Contraseña restablecida correctamente", data=result)
