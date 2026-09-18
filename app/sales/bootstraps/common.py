from app.shared.domain.interfaces.logger import ILogger
from app.shared.infrastructure.settings import get_pharmacies_db_config
from app.shared.infrastructure.persistence.database import PostgresDatabase
from app.sales.infrastructure.persistence.repositories import SalesRepository

def build_sales_repository(logger: ILogger) -> SalesRepository:
    config = get_pharmacies_db_config()
    database = PostgresDatabase(
        host=config.pharmacies_db_host,
        database=config.pharmacies_db_name,
        user=config.pharmacies_db_user,
        password=config.pharmacies_db_password,
        logger=logger,
    )
    return SalesRepository(logger=logger, database=database)
