from enum import Enum
class AuditDbOperations(str, Enum):
    AUDIT_QUERY = "audit.fn_audit_query"
    LOGIN_ATTEMPTS_QUERY = "audit.fn_login_attempts_query"
    ENTITY_TRACE = "audit.fn_entity_trace"
