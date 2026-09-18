from app.shared.domain.interfaces.logger import ILogger
from app.shared.infrastructure.settings import get_pharmacies_db_config
from app.shared.infrastructure.persistence.database import PostgresDatabase
from app.cash.infrastructure.persistence.repositories import CashRepository

def build_cash_repository(logger: ILogger) -> CashRepository:
    config = get_pharmacies_db_config()
    database = PostgresDatabase(
        host=config.pharmacies_db_host,
        database=config.pharmacies_db_name,
        user=config.pharmacies_db_user,
        password=config.pharmacies_db_password,
        logger=logger,
    )
    return CashRepository(logger=logger, database=database)
