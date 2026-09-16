from app.shared.domain.interfaces.logger import ILogger
from app.shared.infrastructure.settings import get_pharmacies_db_config
from app.shared.infrastructure.persistence.database import PostgresDatabase
from app.shared.infrastructure.persistence.repositories import GenericRepositoryPg
from app.shared.application.use_cases import QueryExecutorUseCase

def bootstrap_query_executor_use_case(logger: ILogger) -> QueryExecutorUseCase:
    pharmacies_db_config = get_pharmacies_db_config()
    database = PostgresDatabase(
        host=pharmacies_db_config.pharmacies_db_host,
        database=pharmacies_db_config.pharmacies_db_name,
        user=pharmacies_db_config.pharmacies_db_user,
        password=pharmacies_db_config.pharmacies_db_password,
        logger=logger
    )
    generic_repository = GenericRepositoryPg(
        logger=logger,
        database=database
    )

    return QueryExecutorUseCase(
        logger=logger,
        generic_repository=generic_repository
    )