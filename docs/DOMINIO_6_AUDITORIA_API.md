# API – Dominio 6: Auditoría y Trazabilidad

> **Base URL de desarrollo:** `http://localhost:8000`  
> **Formato:** JSON  
> **Endpoints protegidos:** `Authorization: Bearer <access_token>`  
> **Respuesta estándar:** `{"message":"...","data":{...}}`  
> **Errores esperables:** `400` datos inválidos, `401` sesión/token inválido, `403` sin permiso, `404` no existe, `409` conflicto, `422` regla de negocio.


## Principio de uso

Este dominio es **solo lectura desde la aplicación**. Los eventos son generados automáticamente por los dominios operativos.

No existen endpoints `POST`, `PATCH`, `PUT` ni `DELETE` bajo `/audit`.

**Permiso único:** `AUDIT_VIEW`, reservado al Administrador.

## Endpoints

### GET `/audit/events`
Consulta el historial general.

**Query opcional**
- `target_user_id`
- `event_module`
- `event_action`
- `entity_schema`
- `entity_table`
- `entity_key`
- `date_from`, `date_to` (datetime ISO-8601)
- `limit` 1–100
- `offset` >= 0

**Ejemplo**
```text
/audit/events?event_module=SALES&event_action=UPDATE&limit=50&offset=0
```

**200**
```json
{
  "data":{
    "items":[
      {
        "audit_event_id":123,
        "actor_user_id":1,
        "event_module":"SALES",
        "event_action":"UPDATE",
        "entity_schema":"sales",
        "entity_table":"sales_transactions",
        "entity_key":"15",
        "previous_data":{},
        "new_data":{},
        "created_at":"..."
      }
    ],
    "pagination":{"total":1,"limit":50,"offset":0,"has_more":false}
  }
}
```

### GET `/audit/login-attempts`
Consulta inicios de sesión exitosos/fallidos.

**Query opcional**
- `target_user_id`
- `login_identifier`
- `was_successful` (`true`/`false`)
- `date_from`, `date_to`
- `limit`, `offset`

**Ejemplo**
```text
/audit/login-attempts?login_identifier=admin&was_successful=false&limit=50&offset=0
```

**200:** intentos paginados con identificador, usuario asociado cuando exista, fecha/hora, resultado y metadatos permitidos.

**Nunca debe contener:** contraseña, hash, token, CVV, PIN o número completo de tarjeta.

### GET `/audit/entities/{entity_schema}/{entity_table}/{entity_key}`
Obtiene la trazabilidad cronológica de un registro específico.

**Ejemplo**
```text
/audit/entities/sales/sales_transactions/15?limit=50&offset=0
```
**Query:** `limit`, `offset`.  
**200:** eventos de esa entidad + `pagination`.

## Qué audita y qué no

- Auditoría responde **quién hizo qué, cuándo y sobre qué registro**.
- `inventory.inventory_movements` responde **qué pasó con la existencia**.
- Ambos registros pueden coexistir; no deben sustituirse mutuamente.

## Uso incorrecto a evitar

- No escribir eventos manualmente desde el frontend.
- No permitir edición/borrado de auditoría.
- No usar Auditoría como kardex de inventario.
- No almacenar secretos en `previous_data`/`new_data`.
