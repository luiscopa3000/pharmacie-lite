from app.shared.domain.models.errors import StandardizedError
from app.identity.domain.constants.db_operations import DbOperations
from app.identity.domain.interfaces.repositories import IIdentityRepository
from app.identity.domain.interfaces.token_service import IAccessTokenService
from app.identity.domain.models.session_context import SessionContext
from app.identity.infrastructure.security import InvalidAccessToken


class SessionValidate:
    def __init__(self, repository: IIdentityRepository, token_service: IAccessTokenService) -> None:
        self.repository = repository
        self.token_service = token_service

    def execute(self, token: str, *, request_id: str | None = None, host: str | None = None) -> SessionContext:
        try:
            claims = self.token_service.verify(token)
        except InvalidAccessToken as exc:
            raise StandardizedError(
                error="INVALID_TOKEN",
                error_code="UNAUTHORIZED",
                error_type="AUTH_ERROR",
                user_message="Token inválido o expirado.",
                http_status=401,
            ) from exc

        result = self.repository.execute(
            DbOperations.SESSION_VALIDATE,
            {"user_id": claims.subject, "session_id": claims.session_id},
            request_id=request_id,
            host=host,
            current_user_id=str(claims.subject),
        )
        if not result.get("valid", False):
            raise StandardizedError(
                error="SESSION_INVALID",
                error_code="UNAUTHORIZED",
                error_type="AUTH_ERROR",
                user_message="Sesión inválida, revocada o expirada.",
                http_status=401,
            )

        user = result.get("user") or {}
        db_user_id = user.get("user_id") or result.get("user_id")
        if db_user_id is None or int(db_user_id) != claims.subject:
            raise StandardizedError(
                error="SESSION_IDENTITY_MISMATCH",
                error_code="UNAUTHORIZED",
                error_type="AUTH_ERROR",
                user_message="Sesión inválida.",
                http_status=401,
            )

        return SessionContext(
            user_id=claims.subject,
            session_id=claims.session_id,
            user=user,
            permissions=result.get("permissions") or [],
            must_change_password=bool(result.get("must_change_password", False)),
        )
