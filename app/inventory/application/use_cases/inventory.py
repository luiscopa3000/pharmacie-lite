from typing import Any

from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.inventory.domain.constants import InventoryDbOperations
from app.inventory.domain.interfaces import IInventoryRepository


class InventoryUseCases:
    def __init__(self, logger: ILogger, repository: IInventoryRepository) -> None:
        self.logger = logger
        self.repository = repository

    def _exec(
        self,
        operation: InventoryDbOperations,
        actor_user_id: int,
        payload: dict[str, Any],
        *,
        request_id=None,
        host=None,
    ) -> dict:
        body = {"actor_user_id": actor_user_id, **payload}
        return self.repository.execute(
            operation,
            body,
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )

    @generic_error_handler()
    def stock_query(self, actor_user_id: int, filters: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(
            InventoryDbOperations.STOCK_QUERY,
            actor_user_id,
            {k: v for k, v in filters.items() if v is not None},
            request_id=request_id,
            host=host,
        )

    @generic_error_handler()
    def stock_product_get(
        self,
        actor_user_id: int,
        product_id: int,
        *,
        limit: int,
        offset: int,
        request_id=None,
        host=None,
    ) -> dict:
        return self._exec(
            InventoryDbOperations.STOCK_PRODUCT_GET,
            actor_user_id,
            {"product_id": product_id, "limit": limit, "offset": offset},
            request_id=request_id,
            host=host,
        )

    @generic_error_handler()
    def stock_entry(self, actor_user_id: int, data: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(InventoryDbOperations.STOCK_ENTRY, actor_user_id, data, request_id=request_id, host=host)

    @generic_error_handler()
    def adjustment_register(self, actor_user_id: int, data: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(InventoryDbOperations.ADJUSTMENT_REGISTER, actor_user_id, data, request_id=request_id, host=host)

    @generic_error_handler()
    def disposal_register(self, actor_user_id: int, data: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(InventoryDbOperations.DISPOSAL_REGISTER, actor_user_id, data, request_id=request_id, host=host)

    @generic_error_handler()
    def movements_query(self, actor_user_id: int, filters: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(
            InventoryDbOperations.MOVEMENTS_QUERY,
            actor_user_id,
            {k: v for k, v in filters.items() if v is not None},
            request_id=request_id,
            host=host,
        )

    @generic_error_handler()
    def product_movements_query(
        self,
        actor_user_id: int,
        product_id: int,
        filters: dict[str, Any],
        *,
        request_id=None,
        host=None,
    ) -> dict:
        return self._exec(
            InventoryDbOperations.PRODUCT_MOVEMENTS_QUERY,
            actor_user_id,
            {"product_id": product_id, **{k: v for k, v in filters.items() if v is not None}},
            request_id=request_id,
            host=host,
        )

    @generic_error_handler()
    def lot_register(self, actor_user_id: int, data: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(InventoryDbOperations.LOT_REGISTER, actor_user_id, data, request_id=request_id, host=host)

    @generic_error_handler()
    def lots_query(self, actor_user_id: int, filters: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(
            InventoryDbOperations.LOTS_QUERY,
            actor_user_id,
            {k: v for k, v in filters.items() if v is not None},
            request_id=request_id,
            host=host,
        )

    @generic_error_handler()
    def lots_expiring(self, actor_user_id: int, filters: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(
            InventoryDbOperations.LOTS_EXPIRING,
            actor_user_id,
            {k: v for k, v in filters.items() if v is not None},
            request_id=request_id,
            host=host,
        )

    @generic_error_handler()
    def lots_expired(self, actor_user_id: int, filters: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self._exec(
            InventoryDbOperations.LOTS_EXPIRED,
            actor_user_id,
            {k: v for k, v in filters.items() if v is not None},
            request_id=request_id,
            host=host,
        )
