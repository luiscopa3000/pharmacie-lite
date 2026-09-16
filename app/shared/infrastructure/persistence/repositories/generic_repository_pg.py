from enum import Enum
from datetime import datetime
from typing import List, Dict, Optional
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.database import ISqlDatabase
from app.shared.domain.interfaces.generic_repository import IGenericRepository
from app.shared.decorators import generic_error_handler

class GenericRepositoryPg(IGenericRepository):
    def __init__(self, logger: ILogger, database: ISqlDatabase) -> None:
        self.logger = logger
        self.database = database

    @generic_error_handler()
    def execute_operation(
        self,
        query: Enum | str,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        **kwargs,
    ) -> List[Dict]:
        query_name = query.value if isinstance(query, Enum) else query
    
        parameters = {}

        for k, v in kwargs.items():
            if isinstance(v, Enum):
                parameters[k] = v.value

            elif isinstance(v, datetime):
                parameters[k] = v.strftime("%Y-%m-%d %H:%M:%S.%f")

            else:
                parameters[k] = v
    
        self.logger.info(
            f"Ejecutando '{query_name}' con parámetros {parameters}",
            request_id=request_id, 
            host=host
        )
    
        result = self.database.execute_query_dynamic(
            query_name=query_name,
            obj=parameters,
            request_id=request_id,
            host=host
        )

        return result[0][0] if result else []