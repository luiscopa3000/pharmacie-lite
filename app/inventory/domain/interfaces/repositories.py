from abc import ABC, abstractmethod
from typing import Any

from app.inventory.domain.constants import InventoryDbOperations


class IInventoryRepository(ABC):
    @abstractmethod
    def execute(
        self,
        operation: InventoryDbOperations,
        payload: dict[str, Any],
        *,
        request_id: str | None = None,
        host: str | None = None,
        current_user_id: str | None = None,
    ) -> dict[str, Any]:
        raise NotImplementedError
