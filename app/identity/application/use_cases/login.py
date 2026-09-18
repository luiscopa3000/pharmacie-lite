from typing import Any

from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.security import IPasswordHasher
from app.shared.domain.models.errors import StandardizedError
from app.identity.application.dto import LoginRequest
from app.identity.domain.constants.db_operations import DbOperations
from app.identity.domain.interfaces.repositories import IIdentityRepository
from app.identity.domain.interfaces.token_service import IAccessTokenService


class Login:
    """Autenticación: DB obtiene credencial; backend verifica hash y emite JWT."""

    def __init__(
        self,
        logger: ILogger,
        repository: IIdentityRepository,
        password_hasher: IPasswordHasher,
        token_service: IAccessTokenService,
    ) -> None:
        self.logger = logger
        self.repository = repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    def _invalid_credentials(self) -> StandardizedError:
        return StandardizedError(
            error="INVALID_CREDENTIALS",
            error_code="UNAUTHORIZED",
            error_type="AUTH_ERROR",
            user_message="Credenciales inválidas.",
            http_status=401,
        )

    @generic_error_handler()
    def execute(
        self,
        data: LoginRequest,
        *,
        request_id: str | None = None,
        host: str | None = None,
        user_agent: str | None = None,
    ) -> dict[str, Any]:
        username = data.username.strip()
        credential = self.repository.execute(
            DbOperations.AUTH_CREDENTIAL_GET,
            {"username": username},
            request_id=request_id,
            host=host,
        )

        found = bool(credential.get("found", False))
        password_hash = credential.get("password_hash") if found else None
        user_id = credential.get("user_id") if found else None
        record_status = credential.get("record_status") if found else None

        if not found or not password_hash or user_id is None:
            self.repository.execute(
                DbOperations.LOGIN_FAILURE,
                {"username": username, "client_address": host, "user_agent": user_agent},
                request_id=request_id,
                host=host,
            )
            raise self._invalid_credentials()

        if record_status != "ACTIVE":
            self.repository.execute(
                DbOperations.LOGIN_FAILURE,
                {
                    "username": username,
                    "user_id": int(user_id),
                    "client_address": host,
                    "user_agent": user_agent,
                },
                request_id=request_id,
                host=host,
            )
            raise self._invalid_credentials()

        if not self.password_hasher.verify(data.password, str(password_hash)):
            self.repository.execute(
                DbOperations.LOGIN_FAILURE,
                {
                    "username": username,
                    "user_id": int(user_id),
                    "client_address": host,
                    "user_agent": user_agent,
                },
                request_id=request_id,
                host=host,
            )
            raise self._invalid_credentials()

        issued = self.token_service.issue(int(user_id))
        result = self.repository.execute(
            DbOperations.LOGIN_SUCCESS,
            {
                "actor_user_id": int(user_id),
                "user_id": int(user_id),
                "session_id": issued.session_id,
                "expires_at": issued.expires_at.isoformat(),
                "client_address": host,
                "user_agent": user_agent,
            },
            request_id=request_id,
            host=host,
            current_user_id=str(user_id),
        )

        return {
            "access_token": issued.token,
            "token_type": "bearer",
            "expires_at": issued.expires_at.isoformat(),
            "must_change_password": bool(result.get("must_change_password", False)),
            "user": result.get("user") or {},
            "permissions": result.get("permissions") or [],
        }
