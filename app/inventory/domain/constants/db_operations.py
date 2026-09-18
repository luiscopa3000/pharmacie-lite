from enum import Enum


class InventoryDbOperations(str, Enum):
    STOCK_QUERY = "inventory.fn_stock_query"
    STOCK_PRODUCT_GET = "inventory.fn_stock_product_get"

    STOCK_ENTRY = "inventory.fn_stock_entry"
    ADJUSTMENT_REGISTER = "inventory.fn_adjustment_register"
    DISPOSAL_REGISTER = "inventory.fn_disposal_register"

    MOVEMENTS_QUERY = "inventory.fn_movements_query"
    PRODUCT_MOVEMENTS_QUERY = "inventory.fn_product_movements_query"

    LOT_REGISTER = "inventory.fn_lot_register"
    LOTS_QUERY = "inventory.fn_lots_query"
    LOTS_EXPIRING = "inventory.fn_lots_expiring"
    LOTS_EXPIRED = "inventory.fn_lots_expired"
