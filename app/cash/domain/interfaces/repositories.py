from abc import ABC, abstractmethod
from typing import Any
from app.cash.domain.constants import CashDbOperations

class ICashRepository(ABC):
    @abstractmethod
    def execute(self, operation: CashDbOperations, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
        raise NotImplementedError
