from enum import Enum


class DbOperations(Enum):
    GET_USER_FOR_LOGIN = "obtener_usuario_para_acceso"
    GET_BLOCKED_IDENTIFIER_ATTEMPT = "obtener_intento_identificador_bloqueado"
    RECORD_ATTEMPT_FAILURE = "registrar_intento_fallo"
    RECORD_ATTEMPT_FAILURE_IDENTIFIER = "registrar_intento_fallo_identificador"
    SUCCESSFUL_AUTHENTICATION_REGISTRATION = "registrar_autenticacion_exitoso"
    USER_UPDATE_LAST_ACCESS = "usuario_actualizar_ultimo_acceso"
    AUTH_BY_OAUTH = "autenticacion_por_oauth"
    USER_EXISTS_IN_COMPANY = "existe_usuario_en_compania"

    AUTH_BY_PASSWORD = "auth.get_user_for_login"
    REGISTER_USER = "users.create_user"



