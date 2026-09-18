from datetime import datetime

from fastapi import APIRouter, Depends, Query, Request

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.inventory.bootstraps import bootstrap_inventory


movements_router = APIRouter(tags=["Inventory - Movements"])


@movements_router.get("/movements", response_model=ResponseMessage[dict])
def movements(
    request: Request,
    product_id: int | None = Query(default=None, gt=0),
    stock_lot_id: int | None = Query(default=None, gt=0),
    movement_kind: str | None = Query(default=None, max_length=32),
    performed_by_user_id: int | None = Query(default=None, gt=0),
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("INVENTORY_VIEW")),
) -> ResponseMessage:
    result = bootstrap_inventory(get_logger()).movements_query(
        session.user_id,
        {
            "product_id": product_id,
            "stock_lot_id": stock_lot_id,
            "movement_kind": movement_kind,
            "performed_by_user_id": performed_by_user_id,
            "date_from": date_from,
            "date_to": date_to,
            "limit": limit,
            "offset": offset,
        },
        request_id=getattr(request.state, "request_id", None),
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Movimientos consultados correctamente", data=result)


@movements_router.get("/products/{product_id}/movements", response_model=ResponseMessage[dict])
def product_movements(
    product_id: int,
    request: Request,
    stock_lot_id: int | None = Query(default=None, gt=0),
    movement_kind: str | None = Query(default=None, max_length=32),
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("INVENTORY_VIEW")),
) -> ResponseMessage:
    result = bootstrap_inventory(get_logger()).product_movements_query(
        session.user_id,
        product_id,
        {
            "stock_lot_id": stock_lot_id,
            "movement_kind": movement_kind,
            "date_from": date_from,
            "date_to": date_to,
            "limit": limit,
            "offset": offset,
        },
        request_id=getattr(request.state, "request_id", None),
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Historial del producto consultado correctamente", data=result)
