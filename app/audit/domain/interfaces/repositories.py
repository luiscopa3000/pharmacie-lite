from abc import ABC, abstractmethod
from typing import Any
from app.audit.domain.constants import AuditDbOperations
class IAuditRepository(ABC):
    @abstractmethod
    def execute(self, operation: AuditDbOperations, payload: dict[str,Any], **kwargs)->dict[str,Any]:
        raise NotImplementedError
