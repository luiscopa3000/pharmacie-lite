from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request, status
from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.sales.bootstraps import bootstrap_sales
from app.sales.domain.constants import SalesDbOperations
from app.sales.api.schemas import (
    SaleCreateSchema, SaleItemCreateSchema, SaleItemQuantitySchema,
    SaleConfirmSchema, SaleVoidSchema, PaymentCompleteSchema, PaymentAuthorizeSchema,
)

sales_router = APIRouter(tags=["Sales"])

def _ctx(request: Request):
    return getattr(request.state, "request_id", None), request.client.host if request.client else None

def _run(request: Request, session: SessionContext, op: SalesDbOperations, payload: dict):
    request_id, host = _ctx(request)
    return bootstrap_sales(get_logger()).run(
        op, session.user_id, payload, request_id=request_id, host=host
    )

@sales_router.post("", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def create_sale(request: Request, data: SaleCreateSchema,
                session: SessionContext = Depends(require_permission("SALES_CREATE"))):
    return ResponseMessage(message="Venta pendiente creada correctamente",
        data=_run(request, session, SalesDbOperations.SALE_CREATE, data.model_dump(exclude_none=True)))

@sales_router.post("/{sale_id}/items", response_model=ResponseMessage[dict])
def add_item(sale_id: int, request: Request, data: SaleItemCreateSchema,
             session: SessionContext = Depends(require_permission("SALES_CREATE"))):
    return ResponseMessage(message="Producto agregado a la venta correctamente",
        data=_run(request, session, SalesDbOperations.SALE_ADD_ITEM,
                  {"sale_id": sale_id, **data.model_dump()}))

@sales_router.patch("/items/{sale_item_id}", response_model=ResponseMessage[dict])
def set_item_quantity(sale_item_id: int, request: Request, data: SaleItemQuantitySchema,
                      session: SessionContext = Depends(require_permission("SALES_CREATE"))):
    return ResponseMessage(message="Cantidad actualizada correctamente",
        data=_run(request, session, SalesDbOperations.SALE_SET_ITEM_QUANTITY,
                  {"sale_item_id": sale_item_id, **data.model_dump()}))

@sales_router.delete("/items/{sale_item_id}", response_model=ResponseMessage[dict])
def remove_item(sale_item_id: int, request: Request,
                session: SessionContext = Depends(require_permission("SALES_CREATE"))):
    return ResponseMessage(message="Producto retirado de la venta correctamente",
        data=_run(request, session, SalesDbOperations.SALE_REMOVE_ITEM,
                  {"sale_item_id": sale_item_id}))

@sales_router.post("/{sale_id}/confirm", response_model=ResponseMessage[dict])
def confirm_sale(sale_id: int, request: Request, data: SaleConfirmSchema,
                 session: SessionContext = Depends(require_permission("SALES_CONFIRM"))):
    return ResponseMessage(message="Venta confirmada correctamente",
        data=_run(request, session, SalesDbOperations.SALE_CONFIRM,
                  {"sale_id": sale_id, "payment": data.payment.model_dump(exclude_none=True)}))

@sales_router.post("/{sale_id}/void", response_model=ResponseMessage[dict])
def void_sale(sale_id: int, request: Request, data: SaleVoidSchema,
              session: SessionContext = Depends(require_permission("SALES_VOID"))):
    return ResponseMessage(message="Venta anulada correctamente",
        data=_run(request, session, SalesDbOperations.SALE_VOID,
                  {"sale_id": sale_id, **data.model_dump()}))

@sales_router.post("/{sale_id}/payment/complete", response_model=ResponseMessage[dict])
def complete_payment(sale_id: int, request: Request, data: PaymentCompleteSchema,
                     session: SessionContext = Depends(require_permission("SALES_PAYMENT_RECORD"))):
    return ResponseMessage(message="Datos de pago actualizados correctamente",
        data=_run(request, session, SalesDbOperations.PAYMENT_COMPLETE,
                  {"sale_id": sale_id, **data.model_dump(exclude_none=True)}))

@sales_router.post("/{sale_id}/payment/authorize", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def authorize_payment_edit(sale_id: int, request: Request, data: PaymentAuthorizeSchema,
                           session: SessionContext = Depends(require_permission("SALES_PAYMENT_EDIT_AUTHORIZE"))):
    return ResponseMessage(message="Edición de pago autorizada correctamente",
        data=_run(request, session, SalesDbOperations.PAYMENT_AUTHORIZE,
                  {"sale_id": sale_id, **data.model_dump()}))

@sales_router.get("/payments/pending", response_model=ResponseMessage[dict])
def pending_payments(request: Request,
                     cash_session_id: int | None = Query(default=None, gt=0),
                     limit: int = Query(50, ge=1, le=100),
                     offset: int = Query(0, ge=0),
                     session: SessionContext = Depends(require_permission("SALES_VIEW"))):
    return ResponseMessage(message="Pagos electrónicos pendientes consultados correctamente",
        data=_run(request, session, SalesDbOperations.PAYMENTS_PENDING,
                  {"cash_session_id": cash_session_id, "limit": limit, "offset": offset}))

@sales_router.get("", response_model=ResponseMessage[dict])
def search_sales(request: Request,
                 date_from: datetime | None = None,
                 date_to: datetime | None = None,
                 seller_user_id: int | None = Query(default=None, gt=0),
                 sale_status: str | None = Query(default=None, max_length=20),
                 cash_session_id: int | None = Query(default=None, gt=0),
                 sale_number: str | None = Query(default=None, max_length=80),
                 limit: int = Query(50, ge=1, le=100),
                 offset: int = Query(0, ge=0),
                 session: SessionContext = Depends(require_permission("SALES_VIEW"))):
    payload = {
        "date_from": date_from, "date_to": date_to,
        "seller_user_id": seller_user_id, "sale_status": sale_status,
        "cash_session_id": cash_session_id, "sale_number": sale_number,
        "limit": limit, "offset": offset,
    }
    return ResponseMessage(message="Ventas consultadas correctamente",
        data=_run(request, session, SalesDbOperations.SALES_SEARCH,
                  {k: v for k, v in payload.items() if v is not None}))

@sales_router.get("/by-number/{sale_number}", response_model=ResponseMessage[dict])
def sale_by_number(sale_number: str, request: Request,
                   session: SessionContext = Depends(require_permission("SALES_VIEW"))):
    return ResponseMessage(message="Venta consultada correctamente",
        data=_run(request, session, SalesDbOperations.SALE_GET, {"sale_number": sale_number}))

@sales_router.get("/{sale_id}", response_model=ResponseMessage[dict])
def sale_get(sale_id: int, request: Request,
             session: SessionContext = Depends(require_permission("SALES_VIEW"))):
    return ResponseMessage(message="Venta consultada correctamente",
        data=_run(request, session, SalesDbOperations.SALE_GET, {"sale_id": sale_id}))

@sales_router.get("/{sale_id}/receipt", response_model=ResponseMessage[dict])
def sale_receipt(sale_id: int, request: Request,
                 session: SessionContext = Depends(require_permission("SALES_VIEW"))):
    return ResponseMessage(message="Comprobante interno generado correctamente",
        data=_run(request, session, SalesDbOperations.SALE_RECEIPT, {"sale_id": sale_id}))
