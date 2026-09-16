from enum import Enum
from typing import Any, Optional, Union
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.generic_repository import IGenericRepository


class QueryExecutorUseCase:
    def __init__(
        self,
        logger: ILogger,
        generic_repository: IGenericRepository
    ) -> None:
        self._logger = logger
        self._repository = generic_repository

    def execute(
        self,
        query: Union[str, Enum],
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        **kwargs: Any
    ) -> list[dict]:
        """
        Executes a dynamic query with arbitrary parameters.
        All variable data must be passed via kwargs.
        """
        params: dict[str, Any] = dict(kwargs)

        self._logger.info(
            message=f"Ejecutando query dinámico: {query}, con parametros: {params}",
            request_id=request_id,
            host=host
        )

        return self._repository.execute_operation(
            query=query,
            request_id=request_id,
            host=host,
            **params
        )