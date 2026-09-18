from app.shared.domain.interfaces.logger import ILogger
from app.catalog.application.use_cases import CatalogUseCases
from .common import build_catalog_repository


def bootstrap_catalog(logger: ILogger) -> CatalogUseCases:
    return CatalogUseCases(logger, build_catalog_repository(logger))
