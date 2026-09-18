from enum import Enum


class DbOperations(str, Enum):
    # Autenticación: la BD nunca recibe contraseñas en texto plano.
    AUTH_CREDENTIAL_GET = "identity.fn_auth_credential_get"
    LOGIN_FAILURE = "identity.fn_login_failure"
    LOGIN_SUCCESS = "identity.fn_login_success"
    SESSION_VALIDATE = "identity.fn_session_validate"
    LOGOUT = "identity.fn_logout"
    PASSWORD_CREDENTIAL_GET = "identity.fn_password_credential_get"
    PASSWORD_CHANGE = "identity.fn_password_change"

    # Usuarios, roles y permisos.
    USER_CREATE = "identity.fn_user_create"
    USER_UPDATE = "identity.fn_user_update"
    USER_LIST = "identity.fn_user_list"
    USER_GET = "identity.fn_user_get"
    USER_SET_STATUS = "identity.fn_user_set_status"
    USER_RESET_PASSWORD = "identity.fn_user_reset_password"
    ROLE_ASSIGN = "identity.fn_role_assign"
    PERMISSIONS_GET = "identity.fn_permissions_get"
    PERMISSION_CHECK = "identity.fn_permission_check"
    ROLES_LIST = "identity.fn_roles_list"
