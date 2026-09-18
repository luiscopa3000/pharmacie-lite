# API – Dominio 5: Caja

> **Base URL de desarrollo:** `http://localhost:8000`  
> **Formato:** JSON  
> **Endpoints protegidos:** `Authorization: Bearer <access_token>`  
> **Respuesta estándar:** `{"message":"...","data":{...}}`  
> **Errores esperables:** `400` datos inválidos, `401` sesión/token inválido, `403` sin permiso, `404` no existe, `409` conflicto, `422` regla de negocio.


## Orden recomendado

1. Abrir caja.
2. Corregir monto inicial solo si todavía no existe ninguna venta.
3. Crear/confirmar ventas asociadas a la sesión.
4. Consultar sesión y ventas.
5. Contar efectivo real.
6. Cerrar caja una sola vez.

## Sesiones

### POST `/cash/sessions`
**Permiso:** `CASH_OPEN`.  
**Body**
```json
{"opening_amount":100.00}
```
**201:** sesión `OPEN` con `cash_session_id`, responsable y hora de apertura.  
**No usar:** un usuario no puede tener dos cajas abiertas.

### PATCH `/cash/sessions/{cash_session_id}/opening-amount`
**Permiso:** `CASH_OPEN`.  
**Body**
```json
{"opening_amount":150.00}
```
**200:** monto corregido y auditado.  
**No usar:** se rechaza si ya existe cualquier venta asociada o la caja está cerrada.

### GET `/cash/sessions/current`
**Permiso:** `CASH_VIEW`.  
**200**
```json
{
  "data":{
    "has_open_session":true,
    "session":{"cash_session_id":1,"session_status":"OPEN"}
  }
}
```

### GET `/cash/sessions`
**Permiso:** `CASH_VIEW`.  
**Query:** `responsible_user_id`, `session_status` (`OPEN`/`CLOSED`), `limit` (1–100), `offset`.  
**200:** `items + pagination`.

### GET `/cash/sessions/{cash_session_id}`
**Permiso:** `CASH_VIEW`.  
**200:** datos completos de la sesión, totales por medio de pago y `expected_cash`.

### GET `/cash/sessions/{cash_session_id}/sales`
**Permiso:** `CASH_VIEW`.  
**Query:** `sale_status` (`PENDING`, `CONFIRMED`, `VOIDED`), `limit`, `offset`.  
**200:** ventas exclusivamente de esa caja + `pagination`.

## Cierre

### POST `/cash/sessions/{cash_session_id}/close`
**Permiso:** `CASH_CLOSE`.  
**Body**
```json
{"counted_cash":490.00}
```
**200:** caja cerrada con:
```json
{
  "data":{
    "session_status":"CLOSED",
    "expected_cash":500.00,
    "counted_cash":490.00,
    "cash_difference":-10.00,
    "difference_status":"SHORTAGE",
    "pending_payment_references":[]
  }
}
```
Cálculo servidor:
```text
expected_cash = opening_amount + ventas CASH confirmadas
cash_difference = counted_cash - expected_cash
```
Estados: `BALANCED`, `OVERAGE`, `SHORTAGE`.

## Uso incorrecto a evitar

- No enviar `expected_cash` ni `cash_difference`; los calcula PostgreSQL.
- No sustituir el efectivo contado por el valor calculado.
- No reabrir una caja cerrada.
- No crear nuevas ventas sobre una sesión `CLOSED`.
- No modificar ni eliminar un cierre.
