import sys
import inspect
import logging
from typing import Optional
from app.shared.domain.interfaces.logger import ILogger


class Logger(ILogger):
    LOGGER_NAME = "application"
    DEFAULT_LEVEL = logging.INFO

    def __init__(self) -> None:
        self._logger = self._configure_logger()

    def _configure_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.LOGGER_NAME)

        if not logger.handlers:
            logger.setLevel(self.DEFAULT_LEVEL)

            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(message)s"))

            logger.addHandler(handler)
            logger.propagate = False

        return logger

    @staticmethod
    def _resolve_component(frame) -> str:
        self_obj = frame.f_locals.get("self")
        return self_obj.__class__.__name__ if self_obj else "General"

    @staticmethod
    def _resolve_caller_context() -> tuple[str, str, str]:
        frame = inspect.currentframe()

        while frame:
            module = frame.f_globals.get("__name__", "unknown")

            if (
                not module.startswith("app.shared.infrastructure.logger")
                and not module.startswith("logging")
            ):
                action = frame.f_code.co_name
                component = Logger._resolve_component(frame)
                return module, action, component

            frame = frame.f_back

        return "unknown", "unknown", "General"

    def _format(
        self,
        message: str,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> str:
        module, action, component = self._resolve_caller_context()

        return (
            f"[{request_id or '-'}] "
            f"[{host or '-'}] "
            f"[{component}] "
            f"[{module}] "
            f"[{action}] "
            f"{message}"
        )

    def info(
        self,
        message: str,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        self._logger.info(self._format(message, request_id, host))

    def warning(
        self,
        message: str,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        self._logger.warning(self._format(message, request_id, host))

    def error(
        self,
        message: str,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        self._logger.error(self._format(message, request_id, host))

    def critical(
        self,
        message: str,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        self._logger.critical(self._format(message, request_id, host))