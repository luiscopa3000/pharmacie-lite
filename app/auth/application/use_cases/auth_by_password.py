from datetime import datetime, timezone
from typing import Optional

from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.security import IPasswordHasher
from app.shared.domain.interfaces.generic_repository import IGenericRepository
from app.shared.domain.models.errors import StandardizedError

from app.auth.domain.interfaces.token_generator import ITokenGenerator

from app.auth.domain.interfaces.repositories import IAuthByPasswordRepository
from app.auth.domain.constants.db_operations import DbOperations
from app.auth.application.dto import LoginRequest

def _identificador(user: Optional[str], email: Optional[str]) -> Optional[str]:
    if email and str(email).strip():
        return str(email).strip().lower()
    if user and str(user).strip():
        return str(user).strip().lower()
    return None


class AuthByPassword:
    """
    Caso de uso para autenticar un usuario mediante usuario o email y contraseña.
    Aplica bloqueo por intentos según política de la compañía.
    La contraseña se valida en memoria (hasher + pepper) y nunca se persiste ni se registra.
    """

    def __init__(
        self,
        logger: ILogger,
        auth_by_password_repo: IAuthByPasswordRepository,
        generic_repository: IGenericRepository,
        password_hasher: IPasswordHasher,
        token_generator: ITokenGenerator,
    ) -> None:
        self.logger = logger
        self.auth_by_password_repo = auth_by_password_repo
        self.generic_repository = generic_repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator

    @generic_error_handler()
    def execute(
        self,
        login_request: LoginRequest,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> str:
        identificador = _identificador(login_request.user, login_request.email)
        user_password = self.auth_by_password_repo.get_user_for_login(
            user=login_request.user,
            email=login_request.email,
            request_id=request_id,
            host=host,
        )

        if user_password is None:
            if identificador:
                blocked = self.generic_repository.execute_operation(
                    DbOperations.GET_BLOCKED_IDENTIFIER_ATTEMPT,
                    request_id=request_id,
                    host=host,
                    identificador=identificador,
                )
                if blocked and isinstance(blocked, dict) and blocked.get("bloqueado_hasta"):
                    raise StandardizedError(
                        error="ACCOUNT_LOCKED",
                        error_code="LOCKED",
                        error_type="AUTH_ERROR",
                        user_message="Cuenta temporalmente bloqueada",
                        http_status=423,
                    )
                self.generic_repository.execute_operation(
                    DbOperations.RECORD_ATTEMPT_FAILURE_IDENTIFIER,
                    request_id=request_id,
                    host=host,
                    identificador=identificador,
                )
            raise StandardizedError(
                error="INVALID_CREDENTIALS",
                error_code="UNAUTHORIZED",
                error_type="AUTH_ERROR",
                user_message="Credenciales inválidas",
                http_status=401,
            )

        now_utc = datetime.now(timezone.utc)
        hasta = user_password.bloqueado_hasta
        if hasta:
            if hasta.tzinfo is None:
                hasta = hasta.replace(tzinfo=timezone.utc)
            if hasta > now_utc:
                raise StandardizedError(
                    error="ACCOUNT_LOCKED",
                    error_code="LOCKED",
                    error_type="AUTH_ERROR",
                    user_message="Cuenta temporalmente bloqueada",
                    http_status=423,
                )

        if not self.password_hasher.verify(login_request.password, user_password.password_hash):
            self.generic_repository.execute_operation(
                DbOperations.RECORD_ATTEMPT_FAILURE,
                request_id=request_id,
                host=host,
                id_usuario_password=user_password.id_user_password,
            )
            raise StandardizedError(
                error="INVALID_CREDENTIALS",
                error_code="UNAUTHORIZED",
                error_type="AUTH_ERROR",
                user_message="Credenciales inválidas",
                http_status=401,
            )

        self.generic_repository.execute_operation(
            DbOperations.SUCCESSFUL_AUTHENTICATION_REGISTRATION,
            request_id=request_id,
            host=host,
            id_usuario=user_password.id_user,
            id_usuario_password=user_password.id_user_password,
            identificador=identificador,
        )

        return self.token_generator.generate(subject=str(user_password.id_user))


