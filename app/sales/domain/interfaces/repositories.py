from abc import ABC, abstractmethod
from typing import Any
from app.sales.domain.constants import SalesDbOperations

class ISalesRepository(ABC):
    @abstractmethod
    def execute(self, operation: SalesDbOperations, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
        raise NotImplementedError
