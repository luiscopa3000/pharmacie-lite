from enum import Enum
class ReportsDbOperations(str,Enum):
    DASHBOARD="reports.fn_dashboard"
    SALES_PERIOD="reports.fn_sales_by_period"
    SALES_PRODUCT="reports.fn_sales_by_product"
    SALES_USER="reports.fn_sales_by_user"
    INVENTORY="reports.fn_inventory"
    MOVEMENTS="reports.fn_movements"
    LOW_STOCK="reports.fn_low_stock"
    EXPIRING="reports.fn_expiring"
    EXPIRED="reports.fn_expired"
    VOIDED_SALES="reports.fn_voided_sales"
    CASH_CLOSURES="reports.fn_cash_closures"
