from app.shared.domain.interfaces.logger import ILogger
from app.shared.infrastructure.settings import get_pharmacies_db_config
from app.shared.infrastructure.persistence.database import PostgresDatabase
from app.audit.infrastructure.persistence.repositories import AuditRepository
def build_audit_repository(logger:ILogger)->AuditRepository:
    c=get_pharmacies_db_config()
    db=PostgresDatabase(host=c.pharmacies_db_host,database=c.pharmacies_db_name,user=c.pharmacies_db_user,password=c.pharmacies_db_password,logger=logger)
    return AuditRepository(logger=logger,database=db)
