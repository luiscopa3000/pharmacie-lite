# API – Dominio 4: Ventas

> **Base URL de desarrollo:** `http://localhost:8000`  
> **Formato:** JSON  
> **Endpoints protegidos:** `Authorization: Bearer <access_token>`  
> **Respuesta estándar:** `{"message":"...","data":{...}}`  
> **Errores esperables:** `400` datos inválidos, `401` sesión/token inválido, `403` sin permiso, `404` no existe, `409` conflicto, `422` regla de negocio.


## Orden recomendado

1. Tener caja `OPEN`.
2. Buscar producto mediante **Catálogo**.
3. `POST /sales` para crear venta `PENDING`.
4. Agregar/modificar/eliminar renglones.
5. Confirmar con forma de pago.
6. Completar referencia electrónica si queda pendiente.
7. Consultar/comprobante.
8. Anular solo cuando corresponda.

> La venta `PENDING` no mueve inventario. La confirmación calcula todo en servidor, asigna lotes FEFO y genera movimientos en una sola transacción.

## Búsqueda de productos

**No existe búsqueda duplicada dentro de `/sales`.** Use:
```text
GET /catalog/products?search=Paracetamol&for_sale=true&limit=20&offset=0
GET /catalog/products?barcode=7700000000011&for_sale=true
```

## Venta pendiente

### POST `/sales`
**Permiso:** `SALES_CREATE`.  
**Body**
```json
{"cash_session_id":1}
```
`cash_session_id` es opcional si la BD puede resolver la caja abierta del usuario.  
**201:** venta en estado `PENDING` con `sale_id`.  
**No usar:** no crear ventas sin caja operable.

### POST `/sales/{sale_id}/items`
**Permiso:** `SALES_CREATE`.  
**Body**
```json
{"presentation_id":1,"quantity":2}
```
**200:** detalle agregado/recalculado.  
**No usar:** no enviar precio; el servidor toma el precio vigente.

### PATCH `/sales/items/{sale_item_id}`
**Permiso:** `SALES_CREATE`.  
**Body:** `{"quantity":3}`  
**200:** subtotal recalculado. Solo venta `PENDING`.

### DELETE `/sales/items/{sale_item_id}`
**Permiso:** `SALES_CREATE`.  
**Body:** ninguno.  
**200:** renglón eliminado. No mueve inventario mientras siga `PENDING`.

## Confirmación y pago

### POST `/sales/{sale_id}/confirm`
**Permiso:** `SALES_CONFIRM`.  
**Efectivo**
```json
{"payment":{"payment_method_code":"CASH"}}
```
**QR**
```json
{"payment":{"payment_method_code":"QR","transaction_ref":"QR-2026-000001"}}
```
Métodos: `CASH`, `QR`, `BANK_TRANSFER`, `CARD`.  
**200:** venta `CONFIRMED`, total fijado, lotes FEFO asignados y stock descontado.  
**No usar:** no enviar total, precio final, lotes o movimientos desde frontend.

### POST `/sales/{sale_id}/payment/complete`
**Permiso:** `SALES_PAYMENT_RECORD`.  
**Body**
```json
{
  "transaction_ref":"QR-2026-000001",
  "transaction_at":"2026-09-18T10:30:00-04:00",
  "reason_text":"Referencia verificada"
}
```
`transaction_at` y `reason_text` son opcionales según la situación.

### POST `/sales/{sale_id}/payment/authorize`
**Permiso:** `SALES_PAYMENT_EDIT_AUTHORIZE`.  
**Body**
```json
{
  "reason_text":"Se autoriza completar referencia fuera del plazo",
  "valid_hours":24
}
```
`valid_hours`: 1–168.  
**201:** autorización administrativa.

### GET `/sales/payments/pending`
**Permiso:** `SALES_VIEW`.  
**Query:** `cash_session_id`, `limit`, `offset`.  
**200:** ventas con datos electrónicos pendientes + `pagination`.

## Anulación

### POST `/sales/{sale_id}/void`
**Permiso:** `SALES_VOID`.  
**Body**
```json
{"void_reason":"Venta registrada con producto incorrecto"}
```
**200:** venta `VOIDED`; repone exactamente los lotes originales mediante movimientos inversos.  
**No usar:** no editar ni borrar una venta confirmada.

## Consultas

### GET `/sales`
**Permiso:** `SALES_VIEW`.  
**Query:** `date_from`, `date_to`, `seller_user_id`, `sale_status`, `cash_session_id`, `sale_number`, `limit`, `offset`.  
`sale_status`: `PENDING`, `CONFIRMED`, `VOIDED`.  
**200:** `items + pagination`.

### GET `/sales/by-number/{sale_number}`
**Permiso:** `SALES_VIEW`.  
**200:** venta por número único.

### GET `/sales/{sale_id}`
**Permiso:** `SALES_VIEW`.  
**200:** venta y detalle histórico.

### GET `/sales/{sale_id}/receipt`
**Permiso:** `SALES_VIEW`.  
**200:** datos del comprobante interno. Solo debe emitirse para venta confirmada según regla de negocio.

## Uso incorrecto a evitar

- No enviar `card_number`, `cvv` ni `pin`.
- No calcular total definitivo en frontend.
- No asignar lotes desde frontend.
- No confirmar dos veces la misma venta.
- No modificar una venta confirmada; usar anulación.
