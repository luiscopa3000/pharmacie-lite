# Documentación API – Pharmacy Lite

Base URL local: `http://localhost:8000`

Documentos:
1. `DOMINIO_1_IDENTIDAD_API.md`
2. `DOMINIO_2_CATALOGO_API.md`
3. `DOMINIO_3_INVENTARIO_API.md`
4. `DOMINIO_4_VENTAS_API.md`
5. `DOMINIO_5_CAJA_API.md`
6. `DOMINIO_6_AUDITORIA_API.md`
7. `DOMINIO_7_REPORTES_API.md`

Orden funcional recomendado del sistema:
Identidad → Catálogo → Inventario/Lotes → Caja → Ventas → Auditoría → Reportes.

Nota: Caja debe estar abierta antes de confirmar ventas. Auditoría y Reportes son dominios de consulta; no deben utilizarse para modificar información operativa.
