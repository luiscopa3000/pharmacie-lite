from app.shared.domain.interfaces.logger import ILogger
from app.sales.application.use_cases import SalesUseCases
from .common import build_sales_repository

def bootstrap_sales(logger: ILogger) -> SalesUseCases:
    return SalesUseCases(logger=logger, repository=build_sales_repository(logger))
