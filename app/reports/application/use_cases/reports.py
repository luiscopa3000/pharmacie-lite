from typing import Any
from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.reports.domain.constants import ReportsDbOperations
from app.reports.domain.interfaces import IReportsRepository
class ReportsUseCases:
 def __init__(self,logger:ILogger,repository:IReportsRepository): self.logger=logger; self.repository=repository
 @generic_error_handler()
 def run(self,operation:ReportsDbOperations,actor_user_id:int,payload:dict[str,Any],*,request_id=None,host=None)->dict:
  return self.repository.execute(operation,{"actor_user_id":actor_user_id,**payload},request_id=request_id,host=host,current_user_id=str(actor_user_id))
