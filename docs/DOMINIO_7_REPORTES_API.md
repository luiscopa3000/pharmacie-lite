# API – Dominio 7: Consultas, Alertas y Reportes

> **Base URL de desarrollo:** `http://localhost:8000`  
> **Formato:** JSON  
> **Endpoints protegidos:** `Authorization: Bearer <access_token>`  
> **Respuesta estándar:** `{"message":"...","data":{...}}`  
> **Errores esperables:** `400` datos inválidos, `401` sesión/token inválido, `403` sin permiso, `404` no existe, `409` conflicto, `422` regla de negocio.


## Principio de uso

Todos los endpoints son **solo lectura** y requieren `REPORTS_VIEW`.  
No modifican stock, ventas, lotes, caja ni auditoría.

Paginación estándar: `limit` 1–100, `offset >= 0`.  
El dashboard no se pagina; sus alertas usan `alert_limit`.

## Dashboard

### GET `/reports/dashboard`
**Query:** `business_date` (`YYYY-MM-DD`), `expiry_days` (1–365), `alert_limit` (1–50, default 10).

**Ejemplo**
```text
/reports/dashboard?business_date=2026-09-18&expiry_days=30&alert_limit=10
```

**200**
```json
{
  "data":{
    "business_date":"2026-09-18",
    "sales_today":{
      "confirmed_count":35,
      "net_total":2450.50,
      "voided_count":2,
      "voided_total":95.00
    },
    "low_stock":{"count":7,"items":[]},
    "expiring_soon":{"days":30,"count":5,"items":[]},
    "expired":{"count":2,"quantity":15}
  }
}
```

## Ventas

### GET `/reports/sales/period`
**Query obligatorio:** `date_from`, `date_to`.  
**Query adicional:** `limit`, `offset`.
```text
/reports/sales/period?date_from=2026-09-01&date_to=2026-09-30&limit=50&offset=0
```
**200:** resumen de confirmadas/anuladas + ventas paginadas.

### GET `/reports/sales/products`
**Query obligatorio:** `date_from`, `date_to`; además `limit`, `offset`.  
**200:** cantidad e importe vendidos por producto usando valores históricos.

### GET `/reports/sales/users`
**Query obligatorio:** `date_from`, `date_to`; además `limit`, `offset`.  
**200:** ventas agrupadas por usuario, incluyendo usuarios actualmente inactivos.

### GET `/reports/sales/voided`
**Query opcional:** `date_from`, `date_to`, `limit`, `offset`.  
**200:** número, fechas, total, vendedor, anulador y motivo.

## Inventario

### GET `/reports/inventory`
**Query:** `category_id`, `only_active` (default `true`), `search`, `limit`, `offset`.  
**200:** producto, existencia física/vendible, mínimo, lotes y vencimientos.

### GET `/reports/inventory/movements`
**Query:** `product_id`, `movement_kind`, `performed_by_user_id`, `date_from`, `date_to`, `limit`, `offset`.  
**200:** movimientos con usuario y motivo.

### GET `/reports/inventory/low-stock`
**Query:** `limit`, `offset`.  
**200:** solo productos con `sellable_quantity <= minimum_stock`.

### GET `/reports/inventory/expiring`
**Query:** `days` (1–365, opcional), `limit`, `offset`.  
**200:** lotes con existencia, ordenados por vencimiento próximo.

### GET `/reports/inventory/expired`
**Query:** `limit`, `offset`.  
**200:** lotes vencidos con existencia física > 0; no implica que sean vendibles.

## Caja

### GET `/reports/cash/closures`
**Query:** `date_from`, `date_to`, `responsible_user_id`, `limit`, `offset`.  
**200:** usuario, apertura, cierre, monto inicial, ventas, esperado, contado y diferencia.

## Uso incorrecto a evitar

- No usar Reportes para ejecutar operaciones transaccionales.
- No recalcular históricos usando precios actuales.
- No incluir ventas anuladas dentro del total neto confirmado.
- No tratar stock físico vencido como stock vendible.
- No usar los reportes como sustituto de Auditoría.
