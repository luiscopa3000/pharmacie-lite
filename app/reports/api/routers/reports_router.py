from datetime import date,datetime
from fastapi import APIRouter,Depends,Query,Request
from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.reports.bootstraps import bootstrap_reports
from app.reports.domain.constants import ReportsDbOperations
router=APIRouter(tags=["Reports"])
def _run(request,session,op,p): return bootstrap_reports(get_logger()).run(op,session.user_id,p,request_id=getattr(request.state,"request_id",None),host=request.client.host if request.client else None)
def _clean(p): return {k:v for k,v in p.items() if v is not None}
@router.get('/dashboard',response_model=ResponseMessage[dict])
def dashboard(request:Request,business_date:date|None=None,expiry_days:int|None=Query(None,ge=1,le=365),alert_limit:int=Query(10,ge=1,le=50),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Dashboard consultado correctamente',data=_run(request,session,ReportsDbOperations.DASHBOARD,_clean({'business_date':business_date,'expiry_days':expiry_days,'alert_limit':alert_limit})))
@router.get('/sales/period',response_model=ResponseMessage[dict])
def sales_period(request:Request,date_from:date,date_to:date,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de ventas por período consultado correctamente',data=_run(request,session,ReportsDbOperations.SALES_PERIOD,{'date_from':date_from,'date_to':date_to,'limit':limit,'offset':offset}))
@router.get('/sales/products',response_model=ResponseMessage[dict])
def sales_products(request:Request,date_from:date,date_to:date,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de ventas por producto consultado correctamente',data=_run(request,session,ReportsDbOperations.SALES_PRODUCT,{'date_from':date_from,'date_to':date_to,'limit':limit,'offset':offset}))
@router.get('/sales/users',response_model=ResponseMessage[dict])
def sales_users(request:Request,date_from:date,date_to:date,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de ventas por usuario consultado correctamente',data=_run(request,session,ReportsDbOperations.SALES_USER,{'date_from':date_from,'date_to':date_to,'limit':limit,'offset':offset}))
@router.get('/inventory',response_model=ResponseMessage[dict])
def inventory(request:Request,category_id:int|None=Query(None,gt=0),only_active:bool=True,search:str|None=None,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de inventario consultado correctamente',data=_run(request,session,ReportsDbOperations.INVENTORY,_clean({'category_id':category_id,'only_active':only_active,'search':search,'limit':limit,'offset':offset})))
@router.get('/inventory/movements',response_model=ResponseMessage[dict])
def movements(request:Request,product_id:int|None=Query(None,gt=0),movement_kind:str|None=None,performed_by_user_id:int|None=Query(None,gt=0),date_from:datetime|None=None,date_to:datetime|None=None,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de movimientos consultado correctamente',data=_run(request,session,ReportsDbOperations.MOVEMENTS,_clean({'product_id':product_id,'movement_kind':movement_kind,'performed_by_user_id':performed_by_user_id,'date_from':date_from,'date_to':date_to,'limit':limit,'offset':offset})))
@router.get('/inventory/low-stock',response_model=ResponseMessage[dict])
def low_stock(request:Request,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de stock bajo consultado correctamente',data=_run(request,session,ReportsDbOperations.LOW_STOCK,{'limit':limit,'offset':offset}))
@router.get('/inventory/expiring',response_model=ResponseMessage[dict])
def expiring(request:Request,days:int|None=Query(None,ge=1,le=365),limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de próximos a vencer consultado correctamente',data=_run(request,session,ReportsDbOperations.EXPIRING,_clean({'days':days,'limit':limit,'offset':offset})))
@router.get('/inventory/expired',response_model=ResponseMessage[dict])
def expired(request:Request,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de vencidos consultado correctamente',data=_run(request,session,ReportsDbOperations.EXPIRED,{'limit':limit,'offset':offset}))
@router.get('/sales/voided',response_model=ResponseMessage[dict])
def voided(request:Request,date_from:date|None=None,date_to:date|None=None,limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de anulaciones consultado correctamente',data=_run(request,session,ReportsDbOperations.VOIDED_SALES,_clean({'date_from':date_from,'date_to':date_to,'limit':limit,'offset':offset})))
@router.get('/cash/closures',response_model=ResponseMessage[dict])
def closures(request:Request,date_from:date|None=None,date_to:date|None=None,responsible_user_id:int|None=Query(None,gt=0),limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),session:SessionContext=Depends(require_permission('REPORTS_VIEW'))): return ResponseMessage(message='Reporte de cierres de caja consultado correctamente',data=_run(request,session,ReportsDbOperations.CASH_CLOSURES,_clean({'date_from':date_from,'date_to':date_to,'responsible_user_id':responsible_user_id,'limit':limit,'offset':offset})))
