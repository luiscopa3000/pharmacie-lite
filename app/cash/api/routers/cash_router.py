from fastapi import APIRouter, Depends, Query, Request, status
from app.shared.api.schemas import ResponseMessage
from app.shared.bootstraps import get_logger
from app.identity.api.dependencies import require_permission
from app.identity.domain.models.session_context import SessionContext
from app.cash.api.schemas import CashOpenSchema, CashOpeningAmountUpdateSchema, CashCloseSchema
from app.cash.bootstraps import bootstrap_cash
from app.cash.domain.constants import CashDbOperations

cash_router = APIRouter(tags=["Cash"])

def _run(request: Request, session: SessionContext, op: CashDbOperations, payload: dict):
    request_id = getattr(request.state, "request_id", None)
    host = request.client.host if request.client else None
    return bootstrap_cash(get_logger()).run(
        op, session.user_id, payload, request_id=request_id, host=host
    )

@cash_router.post("/sessions", response_model=ResponseMessage[dict], status_code=status.HTTP_201_CREATED)
def open_cash(request: Request, data: CashOpenSchema,
              session: SessionContext = Depends(require_permission("CASH_OPEN"))):
    return ResponseMessage(
        message="Caja abierta correctamente",
        data=_run(request, session, CashDbOperations.CASH_OPEN, data.model_dump())
    )

@cash_router.patch("/sessions/{cash_session_id}/opening-amount", response_model=ResponseMessage[dict])
def update_opening_amount(cash_session_id: int, request: Request,
                          data: CashOpeningAmountUpdateSchema,
                          session: SessionContext = Depends(require_permission("CASH_OPEN"))):
    return ResponseMessage(
        message="Monto inicial actualizado correctamente",
        data=_run(
            request, session, CashDbOperations.CASH_OPENING_AMOUNT_UPDATE,
            {"cash_session_id": cash_session_id, **data.model_dump()}
        )
    )

@cash_router.get("/sessions/current", response_model=ResponseMessage[dict])
def current_session(request: Request,
                    session: SessionContext = Depends(require_permission("CASH_VIEW"))):
    return ResponseMessage(
        message="Sesión de caja actual consultada correctamente",
        data=_run(request, session, CashDbOperations.CASH_SESSION_GET, {})
    )

@cash_router.get("/sessions", response_model=ResponseMessage[dict])
def list_sessions(request: Request,
                  responsible_user_id: int | None = Query(default=None, gt=0),
                  session_status: str | None = Query(default=None, max_length=16),
                  limit: int = Query(default=50, ge=1, le=100),
                  offset: int = Query(default=0, ge=0),
                  session: SessionContext = Depends(require_permission("CASH_VIEW"))):
    payload = {
        "responsible_user_id": responsible_user_id,
        "session_status": session_status,
        "limit": limit,
        "offset": offset,
    }
    return ResponseMessage(
        message="Sesiones de caja consultadas correctamente",
        data=_run(
            request, session, CashDbOperations.CASH_SESSIONS_LIST,
            {k: v for k, v in payload.items() if v is not None}
        )
    )

@cash_router.get("/sessions/{cash_session_id}", response_model=ResponseMessage[dict])
def get_session(cash_session_id: int, request: Request,
                session: SessionContext = Depends(require_permission("CASH_VIEW"))):
    return ResponseMessage(
        message="Sesión de caja consultada correctamente",
        data=_run(
            request, session, CashDbOperations.CASH_SESSION_GET,
            {"cash_session_id": cash_session_id}
        )
    )

@cash_router.get("/sessions/{cash_session_id}/sales", response_model=ResponseMessage[dict])
def session_sales(cash_session_id: int, request: Request,
                  sale_status: str | None = Query(default=None, max_length=16),
                  limit: int = Query(default=50, ge=1, le=100),
                  offset: int = Query(default=0, ge=0),
                  session: SessionContext = Depends(require_permission("CASH_VIEW"))):
    payload = {
        "cash_session_id": cash_session_id,
        "sale_status": sale_status,
        "limit": limit,
        "offset": offset,
    }
    return ResponseMessage(
        message="Ventas de la sesión de caja consultadas correctamente",
        data=_run(
            request, session, CashDbOperations.CASH_SESSION_SALES,
            {k: v for k, v in payload.items() if v is not None}
        )
    )

@cash_router.post("/sessions/{cash_session_id}/close", response_model=ResponseMessage[dict])
def close_cash(cash_session_id: int, request: Request, data: CashCloseSchema,
               session: SessionContext = Depends(require_permission("CASH_CLOSE"))):
    return ResponseMessage(
        message="Caja cerrada correctamente",
        data=_run(
            request, session, CashDbOperations.CASH_CLOSE,
            {"cash_session_id": cash_session_id, **data.model_dump()}
        )
    )
