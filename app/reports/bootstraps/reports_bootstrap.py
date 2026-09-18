from app.shared.domain.interfaces.logger import ILogger
from app.reports.application.use_cases import ReportsUseCases
from .common import build_reports_repository
def bootstrap_reports(logger:ILogger)->ReportsUseCases: return ReportsUseCases(logger=logger,repository=build_reports_repository(logger))
