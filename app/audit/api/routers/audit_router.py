from datetime import datetime
from fastapi import APIRouter,Depends,Query,Request
from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.audit.bootstraps import bootstrap_audit
from app.audit.domain.constants import AuditDbOperations
router=APIRouter(tags=["Audit"])
def _run(request,session,op,payload):
    return bootstrap_audit(get_logger()).run(op,session.user_id,payload,request_id=getattr(request.state,"request_id",None),host=request.client.host if request.client else None)
@router.get("/events",response_model=ResponseMessage[dict])
def events(request:Request,target_user_id:int|None=Query(None,gt=0),event_module:str|None=None,event_action:str|None=None,entity_schema:str|None=None,entity_table:str|None=None,entity_key:str|None=None,date_from:datetime|None=None,date_to:datetime|None=None,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission("AUDIT_VIEW"))):
    p={"target_user_id":target_user_id,"event_module":event_module,"event_action":event_action,"entity_schema":entity_schema,"entity_table":entity_table,"entity_key":entity_key,"date_from":date_from,"date_to":date_to,"limit":limit,"offset":offset}
    return ResponseMessage(message="Historial de auditoría consultado correctamente",data=_run(request,session,AuditDbOperations.AUDIT_QUERY,{k:v for k,v in p.items() if v is not None}))
@router.get("/login-attempts",response_model=ResponseMessage[dict])
def login_attempts(request:Request,target_user_id:int|None=Query(None,gt=0),login_identifier:str|None=None,was_successful:bool|None=None,date_from:datetime|None=None,date_to:datetime|None=None,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission("AUDIT_VIEW"))):
    p={"target_user_id":target_user_id,"login_identifier":login_identifier,"was_successful":was_successful,"date_from":date_from,"date_to":date_to,"limit":limit,"offset":offset}
    return ResponseMessage(message="Intentos de inicio de sesión consultados correctamente",data=_run(request,session,AuditDbOperations.LOGIN_ATTEMPTS_QUERY,{k:v for k,v in p.items() if v is not None}))
@router.get("/entities/{entity_schema}/{entity_table}/{entity_key}",response_model=ResponseMessage[dict])
def entity_trace(entity_schema:str,entity_table:str,entity_key:str,request:Request,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission("AUDIT_VIEW"))):
    return ResponseMessage(message="Trazabilidad de entidad consultada correctamente",data=_run(request,session,AuditDbOperations.ENTITY_TRACE,{"entity_schema":entity_schema,"entity_table":entity_table,"entity_key":entity_key,"limit":limit,"offset":offset}))
