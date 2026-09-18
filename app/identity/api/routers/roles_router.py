from fastapi import APIRouter, Depends, Request

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission, require_ready_session
from app.identity.api.schemas.role_schemas import PermissionCheckSchema, RoleAssignSchema
from app.identity.bootstraps import bootstrap_roles
from app.identity.domain.models.session_context import SessionContext


roles_router = APIRouter(prefix="/roles", tags=["Identity - Roles & Permissions"])


@roles_router.put("/users/{user_id}", response_model=ResponseMessage[dict])
def assign_role(
    user_id: int,
    request: Request,
    data: RoleAssignSchema,
    session: SessionContext = Depends(require_permission("ROLES_ASSIGN")),
) -> ResponseMessage:
    result = bootstrap_roles(get_logger()).assign(
        session.user_id,
        user_id,
        data.role_code,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Rol asignado correctamente", data=result)


@roles_router.get("", response_model=ResponseMessage[dict])
def list_roles(
    request: Request,
    session: SessionContext = Depends(require_permission("PERMISSIONS_VIEW")),
) -> ResponseMessage:
    result = bootstrap_roles(get_logger()).list_roles(
        session.user_id,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Roles consultados correctamente", data=result)


@roles_router.get("/permissions", response_model=ResponseMessage[dict])
def get_permissions(
    request: Request,
    user_id: int | None = None,
    session: SessionContext = Depends(require_permission("PERMISSIONS_VIEW")),
) -> ResponseMessage:
    result = bootstrap_roles(get_logger()).permissions(
        session.user_id,
        user_id,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Permisos consultados correctamente", data=result)


@roles_router.post("/permissions/check", response_model=ResponseMessage[dict])
def check_permission(
    request: Request,
    data: PermissionCheckSchema,
    session: SessionContext = Depends(require_ready_session),
) -> ResponseMessage:
    result = bootstrap_roles(get_logger()).check(
        session.user_id,
        data.permission_code,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Permiso verificado correctamente", data=result)
