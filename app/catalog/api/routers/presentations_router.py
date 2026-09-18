from decimal import Decimal

from fastapi import APIRouter, Depends, Query, Request

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.catalog.api.schemas import PresentationUpdateSchema, StatusSchema
from app.catalog.bootstraps import bootstrap_catalog


presentations_router = APIRouter(prefix="/presentations", tags=["Catalog - Presentations"])


@presentations_router.patch("/{presentation_id}", response_model=ResponseMessage[dict])
def update_presentation(
    presentation_id: int,
    request: Request,
    data: PresentationUpdateSchema,
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_UPDATE")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).presentation_update(
        session.user_id,
        presentation_id,
        data.model_dump(exclude_none=True),
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Presentación actualizada correctamente", data=result)


@presentations_router.patch("/{presentation_id}/status", response_model=ResponseMessage[dict])
def set_presentation_status(
    presentation_id: int,
    request: Request,
    data: StatusSchema,
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_STATUS")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).product_set_status(
        session.user_id,
        presentation_id=presentation_id,
        record_status=data.record_status,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Estado de la presentación actualizado correctamente", data=result)


@presentations_router.get("/{presentation_id}/price", response_model=ResponseMessage[dict])
def get_price(
    presentation_id: int,
    request: Request,
    quantity: Decimal = Query(default=Decimal("1"), gt=0),
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_VIEW")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).price_get(
        session.user_id,
        presentation_id,
        quantity,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Precio consultado correctamente", data=result)
