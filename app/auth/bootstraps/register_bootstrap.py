from app.shared.domain.interfaces.logger import ILogger
from app.shared.infrastructure.settings import (
    get_hasher_config,
    get_pharmacies_db_config
)
from app.shared.infrastructure.persistence.database import PostgresDatabase
from app.shared.infrastructure.security import PasswordHasher

from app.auth.infrastructure.persistence.repositories.register_user import RegisterUserRepository
from app.auth.application.use_cases.register_user import RegisterUser

def bootstrap_register_user(logger: ILogger) -> RegisterUser:
    """
    Inicializa el caso de uso RegisterUser con todas sus dependencias.
    """
    database_config = get_pharmacies_db_config()
    hasher_config = get_hasher_config()
    
    database = PostgresDatabase(
        host=database_config.pharmacies_db_host,
        database=database_config.pharmacies_db_name,
        user=database_config.pharmacies_db_user,
        password=database_config.pharmacies_db_password,
        logger=logger
    )
    password_hasher = PasswordHasher(
        hasher_config=hasher_config
    )
    
    register_user_repo = RegisterUserRepository(logger, database)
    
    return RegisterUser(
        logger=logger,
        register_user_repo=register_user_repo,
        password_hasher=password_hasher,
    )
