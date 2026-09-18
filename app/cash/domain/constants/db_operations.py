from enum import Enum

class CashDbOperations(str, Enum):
    CASH_OPEN = "cash.fn_cash_open"
    CASH_OPENING_AMOUNT_UPDATE = "cash.fn_cash_opening_amount_update"
    CASH_SESSION_GET = "cash.fn_cash_session_get"
    CASH_SESSIONS_LIST = "cash.fn_cash_sessions_list"
    CASH_SESSION_SALES = "cash.fn_cash_session_sales"
    CASH_CLOSE = "cash.fn_cash_close"
