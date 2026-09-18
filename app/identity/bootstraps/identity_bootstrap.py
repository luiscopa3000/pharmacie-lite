from app.shared.domain.interfaces.logger import ILogger
from app.shared.infrastructure.security import PasswordHasher
from app.shared.infrastructure.settings import get_hasher_config
from app.identity.application.use_cases import (
    ChangePassword,
    Login,
    Logout,
    RoleUseCases,
    SessionValidate,
    UserCommands,
    UserQueries,
)
from app.identity.domain.services import PasswordPolicy
from app.identity.infrastructure.security import AccessTokenService
from app.identity.infrastructure.settings import get_token_config
from .common import build_identity_repository


def _password_hasher() -> PasswordHasher:
    return PasswordHasher(hasher_config=get_hasher_config())


def _token_service() -> AccessTokenService:
    return AccessTokenService(config=get_token_config())


def bootstrap_login(logger: ILogger) -> Login:
    return Login(logger, build_identity_repository(logger), _password_hasher(), _token_service())


def bootstrap_logout(logger: ILogger) -> Logout:
    return Logout(logger, build_identity_repository(logger))


def bootstrap_change_password(logger: ILogger) -> ChangePassword:
    return ChangePassword(
        logger,
        build_identity_repository(logger),
        _password_hasher(),
        PasswordPolicy(),
    )


def bootstrap_user_commands(logger: ILogger) -> UserCommands:
    return UserCommands(
        logger,
        build_identity_repository(logger),
        _password_hasher(),
        PasswordPolicy(),
    )


def bootstrap_user_queries(logger: ILogger) -> UserQueries:
    return UserQueries(logger, build_identity_repository(logger))


def bootstrap_roles(logger: ILogger) -> RoleUseCases:
    return RoleUseCases(logger, build_identity_repository(logger))


def bootstrap_session_validate(logger: ILogger) -> SessionValidate:
    return SessionValidate(build_identity_repository(logger), _token_service())
