from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.identity.domain.constants.db_operations import DbOperations
from app.identity.domain.interfaces.repositories import IIdentityRepository

class RoleUseCases:
    def __init__(self, logger: ILogger, repository: IIdentityRepository) -> None:
        self.logger = logger
        self.repository = repository

    def _exec(self, op, payload, actor_user_id, request_id, host):
        payload["actor_user_id"] = actor_user_id
        return self.repository.execute(op, payload, request_id=request_id, host=host, current_user_id=str(actor_user_id))

    @generic_error_handler()
    def assign(self, actor_user_id: int, user_id: int, role_code: str, *, request_id=None, host=None) -> dict:
        return self._exec(DbOperations.ROLE_ASSIGN, {"user_id": user_id, "role_code": role_code}, actor_user_id, request_id, host)

    @generic_error_handler()
    def permissions(self, actor_user_id: int, user_id: int | None = None, *, request_id=None, host=None) -> dict:
        payload = {"actor_user_id": actor_user_id}
        if user_id is not None:
            payload["user_id"] = user_id
        return self.repository.execute(DbOperations.PERMISSIONS_GET, payload, request_id=request_id, host=host, current_user_id=str(actor_user_id))

    @generic_error_handler()
    def check(self, actor_user_id: int, permission_code: str, *, request_id=None, host=None) -> dict:
        return self.repository.execute(DbOperations.PERMISSION_CHECK, {"actor_user_id": actor_user_id, "permission_code": permission_code}, request_id=request_id, host=host, current_user_id=str(actor_user_id))

    @generic_error_handler()
    def list_roles(self, actor_user_id: int, *, request_id=None, host=None) -> dict:
        return self.repository.execute(DbOperations.ROLES_LIST, {"actor_user_id": actor_user_id}, request_id=request_id, host=host, current_user_id=str(actor_user_id))
