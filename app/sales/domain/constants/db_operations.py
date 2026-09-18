from enum import Enum

class SalesDbOperations(str, Enum):
    SALE_CREATE = "sales.fn_sale_create"
    SALE_ADD_ITEM = "sales.fn_sale_add_item"
    SALE_SET_ITEM_QUANTITY = "sales.fn_sale_set_item_quantity"
    SALE_REMOVE_ITEM = "sales.fn_sale_remove_item"
    SALE_CONFIRM = "sales.fn_sale_confirm"
    SALE_VOID = "sales.fn_sale_void"
    PAYMENT_COMPLETE = "sales.fn_payment_complete"
    PAYMENT_AUTHORIZE = "sales.fn_payment_authorize"
    PAYMENTS_PENDING = "sales.fn_payments_pending"
    SALE_GET = "sales.fn_sale_get"
    SALES_SEARCH = "sales.fn_sales_search"
    SALE_RECEIPT = "sales.fn_sale_receipt"
