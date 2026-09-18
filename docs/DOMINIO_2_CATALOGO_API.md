# API – Dominio 2: Catálogo de Productos y Medicamentos

> **Base URL de desarrollo:** `http://localhost:8000`  
> **Formato:** JSON  
> **Endpoints protegidos:** `Authorization: Bearer <access_token>`  
> **Respuesta estándar:** `{"message":"...","data":{...}}`  
> **Errores esperables:** `400` datos inválidos, `401` sesión/token inválido, `403` sin permiso, `404` no existe, `409` conflicto, `422` regla de negocio.


## Orden recomendado

1. Consultar unidades de medida.
2. Crear referencias: fabricante, forma farmacéutica y principio activo.
3. Crear categorías.
4. Crear producto con al menos una presentación.
5. Consultar/buscar producto y precio.
6. Agregar o editar presentaciones.
7. Activar/desactivar producto, presentación o categoría cuando corresponda.

> Catálogo **no modifica stock**. El stock solo se consulta; entradas y ajustes pertenecen a Inventario.

## Referencias

### GET `/catalog/references/measurement-units`
**Permiso:** `CATALOG_PRODUCT_VIEW`.  
**200:** `data.items` con unidades disponibles.

### POST `/catalog/references`
**Permiso:** `CATALOG_REFERENCE_MANAGE`.  
**Body**
```json
{"reference_kind":"MANUFACTURER","name":"Laboratorios Bagó"}
```
`reference_kind`: `MANUFACTURER`, `DOSAGE_FORM`, `ACTIVE_INGREDIENT`.  
**201:** referencia creada/reutilizada.

### GET `/catalog/references`
**Permiso:** `CATALOG_PRODUCT_VIEW`.  
**Query:** `reference_kind`, `search`, `limit` (1–100), `offset`.  
**200:** `items + pagination`.

## Categorías

### POST `/catalog/categories`
**Permiso:** `CATALOG_CATEGORY_MANAGE`.  
**Body:** `{"category_name":"Analgésicos"}`  
**201:** categoría `ACTIVE`.

### GET `/catalog/categories`
**Permiso:** `CATALOG_PRODUCT_VIEW`.  
**Query:** `record_status`, `search`, `limit`, `offset`.  
**200:** `items + pagination`.

### PATCH `/catalog/categories/{category_id}`
**Permiso:** `CATALOG_CATEGORY_MANAGE`.  
**Body:** `{"category_name":"Analgésicos y Antipiréticos"}`

### PATCH `/catalog/categories/{category_id}/status`
**Permiso:** `CATALOG_CATEGORY_MANAGE`.  
**Body:** `{"record_status":"INACTIVE"}`

### GET `/catalog/categories/{category_id}/products`
**Permiso:** `CATALOG_PRODUCT_VIEW`.  
**Query:** `record_status`, `for_sale`, `limit`, `offset`.  
**200:** productos de esa categoría con `pagination`.

## Productos

### POST `/catalog/products`
**Permiso:** `CATALOG_PRODUCT_CREATE`.  
**Body mínimo representativo**
```json
{
  "internal_code":"MED-001",
  "product_name":"Paracetamol 500 mg",
  "product_kind":"MEDICINE",
  "base_unit_code":"TABLETA",
  "category_id":1,
  "manufacturer_id":1,
  "dosage_form_id":1,
  "allows_fractional_sale":true,
  "base_quantity_step":1,
  "minimum_stock":20,
  "requires_lot_control":true,
  "requires_expiry_control":true,
  "record_status":"ACTIVE",
  "active_ingredients":[
    {"active_ingredient_id":1,"strength_value":500,"strength_unit":"mg"}
  ],
  "presentations":[
    {
      "presentation_name":"Tableta",
      "sale_unit_code":"TABLETA",
      "base_units_per_presentation":1,
      "sale_increment":1,
      "sale_price":0.50,
      "barcode":"7700000000011",
      "is_base_presentation":true,
      "record_status":"ACTIVE"
    }
  ]
}
```
**201:** producto con `product_id`, referencias e información de presentaciones.  
**No usar:** no enviar `stock`, `initial_stock` ni `quantity_on_hand`.

### GET `/catalog/products`
**Permiso:** `CATALOG_PRODUCT_VIEW`.  
**Query:** `search`, `barcode`, `product_kind`, `record_status`, `category_id`, `for_sale`, `limit`, `offset`.  
**Ejemplos**
```text
/catalog/products?search=Paracetamol&for_sale=true&limit=20&offset=0
/catalog/products?barcode=7700000000011&for_sale=true
```
**200:** resultados por producto/presentación + `pagination`.

### GET `/catalog/products/{product_id}`
**Permiso:** `CATALOG_PRODUCT_VIEW`.  
**200:** ficha del producto, presentaciones, ingredientes y datos de consulta.

### PATCH `/catalog/products/{product_id}`
**Permiso:** `CATALOG_PRODUCT_UPDATE`.  
**Body:** campos editables: `product_name`, IDs de referencia, `base_unit_code`, fraccionamiento, mínimo, controles de lote/vencimiento.  
**No usar:** no cambiar stock aquí; cambios estructurales con historial pueden ser rechazados.

### PATCH `/catalog/products/{product_id}/status`
**Permiso:** `CATALOG_PRODUCT_STATUS`.  
**Body:** `{"record_status":"INACTIVE"}`

### GET `/catalog/products/{product_id}/stock`
**Permiso:** `CATALOG_PRODUCT_VIEW`.  
**200:** existencia derivada desde Inventario.  
**No usar:** este endpoint es solo lectura.

### POST `/catalog/products/{product_id}/presentations`
**Permiso:** `CATALOG_PRODUCT_UPDATE`.  
**Body**
```json
{
  "presentation_name":"Caja x 20",
  "sale_unit_code":"CAJA",
  "base_units_per_presentation":20,
  "sale_increment":1,
  "sale_price":9.00,
  "barcode":"7700000000028",
  "is_base_presentation":false,
  "record_status":"ACTIVE"
}
```
**201:** devuelve `presentation_id`.

## Presentaciones

### PATCH `/catalog/presentations/{presentation_id}`
**Permiso:** `CATALOG_PRODUCT_UPDATE`.  
**Body:** `presentation_name`, `sale_unit_code`, `base_units_per_presentation`, `sale_increment`, `sale_price`, `barcode`.

### PATCH `/catalog/presentations/{presentation_id}/status`
**Permiso:** `CATALOG_PRODUCT_STATUS`.  
**Body:** `{"record_status":"INACTIVE"}`

### GET `/catalog/presentations/{presentation_id}/price`
**Permiso:** `CATALOG_PRODUCT_VIEW`.  
**Query:** `quantity` > 0, default 1.  
**Ejemplo:** `/catalog/presentations/2/price?quantity=2`  
**200:** precio unitario, subtotal y unidades base equivalentes.

## Uso incorrecto a evitar

- No crear existencias desde Catálogo.
- No reutilizar códigos internos o códigos de barras.
- No cambiar libremente unidad base/conversión de un producto con historial.
- No usar una presentación inactiva para una nueva venta.
