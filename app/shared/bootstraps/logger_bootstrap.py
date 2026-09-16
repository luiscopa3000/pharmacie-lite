

from typing import Optional
from app.shared.domain.interfaces.logger import ILogger
from app.shared.infrastructure.logger import Logger

_logger: Optional[ILogger] = None


def bootstrap_logger() -> None:
    """
    Se llama UNA sola vez desde main.py
    Inicializa toda la infraestructura global
    """
    global _logger

    if _logger is None:
        _logger = Logger()


def get_logger() -> ILogger:
    """
    Acceso global a la MISMA instancia
    """
    if _logger is None:
        raise RuntimeError(
            "Application not bootstrapped. Call bootstrap() in main.py first."
        )
    return _logger



