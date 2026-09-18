from abc import ABC, abstractmethod
from typing import Any

from app.catalog.domain.constants import CatalogDbOperations


class ICatalogRepository(ABC):
    @abstractmethod
    def execute(
        self,
        operation: CatalogDbOperations,
        payload: dict[str, Any],
        *,
        request_id: str | None = None,
        host: str | None = None,
        current_user_id: str | None = None,
    ) -> dict[str, Any]:
        raise NotImplementedError
