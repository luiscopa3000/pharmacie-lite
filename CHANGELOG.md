# Changelog

Todos los cambios notables de este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-09-18

### Added
- Introducción de nuevos dominios de aplicación y módulos: `audit`, `cash`, `catalog`, `identity`, `inventory`, `reports` y `sales`.
- Añadidos nuevos enrutadores API en `main.py` (`identity_api`, `catalog_api`, `inventory_api`, `sales_api`, `cash_api`, `reports_api`).

### Changed
- Refactorización del sistema de autenticación, reemplazando el antiguo módulo `auth` con el nuevo módulo `identity`.
- Actualizada la ruta de importación de `TokenSetting` en `main.py` para reflejar la transición de `auth` a `identity`.

### Removed
- Eliminado el módulo legado `auth` y sus referencias en `main.py`.

## [0.1.0] - 2026-09-16

### Added
- Configuración inicial del proyecto para el backend del sistema de gestión Pharmacie.
- Aplicación principal FastAPI con manejo estándar de errores HTTP y configuración de middleware.
- Configuración de validación de ajustes de base de datos (validación `.env`).
- Flujo de autenticación mediante tokens JWT (POST `/auth/companies/{id_compania}/access-token`).
- Flujos de trabajo de seguridad y creación de usuarios (POST `/security/users`).
- Documentación básica del proyecto, dependencias y `.gitignore`.
