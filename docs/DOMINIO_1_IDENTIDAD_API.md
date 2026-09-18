# API – Dominio 1: Identidad, Usuarios y Accesos

> **Base URL de desarrollo:** `http://localhost:8000`  
> **Formato:** JSON  
> **Endpoints protegidos:** `Authorization: Bearer <access_token>`  
> **Respuesta estándar:** `{"message":"...","data":{...}}`  
> **Errores esperables:** `400` datos inválidos, `401` sesión/token inválido, `403` sin permiso, `404` no existe, `409` conflicto, `422` regla de negocio.


## Orden recomendado

1. `POST /identity/auth/login`
2. Consultar roles/permisos.
3. Crear/consultar/editar usuarios.
4. Cambiar estado, rol o restablecer contraseña cuando corresponda.
5. `POST /identity/auth/change-password` para cambio propio.
6. `POST /identity/auth/logout` al terminar.

> No enviar hashes al API. Las contraseñas llegan al backend por HTTPS; PostgreSQL recibe únicamente hashes generados por el backend.

## Autenticación

### POST `/identity/auth/login`
**Auth:** no.  
**Body**
```json
{"username":"admin","password":"Admin#2026"}
```
**200**
```json
{
  "message":"Autenticación realizada correctamente",
  "data":{
    "access_token":"eyJ...",
    "token_type":"bearer",
    "expires_at":"...",
    "must_change_password":false,
    "user":{"user_id":1,"username":"admin"},
    "permissions":["USERS_VIEW"]
  }
}
```
**No usar:** no enviar `password_hash`, `jti`, rol ni permisos desde el cliente.

### POST `/identity/auth/logout`
**Auth:** sesión válida. **Body:** ninguno.  
**200:** `data` vacío o confirmación de invalidación.  
**No usar:** no reutilizar el JWT después del logout.

### POST `/identity/auth/change-password`
**Auth:** sesión válida.  
**Body**
```json
{"current_password":"Actual#2026","new_password":"Nueva#2026"}
```
**200:** confirma cambio; las sesiones activas se invalidan.  
**No usar:** no enviar hash ni omitir la contraseña actual.

## Usuarios

### POST `/identity/users`
**Permiso:** `USERS_CREATE`.  
**Body**
```json
{
  "username":"vendedor01",
  "password":"Vendedor#2026",
  "role_code":"VENDEDOR_CAJA",
  "first_name":"Juan",
  "last_name":"Perez",
  "record_status":"ACTIVE",
  "must_change_password":true
}
```
**201:** devuelve el usuario creado, incluido `user_id`.  
**No usar:** no incluir `password_hash`; no crear stock, caja ni datos de otros dominios aquí.

### GET `/identity/users`
**Permiso:** `USERS_VIEW`.  
**Query:** `search`, `role_code`, `record_status`, `limit` (1–200, default 50), `offset` (>=0).  
**200**
```json
{
  "data":{
    "items":[{"user_id":2,"username":"vendedor01","record_status":"ACTIVE"}],
    "pagination":{"total":1,"limit":50,"offset":0,"has_more":false}
  }
}
```
**No usar:** nunca debe devolver `password` ni `password_hash`.

### GET `/identity/users/{user_id}`
**Permiso:** `USERS_VIEW`.  
**Path:** `user_id` entero. **Body:** ninguno.  
**200:** datos públicos/administrativos del usuario, sin hash.

### PATCH `/identity/users/{user_id}`
**Permiso:** `USERS_UPDATE`.  
**Body:** cualquiera de `username`, `first_name`, `last_name`.
```json
{"first_name":"Juan Carlos","last_name":"Perez Quispe"}
```
**200:** usuario actualizado.  
**No usar:** el rol y la contraseña no se modifican aquí.

### PATCH `/identity/users/{user_id}/status`
**Permiso:** `USERS_STATUS`.  
**Body**
```json
{"record_status":"INACTIVE"}
```
Valores: `ACTIVE`, `INACTIVE`.  
**No usar:** no intentar desactivar al último administrador activo.

### POST `/identity/users/{user_id}/reset-password`
**Permiso:** `USERS_RESET_PASSWORD`.  
**Body**
```json
{"temporary_password":"Temporal#2026"}
```
**200:** restablece contraseña, fuerza cambio y revoca sesiones del usuario.  
**No usar:** no registrar ni auditar la contraseña temporal.

## Roles y permisos

### GET `/identity/roles`
**Permiso:** `PERMISSIONS_VIEW`. **Body:** ninguno.  
**200:** roles disponibles: `ADMINISTRADOR`, `VENDEDOR_CAJA`, `ALMACEN`.

### PUT `/identity/roles/users/{user_id}`
**Permiso:** `ROLES_ASSIGN`.  
**Body**
```json
{"role_code":"ALMACEN"}
```
**200:** rol actualizado.  
**No usar:** no cambiar rol desde `PATCH /identity/users/{id}`.

### GET `/identity/roles/permissions`
**Permiso:** `PERMISSIONS_VIEW`.  
**Query opcional:** `user_id`. Sin `user_id`, consulta permisos según la implementación actual del dominio.  
**200:** `data.items` con códigos de permiso.

### POST `/identity/roles/permissions/check`
**Auth:** sesión lista.  
**Body**
```json
{"permission_code":"USERS_CREATE"}
```
**200**
```json
{"message":"Permiso verificado correctamente","data":{"allowed":true}}
```

## Uso incorrecto a evitar

- No confiar en roles/permisos enviados por el frontend o incluidos como autoridad en el JWT.
- No guardar contraseñas en PostgreSQL en texto plano.
- No editar rol mediante el endpoint de edición de usuario.
- No reutilizar un JWT después de cambio de contraseña, cambio de rol, desactivación o logout.
