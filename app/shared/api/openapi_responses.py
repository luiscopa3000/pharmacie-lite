from app.shared.api.schemas import ErrorResponse

STANDARD_ERROR_RESPONSES = {
    # 🔹 4xx – Errores del cliente
    400: {
        "model": ErrorResponse,
        "description": "Solicitud inválida"
    },
    401: {
        "model": ErrorResponse,
        "description": "No autorizado"
    },
    402: {
        "model": ErrorResponse,
        "description": "Pago requerido"
    },
    403: {
        "model": ErrorResponse,
        "description": "Acceso prohibido"
    },
    404: {
        "model": ErrorResponse,
        "description": "Recurso no encontrado"
    },
    405: {
        "model": ErrorResponse,
        "description": "Método no permitido"
    },
    406: {
        "model": ErrorResponse,
        "description": "No aceptable"
    },
    408: {
        "model": ErrorResponse,
        "description": "Tiempo de espera agotado"
    },
    409: {
        "model": ErrorResponse,
        "description": "Conflicto con el estado actual del recurso"
    },
    410: {
        "model": ErrorResponse,
        "description": "Recurso ya no disponible"
    },
    412: {
        "model": ErrorResponse,
        "description": "Precondición fallida"
    },
    413: {
        "model": ErrorResponse,
        "description": "Entidad de solicitud demasiado grande"
    },
    415: {
        "model": ErrorResponse,
        "description": "Tipo de medio no soportado"
    },
    422: {
        "model": ErrorResponse,
        "description": "Entidad no procesable / error de validación"
    },
    423: {
        "model": ErrorResponse,
        "description": "Recurso bloqueado"
    },
    429: {
        "model": ErrorResponse,
        "description": "Demasiadas solicitudes"
    },

    # 🔹 5xx – Errores del servidor
    500: {
        "model": ErrorResponse,
        "description": "Error interno del servidor"
    },
    501: {
        "model": ErrorResponse,
        "description": "Funcionalidad no implementada"
    },
    502: {
        "model": ErrorResponse,
        "description": "Respuesta inválida desde un servicio externo"
    },
    503: {
        "model": ErrorResponse,
        "description": "Servicio no disponible"
    },
    504: {
        "model": ErrorResponse,
        "description": "Tiempo de espera del servidor agotado"
    }
}