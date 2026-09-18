from dataclasses import asdict

from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.security import IPasswordHasher
from app.identity.application.dto import UserCreateRequest, UserUpdateRequest
from app.identity.domain.constants.db_operations import DbOperations
from app.identity.domain.interfaces.repositories import IIdentityRepository
from app.identity.domain.services import PasswordPolicy


class UserCommands:
    def __init__(
        self,
        logger: ILogger,
        repository: IIdentityRepository,
        password_hasher: IPasswordHasher,
        password_policy: PasswordPolicy,
    ) -> None:
        self.logger = logger
        self.repository = repository
        self.password_hasher = password_hasher
        self.password_policy = password_policy

    def _exec(self, op, payload, actor_user_id, request_id, host):
        payload["actor_user_id"] = actor_user_id
        return self.repository.execute(
            op,
            payload,
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )

    @generic_error_handler()
    def create(self, actor_user_id: int, data: UserCreateRequest, *, request_id=None, host=None) -> dict:
        self.password_policy.validate(data.password)
        password_hash = self.password_hasher.hash(data.password)
        payload = asdict(data)
        payload.pop("password", None)
        payload["password_hash"] = password_hash
        return self._exec(DbOperations.USER_CREATE, payload, actor_user_id, request_id, host)

    @generic_error_handler()
    def update(self, actor_user_id: int, data: UserUpdateRequest, *, request_id=None, host=None) -> dict:
        payload = {k: v for k, v in asdict(data).items() if v is not None}
        return self._exec(DbOperations.USER_UPDATE, payload, actor_user_id, request_id, host)

    @generic_error_handler()
    def set_status(self, actor_user_id: int, user_id: int, record_status: str, *, request_id=None, host=None) -> dict:
        return self._exec(
            DbOperations.USER_SET_STATUS,
            {"user_id": user_id, "record_status": record_status},
            actor_user_id,
            request_id,
            host,
        )

    @generic_error_handler()
    def reset_password(
        self,
        actor_user_id: int,
        user_id: int,
        temporary_password: str,
        *,
        request_id=None,
        host=None,
    ) -> dict:
        self.password_policy.validate(temporary_password)
        password_hash = self.password_hasher.hash(temporary_password)
        return self._exec(
            DbOperations.USER_RESET_PASSWORD,
            {"user_id": user_id, "password_hash": password_hash, "must_change_password": True},
            actor_user_id,
            request_id,
            host,
        )


class UserQueries:
    def __init__(self, logger: ILogger, repository: IIdentityRepository) -> None:
        self.logger = logger
        self.repository = repository

    @generic_error_handler()
    def list(self, actor_user_id: int, filters: dict, *, request_id=None, host=None) -> dict:
        payload = {"actor_user_id": actor_user_id, **{k: v for k, v in filters.items() if v is not None}}
        return self.repository.execute(
            DbOperations.USER_LIST,
            payload,
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )

    @generic_error_handler()
    def get(self, actor_user_id: int, user_id: int, *, request_id=None, host=None) -> dict:
        return self.repository.execute(
            DbOperations.USER_GET,
            {"actor_user_id": actor_user_id, "user_id": user_id},
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )
