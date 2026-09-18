from app.shared.domain.interfaces.logger import ILogger
from app.shared.infrastructure.settings import get_pharmacies_db_config
from app.shared.infrastructure.persistence.database import PostgresDatabase
from app.reports.infrastructure.persistence.repositories import ReportsRepository
def build_reports_repository(logger:ILogger)->ReportsRepository:
 c=get_pharmacies_db_config(); db=PostgresDatabase(host=c.pharmacies_db_host,database=c.pharmacies_db_name,user=c.pharmacies_db_user,password=c.pharmacies_db_password,logger=logger); return ReportsRepository(logger=logger,database=db)
