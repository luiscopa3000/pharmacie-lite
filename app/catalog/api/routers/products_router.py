from decimal import Decimal

from fastapi import APIRouter, Depends, Query, Request, status

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.catalog.api.schemas import (
    PresentationCreateSchema,
    PresentationUpdateSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
    StatusSchema,
)
from app.catalog.bootstraps import bootstrap_catalog


products_router = APIRouter(prefix="/products", tags=["Catalog - Products"])


@products_router.post("", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def create_product(
    request: Request,
    data: ProductCreateSchema,
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_CREATE")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).product_create(
        session.user_id,
        data.model_dump(exclude_none=True),
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Producto registrado correctamente", data=result)


@products_router.patch("/{product_id}", response_model=ResponseMessage[dict])
def update_product(
    product_id: int,
    request: Request,
    data: ProductUpdateSchema,
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_UPDATE")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).product_update(
        session.user_id,
        product_id,
        data.model_dump(exclude_none=True),
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Producto actualizado correctamente", data=result)


@products_router.get("", response_model=ResponseMessage[dict])
def search_products(
    request: Request,
    search: str | None = Query(default=None, max_length=180),
    barcode: str | None = Query(default=None, max_length=64),
    product_kind: str | None = Query(default=None),
    record_status: str | None = Query(default=None),
    category_id: int | None = Query(default=None, gt=0),
    for_sale: bool = False,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_VIEW")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).product_search(
        session.user_id,
        {
            "search": search,
            "barcode": barcode,
            "product_kind": product_kind,
            "record_status": record_status,
            "category_id": category_id,
            "for_sale": for_sale,
            "limit": limit,
            "offset": offset,
        },
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Productos consultados correctamente", data=result)


@products_router.get("/{product_id}", response_model=ResponseMessage[dict])
def get_product(
    product_id: int,
    request: Request,
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_VIEW")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).product_get(
        session.user_id,
        product_id,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Producto consultado correctamente", data=result)


@products_router.patch("/{product_id}/status", response_model=ResponseMessage[dict])
def set_product_status(
    product_id: int,
    request: Request,
    data: StatusSchema,
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_STATUS")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).product_set_status(
        session.user_id,
        product_id=product_id,
        record_status=data.record_status,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Estado del producto actualizado correctamente", data=result)


@products_router.get("/{product_id}/stock", response_model=ResponseMessage[dict])
def get_product_stock(
    product_id: int,
    request: Request,
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_VIEW")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).stock_get(
        session.user_id,
        product_id,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Existencia consultada correctamente", data=result)


@products_router.post("/{product_id}/presentations", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def create_presentation(
    product_id: int,
    request: Request,
    data: PresentationCreateSchema,
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_UPDATE")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).presentation_create(
        session.user_id,
        product_id,
        data.model_dump(exclude_none=True),
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Presentación registrada correctamente", data=result)
