from app.shared.domain.interfaces.logger import ILogger
from app.cash.application.use_cases import CashUseCases
from .common import build_cash_repository

def bootstrap_cash(logger: ILogger) -> CashUseCases:
    return CashUseCases(logger=logger, repository=build_cash_repository(logger))
