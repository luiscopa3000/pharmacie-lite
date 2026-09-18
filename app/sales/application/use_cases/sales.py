from typing import Any
from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.sales.domain.constants import SalesDbOperations
from app.sales.domain.interfaces import ISalesRepository

class SalesUseCases:
    def __init__(self, logger: ILogger, repository: ISalesRepository) -> None:
        self.logger = logger
        self.repository = repository

    def _exec(self, operation: SalesDbOperations, actor_user_id: int, payload: dict[str, Any],
              *, request_id=None, host=None) -> dict:
        return self.repository.execute(
            operation,
            {"actor_user_id": actor_user_id, **payload},
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )

    @generic_error_handler()
    def run(self, operation: SalesDbOperations, actor_user_id: int, payload: dict[str, Any],
            *, request_id=None, host=None) -> dict:
        return self._exec(operation, actor_user_id, payload, request_id=request_id, host=host)
