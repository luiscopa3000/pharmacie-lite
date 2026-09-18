from fastapi import APIRouter, Depends, Query, Request, status

from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.catalog.api.schemas import CategoryCreateSchema, CategoryUpdateSchema, StatusSchema
from app.catalog.bootstraps import bootstrap_catalog


categories_router = APIRouter(prefix="/categories", tags=["Catalog - Categories"])


@categories_router.post("", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def create_category(
    request: Request,
    data: CategoryCreateSchema,
    session: SessionContext = Depends(require_permission("CATALOG_CATEGORY_MANAGE")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).category_create(
        session.user_id,
        data.category_name,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Categoría creada correctamente", data=result)


@categories_router.patch("/{category_id}", response_model=ResponseMessage[dict])
def update_category(
    category_id: int,
    request: Request,
    data: CategoryUpdateSchema,
    session: SessionContext = Depends(require_permission("CATALOG_CATEGORY_MANAGE")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).category_update(
        session.user_id,
        category_id,
        data.category_name,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Categoría actualizada correctamente", data=result)


@categories_router.patch("/{category_id}/status", response_model=ResponseMessage[dict])
def set_category_status(
    category_id: int,
    request: Request,
    data: StatusSchema,
    session: SessionContext = Depends(require_permission("CATALOG_CATEGORY_MANAGE")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).category_set_status(
        session.user_id,
        category_id,
        data.record_status,
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Estado de la categoría actualizado correctamente", data=result)


@categories_router.get("", response_model=ResponseMessage[dict])
def list_categories(
    request: Request,
    search: str | None = Query(default=None, max_length=120),
    record_status: str | None = Query(default=None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_VIEW")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).category_list(
        session.user_id,
        {"search": search, "record_status": record_status, "limit": limit, "offset": offset},
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Categorías consultadas correctamente", data=result)


@categories_router.get("/{category_id}/products", response_model=ResponseMessage[dict])
def products_by_category(
    category_id: int,
    request: Request,
    record_status: str | None = Query(default=None),
    for_sale: bool = False,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: SessionContext = Depends(require_permission("CATALOG_PRODUCT_VIEW")),
) -> ResponseMessage:
    result = bootstrap_catalog(get_logger()).products_by_category(
        session.user_id,
        category_id,
        {"record_status": record_status, "for_sale": for_sale, "limit": limit, "offset": offset},
        request_id=request.state.request_id,
        host=request.client.host if request.client else None,
    )
    return ResponseMessage(message="Productos por categoría consultados correctamente", data=result)
