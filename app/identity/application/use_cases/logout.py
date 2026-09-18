from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.identity.domain.constants.db_operations import DbOperations
from app.identity.domain.interfaces.repositories import IIdentityRepository


class Logout:
    def __init__(self, logger: ILogger, repository: IIdentityRepository) -> None:
        self.logger = logger
        self.repository = repository

    @generic_error_handler()
    def execute(
        self,
        actor_user_id: int,
        session_id: str,
        *,
        request_id: str | None = None,
        host: str | None = None,
    ) -> dict:
        return self.repository.execute(
            DbOperations.LOGOUT,
            {"actor_user_id": actor_user_id, "session_id": session_id},
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )
