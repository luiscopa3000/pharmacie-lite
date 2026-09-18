from enum import Enum


class CatalogDbOperations(str, Enum):
    CATEGORY_CREATE = "catalog.fn_category_create"
    CATEGORY_UPDATE = "catalog.fn_category_update"
    CATEGORY_SET_STATUS = "catalog.fn_category_set_status"
    CATEGORY_LIST = "catalog.fn_category_list"

    REFERENCE_UPSERT = "catalog.fn_reference_upsert"
    REFERENCE_LIST = "catalog.fn_reference_list"
    MEASUREMENT_UNITS_LIST = "catalog.fn_measurement_units_list"

    PRODUCT_CREATE = "catalog.fn_product_create"
    PRODUCT_UPDATE = "catalog.fn_product_update"
    PRODUCT_GET = "catalog.fn_product_get"
    PRODUCT_SEARCH = "catalog.fn_product_search"
    PRODUCT_SET_STATUS = "catalog.fn_product_set_status"
    PRODUCTS_BY_CATEGORY = "catalog.fn_products_by_category"

    PRESENTATION_CREATE = "catalog.fn_presentation_create"
    PRESENTATION_UPDATE = "catalog.fn_presentation_update"
    PRICE_GET = "catalog.fn_price_get"
    STOCK_GET = "catalog.fn_stock_get"
