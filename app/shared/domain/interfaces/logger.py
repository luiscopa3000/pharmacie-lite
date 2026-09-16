from typing import Optional, Protocol, runtime_checkable

@runtime_checkable
class ILogger(Protocol):
    def info(
        self,
        message: str,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        ...

    def warning(
        self,
        message: str,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        ...

    def error(
        self,
        message: str,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        ...

    def critical(
        self,
        message: str,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        ...