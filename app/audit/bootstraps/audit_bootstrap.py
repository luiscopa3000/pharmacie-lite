from app.shared.domain.interfaces.logger import ILogger
from app.audit.application.use_cases import AuditUseCases
from .common import build_audit_repository
def bootstrap_audit(logger:ILogger)->AuditUseCases:
    return AuditUseCases(logger=logger,repository=build_audit_repository(logger))
