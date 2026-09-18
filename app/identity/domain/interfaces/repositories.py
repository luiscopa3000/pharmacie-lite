from typing import Any, Protocol, runtime_checkable
from app.identity.domain.constants.db_operations import DbOperations

@runtime_checkable
class IIdentityRepository(Protocol):
    def execute(
        self,
        operation: DbOperations,
        payload: dict[str, Any],
        *,
        request_id: str | None = None,
        host: str | None = None,
        current_user_id: str | None = None,
    ) -> dict[str, Any]: ...
