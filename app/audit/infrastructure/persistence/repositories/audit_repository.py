from typing import Any
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.database import ISqlDatabase
from app.shared.domain.models.errors import StandardizedError
from app.audit.domain.constants import AuditDbOperations
from app.audit.domain.interfaces import IAuditRepository
_SQLSTATE_HTTP={"PH400":(400,"BAD_REQUEST"),"PH401":(401,"UNAUTHORIZED"),"PH403":(403,"FORBIDDEN"),"PH404":(404,"NOT_FOUND"),"PH409":(409,"CONFLICT"),"PH422":(422,"UNPROCESSABLE_ENTITY")}
def _sqlstate(exc):
    for a in ("sqlstate","pgcode"):
        v=getattr(exc,a,None)
        if v:return str(v)
    o=getattr(exc,"orig",None)
    if o:
        for a in ("sqlstate","pgcode"):
            v=getattr(o,a,None)
            if v:return str(v)
    return None
def _first_json(raw:Any)->dict[str,Any]:
    if isinstance(raw,dict): return raw
    cur=raw
    for _ in range(4):
        if isinstance(cur,(list,tuple)) and cur: cur=cur[0]
        else: break
    if isinstance(cur,dict):
        if len(cur)==1:
            only=next(iter(cur.values()))
            if isinstance(only,dict): return only
        return cur
    raise StandardizedError(error="DB_INVALID_RESPONSE",error_code="INTERNAL_SERVER_ERROR",error_type="DATABASE_ERROR",user_message="La base de datos devolvió una respuesta no válida.",http_status=500)
class AuditRepository(IAuditRepository):
    def __init__(self,logger:ILogger,database:ISqlDatabase): self.logger=logger; self.database=database
    def execute(self,operation:AuditDbOperations,payload:dict[str,Any],*,request_id=None,host=None,current_user_id=None)->dict[str,Any]:
        try:
            return _first_json(self.database.execute_query_dynamic(query_name=operation.value,obj=payload,request_id=request_id,host=host,current_user_id=current_user_id))
        except StandardizedError: raise
        except Exception as exc:
            st=_sqlstate(exc)
            if st in _SQLSTATE_HTTP:
                hs,ec=_SQLSTATE_HTTP[st]
                raise StandardizedError(error=st,error_code=ec,error_type="BUSINESS_RULE_ERROR",user_message=str(exc).split("\n",1)[0] or "La operación fue rechazada.",http_status=hs) from exc
            raise StandardizedError(error="DB_ERROR",error_code="INTERNAL_SERVER_ERROR",error_type="DATABASE_ERROR",user_message="Ocurrió un error interno al ejecutar la operación.",http_status=500) from exc
