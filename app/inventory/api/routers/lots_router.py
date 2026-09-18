from fastapi import APIRouter, Depends, Query, Request, status

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.inventory.api.schemas import LotCreateSchema
from app.inventory.bootstraps import bootstrap_inventory


lots_router = APIRouter(prefix="/lots", tags=["Inventory - Lots"])


@lots_router.post("", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def register_lot(
    request: Request,
    data: LotCreateSchema,
    session: SessionContext = Depends(require_permission("INVENTORY_LOT_MANAGE")),
) -> ResponseMessage:
    result = bootstrap_inventory(get_logger()).lot_register(
        session.user_id,
        data.model_dump(exclude_none=True),
        request_id=getattr(request.state, "request_id", None),
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Lote registrado correctamente", data=result)


@lots_router.get("", response_model=ResponseMessage[dict])
def list_lots(
    request: Request,
    product_id: int | None = Query(default=None, gt=0),
    lot_status: str = Query(default="ALL"),
    search: str | None = Query(default=None, max_length=180),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("INVENTORY_VIEW")),
) -> ResponseMessage:
    result = bootstrap_inventory(get_logger()).lots_query(
        session.user_id,
        {
            "product_id": product_id,
            "lot_status": lot_status,
            "search": search,
            "limit": limit,
            "offset": offset,
        },
        request_id=getattr(request.state, "request_id", None),
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Lotes consultados correctamente", data=result)


@lots_router.get("/expiring", response_model=ResponseMessage[dict])
def expiring_lots(
    request: Request,
    days: int = Query(30, ge=1, le=3650),
    product_id: int | None = Query(default=None, gt=0),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("INVENTORY_VIEW")),
) -> ResponseMessage:
    result = bootstrap_inventory(get_logger()).lots_expiring(
        session.user_id,
        {
            "days": days,
            "product_id": product_id,
            "limit": limit,
            "offset": offset,
        },
        request_id=getattr(request.state, "request_id", None),
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Lotes próximos a vencer consultados correctamente", data=result)


@lots_router.get("/expired", response_model=ResponseMessage[dict])
def expired_lots(
    request: Request,
    product_id: int | None = Query(default=None, gt=0),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("INVENTORY_VIEW")),
) -> ResponseMessage:
    result = bootstrap_inventory(get_logger()).lots_expired(
        session.user_id,
        {
            "product_id": product_id,
            "limit": limit,
            "offset": offset,
        },
        request_id=getattr(request.state, "request_id", None),
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Lotes vencidos consultados correctamente", data=result)
