from app.shared.domain.interfaces.logger import ILogger
from app.inventory.application.use_cases import InventoryUseCases
from .common import build_inventory_repository


def bootstrap_inventory(logger: ILogger) -> InventoryUseCases:
    return InventoryUseCases(logger, build_inventory_repository(logger))
