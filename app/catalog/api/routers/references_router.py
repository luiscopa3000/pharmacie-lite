from fastapi import APIRouter, Depends, Query, Request, status

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.catalog.api.schemas import ReferenceUpsertSchema
from app.catalog.bootstraps import bootstrap_catalog


references_router = APIRouter(prefix="/references", tags=["Catalog - References"])


@references_router.post("", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def upsert_reference(
    request: Request,
    data: ReferenceUpsertSchema,
    session: SessionContext = Depends(require_permission("CATALOG_REFERENCE_MANAGE")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).reference_upsert(
        session.user_id,
        data.reference_kind,
        data.name,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Referencia registrada correctamente", data=result)


@references_router.get("", response_model=ResponseMessage[dict])
def list_references(
    request: Request,
    reference_kind: str | None = Query(default=None),
    search: str | None = Query(default=None, max_length=160),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_VIEW")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).reference_list(
        session.user_id,
        {"reference_kind": reference_kind, "search": search, "limit": limit, "offset": offset},
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Referencias consultadas correctamente", data=result)


@references_router.get("/measurement-units", response_model=ResponseMessage[dict])
def list_measurement_units(
    request: Request,
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_VIEW")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).measurement_units_list(
        session.user_id,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Unidades de medida consultadas correctamente", data=result)
