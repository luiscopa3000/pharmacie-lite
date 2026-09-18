from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.security import IPasswordHasher
from app.shared.domain.models.errors import StandardizedError
from app.identity.application.dto import ChangePasswordRequest
from app.identity.domain.constants.db_operations import DbOperations
from app.identity.domain.interfaces.repositories import IIdentityRepository
from app.identity.domain.services import PasswordPolicy


class ChangePassword:
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

    @generic_error_handler()
    def execute(
        self,
        actor_user_id: int,
        data: ChangePasswordRequest,
        *,
        request_id: str | None = None,
        host: str | None = None,
    ) -> dict:
        credential = self.repository.execute(
            DbOperations.PASSWORD_CREDENTIAL_GET,
            {"actor_user_id": actor_user_id, "user_id": actor_user_id},
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )
        current_hash = credential.get("password_hash")
        if not current_hash or not self.password_hasher.verify(data.current_password, str(current_hash)):
            raise StandardizedError(
                error="INVALID_CURRENT_PASSWORD",
                error_code="UNAUTHORIZED",
                error_type="AUTH_ERROR",
                user_message="La contraseña actual no es correcta.",
                http_status=401,
            )

        self.password_policy.validate(data.new_password)
        if self.password_hasher.verify(data.new_password, str(current_hash)):
            raise StandardizedError(
                error="PASSWORD_REUSE",
                error_code="BAD_REQUEST",
                error_type="VALIDATION_ERROR",
                user_message="La nueva contraseña debe ser diferente de la contraseña actual.",
                http_status=400,
            )

        new_hash = self.password_hasher.hash(data.new_password)
        return self.repository.execute(
            DbOperations.PASSWORD_CHANGE,
            {
                "actor_user_id": actor_user_id,
                "user_id": actor_user_id,
                "new_password_hash": new_hash,
            },
            request_id=request_id,
            host=host,
            current_user_id=str(actor_user_id),
        )
