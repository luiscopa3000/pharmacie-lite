from abc import ABC,abstractmethod
from typing import Any
from app.reports.domain.constants import ReportsDbOperations
class IReportsRepository(ABC):
 @abstractmethod
 def execute(self,operation:ReportsDbOperations,payload:dict[str,Any],**kwargs)->dict[str,Any]: raise NotImplementedError
