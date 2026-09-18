from typing import Any
from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.cash.domain.constants import CashDbOperations
from app.cash.domain.interfaces import ICashRepository

class CashUseCases:
    def __init__(self, logger: ILogger, repository: ICashRepository) -> None:
        self.logger = logger
        self.repository = repository

    @generic_error_handler()
    def run(self, operation: CashDbOperations, actor_user_id: int,
            payload: dict[str, Any], *, request_id=None, host=None) -> dict:
        return self.repository.execute(
            operation,
            {"actor_user_id": actor_user_id, **payload},
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )
