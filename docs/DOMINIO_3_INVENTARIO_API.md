# API – Dominio 3: Inventario

> **Base URL de desarrollo:** `http://localhost:8000`  
> **Formato:** JSON  
> **Endpoints protegidos:** `Authorization: Bearer <access_token>`  
> **Respuesta estándar:** `{"message":"...","data":{...}}`  
> **Errores esperables:** `400` datos inválidos, `401` sesión/token inválido, `403` sin permiso, `404` no existe, `409` conflicto, `422` regla de negocio.


## Orden recomendado

1. Tener producto/presentación creado en Catálogo.
2. Registrar lote si corresponde.
3. Registrar entrada de stock.
4. Consultar stock.
5. Usar ajustes o bajas solo para correcciones justificadas.
6. Consultar movimientos y vencimientos.

> El stock es derivado de movimientos. No existe una operación válida para asignar directamente `producto.stock`.

## Stock

### GET `/inventory/stock`
**Permiso:** `INVENTORY_VIEW`.  
**Query:** `search`, `include_inactive`, `limit` (1–100), `offset`.  
**200:** productos con stock consolidado + `pagination`.

### GET `/inventory/stock/out-of-stock`
**Permiso:** `INVENTORY_VIEW`.  
**Query:** `search`, `include_inactive`, `limit`, `offset`.  
**200:** productos con stock vendible igual a cero.

### GET `/inventory/stock/low-stock`
**Permiso:** `INVENTORY_VIEW`.  
**Query:** `search`, `include_inactive`, `limit`, `offset`.  
**200:** productos cuyo stock vendible `<= minimum_stock`.

### GET `/inventory/stock/{product_id}`
**Permiso:** `INVENTORY_VIEW`.  
**Query:** `limit`, `offset` para los lotes.  
**200**
```json
{
  "data":{
    "stock":{"product_id":1,"quantity_on_hand":100,"sellable_quantity":90},
    "lots":[],
    "pagination":{"total":2,"limit":50,"offset":0,"has_more":false}
  }
}
```

### POST `/inventory/stock/entries`
**Permiso:** `INVENTORY_ENTRY`.  
**Body**
```json
{
  "presentation_id":1,
  "quantity":10,
  "reason_text":"Ingreso por compra",
  "batch_code":"L-2026-001",
  "expiry_date":"2027-12-31"
}
```
Para entrada excepcional vencida:
```json
{
  "presentation_id":1,
  "quantity":10,
  "reason_text":"Regularización histórica",
  "batch_code":"L-OLD",
  "expiry_date":"2025-01-01",
  "expired_entry_authorized":true,
  "authorization_reason":"Regularización documentada"
}
```
**201:** movimiento de entrada y estado resultante.  
**No usar:** cantidad <= 0 ni entrada vencida sin autorización.

### POST `/inventory/stock/adjustments`
**Permiso:** `INVENTORY_ADJUST`.  
**Body**
```json
{
  "stock_lot_id":1,
  "quantity":2,
  "adjustment_kind":"ADJUSTMENT_NEGATIVE",
  "reason_text":"Diferencia detectada en conteo físico"
}
```
`adjustment_kind`: `ADJUSTMENT_POSITIVE`, `ADJUSTMENT_NEGATIVE`.  
**201:** movimiento compensatorio.  
**No usar:** nunca editar el movimiento original.

### POST `/inventory/stock/disposals`
**Permiso:** `INVENTORY_DISPOSE`.  
**Body**
```json
{"stock_lot_id":1,"quantity":3,"reason_text":"Producto dañado"}
```
**201:** baja irreversible desde operación normal.

## Movimientos

### GET `/inventory/movements`
**Permiso:** `INVENTORY_VIEW`.  
**Query:** `product_id`, `stock_lot_id`, `movement_kind`, `performed_by_user_id`, `date_from`, `date_to`, `limit`, `offset`.  
**200:** movimientos paginados, normalmente más recientes primero.

### GET `/inventory/products/{product_id}/movements`
**Permiso:** `INVENTORY_VIEW`.  
**Query:** `stock_lot_id`, `movement_kind`, `date_from`, `date_to`, `limit`, `offset`.  
**200:** historial cronológico del producto.

## Lotes

### POST `/inventory/lots`
**Permiso:** `INVENTORY_LOT_MANAGE`.  
**Body**
```json
{"product_id":1,"batch_code":"L-2026-001","expiry_date":"2027-12-31"}
```
**201:** devuelve `stock_lot_id`.  
**No usar:** la cantidad del lote no se establece aquí.

### GET `/inventory/lots`
**Permiso:** `INVENTORY_VIEW`.  
**Query:** `product_id`, `lot_status` (`ALL`, `AVAILABLE`, `DEPLETED`, `EXPIRED`), `search`, `limit`, `offset`.

### GET `/inventory/lots/expiring`
**Permiso:** `INVENTORY_VIEW`.  
**Query:** `days` (1–3650, default 30), `product_id`, `limit`, `offset`.

### GET `/inventory/lots/expired`
**Permiso:** `INVENTORY_VIEW`.  
**Query:** `product_id`, `limit`, `offset`.  
**200:** lotes vencidos con información física; su stock vendible debe ser cero.

## Uso incorrecto a evitar

- No hacer `UPDATE` directo del stock.
- No editar/eliminar movimientos históricos.
- No vender desde Inventario; Ventas consume FEFO al confirmar.
- No considerar lotes vencidos como vendibles.
