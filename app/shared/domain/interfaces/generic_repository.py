from enum import Enum
from typing import Protocol, runtime_checkable, List, Dict, Optional


@runtime_checkable
class IGenericRepository(Protocol):
    def execute_operation(
        self,
        query: Enum | str,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        **kwargs,
    ) -> List[Dict]:
        ...