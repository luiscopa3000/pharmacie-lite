from app.shared.domain.interfaces.logger import ILogger
from app.shared.infrastructure.settings import (
    get_hasher_config,
    get_pharmacies_db_config
)
from app.shared.infrastructure.persistence.database import PostgresDatabase
from app.shared.infrastructure.persistence.repositories import GenericRepositoryPg
from app.shared.infrastructure.security import PasswordHasher

from app.auth.infrastructure.security import TokenGenerator



from app.auth.infrastructure.settings import get_token_config
from app.auth.infrastructure.persistence.repositories import AuthByPasswordRepository
from app.auth.application.use_cases import AuthByPassword


def bootstrap_auth_by_password(logger: ILogger) -> AuthByPassword:
    database_config = get_pharmacies_db_config()
    hasher_config = get_hasher_config()
    token_config = get_token_config()

    database = PostgresDatabase(
        host=database_config.pharmacies_db_host,
        database=database_config.pharmacies_db_name,
        user=database_config.pharmacies_db_user,
        password=database_config.pharmacies_db_password,
        logger=logger
    )
    auth_by_password_repo = AuthByPasswordRepository(
        logger=logger,
        database=database
    )
    generic_repository = GenericRepositoryPg(
        logger=logger,
        database=database
    )

    password_hasher = PasswordHasher(
        hasher_config=hasher_config
    )

    token_generator = TokenGenerator(
        token_config=token_config
    )

    return AuthByPassword(
        logger=logger,
        auth_by_password_repo=auth_by_password_repo,
        generic_repository=generic_repository,
        password_hasher=password_hasher,
        token_generator=token_generator
    )




