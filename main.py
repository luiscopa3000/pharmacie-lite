import os
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.bootstraps import bootstrap_logger
from app.shared.api.openapi_responses import STANDARD_ERROR_RESPONSES

from app.shared.middlewares.standardized_error_middleware import standardized_error_middleware

from app.shared.api.exception_handlers.http_exception_handler import http_exception_handler
from app.shared.api.exception_handlers.starlette_http_exception_handler import starlette_http_exception_handler
from app.shared.api.exception_handlers.validation_exception_handler import validation_exception_handler

from __version__ import __version__
from app.system.version import version_router
#from app.auth.api.auth_router import auth_api

from app.identity.api.identity_router import identity_api
from app.catalog.api.catalog_router import catalog_api
from app.inventory.api.inventory_router import inventory_api
from app.sales.api.sales_router import sales_api
from app.cash.api.cash_router import cash_api
from app.reports.api.reports_router import reports_api
#from app.company.api.company_router import company_api
#from app.catalogs.api.catalog_router import catalogs_api
#from app.product.api.product_router import product_api
#from app.inventory.api.inventory_router import inventory_api
#from app.dashboard.api.dashboard_router import dashboard_api

from app.shared.infrastructure.settings.pharmacies_db import PharmaciesDbSetting
from app.shared.infrastructure.settings.hasher_setting import HasherSetting
from app.identity.infrastructure.settings.token_setting import TokenSetting


def _env_path() -> Path:
    """Ruta al .env en la raíz de pharmacie-backend."""
    return Path(__file__).resolve().parent / ".env"


def validate_settings() -> None:
    """
    Valida que todas las variables de .env requeridas existan y sean válidas
    antes de iniciar la API. Usa el .env de la raíz de pharmacie-backend.
    """
    env_file = _env_path()
    if not env_file.exists():
        print(f"ERROR: No se encontró el archivo .env en {env_file}", file=sys.stderr)
        sys.exit(1)

    settings_to_validate = [
        ("DB (Pharmacies)", lambda: PharmaciesDbSetting(_env_file=env_file)),
        ("Hasher (HASH_PASSWORD_PEPPER)", lambda: HasherSetting(_env_file=env_file)),
        ("JWT (Token)", lambda: TokenSetting(_env_file=env_file)),
    ]
    for name, load_fn in settings_to_validate:
        try:
            load_fn()
        except ValidationError as e:
            print(f"ERROR: Validación de settings fallida para [{name}]. Revisa tu .env en pharmacie-backend/.env", file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)


bootstrap_logger()
validate_settings()

app = FastAPI(
    title="Pharmacie Management System",
    version=__version__,
    description="""
## Sistema de Gestión de Farmacias

### Autenticación
Los endpoints protegidos requieren un token JWT enviado en el header:

**Authorization:** Bearer &lt;token&gt;

Tras el login, para operaciones con contexto de compañía y roles use **POST /auth/companies/{id_compania}/access-token** (token con claim ``company_id``). Ver OpenAPI en la sección **Auth**.

### Casos de uso documentados
- **Crear usuario (POST /security/users):** Flujo, dependencias, autorización y dos casos (empleado existente vs. nuevo). Ver `docs/CREATE_USER_FLOW.md`. Índice de casos de uso: `docs/USE_CASES.md`.
    """.strip(),
    responses=STANDARD_ERROR_RESPONSES,
)

app.middleware("http")(standardized_error_middleware)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)

app.include_router(version_router)
#app.include_router(auth_api)
app.include_router(identity_api)
app.include_router(catalog_api)
app.include_router(inventory_api)
app.include_router(sales_api)
app.include_router(cash_api)
app.include_router(reports_api)

#app.include_router(company_api)
#app.include_router(catalogs_api)
#app.include_router(product_api)
#app.include_router(inventory_api)
#app.include_router(dashboard_api)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)