from typing import Any

from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.catalog.domain.constants import CatalogDbOperations
from app.catalog.domain.interfaces import ICatalogRepository


class CatalogUseCases:
    def __init__(self, logger: ILogger, repository: ICatalogRepository) -> None:
        self.logger = logger
        self.repository = repository

    def _exec(self, operation: CatalogDbOperations, actor_user_id: int, payload: dict[str, Any], *, request_id=None, host=None) -> dict:
        body = {"actor_user_id": actor_user_id, **payload}
        return self.repository.execute(
            operation,
            body,
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )

    @generic_error_handler()
    def category_create(self, actor_user_id: int, category_name: str, *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.CATEGORY_CREATE, actor_user_id, {"category_name": category_name}, request_id=request_id, host=host)

    @generic_error_handler()
    def category_update(self, actor_user_id: int, category_id: int, category_name: str, *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.CATEGORY_UPDATE, actor_user_id, {"category_id": category_id, "category_name": category_name}, request_id=request_id, host=host)

    @generic_error_handler()
    def category_set_status(self, actor_user_id: int, category_id: int, record_status: str, *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.CATEGORY_SET_STATUS, actor_user_id, {"category_id": category_id, "record_status": record_status}, request_id=request_id, host=host)

    @generic_error_handler()
    def category_list(self, actor_user_id: int, filters: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.CATEGORY_LIST, actor_user_id, {k: v for k, v in filters.items() if v is not None}, request_id=request_id, host=host)

    @generic_error_handler()
    def reference_upsert(self, actor_user_id: int, reference_kind: str, name: str, *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.REFERENCE_UPSERT, actor_user_id, {"reference_kind": reference_kind, "name": name}, request_id=request_id, host=host)

    @generic_error_handler()
    def reference_list(self, actor_user_id: int, filters: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.REFERENCE_LIST, actor_user_id, {k: v for k, v in filters.items() if v is not None}, request_id=request_id, host=host)

    @generic_error_handler()
    def measurement_units_list(self, actor_user_id: int, *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.MEASUREMENT_UNITS_LIST, actor_user_id, {}, request_id=request_id, host=host)

    @generic_error_handler()
    def product_create(self, actor_user_id: int, data: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.PRODUCT_CREATE, actor_user_id, data, request_id=request_id, host=host)

    @generic_error_handler()
    def product_update(self, actor_user_id: int, product_id: int, data: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.PRODUCT_UPDATE, actor_user_id, {"product_id": product_id, **data}, request_id=request_id, host=host)

    @generic_error_handler()
    def product_get(self, actor_user_id: int, product_id: int, *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.PRODUCT_GET, actor_user_id, {"product_id": product_id}, request_id=request_id, host=host)

    @generic_error_handler()
    def product_search(self, actor_user_id: int, filters: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.PRODUCT_SEARCH, actor_user_id, {k: v for k, v in filters.items() if v is not None}, request_id=request_id, host=host)

    @generic_error_handler()
    def product_set_status(self, actor_user_id: int, *, product_id: int | None = None, presentation_id: int | None = None, record_status: str, request_id=None, host=None) -> dict:
        payload: dict[str, Any] = {"record_status": record_status}
        if product_id is not None:
            payload["product_id"] = product_id
        if presentation_id is not None:
            payload["presentation_id"] = presentation_id
        return self._exec(CatalogDbOperations.PRODUCT_SET_STATUS, actor_user_id, payload, request_id=request_id, host=host)

    @generic_error_handler()
    def products_by_category(self, actor_user_id: int, category_id: int, filters: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.PRODUCTS_BY_CATEGORY, actor_user_id, {"category_id": category_id, **{k: v for k, v in filters.items() if v is not None}}, request_id=request_id, host=host)

    @generic_error_handler()
    def presentation_create(self, actor_user_id: int, product_id: int, data: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.PRESENTATION_CREATE, actor_user_id, {"product_id": product_id, **data}, request_id=request_id, host=host)

    @generic_error_handler()
    def presentation_update(self, actor_user_id: int, presentation_id: int, data: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.PRESENTATION_UPDATE, actor_user_id, {"presentation_id": presentation_id, **data}, request_id=request_id, host=host)

    @generic_error_handler()
    def price_get(self, actor_user_id: int, presentation_id: int, quantity: Any, *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.PRICE_GET, actor_user_id, {"presentation_id": presentation_id, "quantity": quantity}, request_id=request_id, host=host)

    @generic_error_handler()
    def stock_get(self, actor_user_id: int, product_id: int, *, request_id=None, host=None) -> dict:
        return self._exec(CatalogDbOperations.STOCK_GET, actor_user_id, {"product_id": product_id}, request_id=request_id, host=host)
