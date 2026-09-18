from fastapi import APIRouter, Depends, Query, Request, status

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.inventory.api.schemas import StockEntrySchema, AdjustmentSchema, DisposalSchema
from app.inventory.bootstraps import bootstrap_inventory


stock_router = APIRouter(prefix="/stock", tags=["Inventory - Stock"])


def _ctx(request: Request) -> tuple[str | None, str | None]:
    return (
        getattr(request.state, "request_id", None),
        request.client.host if request.client else None,
    )


@stock_router.get("", response_model=ResponseMessage[dict])
def stock_current(
    request: Request,
    search: str | None = Query(default=None, max_length=180),
    include_inactive: bool = False,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("INVENTORY_VIEW")),
) -> ResponseMessage:
    request_id, host = _ctx(request)
    result = bootstrap_inventory(get_logger()).stock_query(
        session.user_id,
        {
            "search": search,
            "filter": "ALL",
            "include_inactive": include_inactive,
            "limit": limit,
            "offset": offset,
        },
        request_id=request_id,
        host=host,
    )
    return ResponseMessage(message="Stock actual consultado correctamente", data=result)


@stock_router.get("/out-of-stock", response_model=ResponseMessage[dict])
def out_of_stock(
    request: Request,
    search: str | None = Query(default=None, max_length=180),
    include_inactive: bool = False,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("INVENTORY_VIEW")),
) -> ResponseMessage:
    request_id, host = _ctx(request)
    result = bootstrap_inventory(get_logger()).stock_query(
        session.user_id,
        {
            "search": search,
            "filter": "OUT_OF_STOCK",
            "include_inactive": include_inactive,
            "limit": limit,
            "offset": offset,
        },
        request_id=request_id,
        host=host,
    )
    return ResponseMessage(message="Productos sin stock consultados correctamente", data=result)


@stock_router.get("/low-stock", response_model=ResponseMessage[dict])
def low_stock(
    request: Request,
    search: str | None = Query(default=None, max_length=180),
    include_inactive: bool = False,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("INVENTORY_VIEW")),
) -> ResponseMessage:
    request_id, host = _ctx(request)
    result = bootstrap_inventory(get_logger()).stock_query(
        session.user_id,
        {
            "search": search,
            "filter": "LOW_STOCK",
            "include_inactive": include_inactive,
            "limit": limit,
            "offset": offset,
        },
        request_id=request_id,
        host=host,
    )
    return ResponseMessage(message="Productos con stock bajo consultados correctamente", data=result)


@stock_router.get("/{product_id}", response_model=ResponseMessage[dict])
def stock_by_product(
    product_id: int,
    request: Request,
    limit: int = Query(50, ge=1, le=100, description="Cantidad de lotes por página"),
    offset: int = Query(0, ge=0, description="Desplazamiento de lotes"),
    session: SessionContext = Depends(require_permission("INVENTORY_VIEW")),
) -> ResponseMessage:
    request_id, host = _ctx(request)
    result = bootstrap_inventory(get_logger()).stock_product_get(
        session.user_id,
        product_id,
        limit=limit,
        offset=offset,
        request_id=request_id,
        host=host,
    )
    return ResponseMessage(message="Stock del producto consultado correctamente", data=result)


@stock_router.post("/entries", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def register_stock_entry(
    request: Request,
    data: StockEntrySchema,
    session: SessionContext = Depends(require_permission("INVENTORY_ENTRY")),
) -> ResponseMessage:
    request_id, host = _ctx(request)
    result = bootstrap_inventory(get_logger()).stock_entry(
        session.user_id,
        data.model_dump(exclude_none=True),
        request_id=request_id,
        host=host,
    )
    return ResponseMessage(message="Entrada de stock registrada correctamente", data=result)


@stock_router.post("/adjustments", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def register_adjustment(
    request: Request,
    data: AdjustmentSchema,
    session: SessionContext = Depends(require_permission("INVENTORY_ADJUST")),
) -> ResponseMessage:
    request_id, host = _ctx(request)
    result = bootstrap_inventory(get_logger()).adjustment_register(
        session.user_id,
        data.model_dump(),
        request_id=request_id,
        host=host,
    )
    return ResponseMessage(message="Ajuste de inventario registrado correctamente", data=result)


@stock_router.post("/disposals", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def register_disposal(
    request: Request,
    data: DisposalSchema,
    session: SessionContext = Depends(require_permission("INVENTORY_DISPOSE")),
) -> ResponseMessage:
    request_id, host = _ctx(request)
    result = bootstrap_inventory(get_logger()).disposal_register(
        session.user_id,
        data.model_dump(),
        request_id=request_id,
        host=host,
    )
    return ResponseMessage(message="Baja de inventario registrada correctamente", data=result)
