from typing import Any
from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.audit.domain.constants import AuditDbOperations
from app.audit.domain.interfaces import IAuditRepository
class AuditUseCases:
    def __init__(self,logger:ILogger,repository:IAuditRepository): self.logger=logger; self.repository=repository
    @generic_error_handler()
    def run(self,operation:AuditDbOperations,actor_user_id:int,payload:dict[str,Any],*,request_id=None,host=None)->dict:
        return self.repository.execute(operation,{"actor_user_id":actor_user_id,**payload},request_id=request_id,host=host,current_user_id=str(actor_user_id))
